from abc import ABC, abstractmethod
from typing import Union, Dict, List
from pydantic import BaseModel

class BaseOutputParser(ABC):
    @abstractmethod
    def parse(self, output: Union[str, List[str], Dict[str, str]]) -> Union[str, List[str], Dict[str, str]]:
        pass

class NoOpOutputParser(BaseOutputParser):
    def parse(self, output: Union[str, List[str], Dict[str, str]]) -> Union[str, List[str], Dict[str, str]]:
        return output

class StrOutputParser(BaseOutputParser):
    def parse(self, output: Union[str, List[str], Dict[str, str]]) -> str:
        if isinstance(output, str):
            return output
        elif isinstance(output, list):
            return " ".join(output)
        elif isinstance(output, dict):
            return " ".join(value for value in output.values())
        else:
            raise ValueError(f"Unsupported output type: {type(output)}")

class ListOutputParser(BaseOutputParser):
    def parse(self, output: Union[str, List[str], Dict[str, str]]) -> List[str]:
        if isinstance(output, str):
            return [output]
        elif isinstance(output, list):
            return output
        elif isinstance(output, dict):
            return list(output.values())
        else:
            raise ValueError(f"Unsupported output type: {type(output)}")

class DictOutputParser(BaseOutputParser):
    def __init__(self, keys: List[str]):
        self.keys = keys

    def parse(self, output: Union[str, List[str], Dict[str, str]]) -> Dict[str, str]:
        if isinstance(output, str):
            values = output.split()
            return {key: value for key, value in zip(self.keys, values)}
        elif isinstance(output, list):
            return {key: value for key, value in zip(self.keys, output)}
        elif isinstance(output, dict):
            return {key: output[key] for key in self.keys}
        else:
            raise ValueError(f"Unsupported output type: {type(output)}")

class PydanticOutputParser(BaseOutputParser):
    def __init__(self, model: BaseModel):
        self.model = model

    def parse(self, output: Union[str, List[str], Dict[str, str]]) -> BaseModel:
        if isinstance(output, str):
            return self.model.parse_raw(output)
        elif isinstance(output, list):
            return self.model.parse_obj(output)
        elif isinstance(output, dict):
            return self.model(**output)
        else:
            raise ValueError(f"Unsupported output type: {type(output)}")