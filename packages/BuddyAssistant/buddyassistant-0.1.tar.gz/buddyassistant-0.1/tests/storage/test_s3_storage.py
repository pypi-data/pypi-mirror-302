import unittest
from unittest.mock import patch, MagicMock
from storage.s3_storage import S3Storage
import json

class TestS3Storage(unittest.TestCase):

    @patch('storage.s3_storage.boto3.client')
    def setUp(self, mock_boto_client):
        # Mock the S3 client
        self.mock_s3_client = mock_boto_client.return_value
        self.storage = S3Storage(bucket_name="test-bucket")
    
    def test_save_assistant(self):
        assistant_data = {
            "name": "Test Assistant",
            "model": "GPT-3",
            "description": "Test assistant description",
            "threads": {},
        }
        assistant_id = "assistant_1"

        # Call save_assistant
        self.storage.save_assistant(assistant_id, assistant_data)

        # Ensure put_object was called with correct parameters
        self.mock_s3_client.put_object.assert_called_once_with(
            Bucket="test-bucket",
            Key=f"assistants/{assistant_id}.json",
            Body=json.dumps(assistant_data)
        )

    def test_load_assistant(self):
        assistant_id = "assistant_1"
        assistant_data = json.dumps({"name": "Test Assistant", "model": "GPT-3"})

        # Mock S3 response
        self.mock_s3_client.get_object.return_value = {'Body': MagicMock(read=lambda: assistant_data)}

        # Call load_assistant
        loaded_data = self.storage.load_assistant(assistant_id)

        # Check if the correct data was loaded
        self.assertEqual(loaded_data, json.loads(assistant_data))
        self.mock_s3_client.get_object.assert_called_once_with(
            Bucket="test-bucket",
            Key=f"assistants/{assistant_id}.json"
        )

if __name__ == '__main__':
    unittest.main()
