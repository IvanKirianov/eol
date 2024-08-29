# test_public_repo_scanner.py

import unittest
from unittest.mock import patch, Mock
import requests
from public_repo_scanner import get_latest_record, get_latest_release, app

class TestPublicRepoScanner(unittest.TestCase):

    @patch('public_repo_scanner.requests.get')
    def test_get_latest_record(self, mock_get):
        mock_get.return_value.json.return_value = [
            {'date': '2024-08-29', 'version': '1.0.0'},
            {'date': '2024-08-30', 'version': '1.1.0'}
        ]
        data = mock_get.return_value.json()
        result = get_latest_record(data)
        self.assertEqual(result, {'date': '2024-08-30', 'version': '1.1.0'})

    @patch('public_repo_scanner.requests.get')
    def test_get_latest_release(self, mock_get):
        # Test GitHub release URL
        mock_get.return_value.json.return_value = {'tag_name': 'v1.2.3'}
        result = get_latest_release('https://github.com/user/repo/releases/latest')
        self.assertEqual(result, 'v1.2.3')

        # Test generic release URL
        mock_get.return_value.json.return_value = [
            {'created_at': '2024-08-30T00:00:00Z', 'tag_name': 'v1.2.3'},
            {'created_at': '2024-08-29T00:00:00Z', 'tag_name': 'v1.1.0'}
        ]
        result = get_latest_release('https://api.example.com/releases')
        self.assertEqual(result, 'v1.2.3')

    @patch('public_repo_scanner.requests.get')
    def test_get_application_data(self, mock_get):
        mock_get.return_value.json.return_value = {'tag_name': 'v1.2.3'}
        client = app.test_client()
        response = client.get('/api/karpenter')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'version': 'v1.2.3'})

    def test_error_handling(self):
        # Test for handling exceptions in get_latest_release
        with patch('public_repo_scanner.requests.get', side_effect=requests.exceptions.RequestException):
            result = get_latest_release('https://api.example.com/releases')
            self.assertEqual(result, 'Error fetching data')

if __name__ == '__main__':
    unittest.main()
