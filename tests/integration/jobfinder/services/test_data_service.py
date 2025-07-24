import logging
import time

from jobfinder.domain.models import Qualification

logger = logging.getLogger(__name__)


def test_populate_index(fix_dataservice, jobs_testdata):
    startup_count = len(fix_dataservice.get_jobs())
    logger.info("Starting count of jobs in index: %d", startup_count)
    fix_dataservice.store_jobs(jobs_testdata)
    time.sleep(2)

    populated_count = len(fix_dataservice.get_jobs())
    logger.info("Populated count of jobs in index: %d", populated_count)
    assert populated_count >= len(jobs_testdata)


def test_embed_populated_job(fix_dataservice, jobs_testdata):
    try:
        test_id = "test_job_id"
        jobs_testdata = jobs_testdata.copy()[0:1]
        jobs_testdata[0].id = test_id
        jobs_testdata[0].qualifications = [
            Qualification(
                id=test_id, skill="Python", requirement="required", experience="5 years"
            )
        ]

        fix_dataservice.store_jobs(jobs_testdata)
        time.sleep(1)
        fix_dataservice.embed_populated_jobs(jobs_testdata)
        time.sleep(1)
        fix_dataservice.store_jobs(jobs_testdata)

        results = fix_dataservice.search_similar_jobs(jobs_testdata[0].title[0:5])
        assert len(results) > 0, "No similar jobs found after embedding."
        assert results[0].id == jobs_testdata[0].id, (
            "The first job in the search results should match the stored job."
        )
        print("finished")
    except Exception as e:
        raise e


# def test_updating_summary(
#     fix_dataservice,
#     jobs_testdata
# ):
#     _test_id = "FAKE_JOB_ID"
#     _test_qualifications = [
#         {"skill": "Python", "requirement": "required", "experience": "5 years"},
#         {"skill": "SQL", "requirement": "preferred", "experience": "2+ years"},
#     ]

#     test_data = jobs_testdata.copy()[0:1]
#     test_data[0].id = _test_id
#     fix_dataservice.store_jobs(test_data)
#     time.sleep(0.5)
#     returned_job = fix_dataservice.get_by_id(_test_id)
#     assert returned_job is not None
#     assert returned_job.id == _test_id
#     assert returned_job.qualifications == []
#     test_data = test_data.copy()
#     test_data[0].qualifications = [Qualifications(**q) for q in _test_qualifications]
#     fix_dataservice.store_jobs(test_data)
#     time.sleep(0.5)
#     updated_job = fix_dataservice.get_by_id(_test_id)
#     assert updated_job is not None
#     assert updated_job.id == _test_id
#     assert updated_job.qualifications == _test_qualifications

# def test_populate_with_vectors(
#     fix_dataservice,
#     raw_jobs_df
# ):
#     _raw_jobs = load_raw_jobs()

#     _input_data = load_data2(state="processed").copy()
#     _starting_count = len(_input_data)
#     for doc in _input_data.to_dict(orient="records"):
#         job = Job.from_dict(doc)
#     time.sleep(2)
#     response = fix_elasticsearchclient.client.count(index=test_index)
#     print(f"Indexed {response['count']} documents with vectors in index '{test_index}'.")
#     assert response["count"] == len(test_data), (
#         "Not all documents with vectors were indexed correctly."
#     )
