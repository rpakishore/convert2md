from functools import cached_property

import instructor
from template_python import _config
from template_python.utils.credentials import decode, get_password
from template_python.utils.logger import log
from openai import OpenAI
from openai.types.chat import ChatCompletion


class LLM:
    last_completion = {"prompt": 0, "completion": 0}
    SYSTEM: str = "You are a helpful assistant."

    def __init__(self, **kwargs) -> None:
        try:
            self.__api_base = _config.get(
                keys=("openai", "api_base"), default="http://prx-01-gpt:11434/v1"
            )
            self.__model = _config.get(keys=("openai", "model"), default="llama3")
            self.__openai = OpenAI(
                base_url=self.__api_base,
                api_key=decode(get_password(item="openai", username="key")),
                **kwargs,
            )
            self.__instructor = instructor.from_openai(
                self.__openai, mode=instructor.Mode.JSON
            )
        except Exception as e:
            log.critical(f"Exception in `LLM.__init__({kwargs=})`\n{e}")
            raise e

    def __str__(self) -> str:
        return f"StructuredLLM(api_base={self.__api_base}, model={self.__model})"

    def structured_response(
        self, messages: list[dict[str]], response_model, model: str | None = None
    ):
        """Chat with LLM to get structured response

        Args:
            messages (list[dict[str]]): `system`, `user` and `assistant`(optional) messages to pass to LLM
            response_model (_type_): Pydantic model for validation
            model (str | None, optional): Name of model. Defaults to model defined in config.toml.

        Returns:
            Class Instance: Instance of `response_model`.
        """
        _inputs = {
            "model": model or self.__model,
            "messages": messages,
            "response_model": response_model,
        }
        try:
            return self.__instructor.chat.completions.create(**_inputs)
        except Exception as e:
            log.critical(f"Exception in `LLM.structured_response({_inputs=})`\n{e}")
            raise e

    @cached_property
    def models(self) -> list[str]:
        """Get the list of available models"""
        try:
            return [x.id for x in self.__openai.models.list().data]
        except Exception as e:
            log.critical("Exception in `LLM.models`\n{e}")
            raise e

    def response(
        self, messages: list[dict[str]], model: str | None = None, **kwargs
    ) -> str:
        """Get ChatCompletions text from LLM

        Args:
            messages (list[dict[str]]): Input messages
            model (str | None, optional): Name of Model or `None`. Defaults to None.

        Returns:
            str: Response content
        """
        _inputs = {
            "model": model or self.__model,
            "messages": messages,
            "stream": False,
        }
        for k, v in kwargs.items():
            _inputs[k] = v

        try:
            response = self.__openai.chat.completions.create(**_inputs)

            if _inputs["stream"]:
                res_text = ""
                for chunk in response:
                    if res_text == "":
                        log.debug("Streaming response started.")
                    res_text += chunk.choices[0].delta.content or ""
            else:
                res_text = response.choices[0].message.content
                self.__update_token_usage(response=response)
            log.info("Chat response received")
            log.debug(f"Response: {res_text}")
            return res_text
        except Exception as e:
            log.critical(f"Error encountered in `LLM.response({_inputs=})`")
            log.critical(str(e))
            raise e

    def __update_token_usage(self, response: ChatCompletion):
        self.last_completion = {
            "prompt": response.usage.completion_tokens,
            "completion": response.usage.prompt_tokens,
        }

    def msg(self, user_content: str) -> list[dict[str]]:
        """Generate `messages` based on default `self.SYSTEM` message]"""
        return [
            {"role": "system", "content": self.SYSTEM},
            {"role": "user", "content": user_content},
        ]
