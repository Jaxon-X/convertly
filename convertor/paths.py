import os


SHARED_ROOT = os.getenv("CONVERTLY_SHARED_ROOT", "/shared")
INPUT_FILES_DIR = os.path.join(SHARED_ROOT, "input_files")
CONVERTED_FILES_DIR = os.path.join(SHARED_ROOT, "converted_files")
