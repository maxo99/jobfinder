import logging

from jobfinder.utils.loader import load_raw_jobs

logger = logging.getLogger(__name__)


# def test_data_serialization():
#     try:
#         _input_data = load_data2(state="processed").copy()
#         _found_jobs = found_jobs_from_df(_input_data)
#         converted_df = pd.DataFrame([job.model_dump() for job in _found_jobs.values()])
#         assert not converted_df.empty
#         _input_data = pd.concat([_input_data, converted_df], ignore_index=True)

#     except Exception as e:
#         raise e
#     logger.info("PASSED")


# def test_data_serialization2():
#     try:
#         _input_data = load_data2(state="processed").copy()
#         _starting_count = len(_input_data)
#         for doc in _input_data.to_dict(orient="records"):
#             job = Job.from_dict(doc)
#             assert job is not None, "Job conversion failed"
#             print(f"Converted job: {job.id} - {job.name}")
#             _starting_count -= 1
#         assert _starting_count == 0, "Not all jobs were converted successfully"
#     except Exception as e:
#         raise e
#     logger.info("PASSED")


def test_raw_jobs_conversion(raw_jobs_df):
    try:
        assert not raw_jobs_df.empty, "Raw data should not be empty"
        _raw_jobs = load_raw_jobs()
        assert _raw_jobs, "Raw jobs should not be empty"
        assert len(_raw_jobs) == len(raw_jobs_df), "raw jobs != raw data"
    except Exception as e:
        raise e
    logger.info("PASSED")


# def test_jobs_to_df(raw_jobs_df):
