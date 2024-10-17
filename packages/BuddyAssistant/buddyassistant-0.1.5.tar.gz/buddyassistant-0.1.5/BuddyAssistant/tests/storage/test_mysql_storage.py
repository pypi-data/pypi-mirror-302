import json
import unittest
from unittest.mock import MagicMock, patch

from storage.models import AssistantModel, ThreadModel
from storage.mysql_storage import MySQLStorage


class TestMySQLStorage(unittest.TestCase):

    @patch("storage.mysql_storage.create_engine")
    @patch("storage.mysql_storage.sessionmaker")
    def setUp(self, mock_sessionmaker, mock_create_engine):
        # Mock the SQLAlchemy engine and session
        self.mock_engine = mock_create_engine.return_value
        self.mock_sessionmaker = mock_sessionmaker
        self.mock_session = MagicMock()
        self.mock_sessionmaker.return_value = self.mock_session

        # Instantiate the storage with a mock connection string
        self.storage = MySQLStorage(
            connection_string="mysql://user:pass@localhost/testdb"
        )

    def test_save_assistant(self):
        mock_session = self.mock_session.return_value

        # Define assistant data to be saved
        assistant_data = {
            "name": "Test Assistant",
            "model": "GPT-3",
            "description": "Test assistant description",
            "threads": {},
        }
        assistant_id = "assistant_1"

        # Call save_assistant method
        self.storage.save_assistant(assistant_id, assistant_data)

        # Check if merge and commit are called
        mock_session.merge.assert_called_once()
        mock_session.commit.assert_called_once()

        # Check if the saved assistant contains the correct data
        saved_assistant = mock_session.merge.call_args[0][0]
        self.assertEqual(saved_assistant.id, assistant_id)
        self.assertEqual(saved_assistant.name, assistant_data["name"])
        self.assertEqual(saved_assistant.model, assistant_data["model"])
        self.assertEqual(json.loads(saved_assistant.data), assistant_data)

    def test_load_assistant(self):
        mock_session = self.mock_session.return_value

        # Mock the return value of the query
        assistant = AssistantModel(
            id="assistant_1",
            name="Test Assistant",
            model="GPT-3",
            data=json.dumps({"key": "value"}),
        )
        mock_session.query.return_value.filter_by.return_value.first.return_value = (
            assistant
        )

        # Call load_assistant method
        loaded_data = self.storage.load_assistant("assistant_1")

        # Assert that the correct data was loaded
        self.assertEqual(loaded_data, {"key": "value"})
        mock_session.query.assert_called_once_with(AssistantModel)

    def test_save_thread(self):
        mock_session = self.mock_session.return_value

        # Define thread data to be saved
        thread_data = {
            "assistant_id": "assistant_1",
            "messages": [],
        }
        thread_id = "thread_1"

        # Call save_thread method
        self.storage.save_thread(thread_id, thread_data)

        # Check if merge and commit are called
        mock_session.merge.assert_called_once()
        mock_session.commit.assert_called_once()

        # Check if the saved thread contains the correct data
        saved_thread = mock_session.merge.call_args[0][0]
        self.assertEqual(saved_thread.id, thread_id)
        self.assertEqual(saved_thread.assistant_id, thread_data["assistant_id"])
        self.assertEqual(json.loads(saved_thread.data), thread_data)

    def test_load_thread(self):
        mock_session = self.mock_session.return_value

        # Mock the return value of the query
        thread = ThreadModel(
            id="thread_1", assistant_id="assistant_1", data=json.dumps({"key": "value"})
        )
        mock_session.query.return_value.filter_by.return_value.first.return_value = (
            thread
        )

        # Call load_thread method
        loaded_data = self.storage.load_thread("thread_1")
        print(loaded_data)
        # Assert that the correct data was loaded
        self.assertEqual(loaded_data, {"key": "value"})
        mock_session.query.assert_called_once_with(ThreadModel)


if __name__ == "__main__":
    unittest.main()
