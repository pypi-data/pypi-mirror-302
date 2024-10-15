# DAgent: Command Line Interface for Language Model Operations
## Overview
The LLM Package is a Python-based command-line interface (CLI) that provides an easy way to interact with Large Language Models (LLMs). It allows users to chat with the model, make choices based on given options, and more. This package is designed to be simple, intuitive, and extendable for various LLM operations.
## Features
- Chat with the LLM and receive responses.
- Present options to the LLM and get a choice.
- Choose an option and provide arguments for further processing.
- Few-shot learning capabilities for better context understanding.
- Logging of conversation history for future reference.
## Installation
To install the LLM Package, run the following command:
```bash
pip install dagent
```
Ensure that you have Python 3.6 or later installed on your system.
## Dependencies
- Python 3.6+
- dsqlenv
- langchain_core
- langchain_openai
## Usage
### Chatting with the LLM
To send a message to the LLM and receive a response, use the `chat` command:
```bash
dagent chat --message "Hello, how are you?" --role human
```
The `--role` flag can be set to `human`, `ai`, or `system` depending on the context of the message.
### Making a Choice
To present options to the LLM and get a choice, use the `choose` command:
```bash
dagent choose --options "Option 1" "Option 2" "Option 3" --prompt "Choose an option" --need-reason --multiple
```
The `--need-reason` flag will ask the LLM to provide reasons for the choice, and the `--multiple` flag allows the selection of multiple options.
### Choosing with Arguments
To choose an option and provide arguments, use the `choose_with_args` command:
```bash
dagent choose_with_args --options "Option 1" "Option 2" "Option 3" --prompt "Choose an option and provide arguments" --option-type "type" --need-reason --multiple
```
The `--option-type` flag describes the type of options being chosen.
### Providing Few-Shot Examples
You can provide few-shot examples to guide the LLM using the `examples` argument:
```bash
dagent choose --options ... --prompt ... --examples "Example 1" "Example 2"
```
### Adding Notes
Additional notes can be added to the prompt using the `notes` argument:
```bash
dagent choose --options ... --prompt ... --notes "Note 1" "Note 2"
```
## Demo
Here's a simple demo to demonstrate chatting with the LLM:
```bash
# Chat with the LLM
dagent chat --message "What's the weather like today?" --role human
# Output:
# LLM response: The weather is sunny with a few clouds.
```

## Python API
The LLM Package can also be used as a Python library. Here's an example of how to chat with the LLM using the Python API:
```python
from dagent_llm import LLM
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Initialize the LLM model with a specific engine
model = LLM("deepseek")  # 'deepseek' is the engine being used for LLM

# Simple interaction with the model
r = model.chat("Tell me about yourself")
print(r.content)  # Outputs the response from the model

# Define a list of functions with their names and inputs
functions_info = [
    {"name": "get_data", "input": ["id"], "example_input": "a"},
    {"name": "insert_data", "input": ["id", "data"], "example_input": ["a", "b"]},
    {"name": "update_data", "input": ["id", "data"], "example_input": ["a", "b"]},
    {"name": "delete_data", "input": ["id"], "example_input": "a"},
]

# Example 1: Selecting a function based on user input, including reasons for choice
# Here, the model will be asked to select a function and provide the necessary arguments.
r = model.function_choose(
    functions_info,                      # List of functions to choose from
    "Add a record with key-value pair abc and 123",  # The prompt asking what to do
    need_reason=True,                    # Model must provide a reason for its choice
    multiple=False,                      # Single function selection allowed
    add_to_history=True                  # Add this interaction to the conversation history
)
print(r)  # Outputs the selected function and arguments


# Example 2: Function selection with additional context such as examples and notes
# This provides the model with extra guidance on how to make its decision
r2 = model.function_choose(
    functions_info,
    "Delete record with key abc",        # Instruction for deletion operation
    need_reason=True,                    # Model must provide reasoning
    multiple=False,                      # Only one function can be selected
    add_to_history=True,                 # Record this interaction
    examples=[                           # Example to guide the model
        "Add a record with key-value pair abc and 123 -> insert_data('abc', '123')"
    ],
    notes=[                              # Important notes for the operation
        "Delete operation is irreversible",  
        "This will delete all records with key 'abc'"
    ]
)
print(r2)  # Outputs the selected function and explanation


# Example 3: Simple selection scenario for choosing from a list of food options
# Multiple selections are allowed in this case, and the model needs to justify its choice
foods = ["Snail noodles", "Rice noodles", "Beef noodles", "Egg noodles", "Vegetable salad", "Boiled beef"]
r = model.choose(
    foods,                               # List of options to choose from
    "What can I eat while on a diet?",   # The question or prompt
    "Food name",                         # Type of options being chosen
    need_reason=True,                    # Model must provide reasons for its choices
    multiple=True,                       # Multiple choices allowed (diet-friendly foods)
    add_to_history=True                  # Record the conversation
)
print(r)  # Outputs the selected food(s) and reason(s)

# Review conversation history to see how previous interactions were logged
print(model.history)

# If token information is needed (optional debugging for developers):
# print(model.input_tokens)
```
## Contributing
Contributions to the LLM Package are welcome! Please fork the repository, make your changes, and submit a pull request.
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Contact
For any questions or suggestions, please email Zhao Sheng at zhaosheng@nuaa.edu.cn.
