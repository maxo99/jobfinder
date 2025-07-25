import logging

from jinja2 import Template

from jobfinder.domain.constants import PRESET_TEMPLATES
from jobfinder.domain.models import ScoringResponse, jobs_to_df
from jobfinder.utils.service_helpers import render_jinja

logger = logging.getLogger(__name__)


def test_scoring(jobs_testdata, fix_generativeservice):
    try:
        test_jobs = jobs_testdata.copy()[0:2]
        test_job = test_jobs.pop(0)

        _prompt = next(iter(PRESET_TEMPLATES.values()), "")
        rendered_prompt = render_jinja(
            template_str=_prompt,
            data={
                "records": test_jobs,
                "listing": test_job,
            },
        )

        # Navigate to the scoring tab
        # at.button(key="scoring_util").click().run()
        output = fix_generativeservice._chat_client.completions(
            content=rendered_prompt,
            format=ScoringResponse.model_json_schema(),
        )
        assert "score" in output.content, "Score not found in response."
        assert "pros" in output.content, "Pros not found in response."
        assert "cons" in output.content, "Cons not found in response."

    except Exception as e:
        print(f"Error occurred in scoring util test: {e}")
        raise e


def test_extract_qualifications(jobs_testdata, fix_generativeservice):
    try:
        count = 5
        test_jobs = jobs_testdata.copy()[0:count]
        for j in test_jobs:
            j.id = f"job_{j.id}"
        logger.info(f"Testing extraction of qualifications from {count} jobs.")
        fix_generativeservice.extract_qualifications(test_jobs)
        assert len(test_jobs[0].qualifications) > 0
        logger.info(f"Output:\n{test_jobs[0].qualifications}")
        jobs_to_df(test_jobs).head(count).to_csv("test_qualifications.csv", index=False)
        logger.info("Qualifications extracted successfully.")

    except Exception as e:
        raise e
    logger.info("PASSED")


def test_template_population(jobs_testdata):
    jobs = jobs_testdata[:2]
    template = """
    ## Job Listings:
    {% for record in records %}
    ### Job Listing
        #### jobID: {{ record.id }}
        #### Description: {{ record.description }}
    {% endfor %}
    """
    try:
        rendered_template = Template(template).render(
            records=[job.model_dump() for job in jobs]
        )
        assert jobs[0].id in rendered_template, "Template rendering failed."
        logger.info(f"Rendered Template:\n{rendered_template}")
    except Exception as e:
        raise e
