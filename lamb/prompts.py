from abc import ABC, abstractmethod
from typing import Dict, Union, List
from pydantic import BaseModel, validator

class BaseMessage(BaseModel):
    role: str
    content: str

    def get_content(self) -> str:
        return self.content

class HumanMessage(BaseMessage):
    role: str = "human"

class AIMessage(BaseMessage):
    role: str = "ai"

class SystemMessage(BaseMessage):
    role: str = "system"

class BasePromptTemplate(ABC):
    @abstractmethod
    def format(self, **kwargs) -> Union[str, BaseMessage, List[BaseMessage]]:
        pass

class PromptTemplate(BasePromptTemplate):
    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

class MessagePromptTemplate(BasePromptTemplate):
    def __init__(self, prompt: BaseMessage):
        self.prompt = prompt

    def format(self, **kwargs) -> BaseMessage:
        prompt_dict = self.prompt.dict()
        for key, value in kwargs.items():
            prompt_dict["content"] = prompt_dict["content"].replace(f"{{{key}}}", str(value))
        return type(self.prompt)(**prompt_dict)

class ChatPromptTemplate(BasePromptTemplate):
    def __init__(self, messages: List[BaseMessage]):
        self.messages = messages

    def format(self, **kwargs) -> List[BaseMessage]:
        formatted_messages = []
        for message in self.messages:
            formatted_message = MessagePromptTemplate(message).format(**kwargs)
            formatted_messages.append(formatted_message)
        return formatted_messages

class PromptValue:
    def __init__(self, messages: Union[str, BaseMessage, List[BaseMessage]]):
        self.messages = messages

    @validator("messages")
    def validate_messages(cls, v):
        if isinstance(v, str):
            return [HumanMessage(content=v)]
        elif isinstance(v, BaseMessage):
            return [v]
        elif isinstance(v, list) and all(isinstance(msg, BaseMessage) for msg in v):
            return v
        else:
            raise ValueError("Invalid messages format. Expected str, BaseMessage, or List[BaseMessage].")

    def to_string(self) -> str:
        if isinstance(self.messages, str):
            return self.messages
        elif isinstance(self.messages, BaseMessage):
            return self.messages.get_content()
        else:
            return "\n".join(message.get_content() for message in self.messages)

    def to_messages(self) -> List[BaseMessage]:
        if isinstance(self.messages, str):
            return [HumanMessage(content=self.messages)]
        elif isinstance(self.messages, BaseMessage):
            return [self.messages]
        else:
            return self.messages