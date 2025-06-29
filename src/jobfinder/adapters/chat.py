from openai import OpenAI, ChatCompletion
import os
import logging

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_KEY")
)

MODEL = "gpt-4o-mini"


def completions(content: str) -> ChatCompletion:
    logger.info(f"Perfoming completions call with:{MODEL}")
    completion = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    logger.info(f"Returned chat completion {completion.id}")
    return completion
