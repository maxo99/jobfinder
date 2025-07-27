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
        jobs_testdata[0].status = EXCLUDED
        fix_postgresclient.upsert_jobs(jobs_testdata)
        time.sleep(1)
        total_jobs = fix_postgresclient.get_jobs()
        assert len(total_jobs) == len(jobs_testdata), "Total jobs count mismatch."
        non_excluded_jobs = fix_postgresclient.get_jobs(not_status=EXCLUDED)
        assert len(non_excluded_jobs) < len(total_jobs)
        assert all(job.status != EXCLUDED for job in non_excluded_jobs), (
            "Excluded jobs should not be present in the filtered results."
        )
    except Exception as e:
        raise e


def test_get_count(fix_postgresclient, jobs_testdata):
    try:
        jobs_testdata[0].status = EXCLUDED
        fix_postgresclient.upsert_jobs(jobs_testdata)
        time.sleep(1)
        total_count = fix_postgresclient.get_count()
        assert total_count == len(jobs_testdata), "Total count mismatch."
        excluded_count = fix_postgresclient.get_count(status=EXCLUDED)
        assert excluded_count >= 1, "Excluded count should be at least 1."
        non_excluded_count = fix_postgresclient.get_count(not_status=EXCLUDED)
        assert non_excluded_count == len(jobs_testdata) - excluded_count, (
            "Non-excluded count mismatch."
        )
    except Exception as e:
        raise e