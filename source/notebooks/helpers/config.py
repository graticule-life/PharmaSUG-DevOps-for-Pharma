from pathlib import Path


# Study params
STUDY_START_DATE = "2024-01-01"
STUDY_END_DATE = "2024-12-31"


# Developer params
PY_KERNEL_NAME = "python3"
R_KERNEL_NAME = "ir"


# Path params
# Paths defined like this are more reliable than using ".."

# full path to source director (pharmasug-devops-for-pharma/source)
SOURCE_DIR = Path(__file__).parent.parent.parent.absolute()

# root dir of repo (pharmasug-devops-for-pharma/)
ROOT_DIR = SOURCE_DIR.parent.absolute()

# full path to notebooks; pharmasug-devops-for-pharma/source/notebooks
NOTEBOOK_DIR = SOURCE_DIR / "notebooks"

# paths expected by CI/CD
OUTPUT_NB_PATH = ROOT_DIR / "output" / "notebooks"
OUTPUT_ARTIFACT_PATH = ROOT_DIR / "output"/ "artifacts"
