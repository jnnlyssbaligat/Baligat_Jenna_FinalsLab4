from django.test import TestCase
from django.urls import reverse


class StatusEndpointTests(TestCase):
    def test_returns_200_and_json_content_type(self):
        response = self.client.get(reverse("status"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_payload_has_expected_keys(self):
        data = self.client.get(reverse("status")).json()
        for key in ("status", "server_time", "employee_count", "online_now", "departments"):
            self.assertIn(key, data)
        self.assertEqual(data["status"], "ok")

    def test_totals_match_departments(self):
        data = self.client.get(reverse("status")).json()
        self.assertEqual(data["employee_count"], sum(d["staff"] for d in data["departments"]))
        self.assertEqual(data["online_now"], sum(d["online"] for d in data["departments"]))

    def test_url_path(self):
        self.assertEqual(reverse("status"), "/api/status/")

    def test_unknown_url_is_404(self):
        self.assertEqual(self.client.get("/api/nope/").status_code, 404)
