import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import app as api


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.old_path = api.DB_PATH
        api.DB_PATH = Path(self.directory.name) / "test.db"
        self.environment = patch.dict(os.environ, {
            "API_KEY": "test-key",  # pragma: allowlist secret (ficticio de prueba)
            "DEMO_ADMIN_PASSWORD": "test-password",  # pragma: allowlist secret
        })
        self.environment.start()
        api.init_db()
        self.client = api.app.test_client()

    def tearDown(self):
        self.environment.stop()
        api.DB_PATH = self.old_path
        self.directory.cleanup()

    def test_health(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)

    def test_profile_authentication(self):
        self.assertEqual(self.client.get("/api/profile").status_code, 401)
        self.assertEqual(self.client.get(
            "/api/profile", headers={"X-API-Key": "test-key"}
        ).status_code, 200)
        with patch.dict(os.environ, {"API_KEY": ""}):
            self.assertEqual(self.client.get("/api/profile").status_code, 503)

    def test_login_and_sql_injection(self):
        self.assertEqual(self.client.post("/api/login", json={
            "username": "admin", "password": "test-password"  # pragma: allowlist secret
        }).status_code, 200)
        self.assertEqual(self.client.post("/api/login", json={
            "username": "admin' --", "password": "wrong"  # pragma: allowlist secret
        }).status_code, 401)
        self.assertEqual(self.client.post("/api/login", json={
            "username": "admin", "password": "wrong"  # pragma: allowlist secret
        }).status_code, 401)
        self.assertEqual(self.client.post("/api/login", json=[]).status_code, 400)

    def test_password_is_hashed_and_init_is_idempotent(self):
        api.init_db()
        with closing(sqlite3.connect(api.DB_PATH)) as conn:
            rows = conn.execute("SELECT password_hash FROM users").fetchall()
        self.assertEqual(len(rows), 1)
        self.assertNotEqual(rows[0][0], "test-password")

    def test_old_schema_is_not_silently_migrated(self):
        api.DB_PATH = Path(self.directory.name) / "old.db"
        with closing(sqlite3.connect(api.DB_PATH)) as conn:
            conn.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
            conn.commit()
        with self.assertRaisesRegex(RuntimeError, "esquema vulnerable"):
            api.init_db()


if __name__ == "__main__":
    unittest.main()
