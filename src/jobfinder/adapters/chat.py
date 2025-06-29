from openai import OpenAI, ChatCompletion
import os
import logging

logger = logging.getLogger(__name__)



enabled = False
if os.environ.get("OPENAI_KEY",""):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_KEY")
    )
    enabled = True


MODEL = os.environ.get("OPENAI_MODEL","gpt-4o-mini")


def completions(content: str) -> ChatCompletion:
    if not enabled:
        raise Exception("Chat has not been configured")
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
