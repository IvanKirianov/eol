import unittest
from unittest.mock import patch
from public_repo_scanner import get_latest_record, get_latest_release, app
import requests

class TestPublicRepoScanner(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_latest_record(self):
        data = [
            {"date": "2023-01-01", "version": "v1.0"},
            {"date": "2023-02-01", "version": "v1.1"},
            {"date": "2023-03-01", "version": "v1.2"}
        ]
        latest_record = get_latest_record(data)
        self.assertEqual(latest_record['version'], 'v1.2')

    def test_get_latest_release(self):
        with patch('public_repo_scanner.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"tag_name": "v1.0.0"}
            version = get_latest_release('https://api.github.com/repos/org/repo/releases/latest')
            self.assertEqual(version, 'v1.0.0')

    def test_get_latest_release_error(self):
        with patch('public_repo_scanner.requests.get', side_effect=requests.exceptions.RequestException):
            version = get_latest_release('https://api.github.com/repos/org/repo/releases/latest')
            self.assertEqual(version, 'Error fetching data')

    def test_get_application_data(self):
        with patch('public_repo_scanner.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"version": "v1.0.0"}
            response = self.app.get('/api/sample-app')
            self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        with patch('public_repo_scanner.requests.get', side_effect=requests.exceptions.RequestException):
            response = self.app.get('/api/sample-app')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
