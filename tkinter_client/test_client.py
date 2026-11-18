"""Tests for the network logic in client.py (no window needed). Run: python -m unittest discover tkinter_client"""
import sys
import unittest
from pathlib import Path
from unittest import mock

import requests

sys.path.insert(0, str(Path(__file__).parent))

# client.py imports tkinter at the top; stub it so these tests also run where Tk is missing.
try:
    import tkinter  # noqa: F401
except ModuleNotFoundError:
    for name in ("tkinter", "tkinter.ttk"):
        sys.modules[name] = mock.MagicMock()

import client  # noqa: E402


def fake_response(status=200, payload=None, bad_json=False):
    r = mock.Mock()
    r.status_code = status
    if bad_json:
        r.json.side_effect = ValueError("no json")
    else:
        r.json.return_value = payload
    return r


class FetchStatusTests(unittest.TestCase):
    def test_success_returns_data(self):
        with mock.patch("requests.get", return_value=fake_response(200, {"status": "ok"})):
            data, error = client.fetch_status("http://x/")
        self.assertEqual(data, {"status": "ok"})
        self.assertIsNone(error)

    def test_connection_error_is_handled(self):
        with mock.patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            data, error = client.fetch_status("http://x/")
        self.assertIsNone(data)
        self.assertIn("unreachable", error)

    def test_timeout_is_handled(self):
        with mock.patch("requests.get", side_effect=requests.exceptions.Timeout):
            self.assertIn("too long", client.fetch_status("http://x/")[1])

    def test_non_200_is_not_parsed(self):
        resp = fake_response(500, {"status": "ok"})
        with mock.patch("requests.get", return_value=resp):
            data, error = client.fetch_status("http://x/")
        self.assertIsNone(data)
        self.assertIn("500", error)
        resp.json.assert_not_called()

    def test_invalid_json_is_handled(self):
        with mock.patch("requests.get", return_value=fake_response(200, bad_json=True)):
            self.assertIn("valid JSON", client.fetch_status("http://x/")[1])


if __name__ == "__main__":
    unittest.main()
