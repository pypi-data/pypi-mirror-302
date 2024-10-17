import unittest
from unittest.mock import patch, MagicMock
from BuddyAssistant import BuddyAssistant, Thread, Message  # Assuming your classes are in assistant.py

class TestMessage(unittest.TestCase):
    def test_initialization(self):
        msg = Message(role="user", content="Hello!")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello!")
        self.assertIsNotNone(msg.timestamp)

    def test_to_dict(self):
        msg = Message(role="assistant", content="Hi!")
        self.assertEqual(msg.to_dict(), {
            "role": "assistant",
            "content": "Hi!",
            "timestamp": msg.timestamp
        })

    def test_string_representation(self):
        msg = Message(role="user", content="Test message")
        self.assertTrue(isinstance(str(msg), str))


class TestThread(unittest.TestCase):
    def test_initialization(self):
        thread = Thread(instruction="Test instruction")
        self.assertEqual(thread.instruction, "Test instruction")
        self.assertEqual(len(thread.conversation), 0)

    def test_add_message(self):
        thread = Thread()
        message = thread.add_message(role="user", content="Hello")
        self.assertEqual(len(thread.conversation), 1)
        self.assertEqual(thread.conversation[0].content, "Hello")
        self.assertEqual(thread.conversation[0].role, "user")

    def test_get_messages(self):
        thread = Thread()
        thread.add_message(role="user", content="Hello")
        thread.add_message(role="assistant", content="Hi!")
        messages = thread.get_messages(limit=1, sort="asc")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['content'], "Hello")

    def test_to_dict(self):
        thread = Thread(instruction="Test thread")
        thread.add_message(role="user", content="Hello")
        self.assertTrue("instruction" in thread.to_dict())
        self.assertTrue("conversation" in thread.to_dict())


class TestAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = BuddyAssistant(
            name="Test BuddyAssistant",
            model="llama3.2",
            description="A test assistant",
            global_instruction="This is a test assistant",
        )

    def test_initialization(self):
        self.assertEqual(self.assistant.name, "Test BuddyAssistant")
        self.assertEqual(self.assistant.model, "llama3.2")
        self.assertEqual(self.assistant.description, "A test assistant")
        self.assertTrue(isinstance(self.assistant.threads, dict))

    def test_create_thread(self):
        thread_id = self.assistant.create_thread("Test thread instruction")
        self.assertIn(thread_id, self.assistant.threads)
        self.assertEqual(self.assistant.threads[thread_id].instruction, "Test thread instruction")

    @patch('ollama.Client')  # Mocking the external dependency
    def test_chat(self, mock_client):
        mock_response = {'message': {'content': 'Response from assistant'}}
        mock_client.return_value.chat.return_value = mock_response

        thread_id = self.assistant.create_thread("Test thread instruction")
        assistant_message = self.assistant.chat("Hello", thread_id)

        self.assertEqual(len(self.assistant.threads[thread_id].conversation), 3)  # 1 user + 1 assistant +1 system

    # def test_save_to_storage(self):
    #     with patch('storage.local_storage.LocalStorage') as mock_storage:
    #         self.assistant._save_to_storage()
    #         mock_storage.save_assistant.assert_called_once()

    def test_retrieve_assistant(self):
        # Mocking LocalStorage to simulate loading
        mock_storage = MagicMock()
        mock_storage.load_assistant.return_value = {
            "id": "assistant_id",
            "name": "Test BuddyAssistant",
            "model": "llama3.2",
            "description": "A test assistant",
            "global_instruction": "This is a test assistant",
            "emojis": True,
            "tools": [],
            "threads": {}
        }
        assistant = BuddyAssistant.retrive("assistant_id", mock_storage)
        self.assertEqual(assistant.name, "Test BuddyAssistant")


if __name__ == '__main__':
    unittest.main()
