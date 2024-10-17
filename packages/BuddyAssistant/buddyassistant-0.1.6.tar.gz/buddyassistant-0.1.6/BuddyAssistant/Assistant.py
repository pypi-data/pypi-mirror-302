import importlib
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import ollama
from loguru import logger

from storage.local_storage import LocalStorage
from storage.base_storage import BaseStorage

DEFAULT_DIRECTORY = "./assistants"


class Message:
    def __init__(self, role: str, content: str, timestamp: Optional[int] = None):
        """
        Represents a single message in a conversation thread.

        Args:
        - role (str): The role of the message (e.g., 'user', 'assistant', 'system').
        - content (str): The content of the message.
        - timestamp (int, optional): Unix timestamp of the message. Defaults to current time in UTC.
        """
        self.id = f"msg_{str(uuid.uuid4())}"
        self.role = role
        self.content = content
        self.timestamp = timestamp or int(datetime.now(timezone.utc).timestamp())

    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary."""
        return {"role": self.role, "content": self.content, "timestamp": self.timestamp}

    def __str__(self) -> str:
        """Return the message in JSON string format."""
        return json.dumps(self.to_dict())


class Thread:
    def __init__(
        self, instruction: Optional[str] = None, conversation: List[Dict[str, Any]] = []
    ):
        """
        Represents a conversation thread with a unique ID.

        Args:
        - instruction (str, optional): Thread-specific instruction.
        - conversation (list, optional): Initial list of messages in dictionary form.
        """
        self.thread_id = f"thread_{str(uuid.uuid4())}"  # Generate unique thread ID
        self.instruction = instruction
        self.conversation = [Message(**msg) for msg in conversation]

    def add_message(self, role: str, content: str) -> Message:
        """Add a message to the conversation."""
        message = Message(role, content)
        self.conversation.append(message)
        return message

    def get_messages(
        self, limit: Optional[int] = None, sort: str = "asc"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation messages with optional limit and sorting.

        Args:
        - limit (int, optional): Limit the number of messages to retrieve.
        - sort (str): Sort order ('asc' for ascending, 'desc' for descending).

        Returns:
        - list: List of message dictionaries sorted and limited.
        """
        messages = self.conversation if sort == "asc" else self.conversation[::-1]
        if limit:
            messages = messages[:limit]
        return [msg.to_dict() for msg in messages]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the thread to a dictionary."""
        return {
            "instruction": self.instruction,
            "conversation": [msg.to_dict() for msg in self.conversation],
        }

    def __str__(self) -> str:
        """Return the thread in JSON string format."""
        return json.dumps(self.to_dict())


class BuddyAssistant:
    def __init__(
        self,
        name: str,
        model: str,
        description: str,
        global_instruction: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        emojis_on: bool = True,
        verbose: bool = False,
        storage: BaseStorage = LocalStorage(DEFAULT_DIRECTORY),
        id: Optional[str] = None,
        threads: Dict[str, Thread] = None
    ):
        """
        Initialize a new assistant with basic details.
        Generates a unique ID for the assistant.
        Automatically creates the directory if it doesn't exist.

        Args:
        - name (str): Name of the assistant.
        - model (str): The model name.
        - description (str): Description of the assistant's purpose.
        - global_instruction (str): Instruction guiding the assistant's behavior.
        - tools (list, optional): List of function-calling tools.
        - directory (str): Directory for saving the assistant's data.
        - emojis_on (bool): Whether to include emojis in responses.
        - verbose (bool): Enable or disable logging.
        - id (str, optional): Pre-defined ID for the assistant.
        """
        self.storage = storage
        self.name = name
        self.model = model
        self.description = description
        self.global_instruction = global_instruction
        self.emojis_on = emojis_on
        self.tools = tools or []
        self.id = id or f"assistant_{str(uuid.uuid4())}"
        self.threads: Dict[str, Thread] = threads or {}
        self.model_client = ollama.Client()

        # Set logging based on verbosity
        if not verbose:
            logger.disable(__name__)
        else:
            logger.enable(__name__)

        self._save_to_storage()

    def create_thread(
        self, thread_instruction: Optional[str] = None, verbose: bool = False
    ) -> str:
        """Create a new conversation thread with an optional instruction."""
        thread = Thread(instruction=thread_instruction)
        self.threads[thread.thread_id] = thread

        if verbose:
            logger.info(
                f"Thread '{thread.thread_id}' created with instruction: {thread_instruction}."
            )

        self._save_to_storage()
        return thread.thread_id

    def chat(
        self, prompt: str, thread_id: Optional[str] = None, verbose: bool = False
    ) -> Message:
        """
        Interact with the assistant using the model and store the conversation.

        Args:
        - prompt (str): User input prompt.
        - thread_id (str, optional): ID of the thread.
        - verbose (bool): Enable or disable logging.

        Returns:
        - Message: The assistant's response message.
        """
        if not verbose:
            logger.disable(__name__)
        else:
            logger.enable(__name__)

        instruction = (
            self.global_instruction + f" Current datetime is {datetime.now()}."
        )
        if self.emojis_on:
            instruction += " Responses should include emojis."

        thread = self.threads.get(thread_id)
        if thread and thread.instruction:
            instruction += " " + thread.instruction

        if thread_id and thread and not thread.conversation:
            messages = [
                {
                    "role": "system",
                    "content": f"You are a cool assistant named {self.name}. Your instruction: {instruction}.",
                }
            ]
            for message in messages:
                thread.add_message(message["role"], message["content"])

        if thread_id:
            user_message = thread.add_message("user", prompt)

        assistant_response = self._run(prompt=prompt, thread=thread, verbose=verbose)

        if thread_id:
            assistant_message = thread.add_message(
                "assistant", assistant_response["message"]["content"]
            )
            self._save_to_storage()

        logger.info(f"BuddyAssistant response: {assistant_response}")
        return assistant_message

    def _execute_function(self, module_name: str, func_name: str, **kwargs: Any) -> Any:
        """
        Dynamically import and execute a function from a module.
        """
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            if func:
                return func(**kwargs)
            else:
                raise ValueError(
                    f"No function named '{func_name}' found in module '{module_name}'"
                )
        except ImportError as e:
            raise ValueError(f"Module '{module_name}' could not be found. Error: {e}")

    def _check_keywords(self, string1: str, string2: str) -> bool:
        """Check if two strings share common words, returning True if they do."""
        words1 = set(string1.split("_"))
        words2 = set(string2.split())
        return bool(words1.intersection(words2))

    def _run(
        self, prompt: str, thread: Thread, verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run the main model chat with function calls and handle tool execution.

        Args:
        - prompt (str): The user's query.
        - thread (Thread): The conversation thread.
        - verbose (bool): Enable or disable logging.

        Returns:
        - dict: The model's response.
        """
        if not verbose:
            logger.disable(__name__)
        else:
            logger.enable(__name__)

        logger.debug("Sending the following messages to the model:")
        for msg in thread.conversation:
            logger.debug(msg)

        messages = [{"role": i.role, "content": i.content} for i in thread.conversation]

        response = self.model_client.chat(
            model=self.model, messages=messages, tools=self.tools
        )

        logger.debug(f"Model response received: {response}")

        if not response["message"].get(
            "tool_calls"
        ) or not self._check_prompt_related_to_tools(prompt=prompt):
            logger.debug(
                f"The model didn't use any function. Its response: {response['message']['content']}"
            )
        else:
            for tool in response["message"]["tool_calls"]:
                function_name = tool["function"]["name"]
                tool_config = next((t for t in self.tools if t['function']['name'] == function_name), None)
                module_name = tool_config['function']['module']
                function_args = tool["function"]["arguments"]
                logger.debug(
                    f"Function to call: {function_name} with arguments: {function_args}"
                )

                function_response = self._execute_function(
                    func_name=function_name, module_name=module_name, **function_args
                )
                messages.append({"role": "tool", "content": function_response})

        final_response = self.model_client.chat(model=self.model, messages=messages)
        logger.debug(f"Final response from the model: {final_response}")

        return final_response

    def _check_prompt_related_to_tools(self, prompt):
        # Normalize string2 for matching
        normalized_string2 = prompt.lower()

        for tool in self.tools:
            # Extract relevant keywords from each tool dictionary
            keywords = [
                tool["function"]["name"],
                tool["function"]["description"],
            ]

            # Extract parameter descriptions
            parameters = tool["function"]["parameters"]["properties"]
            for param in parameters.values():
                keywords.append(param["description"])

            # Normalize keywords by splitting into words and lowering the case
            keywords = set(
                word.lower() for keyword in keywords for word in keyword.split()
            )

            # Split string2 into words
            words_in_string2 = set(normalized_string2.split())

            # Check for intersection between keywords and words in string2
            related_keywords = keywords.intersection(words_in_string2)
            # If we find any related keywords, return True
            if related_keywords:
                return True

        # If no related keywords are found for any tool, return False
        return False

    def _save_to_storage(self) -> None:
        """Save the assistant's threads and details using the storage backend."""
        data = {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "description": self.description,
            "global_instruction": self.global_instruction,
            "tools": [tool for tool in self.tools],  # Adjust if needed
            "emojis": self.emojis_on,
            "threads": {k: v.to_dict() for k, v in self.threads.items()},
        }
        self.storage.save_assistant(self.id, data)
        logger.debug(f"BuddyAssistant data saved using storage backend")

    @staticmethod
    def retrive(assistant_id: str, storage: BaseStorage = LocalStorage(directory=DEFAULT_DIRECTORY)):
        """Load an assistant using the storage backend."""
        data = storage.load_assistant(assistant_id)
        if data:
            assistant = BuddyAssistant(
                id=assistant_id,
                name=data["name"],
                model=data["model"],
                tools=data['tools'],
                description=data["description"],
                global_instruction=data["global_instruction"],
                storage=storage,  # Pass the same storage backend
                emojis_on=data["emojis"],
                threads={
                tid: Thread(**td) for tid, td in data.get("threads", {}).items()
            }
            )

            return assistant
        else:
            logger.error(f"No assistant found with ID: {assistant_id}.")
            return None
