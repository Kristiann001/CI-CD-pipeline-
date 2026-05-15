"""
Unit Tests for the Counter Service
Run with: nosetests -v --with-spec --spec-color --with-coverage --cover-package=app
"""
import unittest
from app import app


class TestCounterService(unittest.TestCase):
    """Test cases for the Counter REST API."""

    def setUp(self):
        """Set up test client and clear counters before each test."""
        self.app = app.test_client()
        self.app.testing = True
        # Clear all counters before each test
        from app import counter
        counter.COUNTERS.clear()

    # ── Health Check ──────────────────────────────────────────────────────
    def test_index_returns_200(self):
        """GET / should return 200 OK."""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_index_returns_json(self):
        """GET / should return a JSON body with status OK."""
        resp = self.app.get("/")
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    # ── Create Counter (POST) ─────────────────────────────────────────────
    def test_create_counter_returns_201(self):
        """POST /counters/<name> should create a counter and return 201."""
        resp = self.app.post("/counters/hits")
        self.assertEqual(resp.status_code, 201)

    def test_create_counter_initial_value_is_zero(self):
        """A newly created counter should start at 0."""
        resp = self.app.post("/counters/hits")
        data = resp.get_json()
        self.assertEqual(data["hits"], 0)

    def test_create_duplicate_counter_returns_409(self):
        """Creating a counter that already exists should return 409 Conflict."""
        self.app.post("/counters/hits")
        resp = self.app.post("/counters/hits")
        self.assertEqual(resp.status_code, 409)

    # ── Read Counter (GET) ────────────────────────────────────────────────
    def test_read_counter_returns_200(self):
        """GET /counters/<name> should return 200 for an existing counter."""
        self.app.post("/counters/visits")
        resp = self.app.get("/counters/visits")
        self.assertEqual(resp.status_code, 200)

    def test_read_counter_value(self):
        """GET /counters/<name> should return the correct value."""
        self.app.post("/counters/visits")
        resp = self.app.get("/counters/visits")
        data = resp.get_json()
        self.assertEqual(data["visits"], 0)

    def test_read_nonexistent_counter_returns_404(self):
        """GET /counters/<name> for unknown counter should return 404."""
        resp = self.app.get("/counters/ghost")
        self.assertEqual(resp.status_code, 404)

    # ── Update Counter (PUT) ──────────────────────────────────────────────
    def test_update_counter_increments_by_one(self):
        """PUT /counters/<name> should increment the counter by 1."""
        self.app.post("/counters/clicks")
        resp = self.app.put("/counters/clicks")
        data = resp.get_json()
        self.assertEqual(data["clicks"], 1)

    def test_update_counter_multiple_times(self):
        """Multiple PUTs should keep incrementing the counter."""
        self.app.post("/counters/clicks")
        self.app.put("/counters/clicks")
        self.app.put("/counters/clicks")
        resp = self.app.put("/counters/clicks")
        data = resp.get_json()
        self.assertEqual(data["clicks"], 3)

    def test_update_nonexistent_counter_returns_404(self):
        """PUT on unknown counter should return 404."""
        resp = self.app.put("/counters/ghost")
        self.assertEqual(resp.status_code, 404)

    # ── Delete Counter (DELETE) ───────────────────────────────────────────
    def test_delete_counter_returns_204(self):
        """DELETE /counters/<name> should return 204 No Content."""
        self.app.post("/counters/temp")
        resp = self.app.delete("/counters/temp")
        self.assertEqual(resp.status_code, 204)

    def test_delete_counter_removes_it(self):
        """After DELETE, the counter should no longer exist (404)."""
        self.app.post("/counters/temp")
        self.app.delete("/counters/temp")
        resp = self.app.get("/counters/temp")
        self.assertEqual(resp.status_code, 404)

    def test_delete_nonexistent_counter_returns_404(self):
        """DELETE on unknown counter should return 404."""
        resp = self.app.delete("/counters/ghost")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
