import unittest
from unittest.mock import mock_open, patch
from storage.local_storage import LocalStorage
import json
import os

class TestLocalStorage(unittest.TestCase):

    def setUp(self):
        """Set up the test directory and LocalStorage instance."""
        self.test_directory = "test_directory"
        self.storage = LocalStorage(directory=self.test_directory)

    def tearDown(self):
        """Clean up the test directory after each test."""
        if os.path.exists(self.test_directory):
            for filename in os.listdir(self.test_directory):
                file_path = os.path.join(self.test_directory, filename)
                os.remove(file_path)
            os.rmdir(self.test_directory)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_assistant(self, mock_file):
        assistant_data = {
            "name": "Test Assistant",
            "model": "GPT-3",
            "description": "Test assistant description",
            "threads": {},
        }
        assistant_id = "assistant_1"

        # Call save_assistant
        self.storage.save_assistant(assistant_id, assistant_data)

        # Check that the correct file was written to
        expected_json = json.dumps(assistant_data, indent=4)
        
        # Collect all calls to write
        write_calls = mock_file().write.call_args_list
        # Join all the write calls into a single string
        written_data = ''.join(call[0][0] for call in write_calls)

        # Assert that the entire written data matches the expected JSON
        self.assertEqual(written_data.strip(), expected_json)

    @patch('builtins.open', new_callable=mock_open, read_data='{"name": "Test Assistant", "model": "GPT-3"}')
    @patch('os.path.exists', return_value=True)
    def test_load_assistant(self, mock_exists, mock_file):
        assistant_id = "assistant_1"

        # Call load_assistant
        loaded_data = self.storage.load_assistant(assistant_id)

        # Assert that the correct data was loaded
        self.assertEqual(loaded_data, {"name": "Test Assistant", "model": "GPT-3"})
        mock_file.assert_called_once_with(os.path.join(self.test_directory, f"{assistant_id}.json"), 'r')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_thread(self, mock_file):
        thread_data = {
            "messages": [],
            "metadata": {
                "created": "2024-10-16",
            }
        }
        thread_id = "thread_1"

        # Call save_thread
        self.storage.save_thread(thread_id, thread_data)

        # Check that the correct file was written to
        expected_json = json.dumps(thread_data, indent=4)
        
        # Collect all calls to write
        write_calls = mock_file().write.call_args_list
        # Join all the write calls into a single string
        written_data = ''.join(call[0][0] for call in write_calls)

        # Assert that the entire written data matches the expected JSON
        self.assertEqual(written_data.strip(), expected_json)

    @patch('builtins.open', new_callable=mock_open, read_data='{"messages": [], "metadata": {"created": "2024-10-16"}}')
    @patch('os.path.exists', return_value=True)
    def test_load_thread(self, mock_exists, mock_file):
        thread_id = "thread_1"

        # Call load_thread
        loaded_data = self.storage.load_thread(thread_id)

        # Assert that the correct data was loaded
        self.assertEqual(loaded_data, {"messages": [], "metadata": {"created": "2024-10-16"}})
        mock_file.assert_called_once_with(os.path.join(self.test_directory, f"{thread_id}.json"), 'r')

if __name__ == '__main__':
    unittest.main()
