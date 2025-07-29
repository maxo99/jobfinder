import pytest

from jobfinder.domain.models import Job
from jobfinder.utils.loader import load_raw_jobs_df

# @pytest.fixture(scope="session")
# def jobs_data_f():
#     return load_data2(state="processed")


@pytest.fixture(scope="session")
def raw_jobs_df():
    raw = load_raw_jobs_df()
    return raw


@pytest.fixture(scope="session")
def jobs_testdata(raw_jobs_df) -> list[Job]:
    _out = []
    df = raw_jobs_df.copy()
    for doc in df.to_dict(orient="records"):
        try:
            job = Job.from_dict(doc)
            _out.append(job)
        except Exception as e:
            raise e
    return _out
