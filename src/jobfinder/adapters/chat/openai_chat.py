import logging
import os

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from jobfinder.adapters.chat.chat_client import ChatClient, CompletionResponse

logger = logging.getLogger(__name__)


class OpenAIChatClient(ChatClient):
    def __init__(self):
        if os.environ.get("OPENAI_KEY", ""):
            self._client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))
            self.model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        else:
            raise ValueError(
                "OpenAI client is not configured. Set OPENAI_KEY environment variable."
            )
        logger.info(f"OpenAI chat client initialized with model {self.model}")

    def _completions(self, content: str, format=...) -> ChatCompletion:
        try:
            logger.info(f"Perfoming completions call with:{self.model}")
            completion = self._client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_schema", "json_schema": format},
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
            )
            logger.info(f"Returned chat completion {completion.id}")
            return completion
        except Exception as e:
            raise e

    def _to_completion_response(self, response: ChatCompletion) -> CompletionResponse:
        return CompletionResponse(
            id=response.id, content=str(response.choices[0].message.content),
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            total_tokens=response.usage.total_tokens if response.usage else 0,
        )
