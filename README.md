# LaMb: Language Model Building Framework

LaMb is a Python framework designed to simplify the process of building and working with large language models (LLMs) and generative AI applications. It provides a high-level, expressive API for defining and composing language model pipelines, making it easier to experiment with and deploy LLM-based solutions.

## Features

- **Flexible Prompt Templates**: Define prompt templates using a simple and intuitive syntax, allowing for dynamic substitution of variables and generation of structured prompts.

- **Language Model Abstraction**: Work with different types of language models, including LLMs and chat models, through a unified interface. Easily integrate with popular LLM providers such as OpenAI.

- **Output Parsing**: Parse and format the output from language models using built-in output parsers, including string, list, dictionary, and Pydantic model parsers.

- **Chaining and Composition**: Build complex language model pipelines by chaining together prompt templates, language models, and output parsers. Create sequential and parallel chains to orchestrate multiple components.

- **Extensibility**: Extend LaMb with custom prompt templates, language models, output parsers, and chains to suit your specific requirements. Leverage the modular architecture to integrate with external libraries and frameworks.

- **Integration with LangChain and OLLaMA**: Seamlessly integrate LaMb with the LangChain and OLLaMA frameworks, enabling interoperability and leveraging their capabilities alongside LaMb.

## Installation

To install LaMb, use the following command:

```
pip install lamb
```

## Getting Started

Here's a simple example that demonstrates how to use LaMb to generate text using a prompt template and a language model:

```python
from lamb.prompts import PromptTemplate
from lamb.models import OpenAILLM
from lamb.chains import SimpleSequentialChain

prompt = PromptTemplate(template="What is the capital of {country}?")
llm = OpenAILLM(model_name="text-davinci-002", api_key="your_api_key")

chain = SimpleSequentialChain(prompt=prompt, llm=llm)

output = chain({"country": "France"})
print(output)
```

For more examples and detailed usage instructions, please refer to the documentation.

## Contributing

Contributions to LaMb are welcome! If you encounter any issues, have suggestions for improvements, or want to contribute new features, please open an issue or submit a pull request on the GitHub repository.

Before contributing, please review the contribution guidelines.

## License

LaMb is open-source software licensed under the MIT License.

## Acknowledgements

LaMb builds upon the ideas and concepts from various open-source projects, including:

- **LangChain**
- **OLLaMA**

We would like to express our gratitude to the developers and communities behind these projects for their valuable contributions to the field of language models and generative AI.

## Contact

For any questions, suggestions, or feedback, please contact the LaMb team at lamb@example.com.
