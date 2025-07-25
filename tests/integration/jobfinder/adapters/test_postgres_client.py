import logging
import time

from jobfinder.domain.constants import EXCLUDED

logger = logging.getLogger(__name__)


def test_connection(fix_postgresclient):
    try:
        result = fix_postgresclient.get_jobs()
        print(f"Connection successful, retrieved {len(result)} jobs.")
    except Exception as e:
        fix_postgresclient.client.info()
        print("PostgreSQL connection failed:", e)
        raise e


def test_add_job(fix_postgresclient, jobs_testdata):
    logger.info("Testing adding a job to Postgres")
    job = jobs_testdata[0]
    test_id = "test_job_id"
    job.id = test_id
    fix_postgresclient.upsert_job(job)
    retrieved_job = fix_postgresclient.get_job_by_id(job.id)
    assert retrieved_job is not None, "Job should be retrievable by ID."
    assert retrieved_job.id == job.id, "Retrieved job ID should match added job ID."


def test_populate_jobs(fix_postgresclient, jobs_testdata):
    fix_postgresclient.upsert_jobs(jobs_testdata)
    time.sleep(2)
    populated_count = len(fix_postgresclient.get_jobs())
    assert populated_count == len(jobs_testdata), (
        "Not all documents were indexed correctly."
    )


def test_get_jobs_with_filters(fix_postgresclient, jobs_testdata):
    try:
        fix_postgresclient.upsert_jobs(jobs_testdata)
        time.sleep(2)
        total_jobs = fix_postgresclient.get_jobs()
        assert len(total_jobs) == len(jobs_testdata), "Total jobs count mismatch."
        jobs_testdata[0].status = EXCLUDED
        # Test with a filter that should return some jobs
        results = fix_postgresclient.get_jobs(location="NYC")
        assert len(results) > 0, "No jobs found with location 'NYC'."

        # Test with a filter that should return no jobs
        results = fix_postgresclient.get_jobs(location="NonExistentLocation")
        assert len(results) == 0, "Jobs found when none were expected."

        # Test with a 'not_' filter
        results = fix_postgresclient.get_jobs(not_status="D")
        assert len(results) > 0, "No jobs found with status not equal to 'D'."
    except Exception as e:
        raise e
