import io
import yaml
import json
import os
import zipfile
import cv2
import numpy as np
import datetime

from struct import unpack
from abc import ABC, abstractmethod
from typing import Union, IO, Any, Dict, Tuple
from binaexperts.convertors.const import *
from jsonschema import validate, ValidationError


# Function to get image dimensions from bytes
def get_image_dimensions(image_bytes: bytes) -> Tuple[int, int]:

    """
    Get the dimensions (width, height) of an image from its byte content using PIL.

    This function leverages the Pillow (PIL) library to determine the dimensions of an image.
    It supports various image formats such as JPEG, PNG, GIF, and others. If the image content
    is invalid or if the dimensions cannot be determined, it returns default dimensions (640x480).

    :param image_bytes: Byte content of the image.
    :return: A tuple containing the width and height of the image.

    Exceptions:
        - If an error occurs during the image loading process (e.g., invalid image format),
          the function will print an error message and return default dimensions.

    Notes:
        - This function uses the Pillow (PIL) library, which must be installed (`pip install Pillow`).
        - The function returns default dimensions (640x480) if the image content is invalid or unreadable.
    """

    # Minimum length check to prevent processing invalid or mock content
    if len(image_bytes) < 10:
        print("Warning: Image content too short to determine dimensions. Returning default dimensions.")
        return 640, 480  # Return default dimensions for mock or invalid content

    # Read the first few bytes of the image to determine the format and size
    with io.BytesIO(image_bytes) as img_file:
        # Check if it's a JPEG file
        img_file.seek(0)
        img_file.read(2)
        b = img_file.read(1)
        try:
            # Counter to avoid infinite loops
            max_iterations = 100  # Set an appropriate limit for iterations
            iteration_count = 0

            while b and b != b'\xDA':  # Search for the start of the image data (SOS marker)
                # Increment iteration counter
                iteration_count += 1
                if iteration_count > max_iterations:
                    print("Warning: Exceeded maximum iterations. Returning default dimensions.")
                    return 640, 480  # Return default dimensions to avoid infinite loop

                while b != b'\xFF':  # Find marker
                    b = img_file.read(1)
                while b == b'\xFF':  # Skip padding
                    b = img_file.read(1)
                if b >= b'\xC0' and b <= b'\xC3':  # Start of Frame markers for JPEG
                    img_file.read(3)  # Skip segment length and precision
                    h, w = unpack('>HH', img_file.read(4))  # Read height and width
                    return w, h
                else:
                    segment_length = unpack('>H', img_file.read(2))[0]
                    if segment_length <= 2:  # Prevent zero or negative length reads
                        print("Warning: Invalid segment length. Returning default dimensions.")
                        return 640, 480
                    img_file.read(segment_length - 2)  # Skip other segments
                b = img_file.read(1)
        except Exception as e:
            print(f"Error reading image dimensions: {e}. Returning default dimensions.")
        return 640, 480  # Fallback if dimensions couldn't be read


class BaseConvertor(ABC):
    """
    Base class for data format converters. This class provides a framework
    for converting datasets between different formats, such as COCO, YOLO,
    and others, using a normalized intermediate format.
    """

    def __init__(self):
        """
        Initialize the base converter class. This base class is intended to be
        inherited by specific format converters (e.g., COCO, YOLO).
        """
        pass

    @abstractmethod
    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Any:
        """
        Load the data from the source format.

        :param source: File-like object or path representing the source dataset.
        :return: Loaded data in the source format.
        """
        raise NotImplementedError("The 'load' method must be overridden by subclasses.")

    @abstractmethod
    def normalize(
            self,
            data: Any
    ) -> Dict:
        """
        Convert the source format data to the normalized format.

        :param data: Loaded data in the source format.
        :return: Data converted to the normalized format as a dictionary.
        """
        raise NotImplementedError("The 'normalize' method must be overridden by subclasses.")

    @abstractmethod
    def convert(
            self,
            normalized_data: Dict,
            destination: Union[str, IO[bytes]]
    ) -> Any:
        """
        Convert the normalized format data to the target format.

        :param normalized_data: Data in the normalized format as a dictionary.
        :param destination: File-like object or path representing the target dataset.
        :return: Converted data in the target format.
        """
        raise NotImplementedError("The 'convert' method must be overridden by subclasses.")

    @abstractmethod
    def save(
            self,
            data: Any,
            destination: Union[str, IO[bytes]]
    ) -> None:
        """
        Save the data in the target format.

        :param data: Data in the target format.
        :param destination: File-like object to save the target dataset.
        """
        raise NotImplementedError("The 'save' method must be overridden by subclasses.")


