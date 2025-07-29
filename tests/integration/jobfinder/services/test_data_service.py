import logging
import time

from jobfinder.domain.models import Qualification

logger = logging.getLogger(__name__)


FAKE_SKILLS = [
    "Python",
    "SQL",
    "JavaScript",
    "Java",
    "C++",
    "Ruby",
    "Go",
    "Swift",
    "PHP",
    "HTML/CSS",
]
REQUIREMENTS = ["required", "preferred", "optional"]
EXPERIENCE_LEVELS = ["1 year", "2+ years", "5 years", "10+ years"]


def _build_fake_qualifications(job_id, count=2):
    qualifications = []
    for i in range(count):
        qualifications.append(
            Qualification(
                id=f"{job_id}_qual{i + 1}",
                skill=FAKE_SKILLS[i % len(FAKE_SKILLS)],
                requirement=REQUIREMENTS[i % len(REQUIREMENTS)],
                experience=EXPERIENCE_LEVELS[i % len(EXPERIENCE_LEVELS)],
            )
        )
    return qualifications


def test_populate_index(fix_dataservice, jobs_testdata):
    startup_count = len(fix_dataservice.get_jobs())
    logger.info("Starting count of jobs in index: %d", startup_count)
    fix_dataservice.store_jobs(jobs_testdata)
    time.sleep(2)

    populated_count = len(fix_dataservice.get_jobs())
    logger.info("Populated count of jobs in index: %d", populated_count)
    assert populated_count >= len(jobs_testdata)


# @pytest.mark.usefixtures("fix_populated_index")
def test_qualifications_search(fix_dataservice, fix_generativeservice, jobs_testdata):
    try:
        test_jobs = jobs_testdata.copy()[0:2]
        # fix_generativeservice.extract_qualifications(test_jobs)
        jobs_1 = [test_jobs[0]]
        jobs_1[0].id = "job123"

        quals = _build_fake_qualifications(jobs_1[0].id, count=3)
        jobs_1[0].qualifications = quals
        fix_dataservice.embed_populated_jobs(jobs_1)
        fix_dataservice.store_jobs(jobs_1)

        jobs_2 = [test_jobs[1]]
        jobs_2[0].id = "job456"
        jobs_2[0].qualifications = _build_fake_qualifications(jobs_2[0].id, count=2)

        results = fix_dataservice.search_by_qualifications(jobs_2[0])
        assert len(results.jobs) > 0, "No similar jobs found."
    except Exception as e:
        raise e


# @pytest.mark.usefixtures("fix_populated_index")
def test_title_search(fix_dataservice, fix_generativeservice, jobs_testdata):
    try:
        test_jobs = jobs_testdata.copy()[0:2]
        jobs_1 = [test_jobs[0]]
        jobs_1[0].id = "job123"
        fix_dataservice.embed_populated_jobs(jobs_1)
        fix_dataservice.store_jobs(jobs_1)

        jobs_2 = [test_jobs[1]]
        jobs_2[0].id = "job456"

        results = fix_dataservice.search_by_title(jobs_2[0])
        assert len(results.jobs) > 0, "No similar jobs found."
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
