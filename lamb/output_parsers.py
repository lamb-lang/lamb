from abc import ABC, abstractmethod
from typing import Union

class BaseOutputParser(ABC):
    @abstractmethod
    def parse(self, output: Union[str, 'BaseMessage']) -> str:
        pass

class StrOutputParser(BaseOutputParser):
    def parse(self, output: Union[str, 'BaseMessage']) -> str:
        if isinstance(output, str):
            return output
        else:
            return output.get_content()