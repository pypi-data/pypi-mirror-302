import io
import os
import zipfile
from io import BytesIO

from typing import Any, Union, IO
from binaexperts.convertors import const
from binaexperts.convertors.base import YOLOConvertor, COCOConvertor, BinaExpertsConvertor


class Convertor:
    """
    A class responsible for converting datasets between different formats (YOLO, COCO, BinaExperts).

    This class facilitates the conversion of datasets by using the appropriate convertor based on the source
    and target format types. It supports loading data from different sources (file paths, in-memory objects),
    normalizing it, and converting it to the target format.

    Methods
    -------
    get_convertor(format_type: str):
        Returns the appropriate convertor class based on the format type.

    convert(source_format: str, target_format: str, source: Union[str, IO[bytes]],
            destination: Union[str, IO[bytes]] = None) -> Union[None, IO[bytes]]:
        Converts a dataset from the source format to the target format and saves it to the destination or returns
        the result as an in-memory object.
    """

    def __init__(self):
        """
        Initialize the Convertor class.

        This constructor doesn't initialize any properties as it serves as a utility class for conversion operations.
        """
        pass

    @staticmethod
    def get_convertor(format_type: str):
        """
        Get the appropriate convertor class based on the provided format type.

        :param format_type: The type of dataset format (e.g., 'yolo', 'coco', 'binaexperts').
        :return: An instance of the corresponding convertor class (YOLOConvertor, COCOConvertor, BinaExpertsConvertor).
        :raises ValueError: If the provided format type is not supported.
        """
        if format_type.lower() == const.CONVERTOR_FORMAT_YOLO:
            return YOLOConvertor()
        elif format_type.lower() == const.CONVERTOR_FORMAT_COCO:
            return COCOConvertor()
        elif format_type.lower() == const.CONVERTOR_FORMAT_BINAEXPERTS:
            return BinaExpertsConvertor()
        else:
            raise ValueError(f"Unsupported format type: {format_type}")

    def convert(
            self,
            source_format: str,
            target_format: str,
            source: Union[str, IO[bytes]],
            destination: Union[str, IO[bytes]] = None
    ) -> Union[None, IO[bytes]]:
        """
        Convert a dataset from the source format to the target format and save the output.

        This method converts a dataset from one format to another (e.g., YOLO to COCO, COCO to BinaExperts).
        It uses the appropriate convertor to load the dataset, normalize it, and convert it to the target format.
        The converted dataset can either be saved to a file (specified in `destination`) or returned as an
        in-memory object if no destination is provided.

        :param source_format: The format of the source dataset (e.g., 'yolo', 'coco', 'binaexperts').
        :param target_format: The format of the target dataset (e.g., 'yolo', 'coco', 'binaexperts').
        :param source: The source dataset, either as a file path or an in-memory object (BytesIO).
        :param destination: (Optional) The destination to save the converted dataset. Can be a directory path,
                            file path, or an in-memory object (BytesIO).
        :return: None if saved to disk, or an in-memory IO object containing the converted dataset.
        :raises ValueError: If the source format or target format is unsupported.

        Example:
            ```python
            converter = Convertor()
            source_file = 'dataset.zip'
            target_file = 'converted_dataset.zip'
            converter.convert('yolo', 'coco', source_file, target_file)
            ```
        """
        # Get the correct convertors based on the formats passed
        source_convertor = self.get_convertor(source_format)
        target_convertor = self.get_convertor(target_format)

        # Handle source as either a path or file-like object
        if isinstance(source, str):
            if zipfile.is_zipfile(source):  # Handle zip file case
                with zipfile.ZipFile(source, 'r') as zip_ref:
                    source_data = source_convertor.load(zip_ref)
            else:
                with open(source, 'rb') as source_file:
                    source_data = source_convertor.load(source_file)
        else:
            source_data = source_convertor.load(source)

        # Convert to the normalized format
        normalized_data = source_convertor.normalize(source_data)

        # If destination is specified, save the output to it
        if destination:
            # Handle destination as directory or file-like object
            if isinstance(destination, str) and os.path.isdir(destination):
                destination_file_path = os.path.join(destination, 'converted_dataset.zip')
                with open(destination_file_path, 'wb') as destination_file:
                    target_data = target_convertor.convert(normalized_data, destination_file)
            else:
                target_data = target_convertor.convert(normalized_data, destination)

            # Save the target format dataset
            target_convertor.save(target_data, destination)
            return None  # No need to return anything when saved to disk

        else:
            # No destination provided, output the result as an in-memory IO object
            in_memory_output = BytesIO()
            target_data = target_convertor.convert(normalized_data, in_memory_output)
            in_memory_output.seek(0)  # Reset pointer to the beginning of the BytesIO object
            # Return the in-memory output for further use
            return in_memory_output