class COCOConvertor(BaseConvertor):
    """
    A convertor class for handling datasets in COCO format.

    This class extends the `BaseConvertor` and provides methods for loading, normalizing,
    and converting datasets specifically to and from the COCO format. It supports
    operations such as reading COCO-formatted data, transforming it to a normalized
    internal structure, and writing it back into the COCO format.

    COCO (Common Objects in Context) is a popular dataset format for object detection,
    segmentation, and image captioning tasks.

    Inherits from:
        BaseConvertor: A base class for dataset convertors that provides
        common methods for dataset operations.

    Usage:
        The `COCOConvertor` can be used to load a COCO dataset, normalize it for
        intermediate processing, and convert it back into COCO format or another supported format.

    Attributes:
        coco_schema (dict): A dictionary representing the COCO JSON schema, used
        for validation of COCO datasets during load and save operations.
    """

    def __init__(self):
        """
        Initializes the converter class by loading the required JSON schemas for COCO and normalizer formats.

        This constructor performs the following steps:
        1. Calls the superclass constructor to ensure proper initialization.
        2. Loads the COCO dataset schema from a JSON file located in the schema directory.
        3. Loads the normalizer dataset schema from a JSON file located in the schema directory.

        Raises:
            FileNotFoundError: If the schema files are not found at the specified paths.
            JSONDecodeError: If the schema files contain invalid JSON.
        """
        super().__init__()

        # Load the JSON schema using a relative path from the current file
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'coco.json')
        with open(schema_path, 'r') as schema_file:
            self.coco_schema = json.load(schema_file)

        # Load the normalizer JSON schema
        normalizer_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'normalizer.json')
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def _loadhelper_coco_data(
            self,
            coco_data,
            dataset,
            subdir,
            source_zip=None
    ):

        """
        Helper method to load categories, images, and annotations from COCO-formatted data.

        This method populates the given `dataset` dictionary with categories, images, and annotations
        from the provided `coco_data` (in COCO JSON format). It handles the uniqueness of image IDs by
        prefixing the image ID with the subdirectory (split) name.

        :param coco_data: The parsed COCO dataset in JSON format, containing categories, images, and annotations.
        :param dataset: The destination dictionary where categories, images, and annotations will be appended.
        :param subdir: The subdirectory representing the data split (e.g., 'train', 'valid', 'test') which is used to uniquely identify images across splits.
        :param source_zip: (optional) A zip file object. If provided, this method will attempt to read image content directly from the zip file.

        :raises None: No exceptions are raised by this method.

        :warning: If an image file cannot be found in the zip archive (if provided), a warning is printed. If segmentation data for an annotation is not in the correct format (a list of lists of coordinates), a warning is printed.

        :note: The unique image ID ensures that images from different splits (e.g., 'train', 'valid', 'test') do not conflict when merged into the same dataset. Segmentation data is included in annotations, but a warning is printed if its format is incorrect.
        """

        # Load categories if not already present
        if not dataset['categories']:
            for cat in coco_data.get('categories', []):
                category = {
                    'id': cat['id'],
                    'name': cat['name'],
                    'supercategory': cat.get('supercategory', 'none')
                }
                dataset['categories'].append(category)

        # Load images
        for img in coco_data.get('images', []):
            unique_image_id = f"{subdir}_{img['id']}"  # Prefix with split
            image_file_name = img['file_name']
            image_path = f"{subdir}/{image_file_name}"

            image_content = None
            # Read image content if available in the source zip
            if source_zip and image_path in source_zip.namelist():
                with source_zip.open(image_path) as img_file:
                    image_content = img_file.read()
            elif source_zip:
                print(f"Warning: Image file {image_path} not found in zip archive.")

            image = {
                'id': unique_image_id,
                'file_name': image_file_name,
                'width': img.get('width', 0),
                'height': img.get('height', 0),
                'split': subdir,
                'source_zip': source_zip,
                'image_content': image_content
            }
            dataset['images'].append(image)

        # Load annotations
        for ann in coco_data.get('annotations', []):
            unique_image_id = f"{subdir}_{ann['image_id']}"  # Ensure mapping to unique image ID
            annotation = {
                'id': ann['id'],
                'image_id': unique_image_id,
                'category_id': ann['category_id'],
                'bbox': ann['bbox'],
                'segmentation': ann.get('segmentation', []),  # Include segmentation data
                'area': ann.get('area', 0.0),
                'iscrowd': ann.get('iscrowd', 0)
            }
            # Ensure segmentation is correctly formatted (a list of lists of coordinates)
            if not isinstance(annotation['segmentation'], list):
                print(f"Warning: Invalid segmentation format for annotation ID {ann['id']}.")

            dataset['annotations'].append(annotation)

    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Dict:
        """
        Load a COCO dataset from various sources, including a zip file, directory, or an in-memory object.

        This method loads a COCO dataset, validates it against the COCO schema, and returns it as a dictionary.
        It supports loading data from:
        - A zip file containing COCO-formatted annotations and images.
        - A directory containing COCO-formatted annotation files.
        - An in-memory file-like object (e.g., BytesIO).

        The dataset is divided into 'train', 'test', and 'valid' splits, and the method searches for
        `_annotations.coco.json` files within each split directory. The data is validated against the
        COCO schema before being loaded into a unified dataset dictionary.

        :param source: A string representing a file path to a zip archive or directory, or a file-like
                       object (such as a BytesIO or an opened ZipFile) containing the COCO dataset.

        :return: A dictionary representing the COCO dataset, containing the following keys:
                 - 'info': General information about the dataset.
                 - 'images': A list of image metadata, including image IDs, file names, dimensions, and more.
                 - 'annotations': A list of annotations, including bounding boxes, segmentation, and other relevant details.
                 - 'categories': A list of categories (object classes) defined in the dataset.
                 - 'licenses': License information related to the dataset.

        :raises ValueError: If the source is not a valid directory path, file-like object, or an opened zip file.
        :raises ValidationError: If the COCO dataset does not conform to the expected schema.

        :warning: If an annotation file is not found in any of the expected subdirectories (train, test, valid),
                  a warning is printed, and that subdirectory is skipped.
                  If validation of a subdirectory's annotations fails, a warning is printed, and that subdirectory
                  is skipped.

        :note:
            - This method is flexible enough to handle both file paths (directories and zip files) and in-memory
              file-like objects.
            - The helper method `_loadhelper_coco_data` is used to manage the loading and processing of the
              COCO-formatted data.
        """

        subdirs = ['train', 'test', 'valid']
        dataset = {
            'info': {},
            'images': [],
            'annotations': [],
            'categories': [],
            'licenses': []
        }

        if isinstance(source, str):
            # If the source is a file path (zip file)
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    for subdir in subdirs:
                        annotation_path = f"{subdir}/_annotations.coco.json"

                        # Skip subdir if the annotation file does not exist
                        if annotation_path not in zip_file.namelist():
                            print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                            continue

                        with zip_file.open(annotation_path) as file:
                            coco_data = json.load(file)

                            # Validate coco_data against the loaded schema to ensure its structure is correct
                            try:
                                validate(instance=coco_data, schema=self.coco_schema)
                            except ValidationError as e:
                                print(f"Validation error in {subdir}: {e.message}")
                                continue  # Skip processing this subdir if validation fails

                        # Use the helper method to load data
                        self._loadhelper_coco_data(coco_data, dataset, subdir, source_zip=zip_file)

            else:
                # If the source is a directory path
                for subdir in subdirs:
                    annotation_file = os.path.join(source, subdir, '_annotations.coco.json')

                    # Skip subdir if the annotation file does not exist
                    if not os.path.isfile(annotation_file):
                        print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                        continue

                    with open(annotation_file, 'r') as file:
                        coco_data = json.load(file)

                        # Validate coco_data against the loaded schema to ensure its structure is correct
                        try:
                            validate(instance=coco_data, schema=self.coco_schema)
                        except ValidationError as e:
                            print(f"Validation error in {subdir}: {e.message}")
                            continue  # Skip processing this subdir if validation fails

                    # Use the helper method to load data
                    self._loadhelper_coco_data(coco_data, dataset, subdir)

        elif isinstance(source, zipfile.ZipFile):
            # Handle opened zip file case
            for subdir in subdirs:
                annotation_path = f"{subdir}/_annotations.coco.json"

                # Skip subdir if the annotation file does not exist
                if annotation_path not in source.namelist():
                    print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                    continue

                with source.open(annotation_path) as file:
                    coco_data = json.load(file)

                    # Validate coco_data against the loaded schema to ensure its structure is correct
                    try:
                        validate(instance=coco_data, schema=self.coco_schema)
                    except ValidationError as e:
                        print(f"Validation error in {subdir}: {e.message}")
                        continue  # Skip processing this subdir if validation fails

                # Use the helper method to load data
                self._loadhelper_coco_data(coco_data, dataset, subdir, source_zip=source)

        elif hasattr(source, 'read'):
            # If the source is a file-like object (e.g., BytesIO), open it as a zip file
            with zipfile.ZipFile(source, 'r') as zip_file:
                for subdir in subdirs:
                    annotation_path = f"{subdir}/_annotations.coco.json"

                    # Skip subdir if the annotation file does not exist
                    if annotation_path not in zip_file.namelist():
                        print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                        continue

                    with zip_file.open(annotation_path) as file:
                        coco_data = json.load(file)

                        # Validate coco_data against the loaded schema to ensure its structure is correct
                        try:
                            validate(instance=coco_data, schema=self.coco_schema)
                        except ValidationError as e:
                            print(f"Validation error in {subdir}: {e.message}")
                            continue  # Skip processing this subdir if validation fails

                    # Use the helper method to load data
                    self._loadhelper_coco_data(coco_data, dataset, subdir, source_zip=zip_file)

        else:
            raise ValueError("Source must be either a directory path, a file-like object, or an opened zip file.")

        return dataset

    def normalize(
            self,
            data: dict
    ) -> dict:
        """
        Convert a COCO-formatted dataset dictionary into a normalized dataset dictionary.

        This method processes the input COCO dataset, which may contain both object detection
        and segmentation data, and converts it into a normalized format that is simpler and
        more consistent for downstream use. It maps COCO's categories, images, and annotations
        into a format that supports object detection and segmentation.

        :param data: A dictionary representing the COCO dataset. It must contain the following keys:
                     - `images`: A list of dictionaries with image metadata (file names, dimensions, etc.).
                     - `annotations`: A list of dictionaries with annotation metadata (bounding boxes, categories, etc.).
                     - `categories`: A list of dictionaries representing object classes.
                     - Optionally, `licenses`: A list of dictionaries with licensing information.

        :return: A dictionary representing the normalized dataset with keys:
                 - `info`: Information about the dataset.
                 - `images`: A list of image metadata dictionaries.
                 - `annotations`: A list of annotation metadata dictionaries.
                 - `categories`: A list of category dictionaries.
                 - `licenses`: A list of license dictionaries (if provided).
                 - `nc`: Number of categories.
                 - `names`: A list of category names.

        :raises KeyError: If a required field (such as 'images', 'annotations', or 'categories') is missing from `data`.
        :raises ValueError: If an image or annotation does not meet the required format.

        :notes:
            - The method will print warnings for any images or annotations that are skipped due to missing or invalid data.
            - The bounding boxes (bbox) are expected to be in COCO's xywh format (x, y, width, height).
            - Segmentation data is included in the normalized annotations if present.
            - Categories are mapped from the COCO format to a normalized format, and an internal ID mapping is created for consistency.

        """

        normalized_dataset = {
            "info": {
                "description": "Converted from COCO",
                "dataset_name": "COCO Dataset",
                "dataset_type": "Object Detection and Segmentation",
                "splits": {}  # Add split information if necessary
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": data.get("licenses", []),
            "nc": len(data['categories']),
            "names": [cat['name'] for cat in data['categories']]
        }

        # Create category ID mapping
        category_id_map = {cat['id']: idx for idx, cat in enumerate(data['categories'])}

        # Map image IDs to normalized IDs
        image_id_map = {image['id']: idx for idx, image in enumerate(data['images'])}

        annotation_id = 1  # Initialize annotation ID

        # Convert and add images
        for image in data['images']:
            # Ensure 'width' and 'height' are present
            if 'width' not in image or 'height' not in image:
                print(f"Warning: Image {image['file_name']} is missing 'width' or 'height'. Skipping...")
                continue  # Skip images without width or height

            normalized_image = {
                "id": image_id_map[image['id']],
                "file_name": image['file_name'],
                "width": image['width'],  # Ensure width is present
                "height": image['height'],  # Ensure height is present
                "split": image.get('split', 'train'),  # Default to 'train' if split not specified
                "source_zip": image.get('source_zip'),
                "image_content": image.get('image_content')
            }
            normalized_dataset["images"].append(normalized_image)
            print(
                f"Normalized Image: {normalized_image['file_name']}, ID: {normalized_image['id']}, Width: {normalized_image['width']}, Height: {normalized_image['height']}")

        # Convert and add annotations
        for ann in data['annotations']:
            if ann['category_id'] not in category_id_map:
                print(f"Warning: Unknown category_id {ann['category_id']} for annotation ID {ann['id']}. Skipping...")
                continue  # Skip unknown categories

            if 'image_id' not in ann:
                print(f"Warning: Annotation ID {ann['id']} is missing 'image_id'. Skipping...")
                continue  # Skip annotations without image_id

            if ann['image_id'] not in image_id_map:
                print(f"Warning: Image ID {ann['image_id']} for annotation ID {ann['id']} does not exist. Skipping...")
                continue  # Skip annotations with invalid image_id

            normalized_annotation = {
                "id": annotation_id,
                "image_id": image_id_map[ann['image_id']],
                "category_id": category_id_map[ann['category_id']],
                "bbox": ann.get('bbox', []),
                "segmentation": ann.get('segmentation', []),
                "area": ann.get('area', 0.0),
                "iscrowd": ann.get('iscrowd', 0),
                "bbox_format": 'xywh'  # COCO uses xywh format
            }
            normalized_dataset["annotations"].append(normalized_annotation)
            print(
                f"Normalized Annotation ID: {normalized_annotation['id']}, Image ID: {normalized_annotation['image_id']}, Class ID: {normalized_annotation['category_id']}, BBox: {normalized_annotation['bbox']}, Segmentation: {normalized_annotation['segmentation']}")
            annotation_id += 1

        # Convert and add categories
        for cat in data['categories']:
            normalized_category = {
                "id": category_id_map[cat['id']],
                "name": cat['name'],
                "supercategory": cat.get('supercategory', 'none')
            }
            normalized_dataset["categories"].append(normalized_category)
            print(f"Normalized Category: {normalized_category['name']}, ID: {normalized_category['id']}")

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:
        """
        Convert the normalized dataset format back to the COCO format and save it.

        This method converts a normalized dataset (which might be in formats such as YOLO or custom formats)
        back into the COCO dataset format. The function constructs the COCO-compliant dataset by adding
        required metadata, images, annotations, categories, and licenses. It also validates the dataset
        against the COCO schema to ensure the correct structure before saving.

        :param normalized_data: A dictionary representing the normalized data. It should contain:
                                - `info`: General information about the dataset (e.g., description, dataset name, type, etc.).
                                - `images`: A list of dictionaries representing image metadata (file names, dimensions, etc.).
                                - `annotations`: A list of dictionaries representing annotations (bounding boxes, segmentation, etc.).
                                - `categories`: A list of dictionaries representing object categories (names, supercategories, etc.).
                                - `licenses`: (Optional) A list of dictionaries representing licensing information.

        :param destination: The path or in-memory object (e.g., a BytesIO object) to save the COCO dataset.

        :return: A dictionary representing the COCO dataset, following the COCO format.

        :raises ValidationError: If the resulting COCO dataset doesn't conform to the COCO schema.
        """

        # Create a COCO dataset object with the required metadata
        coco_dataset = {
            "info": {
                "description": normalized_data.get("description", "Converted YOLO Dataset"),  # Default description
                "dataset_name": normalized_data.get("dataset_name", "YOLO to COCO Conversion"),  # Default dataset name
                "dataset_type": normalized_data.get("dataset_type", "Object Detection"),  # Default dataset type
                "date_created": normalized_data.get("date_created",
                                                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": normalized_data.get("licenses", [{"id": 1, "name": "Unknown License", "url": ""}])
            # Default license
        }

        # Add images to the COCO dataset
        for normalized_image in normalized_data.get("images", []):
            coco_image = {
                "id": normalized_image.get("id"),
                "file_name": normalized_image.get("file_name"),
                "width": normalized_image.get("width", 0),
                "height": normalized_image.get("height", 0),
                "split": normalized_image.get("split", ""),
                "source_zip": normalized_image.get("source_zip", None),
                "image_content": normalized_image.get("image_content", None)
            }
            coco_dataset["images"].append(coco_image)

        annotation_id = 1
        # Add annotations to the COCO dataset
        for normalized_annotation in normalized_data.get("annotations", []):
            # Extract segmentation data, ensuring it's correctly formatted for COCO
            segmentation = normalized_annotation.get("segmentation", [])
            if segmentation:
                # Ensure segmentation is a list of lists for polygons or RLE for masks
                if not isinstance(segmentation, list) or not all(isinstance(seg, list) for seg in segmentation):
                    print(f"Warning: Invalid segmentation format for annotation ID {annotation_id}.")

            coco_annotation = {
                "id": annotation_id,
                "image_id": normalized_annotation.get("image_id"),
                "category_id": normalized_annotation.get("category_id"),
                "bbox": normalized_annotation.get("bbox", []),
                "segmentation": segmentation,  # Include segmentation data as is
                "area": normalized_annotation.get("area", 0.0),
                "iscrowd": normalized_annotation.get("iscrowd", 0)
            }
            coco_dataset["annotations"].append(coco_annotation)
            annotation_id += 1

        # Add categories to the COCO dataset
        for normalized_category in normalized_data.get("categories", []):
            coco_category = {
                "id": normalized_category.get("id"),
                "name": normalized_category.get("name"),
                "supercategory": normalized_category.get("supercategory", "none")
            }
            coco_dataset["categories"].append(coco_category)

        # Validate the COCO dataset against the loaded COCO schema
        try:
            validate(instance=coco_dataset, schema=self.coco_schema)
            print("COCO dataset successfully validated against the COCO schema.")
        except ValidationError as e:
            print(f"Validation error in COCO dataset: {e.message}")
            raise

        # Write the COCO format dataset to the destination
        self.save(coco_dataset, destination)

        return coco_dataset

    def save(
            self,
            data: dict,
            destination: Union[str, IO[bytes], None] = None
    ):
        """
        Save the COCO dataset to a zip file or an in-memory buffer.

        This method validates the COCO dataset and saves it to the specified destination. The dataset is organized
        into 'train', 'valid', and 'test' splits, and each split's images and annotations are stored separately in
        the zip file or in-memory buffer.

        :param data: A dictionary representing the COCO dataset. It must include keys such as 'info', 'images',
                     'annotations', and 'categories'.
        :param destination: Path, file-like object (e.g., BytesIO), or None where the zip archive will be written.
                            If None, an in-memory buffer (BytesIO) is used.

        :raises ValidationError: If the COCO dataset does not conform to the COCO schema.

        Notes:
        - The method handles multiple formats ('valid', 'val', 'validation') for the 'valid' split from YOLO and BinaExperts.
        - The saved zip file contains image and annotation files for 'train', 'valid', and 'test' splits.
        - If no images are found for a split, it is skipped and a warning is printed.
        """

        # Handle the case when destination is None by using BytesIO
        if destination is None:
            print("No destination provided, using in-memory buffer.")
            destination = io.BytesIO()

        is_file_like = not isinstance(destination, str)

        # Validate the COCO dataset against the loaded COCO schema before saving
        try:
            validate(instance=data, schema=self.coco_schema)
            print("COCO dataset successfully validated against the COCO schema.")
        except ValidationError as e:
            print(f"Validation error in COCO dataset: {e.message}")
            raise

        # Prepare the zip file
        if is_file_like:
            zip_file = zipfile.ZipFile(destination, 'w')
        else:
            if not destination.lower().endswith('.zip'):
                destination += '.zip'
            zip_file = zipfile.ZipFile(destination, 'w')

        # Debug: Print unique splits in data
        unique_splits = set(img.get('split', '').lower() for img in data.get('images', []))
        print(f"Unique splits in data: {unique_splits}")

        with zip_file as zip_file:
            # Define the splits to process
            splits = ['train', 'valid', 'test']

            for split in splits:
                if split == 'valid':
                    # For 'valid' split, include 'valid', 'val', and 'validation' from YOLO and BinaExperts
                    split_images = [
                        img for img in data.get('images', [])
                        if img.get('split', '').lower() in ['valid', 'val', 'validation']
                    ]
                    print(f"Found {len(split_images)} images for 'valid' split (including 'val' and 'validation').")
                else:
                    # For 'train' and 'test', include only respective splits
                    split_images = [
                        img for img in data.get('images', [])
                        if img.get('split', '').lower() == split
                    ]
                    print(f"Found {len(split_images)} images for '{split}' split.")

                # Collect corresponding annotations
                split_annotations = [
                    ann for ann in data.get('annotations', [])
                    if ann.get('image_id') in {img.get('id') for img in split_images}
                ]
                print(f"Found {len(split_annotations)} annotations for '{split}' split.")

                # If no images are found for this split, skip
                if not split_images:
                    print(WARNING_NO_IMAGES_FOUND.format(split))
                    continue

                # Determine output split name
                output_split = 'valid' if split == 'valid' else split

                # Prepare the split COCO format dictionary
                split_coco = {
                    "info": {
                        "description": data.get('info', {}).get("description", "Dataset conversion"),
                        "dataset_name": data.get('info', {}).get("dataset_name", "Converted Dataset"),
                        "dataset_type": data.get('info', {}).get("dataset_type", "Object Detection"),
                        "date_created": data.get('info', {}).get(
                            "date_created",
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ),
                    },
                    "licenses": data.get('licenses', []),
                    "images": [
                        {
                            "id": img.get('id'),
                            "file_name": img.get('file_name'),
                            "width": img.get('width', 0),
                            "height": img.get('height', 0),
                            "split": output_split  # Assign split to output_split
                        }
                        for img in split_images
                    ],
                    "annotations": [
                        {
                            "id": ann.get('id'),
                            "image_id": ann.get('image_id'),
                            "category_id": ann.get('category_id'),
                            "bbox": ann.get('bbox', []),
                            "segmentation": ann.get('segmentation', []),
                            "area": ann.get('area', 0.0),
                            "iscrowd": ann.get('iscrowd', 0)
                        }
                        for ann in split_annotations
                    ],
                    "categories": [
                        {
                            "id": cat.get('id'),
                            "name": cat.get('name'),
                            "supercategory": cat.get('supercategory', 'none')
                        }
                        for cat in data.get('categories', [])
                    ]
                }

                # Debug: Print details of each image being saved
                print(f"Saving {len(split_coco['images'])} images to '{output_split}' split.")
                for img in split_coco['images']:
                    print(f"Image ID: {img['id']}, File: {img['file_name']}, Split: {img['split']}")

                # Log segmentation data for validation
                for ann in split_annotations:
                    if 'segmentation' in ann and ann['segmentation']:
                        if not isinstance(ann['segmentation'], list) or not all(
                                isinstance(seg, list) for seg in ann['segmentation']
                        ):
                            print(
                                f"Warning: Segmentation data is not in the correct format for annotation ID {ann['id']}."
                            )

                # Create the filename for the annotations JSON file
                json_filename = ANNOTATION_JSON_PATH_TEMPLATE.format(output_split)

                # Convert the COCO dictionary to JSON and write it to the zip file
                coco_json_content = json.dumps(split_coco, indent=4)
                zip_file.writestr(json_filename, coco_json_content)
                print(f"Saved annotations for '{output_split}' split with {len(split_annotations)} annotations.")

                # Save images directly in the split directory inside the zip file
                for image in split_images:
                    # Assign 'valid' to 'valid' split, otherwise keep the split as is
                    image_split = 'valid' if split == 'valid' else split
                    # No need to reassign based on image's split since images are already filtered
                    image_split = output_split
                    image_path = os.path.join(image_split, image.get('file_name'))

                    if image.get('image_content'):
                        zip_file.writestr(image_path, image.get('image_content'))
                        print(f"Saved image: {image_path}")
                    else:
                        print(f"Warning: No image content found for {image.get('file_name')}")

        # Final success message
        if isinstance(destination, io.BytesIO):
            print("COCO dataset successfully saved to the in-memory zip file.")
        else:
            print(f"COCO dataset successfully saved to '{destination}'.")


class YOLOConvertor(BaseConvertor):
    """
        A convertor class for handling datasets in YOLO format.

        This class extends the `BaseConvertor` and provides methods for loading, normalizing,
        and converting datasets specifically to and from the YOLO format. YOLO (You Only Look Once)
        is a widely used format for object detection tasks, where annotations are typically represented
        as bounding boxes normalized to the image size.

        The `YOLOConvertor` supports reading YOLO-formatted data (usually stored in `.txt` files),
        converting it into a normalized structure, and writing it back into the YOLO format or other
        supported formats.

        Inherits from:
            BaseConvertor: A base class for dataset convertors that provides
            common methods for dataset operations.

        Usage:
            The `YOLOConvertor` can be used to load a YOLO dataset, normalize it for
            intermediate processing, and convert it back into YOLO format or another supported format.

        Attributes:
            yolo_schema (dict): A dictionary representing the YOLO JSON schema, used
            for validation of YOLO datasets during load and save operations.
        """

    def __init__(self):

        """
        Initialize the converter class and load the YOLO and Normalizer JSON schemas.

        This constructor method loads the JSON schema files for both YOLO and Normalizer formats, which are required
        to validate datasets during conversion processes. The schema files are loaded from predefined paths relative
        to the current file's directory.

        :raises FileNotFoundError: If the schema files cannot be found at the specified paths.
        :raises json.JSONDecodeError: If the schema files cannot be decoded as valid JSON.

        Notes:
        - The paths for the schemas are assumed to be relative to the current file. Ensure that the file structure
          follows the expected organization.
        """

        super().__init__()
        # Load the JSON schema for YOLO and Normalizer using relative paths from the current file
        yolo_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'yolo.json')
        normalizer_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'normalizer.json')

        # Load YOLO schema
        with open(yolo_schema_path, 'r') as schema_file:
            self.yolo_schema = json.load(schema_file)

        # Load Normalizer schema
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def _loadhelper_yolo_from_zip(
            self,
            zip_file: zipfile.ZipFile,
            dataset: dict,
            subdirs: list
    ):

        """
        Helper method to load YOLO data from a zip file into the dataset.

        This method extracts images, labels, and class names from the provided zip file, and loads them into the
        `dataset` dictionary. It processes image files, corresponding annotation files (YOLO labels), and class names
        from `data.yaml` if available.

        :param zip_file:
            A `zipfile.ZipFile` object representing the YOLO dataset archive.

        :param dataset:
            A dictionary that will be populated with the extracted YOLO dataset. The dataset will include:
            - `images`: A list of dictionaries, each representing an image and its annotations.
            - `class_names`: A list of class names extracted from the `data.yaml` file (if present).
            - `licenses`: A list of licenses, if defined in `data.yaml`.

        :param subdirs:
            A list of subdirectory names (e.g., ['train', 'valid', 'test']) representing the different data splits.

        The method performs the following:
        1. If `data.yaml` exists in the zip file, load the class names and licenses from it.
        2. For each subdirectory (e.g., 'train', 'valid', 'test'), load the images and corresponding label files.
        3. For each image, if a corresponding label file exists, parse the bounding boxes and segmentation points.
        4. Store the images and their annotations (bounding boxes or segmentation) in the `dataset`.

        Warnings:
            - If a label file contains invalid data, the annotation for that image is skipped.
            - If a label file is missing for an image, the image will be loaded without annotations.

        Notes:
            - The method assumes YOLO-style annotation files (`.txt` files with bounding boxes or segmentation data).
            - Class names and licenses are optional and only loaded if `data.yaml` exists in the zip file.
            - Bounding boxes are expected to be in YOLO format (class_id, cx, cy, width, height), while segmentation data
              is a series of coordinates (x1, y1, x2, y2, ...).
        """

        if YOLO_YAML_FILENAME in zip_file.namelist():
            with zip_file.open(YOLO_YAML_FILENAME) as file:
                data_yaml = yaml.safe_load(file)
                dataset["class_names"] = data_yaml.get('names', [])
                dataset["licenses"] = [{"id": 1, "name": data_yaml.get('license', 'Unknown License'),
                                        "url": data_yaml.get('license_url', '')}]

        for subdir in subdirs:
            image_dir = YOLO_IMAGE_DIR_PATH_TEMPLATE.format(subdir)
            label_dir = YOLO_LABEL_DIR_PATH_TEMPLATE.format(subdir)

            if not any(path.startswith(image_dir) for path in zip_file.namelist()):
                continue

            for img_path in zip_file.namelist():
                if img_path.startswith(image_dir) and (img_path.endswith('.jpg') or img_path.endswith('.png')):
                    image_file_name = os.path.basename(img_path)
                    image_path = f"{subdir}/images/{image_file_name}"
                    label_file_name = image_file_name.replace('.jpg', '.txt').replace('.png', '.txt')
                    label_path = f"{subdir}/labels/{label_file_name}"

                    if image_path in zip_file.namelist():
                        with zip_file.open(image_path) as img_file:
                            image_content = img_file.read()

                        yolo_image = {
                            "file_name": image_file_name,
                            "annotations": [],
                            "split": subdir,
                            "source_zip": zip_file,
                            "image_content": image_content
                        }

                        if label_path in zip_file.namelist():
                            with zip_file.open(label_path) as label_file:
                                for line in io.TextIOWrapper(label_file, encoding='utf-8'):
                                    values = list(map(float, line.strip().split()))
                                    if len(values) == 5:
                                        # Handle bounding box annotations
                                        class_id, cx, cy, w, h = values
                                        yolo_annotation = {
                                            "class_id": int(class_id),
                                            "cx": cx,
                                            "cy": cy,
                                            "width": w,
                                            "height": h
                                        }
                                        yolo_image["annotations"].append(yolo_annotation)
                                    elif len(values) > 5:
                                        # Handle segmentation data
                                        class_id = int(values[0])
                                        segmentation = values[
                                                       1:]  # All remaining values are segmentation points (x1, y1, x2, y2, ...)
                                        yolo_annotation = {
                                            "class_id": class_id,
                                            "segmentation": segmentation
                                        }
                                        yolo_image["annotations"].append(yolo_annotation)

                        dataset["images"].append(yolo_image)

    def _loadhelper_yolo_from_directory(
            self,
            source: str,
            dataset: dict,
            subdirs: list
    ):

        """
        Helper method to load YOLO data from a directory.

        This method processes images and their corresponding annotation files (YOLO labels) from a specified directory
        structure. It supports YOLO's convention of having separate image and label folders for each data split
        (e.g., 'train', 'valid', 'test').

        :param source:
            A string representing the root directory containing the YOLO dataset. Each subdirectory (e.g., 'train', 'valid', 'test')
            is expected to have 'images' and 'labels' subfolders.

        :param dataset:
            A dictionary to be populated with the YOLO dataset. The dataset will include:
            - `images`: A list of dictionaries, each representing an image and its annotations.
            - `annotations`: Bounding box or segmentation data corresponding to each image.

        :param subdirs:
            A list of subdirectory names (e.g., ['train', 'valid', 'test']) representing different data splits.

        The method performs the following:
        1. For each subdirectory (e.g., 'train', 'valid', 'test'), it checks for the presence of the 'images' and 'labels' subfolders.
        2. If the required folders are present, the method iterates over each image file in the 'images' folder.
        3. For each image, it attempts to load the corresponding annotation file from the 'labels' folder.
        4. Annotations are parsed, and bounding boxes or segmentation data are extracted and added to the dataset.

        Warnings:
            - If the 'images' or 'labels' folder is missing from any subdirectory, a warning is printed, and that subdirectory is skipped.
            - If a label file contains invalid data or is missing, the image will be loaded without annotations.

        Notes:
            - This method assumes that image files have extensions `.jpg` or `.png` and that corresponding label files
              are `.txt` files in YOLO format (bounding boxes or segmentation).
            - Bounding boxes are expected to be in YOLO format (class_id, cx, cy, width, height), while segmentation data
              is a series of coordinates (x1, y1, x2, y2, ...).
            - The method reads the image content and includes it in the dataset, but the actual handling of the image data
              will depend on the use case (e.g., saving to a zip file or using it in a model).

        """

        for subdir in subdirs:
            image_dir = os.path.join(source, subdir, YOLO_IMAGES_SUBDIR)
            label_dir = os.path.join(source, subdir, YOLO_LABELS_SUBDIR)

            # Skip subdir if images or labels folders do not exist
            if not os.path.isdir(image_dir) or not os.path.isdir(label_dir):
                print(WARNING_MISSING_DIR.format(subdir))
                continue

            # Load images and annotations from the directory
            for image_file_name in os.listdir(image_dir):
                if image_file_name.endswith('.jpg') or image_file_name.endswith('.png'):
                    image_path = os.path.join(image_dir, image_file_name)
                    label_file_name = image_file_name.replace('.jpg', '.txt').replace('.png', '.txt')
                    label_path = os.path.join(label_dir, label_file_name)

                    # Read image content
                    with open(image_path, 'rb') as img_file:
                        image_content = img_file.read()

                    yolo_image = {
                        "file_name": image_file_name,
                        "annotations": [],
                        "split": subdir,
                        "image_content": image_content
                    }

                    # Load annotations if the corresponding label file exists
                    if os.path.isfile(label_path):
                        with open(label_path, 'r') as label_file:
                            for line in label_file:
                                values = list(map(float, line.strip().split()))
                                if len(values) == 5:
                                    # Handle bounding box annotations
                                    class_id, cx, cy, w, h = values
                                    yolo_annotation = {
                                        "class_id": int(class_id),
                                        "cx": cx,
                                        "cy": cy,
                                        "width": w,
                                        "height": h
                                    }
                                    yolo_image["annotations"].append(yolo_annotation)
                                elif len(values) > 5:
                                    # Handle segmentation data
                                    class_id = int(values[0])
                                    segmentation = values[
                                                   1:]  # All remaining values are segmentation points (x1, y1, x2, y2, ...)
                                    yolo_annotation = {
                                        "class_id": class_id,
                                        "segmentation": segmentation
                                    }
                                    yolo_image["annotations"].append(yolo_annotation)

                    dataset["images"].append(yolo_image)

    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> dict:

        """
        Load a YOLO dataset from various sources, including a zip file, directory, or in-memory object.

        This method supports loading YOLO datasets from different sources, such as:
        - A zip file containing YOLO-formatted data.
        - A directory path containing the necessary files for YOLO.
        - An in-memory file-like object (e.g., BytesIO) that contains the YOLO dataset.

        The method processes the dataset and populates it into a dictionary with images, class names, and licenses.
        The dataset is validated against the YOLO schema to ensure correct formatting.

        :param source:
            A string representing either a path to a zip file or directory, or a file-like object (e.g., BytesIO)
            containing the YOLO data.

        :return:
            A dictionary representing the YOLO dataset. The dictionary contains:
            - `images`: A list of dictionaries representing image metadata.
            - `class_names`: A list of class names in the dataset.
            - `licenses`: License information for the dataset, if available.

        :raises ValueError:
            If the provided source is neither a valid directory path, a file-like object, nor an opened zip file.

        :raises ValidationError:
            If the YOLO dataset does not conform to the expected schema (as defined in `yolo.json`).

        Processing Steps:
        1. If the source is a zip file, open it and load class names from `data.yaml` if available.
        2. If the source is a directory, load the necessary YOLO files from the directory structure.
        3. Validate the dataset against the YOLO schema.
        4. Return the loaded dataset.

        Notes:
        - The method supports three types of input sources: a zip file path, a directory path, and an in-memory file-like object.
        - A helper method (`_loadhelper_yolo_from_zip` or `_loadhelper_yolo_from_directory`) is used to handle different source types.
        """

        subdirs = [TRAIN_DIR, VALID_DIR, TEST_DIR]
        dataset = {
            "images": [],
            "class_names": [],
            "licenses": []
        }

        if isinstance(source, str):
            # Case 1: If the source is a file path (zip file)
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    # Load class names from data.yaml if available
                    self._loadhelper_yolo_from_zip(zip_file, dataset, subdirs)
            else:
                # Case 2: If the source is a directory path
                self._loadhelper_yolo_from_directory(source, dataset, subdirs)

        elif isinstance(source, zipfile.ZipFile):
            # Handle opened zip file case
            self._loadhelper_yolo_from_zip(source, dataset, subdirs)

        elif hasattr(source, 'read'):
            # Handle in-memory file-like object (e.g., BytesIO)
            with zipfile.ZipFile(source) as zip_file:
                self._loadhelper_yolo_from_zip(zip_file, dataset, subdirs)

        else:
            raise ValueError(INVALID_SOURCE_ERROR)

        # Validate the loaded dataset against the yolo.json schema
        try:
            validate(instance=dataset, schema=self.yolo_schema)
            print("YOLO dataset successfully validated against the YOLO schema.")
        except ValidationError as e:
            print(f"Validation error: {e.message}")

        return dataset

    def normalize(
            self,
            data: dict
    ) -> dict:

        """
        Normalize the YOLO dataset into a standardized format, supporting both object detection and segmentation datasets.

        This method processes the input YOLO dataset and converts it into a normalized format that is compatible
        with downstream applications, such as COCO-like object detection or segmentation tasks.

        :param data:
            A dictionary representing the YOLO dataset. The YOLO dataset should include:
            - `images`: A list of dictionaries, each containing image metadata (file names, content, etc.) and
              annotations (bounding boxes or segmentation data).
            - `class_names`: A list of class names used in the dataset.
            - Optionally, `licenses`: A list of license dictionaries associated with the dataset.

        :return:
            A dictionary representing the normalized dataset. The normalized dataset includes:
            - `info`: General metadata about the dataset (e.g., description, dataset name, type, creation date).
            - `images`: A list of image dictionaries with normalized metadata (file names, dimensions, split, etc.).
            - `annotations`: A list of annotation dictionaries for each image, including bounding boxes or segmentation data.
            - `categories`: A list of object categories from the dataset.
            - `licenses`: A list of licenses from the dataset (if provided).
            - `nc`: The number of categories in the dataset.
            - `names`: A list of category names.

        Raises:
            ValidationError: If the normalized dataset does not conform to the Normalizer schema.

        Notes:
            - The method automatically detects whether the dataset includes object detection or segmentation data by
              inspecting annotations. It sets the `dataset_type` field to "Object Detection" or "Segmentation" accordingly.
            - Bounding boxes (in YOLO format) are converted to COCO's "xywh" format (x, y, width, height), and segmentation
              data is transformed into a compatible format if present.
            - For segmentation data, the method calculates the bounding box and area from the segmentation points using
              OpenCV functions.
            - If an image's dimensions (width, height) are missing or invalid, the image and its annotations are skipped.


        Processing Steps:
            1. The method first checks if any segmentation data is present in the annotations. If found, the dataset type is set to "Segmentation".
            2. Each image in the dataset is processed: its metadata is extracted, and dimensions are calculated from the content if provided.
            3. Annotations are converted from YOLO's format to a normalized format. Bounding boxes are translated from YOLO's center format (cx, cy, width, height) to COCO's "xywh" format. Segmentation data is processed if present.
            4. Categories are added to the dataset, and a mapping between class IDs and category names is created.
            5. The resulting dataset is validated against the Normalizer schema to ensure its correctness.

        Warnings:
            - If an image is missing width or height information, it will be skipped with a warning.
            - If any annotations contain invalid bounding boxes or segmentation data, they will be skipped with a warning.
        """

        # Determine the dataset type (Object Detection or Segmentation)
        dataset_type = "Object Detection"
        for image in data.get('images', []):
            for ann in image.get('annotations', []):
                if 'segmentation' in ann and ann['segmentation']:
                    dataset_type = "Segmentation"
                    break  # Stop checking further once segmentation is detected

        # Create the normalized dataset structure with metadata
        normalized_dataset = {
            "info": {
                "description": f"Converted from YOLO Dataset ({dataset_type})",
                "dataset_name": "YOLO Dataset",
                "dataset_type": dataset_type,  # Use the detected dataset type
                "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "splits": {},
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": data.get("licenses", []),
            "nc": len(data.get("class_names", [])),
            "names": data.get("class_names", []),
        }

        image_id_map = {}
        annotation_id = 1

        # Convert images
        for idx, yolo_image in enumerate(data.get('images', [])):
            image_content = yolo_image.get('image_content')
            file_name = yolo_image['file_name']
            split = yolo_image['split']

            if image_content:
                width, height = get_image_dimensions(image_content)

            if width == 0 or height == 0:
                continue

            normalized_image = {
                "id": idx,
                "file_name": file_name,
                "width": width,
                "height": height,
                "split": split,
                "source_zip": yolo_image.get('source_zip'),
                "image_content": image_content
            }
            image_id_map[file_name] = idx
            normalized_dataset["images"].append(normalized_image)

        # Convert annotations
        for yolo_image in data.get('images', []):
            image_id = image_id_map.get(yolo_image['file_name'])
            if image_id is None:
                continue

            width = normalized_dataset["images"][image_id]["width"]
            height = normalized_dataset["images"][image_id]["height"]

            for ann in yolo_image.get('annotations', []):
                if 'segmentation' in ann and ann['segmentation']:
                    # Handle segmentation data
                    segmentation = [[coord * width if i % 2 == 0 else coord * height for i, coord in
                                     enumerate(ann['segmentation'])]]
                    area = cv2.contourArea(np.array(segmentation).reshape(-1, 2).astype(np.float32))
                    bbox = cv2.boundingRect(np.array(segmentation).reshape(-1, 2).astype(np.float32))
                    x, y, w, h = bbox
                else:
                    # Convert bbox from YOLO format (cx, cy, w, h) to COCO format (x, y, w, h)
                    cx, cy, w, h = ann['cx'], ann['cy'], ann['width'], ann['height']
                    x = (cx - w / 2) * width
                    y = (cy - h / 2) * height
                    bbox = [x, y, w * width, h * height]
                    segmentation = []  # No segmentation data in this case
                    area = w * h * width * height

                normalized_annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": ann['class_id'],
                    "bbox": bbox,
                    "segmentation": segmentation,
                    "area": area,
                    "iscrowd": 0,
                    "bbox_format": "xywh"
                }
                normalized_dataset["annotations"].append(normalized_annotation)
                annotation_id += 1

        # Convert categories
        for idx, class_name in enumerate(data.get("class_names", [])):
            normalized_category = {
                "id": idx,
                "name": class_name,
                "supercategory": "none"
            }
            normalized_dataset["categories"].append(normalized_category)

        # Validate the normalized dataset
        try:
            validate(instance=normalized_dataset, schema=self.normalizer_schema)
            print("Normalized dataset successfully validated against the Normalizer schema.")
        except ValidationError as e:
            print(f"Validation error in normalized dataset: {e.message}")

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:

        """
        Convert a normalized dataset to YOLO format and save it to a specified destination.

        This method takes a normalized dataset, which may include bounding box or segmentation data, and converts
        it into the YOLO format. The function processes images and their corresponding annotations, ensuring that
        bounding boxes and segmentation data are formatted correctly for YOLO. It then saves the YOLO dataset to
        the provided destination, either as a file or in-memory object.

        :param normalized_data:
            A dictionary representing the normalized dataset. The expected keys are:
            - `images`: A list of dictionaries with image metadata (file names, dimensions, content, etc.).
            - `annotations`: A list of dictionaries with annotation data (bounding boxes or segmentation).
            - `names`: A list of category names for the dataset (object classes).

        :param destination:
            A path (string) or a file-like object (such as BytesIO) where the YOLO dataset will be saved. The
            function writes the dataset to a zip file in YOLO format.

        :return:
            A dictionary representing the YOLO dataset. This includes:
            - `images`: A list of images with annotations formatted in YOLO-style.
            - `class_names`: A list of object categories from the dataset.

        Raises:
            ValueError: If the `destination` is not a valid path or file-like object.
            KeyError: If required fields (such as 'images' or 'annotations') are missing in the normalized dataset.

        Notes:
            - Bounding boxes are converted from COCO format (x, y, width, height) to YOLO format (cx, cy, width, height).
            - Segmentation data is normalized by scaling polygon coordinates relative to the image dimensions.
            - Each annotation is processed to ensure that values are normalized between 0 and 1 (as required by YOLO format).
            - The method checks for both bounding box and segmentation data in the annotations. If neither is found,
              the annotation is skipped with a warning.
            - Width and height values are required for all images; images without these values will be skipped.

        Processing Steps:
            1. For each image in the dataset, retrieve its annotations and process bounding boxes or segmentation data.
            2. Convert bounding boxes from COCO's "xywh" format to YOLO's "cxcywh" format (center x, center y, width, height).
            3. Ensure all bounding box values are normalized (between 0 and 1) and round to six decimal places.
            4. If segmentation data is present, normalize the coordinates and format them for YOLO.
            5. Group the annotations by image and save the resulting YOLO dataset to the provided destination.

        Warnings:
            - If an image has missing or invalid dimensions (width, height), it will be skipped.
            - If an annotation lacks both bounding box and segmentation data, it will be skipped with a warning.
            - Segmentation data is expected to be in the form of a list of polygons (list of lists). If it's not in the correct format,
              the segmentation will be skipped with a warning.
        """

        # Initialize a list to store YOLO-format images
        yolo_images = []

        # Create a mapping from image ID to annotations
        image_to_annotations = {}
        for annotation in normalized_data.get('annotations', []):
            if annotation['image_id'] not in image_to_annotations:
                image_to_annotations[annotation['image_id']] = []
            image_to_annotations[annotation['image_id']].append(annotation)

        print(f"Total Images to Convert: {len(normalized_data.get('images', []))}")
        print(f"Total Annotations: {len(normalized_data.get('annotations', []))}\n")

        # Process each image and its corresponding annotations
        for normalized_image in normalized_data.get('images', []):
            annotations = image_to_annotations.get(normalized_image['id'], [])

            print(f"Processing Image: {normalized_image['file_name']}, Annotations Count: {len(annotations)}")

            # List of YOLO-format annotations for this image
            yolo_annotations = []

            for normalized_annotation in annotations:
                # Ensure 'width' and 'height' are present
                if 'width' not in normalized_image or 'height' not in normalized_image:
                    print(
                        f"Error: Missing 'width' or 'height' for image {normalized_image['file_name']}. Skipping this image.")
                    break  # Skip to next image

                img_width = normalized_image['width']
                img_height = normalized_image['height']

                # Check if 'bbox' exists or 'segmentation' exists
                has_bbox = 'bbox' in normalized_annotation and normalized_annotation['bbox']
                has_segmentation = 'segmentation' in normalized_annotation and normalized_annotation['segmentation']

                if not has_bbox and not has_segmentation:
                    print(
                        f"Warning: No bbox or segmentation found for annotation in image {normalized_image['file_name']}.")
                    continue  # Skip annotations without bbox or segmentation

                # Process bounding box if present
                if has_bbox:
                    if normalized_annotation.get('bbox_format') == 'xywh':  # COCO format
                        x, y, w, h = normalized_annotation['bbox']
                        # Convert COCO bbox (xywh) to YOLO bbox (cxcywh)
                        cx = (x + w / 2) / img_width
                        cy = (y + h / 2) / img_height
                        width = w / img_width
                        height = h / img_height
                    else:
                        print(f"Warning: Unsupported bbox format: {normalized_annotation.get('bbox_format')}")
                        continue

                    # Ensure values are between 0 and 1 (for YOLO format)
                    cx = min(max(cx, 0.0), 1.0)
                    cy = min(max(cy, 0.0), 1.0)
                    width = min(max(width, 0.0), 1.0)
                    height = min(max(height, 0.0), 1.0)

                    # Round values to six decimal places
                    cx = round(cx, 6)
                    cy = round(cy, 6)
                    width = round(width, 6)
                    height = round(height, 6)

                    print(
                        f"  Annotation Class ID: {normalized_annotation['category_id']}, BBox: ({cx}, {cy}, {width}, {height})")

                    # Create a YOLO annotation dictionary entry
                    yolo_annotation = {
                        'class_id': normalized_annotation['category_id'],
                        'bbox': [cx, cy, width, height],
                        'segmentation': normalized_annotation.get('segmentation', [])
                    }
                    yolo_annotations.append(yolo_annotation)

                # Process segmentation if present
                if has_segmentation and normalized_annotation['segmentation']:
                    # Handle segmentation annotations
                    # Assuming segmentation is a list of polygons (list of lists)
                    for seg in normalized_annotation['segmentation']:
                        if not isinstance(seg, list):
                            print(
                                f"Warning: Segmentation data is not a list of lists for image {normalized_image['file_name']}. Skipping this segmentation.")
                            continue
                        try:
                            normalized_segmentation = [
                                coord / img_width if i % 2 == 0 else coord / img_height
                                for i, coord in enumerate(seg)
                                if isinstance(coord, (int, float))
                            ]
                            print(
                                f"  Processing Segmentation for Class ID: {normalized_annotation['category_id']}, Segmentation: {normalized_segmentation}")

                            # Prepare the line to include class_id followed by segmentation points
                            seg_str = " ".join(f"{coord:.6f}" for coord in normalized_segmentation)
                            seg_annotation = {
                                'class_id': normalized_annotation['category_id'],
                                'segmentation': [normalized_segmentation],  # Wrap in list
                                'bbox': []  # No bbox for segmentation-only annotations
                            }
                            yolo_annotations.append(seg_annotation)
                        except Exception as e:
                            print(f"Error processing segmentation for image {normalized_image['file_name']}: {e}")

            if len(yolo_annotations) == 0:
                print(f"Warning: No annotations found for image {normalized_image['file_name']}")

            # Create the image entry, including 'width' and 'height'
            yolo_image = {
                "file_name": normalized_image['file_name'],
                "annotations": yolo_annotations,
                "split": normalized_image['split'],  # Include split attribute
                "source_zip": normalized_image.get('source_zip'),
                "image_content": normalized_image.get('image_content'),
                "width": normalized_image['width'],
                "height": normalized_image['height']
            }

            yolo_images.append(yolo_image)

        # Prepare YOLO dataset
        yolo_dataset = {
            "images": yolo_images,
            "class_names": normalized_data.get('names', [])
        }

        # Save the YOLO dataset to destination
        self.save(yolo_dataset, destination)

        return yolo_dataset

    def save(
            self,
            data: dict,
            destination: Union[str, io.BytesIO, None] = None
    ):

        """
        Save the YOLO dataset to a zip file or an in-memory buffer.

        This method validates the YOLO dataset against the YOLO schema, then writes the dataset to the specified
        destination in YOLO format, including images, annotations, and the `data.yaml` configuration file.

        :param data:
            A dictionary representing the YOLO dataset. The dictionary should have the following structure:
            - `images`: A list of dictionaries with image metadata, including:
                - `file_name`: The name of the image file.
                - `annotations`: A list of annotations for the image, which can include:
                    - `class_id`: The category ID for the object in the image.
                    - `bbox`: The bounding box for the object (in YOLO format).
                    - `segmentation`: The segmentation points (if applicable).
                - `split`: The data split to which the image belongs (e.g., 'train', 'valid', or 'test').
                - `image_content`: The raw binary content of the image file.
            - `class_names`: A list of object class names.

        :param destination:
            The path or BytesIO object where the YOLO dataset will be saved. If `None`, the dataset is written to
            an in-memory BytesIO zip file and returned.

        :return:
            If `destination` is a BytesIO object or `None`, the method returns the in-memory BytesIO object containing
            the zip file. Otherwise, it returns `None`.

        Raises:
            ValidationError: If the YOLO dataset does not conform to the expected schema.

        Notes:
            - This method generates the YOLO `data.yaml` configuration file, which includes paths to the images, the number
              of classes (`nc`), and the class names (`names`).
            - Each image is saved into its corresponding split folder (`train`, `valid`, or `test`), and the annotations are
              saved as text files in the respective `labels` folder.
            - Bounding boxes are expected to be in YOLO format (cx, cy, width, height), where all values are normalized between 0 and 1.
            - Segmentation data, if available, is saved in the label files following the class ID and bounding box data.

        Warnings:
            - If an image is missing 'width' or 'height', it will be skipped, and a warning will be printed.
            - If an annotation contains invalid bounding box or segmentation data, it will be skipped with a warning.
            - Empty label files are not saved, and a warning is printed if there are no valid annotations for an image.

        Processing Steps:
            1. Validate the YOLO dataset against the provided YOLO schema.
            2. Write the `data.yaml` file with the dataset's structure and class names.
            3. Save each image and its corresponding label (if available) into their respective split directories (`train`, `valid`, `test`).
            4. Ensure segmentation and bounding box data are correctly formatted and saved in the label files.
            5. Return the in-memory zip file if no destination is provided.
        """

        # Validate the data against the YOLO schema before saving
        try:
            validate(instance=data, schema=self.yolo_schema)
            print("YOLO dataset successfully validated against the YOLO schema.")
        except ValidationError as e:
            print(f"Validation error in YOLO dataset: {e.message}")
            raise

        # If destination is None, create an in-memory BytesIO zip file
        if destination is None:
            destination = io.BytesIO()

        with zipfile.ZipFile(destination, 'w') as zip_file:
            # Create the YAML structure with correct paths and names formatting
            dataset_yaml = {
                'train': '../train/images',
                'val': '../valid/images',
                'test': '../test/images',
                'nc': len(data['class_names']),
                'names': data['class_names']
            }

            # Use yaml.safe_dump to generate the YAML content
            yaml_content = yaml.safe_dump(
                dataset_yaml,
                default_flow_style=False,
                sort_keys=False
            )

            # Manually adjust the 'names' field to be formatted with single quotes inside brackets
            yaml_lines = yaml_content.splitlines()
            formatted_lines = []
            for line in yaml_lines:
                if line.startswith('names:'):
                    # Correctly format the names list with single quotes
                    names_str = ', '.join([f"'{name}'" for name in data['class_names']])
                    formatted_lines.append(f"names: [{names_str}]")
                elif not line.startswith('- '):  # Avoid adding extra list items
                    formatted_lines.append(line)
            yaml_content = '\n'.join(formatted_lines)

            # Write the corrected YAML content to the zip file
            zip_file.writestr("data.yaml", yaml_content)
            print("Saved data.yaml")

            # Save images and labels into respective directories within the zip file
            for image in data['images']:
                # Rename 'validation' folder to 'valid' for consistency
                split_dir = f"{'valid' if image['split'] == 'validation' else image['split']}/images"
                labels_dir = f"{'valid' if image['split'] == 'validation' else image['split']}/labels"

                # Save image content if available
                if image.get('image_content'):
                    zip_file.writestr(os.path.join(split_dir, image['file_name']), image['image_content'])
                    print(f"Saved image: {os.path.join(split_dir, image['file_name'])}")
                else:
                    print(f"Warning: No image content available for {image['file_name']}")

                # Create and add the label file to the zip archive
                label_file_name = os.path.splitext(image['file_name'])[0] + '.txt'
                label_zip_path = os.path.join(labels_dir, label_file_name)  # Save to the labels folder
                label_content = ""

                # Ensure 'width' and 'height' are present
                if 'width' not in image or 'height' not in image:
                    print(
                        f"Error: Missing 'width' or 'height' for image {image['file_name']}. Skipping label creation.")
                    continue

                width = image['width']
                height = image['height']

                # Generate label content
                for annotation in image.get('annotations', []):
                    if isinstance(annotation, dict):
                        if 'segmentation' in annotation and annotation['segmentation']:
                            # Handle segmentation annotations
                            try:
                                # Check if segmentation is a list of lists
                                if not all(isinstance(seg, list) for seg in annotation['segmentation']):
                                    print(
                                        f"Warning: Segmentation data is not a list of lists for image {image['file_name']}. Skipping this segmentation.")
                                    continue

                                # Normalize and flatten all polygons
                                normalized_segmentation = [
                                    coord / width if i % 2 == 0 else coord / height
                                    for seg in annotation['segmentation']
                                    for i, coord in enumerate(seg)
                                    if isinstance(coord, (int, float))
                                ]

                                # Prepare the line to include class_id followed by segmentation points
                                seg_str = " ".join(f"{coord:.6f}" for coord in normalized_segmentation)
                                line = f"{annotation['class_id']} {seg_str}"
                                label_content += line + "\n"
                            except Exception as e:
                                print(f"Error processing segmentation for image {image['file_name']}: {e}")
                        elif 'bbox' in annotation and annotation['bbox']:
                            # Handle bounding box annotations
                            bbox = annotation['bbox']
                            if isinstance(bbox, list) and len(bbox) == 4:
                                cx, cy, width_norm, height_norm = bbox
                                # Prepare the line to include class_id and normalized bbox coordinates
                                line = f"{annotation['class_id']} {cx:.6f} {cy:.6f} {width_norm:.6f} {height_norm:.6f}"
                                label_content += line + "\n"
                            else:
                                print(f"Warning: Invalid bbox format for annotation in image {image['file_name']}.")
                        else:
                            print(
                                f"Warning: Missing bbox or segmentation data for annotation in image {image['file_name']}.")
                    else:
                        print(f"Warning: Annotation for image {image['file_name']} is not a dictionary. Skipping...")

                # Ensure the label content is not empty before writing to file
                if label_content.strip():
                    zip_file.writestr(label_zip_path, label_content)
                    print(f"Saved label file: {label_zip_path} with {len(image.get('annotations', []))} annotations")
                else:
                    print(f"Warning: Empty label file for {image['file_name']}")

        # Final success message
        if isinstance(destination, io.BytesIO):
            print("YOLO dataset successfully written to the in-memory zip file.")
        else:
            print(f"YOLO dataset successfully saved to '{destination}'.")

        # Return the in-memory zip file if destination was None
        if isinstance(destination, io.BytesIO):
            destination.seek(0)
            return destination


class BinaExpertsConvertor(BaseConvertor):

    """
        BinaExpertsConvertor is responsible for converting datasets to and from the BinaExperts format.

        This class inherits from `BaseConvertor` and provides methods to handle conversions between
        normalized datasets and the BinaExperts-specific dataset format. The format includes metadata,
        image data, annotations, and specific settings required by the BinaExperts platform.

        Attributes:
            binaexperts_schema (dict):
                The JSON schema for validating BinaExperts dataset formats.
            normalizer_schema (dict):
                The JSON schema for validating normalized datasets before conversion.

        Methods:
            convert(normalized_data: dict, destination: Union[str, IO[bytes]]) -> dict:
                Converts a normalized dataset into the BinaExperts format and saves it to the specified destination.

            normalize(data: dict) -> dict:
                Converts a BinaExperts dataset into a normalized format.

            save(data: dict, destination: Union[str, IO[bytes]] = None):
                Saves the BinaExperts dataset to a zip file or an in-memory buffer.


        Notes:
            - The BinaExperts format includes additional fields like `labels`, `errors`, `tile_settings`, and
              `augmentation_settings`, which are not part of standard formats like COCO or YOLO.
            - This converter ensures that these additional fields are handled appropriately during conversion.
        """

    def __init__(self):
        """
            Initialize the BinaExpertsConvertor class.

            This constructor loads the JSON schemas for BinaExperts and Normalizer formats, which are used
            for validating datasets during the conversion process. The schemas are stored in JSON files
            and loaded when the class is instantiated.

            The BinaExperts schema defines the structure for datasets in the BinaExperts format, and the
            Normalizer schema provides the structure for normalized datasets that will be converted into
            or from the BinaExperts format.

            The schemas are loaded from the following paths:
            - `binaexperts.json`: Defines the structure of BinaExperts datasets.
            - `normalizer.json`: Defines the structure of the normalized dataset format.

            Attributes:
                binaexperts_schema (dict):
                    A dictionary representing the BinaExperts dataset schema, loaded from `binaexperts.json`.
                normalizer_schema (dict):
                    A dictionary representing the normalized dataset schema, loaded from `normalizer.json`.

            """

        super().__init__()
        # Load the JSON schema for BinaExperts and Normalizer using relative paths from the current file
        binaexperts_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'binaexperts.json')
        normalizer_schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'normalizer.json')

        # Load BinaExperts schema
        with open(binaexperts_schema_path, 'r') as schema_file:
            self.binaexperts_schema = json.load(schema_file)

        # Load Normalizer schema
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def _loadhelper_binaexperts_data(
            self,
            bina_data,
            dataset,
            image_folder,
            source_zip=None
    ):

        """
            Helper method to load categories, images, annotations, and additional fields from BinaExperts data.

            This method processes the input BinaExperts dataset and loads the categories, images, annotations, and
            additional fields (e.g., labels, classifications, augmentation settings) into the `dataset` dictionary.
            It handles both local files and files contained in a zip archive.

            :param bina_data: dict
                The parsed BinaExperts dataset in JSON format, containing categories, images, annotations,
                and additional fields such as 'labels', 'classifications', 'augmentation_settings', and 'tile_settings'.
            :param dataset: dict
                The target dictionary where the categories, images, annotations, and additional fields will be added.
            :param image_folder: str
                The folder name where the image data is stored (e.g., 'train_images', 'valid_images'). This name is
                used to assign the 'split' attribute to each image (e.g., 'train', 'valid').
            :param source_zip: zipfile.ZipFile, optional
                An optional zip file object. If provided, this method will attempt to read image content directly
                from the zip file. Otherwise, it will assume that the images are available locally.

            :return: None
                The `dataset` dictionary is modified in place with categories, images, annotations, and additional fields.

            Warnings:
                - If an image file cannot be found in the provided zip archive, a warning will be printed.
                - If an annotation refers to an image ID that does not exist in the dataset, the annotation will be skipped.

            Processing Steps:
                1. Load categories from `bina_data` if not already present in the `dataset`.
                2. Load images and attempt to read their content from `source_zip`, if provided.
                3. Load annotations, ensuring that each annotation refers to an existing image.
                4. Load additional fields such as 'labels', 'classifications', 'augmentation_settings', 'tile_settings',
                   and 'false_positive'.
                5. Safely handle the 'errors' field by ensuring it exists in the `dataset`.

            Notes:
                - The 'split' attribute for each image is determined by removing the '_images' suffix from `image_folder`.
                  For example, 'train_images' will be converted to 'train'.
                - The method ensures that the 'errors' field is safely added to the `dataset`, even if it doesn't exist
                  in the input `bina_data`.
        """

        # Load categories if not already present
        if not dataset['categories']:
            for cat in bina_data.get('categories', []):
                category = {
                    'id': cat['id'],
                    'name': cat['name'],
                    'supercategory': cat.get('supercategory', 'none')
                }
                dataset['categories'].append(category)

        # Load images
        for img in bina_data.get('images', []):
            image_id = img['id']  # Use image 'id' as is
            image_file_name = img['file_name']
            image_path = f"{image_folder}/{image_file_name}"

            image_content = None
            if source_zip and image_path in source_zip.namelist():
                with source_zip.open(image_path) as img_file:
                    image_content = img_file.read()
            elif source_zip:
                print(f"Warning: Image file {image_path} not found in zip archive.")

            image = {
                'id': image_id,
                'file_name': image_file_name,
                'width': img.get('width', 0),
                'height': img.get('height', 0),
                'split': image_folder.replace('_images', ''),  # 'train_images' -> 'train'
                'source_zip': source_zip,
                'image_content': image_content
            }
            dataset['images'].append(image)

        # Load annotations
        image_ids = set(img['id'] for img in dataset['images'])
        for ann in bina_data.get('annotations', []):
            image_id = ann['image_id']  # Assuming it's same as 'id' in images
            if image_id not in image_ids:
                print(f"Warning: Image ID {image_id} for annotation ID {ann['id']} does not exist. Skipping...")
                continue
            annotation = {
                'id': ann['id'],
                'image_id': image_id,
                'category_id': ann['category_id'],
                'bbox': ann['bbox'],
                'segmentation': ann.get('segmentation', []),
                'area': ann.get('area', 0.0),
                'iscrowd': ann.get('iscrowd', 0),
                'bbox_format': 'xywh'
            }
            dataset['annotations'].append(annotation)

        # Load additional fields, if present
        dataset['labels'] = bina_data.get('labels', [])
        dataset['classifications'] = bina_data.get('classifications', [])
        dataset['augmentation_settings'] = bina_data.get('augmentation_settings', {})
        dataset['tile_settings'] = bina_data.get('tile_settings', {"type": None, "enabled": False, "tile_width": None,
                                                                   "tile_height": None})
        dataset['false_positive'] = bina_data.get('false_positive', {"False_positive": False})

        # Safely load 'errors' field if present
        if 'errors' in bina_data:
            if 'errors' not in dataset:
                dataset['errors'] = []
            dataset['errors'].extend(bina_data.get('errors', []))
        else:
            # Ensure 'errors' key exists
            if 'errors' not in dataset:
                dataset['errors'] = []

    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Dict:

        """
            Load BinaExperts dataset from a zip file, directory, or an in-memory object.

            This method loads a BinaExperts dataset, validates it against the BinaExperts schema, and returns it as a dictionary.
            It supports loading data from:
            - A zip file containing BinaExperts-formatted annotations and images
            - A directory containing BinaExperts-formatted annotation files
            - An in-memory file-like object (e.g., BytesIO)

            The dataset is divided into 'train', 'test', and 'valid' splits, and the method searches for the corresponding
            annotation files within each split directory. The data is validated against the BinaExperts schema before being
            loaded into a unified dataset dictionary.

            :param source:
                A Path, a file-like object (such as a BytesIO), or an opened ZipFile containing the BinaExperts data.

            :return:
                A dictionary representing the BinaExperts dataset, containing the following keys:
                - 'info': General information about the dataset.
                - 'images': A list of image metadata, including image IDs, file names, dimensions, and more.
                - 'annotations': A list of annotations, including bounding boxes, segmentation, and other relevant details.
                - 'categories': A list of categories (object classes) defined in the dataset.
                - 'licenses': License information related to the dataset.

            :raises ValueError:
                If the source is not a valid directory path, file-like object, or an opened zip file.

            :raises ValidationError:
                If the dataset in a split does not conform to the BinaExperts schema.

            Warnings:
                - If an annotation file is not found in any of the expected subdirectories (train, test, valid), a warning is printed,
                  and that subdirectory is skipped.
                - If validation of a subdirectory's annotations fails, a warning is printed, and that subdirectory is skipped.

            Notes:
                - This method is flexible enough to handle both file paths (directories and zip files) and in-memory file-like objects.
                - The helper method `_loadhelper_binaexperts_data` is used to manage the loading and processing of BinaExperts-formatted data.
            """

        subdir_mapping = {
            'train': 'train_images',
            'test': 'test_images',
            'valid': 'validation_images'
        }

        annotation_files = {
            'train': 'train_coco.json',
            'test': 'test_coco.json',
            'valid': 'val_coco.json'
        }

        dataset = {
            'info': {},
            'images': [],
            'annotations': [],
            'categories': [],
            'licenses': []
        }

        if isinstance(source, str):
            # If the source is a file path (zip file)
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    for split, subdir in subdir_mapping.items():
                        annotation_path = f"cocos/{annotation_files[split]}"

                        # Skip split if the annotation file does not exist
                        if annotation_path not in zip_file.namelist():
                            print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                            continue

                        with zip_file.open(annotation_path) as file:
                            coco_data = json.load(file)

                            # Validate coco_data against the loaded schema to ensure its structure is correct
                            try:
                                validate(instance=coco_data, schema=self.binaexperts_schema)
                            except ValidationError as e:
                                print(f"Validation error in {subdir}: {e.message}")
                                continue  # Skip processing this subdir if validation fails

                        # Use the helper method to load data
                        self._loadhelper_binaexperts_data(coco_data, dataset, subdir, source_zip=zip_file)

            else:
                # If the source is a directory path
                for split, subdir in subdir_mapping.items():
                    annotation_file = os.path.join(source, 'cocos', annotation_files[split])

                    # Skip subdir if the annotation file does not exist
                    if not os.path.isfile(annotation_file):
                        print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                        continue

                    with open(annotation_file, 'r') as file:
                        coco_data = json.load(file)

                        # Validate coco_data against the loaded schema to ensure its structure is correct
                        try:
                            validate(instance=coco_data, schema=self.binaexperts_schema)
                        except ValidationError as e:
                            print(f"Validation error in {subdir}: {e.message}")
                            continue  # Skip processing this subdir if validation fails

                    # Use the helper method to load data
                    self._loadhelper_binaexperts_data(coco_data, dataset, subdir)

        elif isinstance(source, zipfile.ZipFile):
            # Handle opened zip file case
            for split, subdir in subdir_mapping.items():
                annotation_path = f"cocos/{annotation_files[split]}"

                # Skip split if the annotation file does not exist
                if annotation_path not in source.namelist():
                    print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                    continue

                with source.open(annotation_path) as file:
                    coco_data = json.load(file)

                    # Validate coco_data against the loaded schema to ensure its structure is correct
                    try:
                        validate(instance=coco_data, schema=self.binaexperts_schema)
                    except ValidationError as e:
                        print(f"Validation error in {subdir}: {e.message}")
                        continue  # Skip processing this subdir if validation fails

                # Use the helper method to load data
                self._loadhelper_binaexperts_data(coco_data, dataset, subdir, source_zip=source)

        elif hasattr(source, 'read'):
            # If the source is a file-like object (e.g., BytesIO), open it as a zip file
            with zipfile.ZipFile(source, 'r') as zip_file:
                for split, subdir in subdir_mapping.items():
                    annotation_path = f"cocos/{annotation_files[split]}"

                    # Skip split if the annotation file does not exist
                    if annotation_path not in zip_file.namelist():
                        print(f"Warning: Annotation file not found in {subdir}. Skipping this subdir.")
                        continue

                    with zip_file.open(annotation_path) as file:
                        coco_data = json.load(file)

                        # Validate coco_data against the loaded schema to ensure its structure is correct
                        try:
                            validate(instance=coco_data, schema=self.binaexperts_schema)
                        except ValidationError as e:
                            print(f"Validation error in {subdir}: {e.message}")
                            continue  # Skip processing this subdir if validation fails

                    # Use the helper method to load data
                    self._loadhelper_binaexperts_data(coco_data, dataset, subdir, source_zip=zip_file)

        else:
            raise ValueError("Source must be either a directory path, a file-like object, or an opened zip file.")

        return dataset

    def normalize(
            self,
            data: dict
    ) -> dict:

        """
            Convert BinaExperts dataset dictionary to a normalized dataset dictionary.

            This method converts a BinaExperts dataset into a normalized format that simplifies downstream processing
            and ensures consistency across different datasets. It preserves key information from the BinaExperts format
            (such as images, annotations, categories, and additional metadata) and maps it into a format that is more
            widely usable for machine learning tasks, including object detection and segmentation.

            :param data:
                A dictionary representing the BinaExperts dataset, which should include the following keys:
                - `info`: Metadata about the dataset (e.g., dataset name, type, etc.).
                - `images`: A list of dictionaries representing images and their metadata.
                - `annotations`: A list of dictionaries representing annotations for the images (e.g., bounding boxes, segmentation).
                - `categories`: A list of dictionaries representing object categories.
                - `licenses`: (Optional) A list of dictionaries representing license information.
                - `errors`: (Optional) A list of dictionaries representing errors.
                - `labels`, `classifications`, `augmentation_settings`, `tile_settings`, and `false_positive`: (Optional) Additional fields.

            :return:
                A dictionary representing the normalized dataset with the following keys:
                - `info`: General information about the dataset.
                - `images`: A list of normalized image metadata.
                - `annotations`: A list of normalized annotations (with bbox and segmentation data).
                - `categories`: A list of normalized categories.
                - `licenses`: License information if provided.
                - Additional fields: `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`, `false_positive`.
                - `nc`: Number of categories.
                - `names`: List of category names.

            :raises KeyError:
                If required fields (like 'images', 'annotations', or 'categories') are missing from `data`.

            Warnings:
                - If an image is missing 'width' or 'height', it will be skipped.
                - If an annotation is missing 'category_id' or 'image_id', it will be skipped.

            Notes:
                - Bounding boxes (bbox) are expected to be in the xywh format (x, y, width, height).
                - Segmentation data, if present, is carried over in the annotations.
                - The method creates unique mappings for category and image IDs to ensure consistency.
            """

        normalized_dataset = {
            "info": {
                "description": "Converted from BinaExperts",
                "dataset_name": data['info'].get('dataset', 'BinaExperts Dataset'),
                "dataset_type": data['info'].get('dataset_type', 'Object Detection and Segmentation'),
                "splits": {}  # Add split information if necessary
            },
            "images": [],
            "annotations": [],
            "categories": [],
            "licenses": data.get("licenses", []),
            "nc": len(data['categories']),
            "names": [cat['name'] for cat in data['categories']],
            "errors": data.get('errors', []),
            "labels": data.get('labels', []),
            "classifications": data.get('classifications', []),
            "augmentation_settings": data.get('augmentation_settings', {}),
            "tile_settings": data.get('tile_settings',
                                      {"type": None, "enabled": False, "tile_width": None, "tile_height": None}),
            "false_positive": data.get('false_positive', {"False_positive": False})
        }

        # Create category ID mapping
        category_id_map = {cat['id']: idx for idx, cat in enumerate(data['categories'])}

        # Map image IDs to normalized IDs
        image_id_map = {image['id']: idx for idx, image in enumerate(data['images'])}

        annotation_id = 1  # Initialize annotation ID

        # Convert and add images
        for image in data['images']:
            # Ensure 'width' and 'height' are present
            if 'width' not in image or 'height' not in image:
                print(f"Warning: Image {image['file_name']} is missing 'width' or 'height'. Skipping...")
                continue  # Skip images without width or height

            normalized_image = {
                "id": image_id_map[image['id']],
                "file_name": image['file_name'],
                "width": image['width'],
                "height": image['height'],
                "split": image.get('split', 'train'),  # Default to 'train' if split not specified
                "source_zip": image.get('source_zip'),
                "image_content": image.get('image_content')
            }
            normalized_dataset["images"].append(normalized_image)

        # Convert and add annotations
        for ann in data['annotations']:
            if ann['category_id'] not in category_id_map:
                print(f"Warning: Unknown category_id {ann['category_id']} for annotation ID {ann['id']}. Skipping...")
                continue  # Skip unknown categories

            if 'image_id' not in ann:
                print(f"Warning: Annotation ID {ann['id']} is missing 'image_id'. Skipping...")
                continue  # Skip annotations without image_id

            if ann['image_id'] not in image_id_map:
                print(f"Warning: Image ID {ann['image_id']} for annotation ID {ann['id']} does not exist. Skipping...")
                continue  # Skip annotations with invalid image_id

            normalized_annotation = {
                "id": annotation_id,
                "image_id": image_id_map[ann['image_id']],
                "category_id": category_id_map[ann['category_id']],
                "bbox": ann.get('bbox', []),
                "segmentation": ann.get('segmentation', []),
                "area": ann.get('area', 0.0),
                "iscrowd": ann.get('iscrowd', 0),
                "bbox_format": 'xywh'  # BinaExperts uses xywh format like COCO
            }
            normalized_dataset["annotations"].append(normalized_annotation)
            annotation_id += 1

        # Convert and add categories
        for cat in data['categories']:
            normalized_category = {
                "id": category_id_map[cat['id']],
                "name": cat['name'],
                "supercategory": cat.get('supercategory', 'none')
            }
            normalized_dataset["categories"].append(normalized_category)

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:


        """
            Convert the normalized dataset format back to BinaExperts format and write it to the destination.

            This method takes a normalized dataset and converts it into the BinaExperts format, populating
            metadata, images, annotations, and additional fields like errors, labels, classifications, and tile settings.
            The converted dataset is then written to the specified destination, either as a zip file or a file-like object.

            :param normalized_data:
                A dictionary representing the normalized dataset. It should contain:
                - `description`: A string describing the dataset.
                - `organization`: A string representing the dataset's organization.
                - `dataset_name`: The name of the dataset.
                - `dataset_type`: The type of the dataset (e.g., Object Detection).
                - `date_created`: The creation date of the dataset.
                - `licenses`: A list of licenses related to the dataset.
                - `images`: A list of image metadata (image file names, dimensions, etc.).
                - `annotations`: A list of annotations, including bounding boxes and other metadata.
                - `categories`: A list of object categories (e.g., names of object classes).
                - `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`, `False_positive`: (Optional) Additional fields.

            :param destination:
                A file-like object (e.g., zip file, directory path) where the BinaExperts dataset will be written.

            :return:
                A dictionary representing the BinaExperts dataset, including:
                - `info`: General metadata about the dataset.
                - `images`: A list of images with file names and dimensions.
                - `annotations`: A list of annotations with bounding boxes and segmentation.
                - `categories`: Object category information.
                - `licenses`: License information.
                - `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`, `False_positive`: Additional fields.

            Warnings:
                - If an annotation's bounding box height exceeds 1.0, an error entry is added to the `errors` list.
                - If certain fields (e.g., `augmentation_settings`, `labels`, `classifications`, `tile_settings`) are missing,
                  default values will be added to ensure a complete BinaExperts dataset.

            Notes:
                - The method ensures that fields like `augmentation_settings`, `labels`, `classifications`, and `tile_settings`
                  are always present in the output dataset, even if they are not provided in the normalized dataset.
                - Bounding boxes are expected to be in the xywh format (x, y, width, height).
                - The method performs error handling on annotations, particularly checking bounding box dimensions and logging
                  errors for anomalies.
        """

        # Create a BinaExperts dataset object with required metadata
        binaexperts_dataset = {
            "info": {
                "description": normalized_data.get("description", ""),
                "organization": normalized_data.get("organization", ""),
                "dataset": normalized_data.get("dataset_name", ""),
                "dataset_type": normalized_data.get("dataset_type", ""),
                "date_created": normalized_data.get("date_created", datetime.datetime.now().strftime('%Y-%m-%d'))
                # Consistent with import
            },
            "licenses": normalized_data.get("licenses", []),
            "images": normalized_data.get("images", []),
            "annotations": normalized_data.get("annotations", []),
            "categories": normalized_data.get("categories", []),
            "errors": [],
            "labels": [],
            "classifications": [],
            "augmentation_settings": {},
            "tile_settings": {
                "tile_type": None,
                "enabled": False,
                "tile_width": None,
                "tile_height": None
            },
            "False_positive": {
                "False_positive": False
            }
        }

        # Processing logic for errors
        for annotation in normalized_data.get("annotations", []):
            if annotation['bbox'][3] > 1.0:  # Assume the height value should not be greater than 1.0
                error = {
                    "annotation_type": "box",
                    "annotation": {
                        "x": annotation['bbox'][0],
                        "y": annotation['bbox'][1],
                        "width": annotation['bbox'][2],
                        "height": annotation['bbox'][3]
                    },
                    "image_id": annotation['image_id'],
                    "image_file_name": next(
                        (img['file_name'] for img in normalized_data['images'] if img['id'] == annotation['image_id']),
                        ""),
                    "error_message": f"Albumentations: Expected bbox height to be <= 1.0, got {annotation['bbox'][3]}"
                }
                binaexperts_dataset['errors'].append(error)

        # Ensure augmentation settings, labels, classifications, and tile settings are added (even if empty)
        binaexperts_dataset['augmentation_settings'] = normalized_data.get("augmentation_settings", {})
        binaexperts_dataset['labels'] = normalized_data.get("labels", [])
        binaexperts_dataset['classifications'] = normalized_data.get("classifications", [])
        binaexperts_dataset['tile_settings'] = normalized_data.get("tile_settings", {
            "tile_type": None,
            "enabled": False,
            "tile_width": None,
            "tile_height": None
        })
        binaexperts_dataset['False_positive'] = normalized_data.get("False_positive", {
            "False_positive": False
        })

        # Write the BinaExperts format dataset to the destination
        self.save(binaexperts_dataset, destination)

        return binaexperts_dataset

    def save(
            self,
            data: dict,
            destination: Union[str, IO[bytes]] = None
    ):


        """
            Save the BinaExperts dataset into a zip file with the appropriate folder structure.

            This method saves a BinaExperts dataset into a zip archive. It includes the dataset's images, annotations,
            and additional fields specific to the BinaExperts format (such as errors, labels, classifications, augmentation settings,
            and tile settings). The resulting archive contains images split into folders based on their dataset split (e.g.,
            'train_images', 'validation_images') and COCO-formatted JSON files for annotations.

            :param data:
                A dictionary representing the BinaExperts dataset. It should include:
                - `info`: General information about the dataset.
                - `images`: A list of dictionaries representing image metadata (file names, dimensions, etc.).
                - `annotations`: A list of dictionaries representing annotations (bounding boxes, segmentation, etc.).
                - `categories`: A list of dictionaries representing object categories.
                - `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`: (Optional) Additional fields.

            :param destination:
                A path or a file-like object (e.g., a BytesIO object) where the zip archive will be written.
                If no destination is provided, an in-memory BytesIO object is used.

            :return:
                If a file-like object (e.g., BytesIO) was provided as the destination, the method returns the BytesIO object
                containing the zip archive.

            Warnings:
                - If an image file is not found in the zip archive when provided via a zip source, a warning is logged.
                - If an image has no content associated with it, a warning is logged.

            Notes:
                - The method ensures that fields like `errors`, `labels`, `classifications`, `augmentation_settings`,
                  and `tile_settings` are always present in the output dataset, even if they are not provided in the
                  input dataset.
                - The method handles the conversion of the `tile_settings` field, correcting the field names from
                  the internal format (`tile_type`) to the BinaExperts format (`type`).
        """

        if destination is None:
            destination = io.BytesIO()

        with zipfile.ZipFile(destination, 'w') as zip_file:
            # Save 'train_images', 'test_images', 'validation_images' and their corresponding images
            for image in data.get('images', []):
                # Set correct folder names for the image splits
                if image['split'] == 'valid' or image['split'] == 'validation':
                    split_dir = 'validation_images'
                else:
                    split_dir = f"{image['split']}_images"

                image_file_name = image['file_name']
                image_content = image.get('image_content')

                if image_content:
                    image_path = os.path.join(split_dir, image_file_name)
                    zip_file.writestr(image_path, image_content)
                    print(f"Saved image: {image_path}")
                else:
                    print(f"Warning: No image content available for {image_file_name}")

            # Save the COCO files into the 'cocos' folder
            for split in ['train', 'test', 'valid']:
                split_images = [img for img in data['images'] if
                                img['split'] == split or (split == 'valid' and img['split'] == 'validation')]
                split_annotations = [ann for ann in data['annotations'] if
                                     ann['image_id'] in {img['id'] for img in split_images}]

                # If there are no images or annotations for the split, skip it
                if not split_images or not split_annotations:
                    print(f"Warning: No images or annotations found for split '{split}'. Skipping.")
                    continue

                # Create the COCO format dictionary, including additional fields for BinaExperts format
                coco_dict = {
                    "info": data.get("info", {}),
                    "licenses": data.get("licenses", []),
                    "images": [
                        {
                            "id": img['id'],
                            "file_name": img['file_name'],
                            "width": img.get('width', 0),
                            "height": img.get('height', 0),
                        }
                        for img in split_images
                    ],
                    "annotations": [
                        {
                            "id": ann['id'],
                            "image_id": ann['image_id'],
                            "category_id": ann['category_id'],
                            "bbox": ann['bbox'],
                            "segmentation": ann.get('segmentation', []),
                            "area": ann.get('area', 0.0),
                            "iscrowd": ann.get('iscrowd', 0),
                        }
                        for ann in split_annotations
                    ],
                    "categories": data.get("categories", []),
                    # Add additional BinaExperts-specific fields, ensuring they are included even if empty
                    "errors": data.get("errors", []),
                    "labels": data.get("labels", []),
                    "classifications": data.get("classifications", []),
                    "augmentation_settings": data.get("augmentation_settings", {}),
                    # Correct the tile_settings field, using "type" instead of "tile_type"
                    "tile_settings": {
                        "type": data.get("tile_settings", {}).get("type", None),
                        "enabled": data.get("tile_settings", {}).get("enabled", False),
                        "tile_width": data.get("tile_settings", {}).get("tile_width", None),
                        "tile_height": data.get("tile_settings", {}).get("tile_height", None)
                    },
                    "False_positive": data.get("False_positive", {"False_positive": False})
                }

                # Handle naming for validation split as 'val_coco.json'
                if split == 'valid':
                    coco_file_name = f"cocos/val_coco.json"
                else:
                    coco_file_name = f"cocos/{split}_coco.json"

                # Convert the COCO dictionary to JSON and write it to the zip file
                coco_json_content = json.dumps(coco_dict, indent=4)
                zip_file.writestr(coco_file_name, coco_json_content)
                print(f"Saved COCO JSON: {coco_file_name}")

            # Final success message
            print(f"BinaExperts dataset successfully saved to '{destination}'")

        if isinstance(destination, io.BytesIO):
            destination.seek(0)
            return destination
