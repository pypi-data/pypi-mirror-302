# BuddyAssistant

## Overview
BuddyAssistant is a conversational AI assistant built using Python, utilizing the Ollama framework. The assistant can manage conversations, execute functions, and store chat history. This project is designed to facilitate interactions in a user-friendly way while allowing for extensibility through tools and functions.

## Features
- **Conversational Threads**: Create and manage multiple conversation threads with unique instructions.
- **Function Execution**: Dynamically import and execute functions based on user queries.
- **Storage**: Persist conversations and assistant state using local storage.
- **Custom Instructions**: Define global and thread-specific instructions for personalized interactions.
- **Emoji Support**: Optionally include emojis in responses to enhance user experience.

## Requirements
To run this project, you will need the following Python packages:

- `ollama`

You can install these packages using:

```bash
pip install -r requirements.txt
```

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/my-assistant.git
    cd my-assistant
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Ensure you have the necessary model downloaded: If you're using `ollama`, make sure to pull the required model:

    ```bash
    ollama pull test_model
    ```

    Replace with the actual model (personally i use llama3.2)

## Usage

To create and interact with the assistant, you can use the following example:


```python
from BuddyAssistant import BuddyAssistant

# Initialize the assistant
assistant = BuddyAssistant(
    name="My Assistant",
    model="test_model",
    description="A friendly conversational assistant.",
    global_instruction="Always respond politely."
)

# Create a new thread
thread_id = assistant.create_thread(thread_instruction="Help me with my questions.")

# Chat with the assistant
response = assistant.chat("Hello, how can you assist me?", thread_id)
print(response.content)

```
## Running tests

To ensure the functionality of the assistant, you can run the unit tests included in the project. Use the following command:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## Acknowledgements
- Thank you to the `Ollama` team for providing a powerful framework for building conversational agents.

- Thanks to the open-source community for their valuable resources and libraries.