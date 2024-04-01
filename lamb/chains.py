from typing import List, Union, Dict
from prompts import BasePromptTemplate, PromptValue
from models import BaseLanguageModel
from output_parsers import BaseOutputParser

class BaseChain:
    def __init__(self, steps: List[Union[BasePromptTemplate, BaseLanguageModel, BaseOutputParser]]):
        self.steps = steps

    def __call__(self, inputs: Union[str, Dict[str, str]], return_intermediate_steps: bool = False, **kwargs):
        intermediate_steps = []
        step_output = inputs

        for step in self.steps:
            if isinstance(step, BasePromptTemplate):
                if isinstance(step_output, dict):
                    step_output = step.format(**step_output)
                else:
                    step_output = step.format(text=step_output)
            elif isinstance(step, BaseLanguageModel):
                step_output = step(step_output, **kwargs)
            elif isinstance(step, BaseOutputParser):
                step_output = step.parse(step_output)

            if return_intermediate_steps:
                intermediate_steps.append(step_output)

        if return_intermediate_steps:
            return step_output, intermediate_steps
        else:
            return step_output

class SimpleSequentialChain(BaseChain):
    def __init__(self, prompt: BasePromptTemplate, llm: BaseLanguageModel, output_parser: BaseOutputParser):
        super().__init__(steps=[prompt, llm, output_parser])

class SequentialChain(BaseChain):
    def __init__(self, chains: List[BaseChain], input_keys: List[str], output_keys: List[str]):
        self.chains = chains
        self.input_keys = input_keys
        self.output_keys = output_keys

    def __call__(self, inputs: Dict[str, str], return_intermediate_steps: bool = False, **kwargs):
        step_output = inputs
        intermediate_steps = []

        for i, chain in enumerate(self.chains):
            step_input = {key: step_output[key] for key in self.input_keys[i]}
            step_output = chain(step_input, return_intermediate_steps=return_intermediate_steps, **kwargs)

            if return_intermediate_steps:
                step_output, chain_intermediate_steps = step_output
                intermediate_steps.extend(chain_intermediate_steps)

            step_output = {key: value for key, value in zip(self.output_keys[i], step_output)}

        if return_intermediate_steps:
            return step_output, intermediate_steps
        else:
            return step_output