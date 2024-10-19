# Utility functions for file operations like reading and writing files, extracting zip files, etc.

import os
import zipfile


def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
