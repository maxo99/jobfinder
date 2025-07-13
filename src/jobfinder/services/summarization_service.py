from jobfinder.constants import SUMMARIZATION_TEMPLATE
from jobfinder.model import UserType
from jobfinder.session import get_jobs_df, set_jobs_df, update_by_id
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data2
from jobfinder.views.summarization_util import logger


import pandas as pd
from jinja2 import Template


import json


def summarize_jobs(chat_client, selection_df: pd.DataFrame, save_jobs: bool = True) -> bool:
    try:
        logger.info("Summarizing jobs...")
        rendered_prompt = Template(SUMMARIZATION_TEMPLATE).render(
            data={
                "records": selection_df.to_dict("records"),
            }
        )
        _completion = chat_client.completions(rendered_prompt)
        _content = str(_completion.choices[0].message.content)
        if not _content:
            logger.error("No content returned from AI completion. Please check the prompt.")
            return False
        _x = json.loads(_content)
        for x in _x['summaries']:
            # TODO: Bulk this operation
            logger.info(f"ID:{x['id']} summary:{x['summary']}")
            df = update_by_id(get_jobs_df(), x['id'], {
                "summary": x['summary'],
                "summarizer": UserType.AI.value,
                "modified": get_now(),
            })
            set_jobs_df(df)
        if save_jobs:
            save_data2(get_jobs_df())
        return True
    except Exception as e:
        raise e