# langchain_huggy

langchain_huggy is a Python package that provides an easy-to-use interface for interacting with HuggingChat models through the LangChain framework. It allows you to leverage powerful language models in your applications with minimal setup.

## Available Models

langchain_huggy comes with several pre-configured models:

1. 'meta-llama/Meta-Llama-3.1-70B-Instruct'
2. 'CohereForAI/c4ai-command-r-plus-08-2024'
3. 'Qwen/Qwen2.5-72B-Instruct' (default)
4. 'meta-llama/Llama-3.2-11B-Vision-Instruct'
5. 'NousResearch/Hermes-3-Llama-3.1-8B'
6. 'mistralai/Mistral-Nemo-Instruct-2407'
7. 'microsoft/Phi-3.5-mini-instruct'

You can choose any of these models when initializing the HuggingChat instance.

## Installation

Install the package using pip:

```bash
pip install langchain_huggy
```

## Quick Start

Here's a simple example to get you started:

```python
from langchain_huggy import HuggingChat
from langchain_core.messages import HumanMessage

# Initialize the HuggingChat model
llm = HuggingChat(
    hf_email="your_huggingface_email@example.com",
    hf_password="your_huggingface_password",
    model="Qwen/Qwen2.5-72B-Instruct"  # Optional: specify a model
)

# Generate a response
response = llm.invoke("hi!")
print(response.content)

# Stream a response
llm.stream("Tell me a short story about a robot.")

# Get web Search results set web_search = True
llm.invoke("latest climate news",web_search = True)
llm.stream("Tell me a short story about a robot.",web_search = True)

```

## Features

- Easy integration with LangChain
- WebSearch Hurray!!!
- Support for multiple HuggingChat models
- Built-in error handling and type checking

## Configuration

You can configure the HuggingChat instance with the following parameters:

- `hf_email`: Your HuggingFace account email
- `hf_password`: Your HuggingFace account password
- `model`: (Optional) Specify a particular model to use from the available models list

## Available Methods

- `invoke`: Generate a complete response for given input
- `generate`: Generate a ChatResult object (compatible with LangChain)
- `stream`: Stream the response as an iterator of message chunks
- `pstream`: Print the streamed response directly to console

## Viewing Available Models

You can view the list of available models at any time using:

```python
print(llm.get_available_models)
```

## Error Handling

The package includes built-in error handling. If you encounter any issues during streaming or generation, informative error messages will be printed to the console.

## Note on Credentials

Make sure to keep your HuggingFace credentials secure. You can set them as environment variables:

```bash
export HUGGINGFACE_EMAIL="your_email@example.com"
export HUGGINGFACE_PASSWD="your_password"
```

Never share your credentials in public repositories or include them directly in your code.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

Happy chatting with langchain_huggy!