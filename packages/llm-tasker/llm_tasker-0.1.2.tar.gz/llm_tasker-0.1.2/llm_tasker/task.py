from dataclasses import dataclass
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict
from openai import AsyncOpenAI

from llm_tasker.parser import parse_json


@dataclass
class TaskConfig:
    client: AsyncOpenAI | None = None
    model: str | None = None
    max_result_validation_retries: int = 3


class LLMTask(BaseModel):
    config: ClassVar[TaskConfig]
    result: str | None = None
    
    model_config = ConfigDict(
        validate_assignment=True,
    )

    @property
    def status(self) -> Literal["pending", "in_progress", "completed", "error"]:
        pass

    @property
    def info(self) -> str | None:
        pass
    
    def __str__(self) -> str:
        prompt_template = self.__doc__

        if not prompt_template:
            raise ValueError(
                "You need to provide a task prompt template, which, technically, is a class docstring."
            )

        data = {key: str(value) for key, value in self.model_dump().items()}

        return prompt_template.format(**data)

    async def _push(self) -> None:
        pass

    async def __call__(self, model: str | None = None, n_turns: int = 3, log: bool = False) -> None:
        if not self.config.client:
            pass

        model = model or self.config.model

        if not model:
            pass

        messages = [{"role": "system", "content": str(self)}]

        for _ in range(n_turns):
            result = await self.config.client.chat.completions.create(
                messages=messages, model=model, timeout=10_000
            )
            result = result.choices[0].message.content
            if result := parse_json(result):
                try:
                    self.result = result
                except (TypeError, AssertionError, ValueError):
                    continue
                     
            self.result = result
            break
                


