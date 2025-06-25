import os
from datetime import datetime
from pathlib import Path


def get_now(underscore: bool = False) -> str:
    if underscore:
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent

def get_data_dir() -> Path:
    # return os.path.join(get_project_root().joinpath(),"data")
    _data_path =  get_project_root().joinpath("data")
    if not os.path.exists(_data_path):
        os.mkdir(_data_path)
    return _data_path