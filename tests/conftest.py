import pytest

from jobfinder.utils.loader import load_data2




@pytest.fixture(scope="session")
def jobs_data_f():
    return load_data2(state="processed")
