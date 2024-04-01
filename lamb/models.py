from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any
from prompts import PromptValue, BaseMessage

class BaseLanguageModel(ABC):
    @abstractmethod
    def __call__(self, prompt: Union[str, PromptValue], stop: Optional[List[str]] = None, **kwargs) -> Union[str, BaseMessage, List[BaseMessage]]:
        pass

class BaseLLM(BaseLanguageModel):
    @abstractmethod
    def _generate(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        pass

    def __call__(self, prompt: Union[str, PromptValue], stop: Optional[List[str]] = None, **kwargs) -> str:
        if isinstance(prompt, PromptValue):
            prompt_str = prompt.to_string()
        else:
            prompt_str = prompt

        return self._generate(prompt_str, stop=stop, **kwargs)

class OpenAILLM(BaseLLM):
    def __init__(self, model_name: str, api_key: str, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.client = OpenAIClient(api_key=self.api_key)

    def _generate(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        response = self.client.completions.create(
            engine=self.model_name,
            prompt=prompt,
            max_tokens=kwargs.get("max_tokens", 100),
            n=1,
            stop=stop,
            temperature=kwargs.get("temperature", 0.7),
        )

        return response.choices[0].text.strip()

class BaseChatModel(BaseLanguageModel):
    @abstractmethod
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs) -> BaseMessage:
        pass

    def __call__(self, prompt: Union[PromptValue, List[BaseMessage]], stop: Optional[List[str]] = None, **kwargs) -> List[BaseMessage]:
        if isinstance(prompt, PromptValue):
            messages = prompt.to_messages()
        else:
            messages = prompt

        return self._generate(messages, stop=stop, **kwargs)

class OpenAIChatModel(BaseChatModel):
    def __init__(self, model_name: str, api_key: str, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.client = OpenAIClient(api_key=self.api_key)

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs) -> BaseMessage:
        response = self.client.chat_completions.create(
            model=self.model_name,
            messages=[{"role": message.role, "content": message.content} for message in messages],
            max_tokens=kwargs.get("max_tokens", 100),
            n=1,
            stop=stop,
            temperature=kwargs.get("temperature", 0.7),
        )

        return AIMessage(content=response.choices[0].message.content.strip())