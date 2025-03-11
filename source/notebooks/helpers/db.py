from sqlalchemy import create_engine
from notebooks.helpers.config import ROOT_DIR


def get_engine():
    return create_engine(f"sqlite:///{str(ROOT_DIR)}/sample.sqlite")
