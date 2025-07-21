import logging
import time

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
