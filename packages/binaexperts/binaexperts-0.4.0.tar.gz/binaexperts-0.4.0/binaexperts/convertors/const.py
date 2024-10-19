CONVERTOR_FORMAT_COCO = 'coco'
CONVERTOR_FORMAT_YOLO = 'yolo'
CONVERTOR_FORMAT_BINAEXPERTS = 'binaexperts'
TRAIN_DIR = 'train'
TEST_DIR = 'test'
VALID_DIR = 'valid'
NONE = 'none'
SUPER_CATEGORY = 'supercategory'
COCO_CATEGORIES = 'categories'
COCO_CATEGORIES_ID = 'id'
COCO_CATEGORIES_NAME = 'name'
COCO_IMAGES = 'images'
COCO_IMAGES_ID = 'id'
UTF8_ENCODING= 'utf-8'
COCO_IMAGE_FILENAME = 'file_name'
COCO_IMAGE_WIDTH = 'width'
COCO_IMAGE_HEIGHT = 'height'
COCO_ANNOTATIONS = 'annotations'
NORMALIZE_BBOX_FORMAT = 'xywh'
COCO_BBOX_FORMAT = 'xywh'
YOLO_BBOX_FORMAT = 'cxcywh'
NORMALIZED_DATA_DESCRIPTION =  'description'
NORMALIZED_DATA_NAME = 'name'
NORMALIZED_DATA_ID = 'id'
YOLO_YAML_FILENAME = 'data.yaml'
YOLO_YAML_NAME = 'names'
YOLO_IMAGES_SUBDIR = 'images'
YOLO_LABELS_SUBDIR = 'labels'
YOLO_IMAGE_DIR_PATH_TEMPLATE = "{}/images"
YOLO_LABEL_DIR_PATH_TEMPLATE = "{}/labels"

YOLO_IMAGE_FOLDER = "images"
SPLIT_DIR_FORMAT = "{}/" + YOLO_IMAGE_FOLDER + "/"
YOLO_LABEL_FOLDER = "labels"
LABELS_DIR_FORMAT = "{}/" + YOLO_LABEL_FOLDER + "/"

ANNOTATION_JSON_PATH_TEMPLATE = "{}/_annotations.coco.json"



# File Paths and Extensions
COCO_ANNOTATION_FILE_NAME = "_annotations.coco.json"

COCO_ANNOTATION_FILE_PATH = "{}/" + COCO_ANNOTATION_FILE_NAME  # format string for creating paths

# Warning Messages
ANNOTATION_FILE_NOT_FOUND_WARNING = "Warning: Annotation file not found in {}. Skipping this subdir."
SUBDIR_FOLDER_NOT_FOUND_WARNING = "Warning: Subdir folder not found in {}. Skipping this subdir."
IMAGE_NOT_FOUND_WARNING = "Warning: Image file {} not found in zip archive."
INVALID_SOURCE_ERROR = "Source must be either a directory path or a file-like object."
UNKNOWN_CATEGORY_ERROR = "Annotation with unknown category_id: {}"
WARNING_NO_IMAGES_FOUND = "Warning: No images found for split '{}'. Skipping."
WARNING_MISSING_DIR = "Warning: Directory {} is missing images or labels folder. Skipping this subdir."
WARNING_MISSING_IMAGE_CONTENT = "Warning: Missing image content for {}. Skipping."
WARNING_UNABLE_TO_DETERMINE_DIMENSIONS = "Warning: Unable to determine dimensions for {}. Skipping."
WARNING_NO_IMAGE_CONTENT = "Warning: No image content found for {}"