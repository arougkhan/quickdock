#!flask/bin/python#
import os
import unittest
#
from flask import current_app
from app import create_app
#
#jwt = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJVlpJVHhXWnZUeGZNOW5DQlhmMHQ4QTFqQ2xMdlpDOXcxTVFlSjlVMU44In0.eyJleHAiOjE2NDIwOTc4MjYsImlhdCI6MTY0MjA2OTAyNiwianRpIjoiNGNmMDE0ZjUtZGJkZS00Zjc0LWI2NmEtNDY5M2MwNTNlNjJkIiwiaXNzIjoiaHR0cHM6Ly9kZXYud2ViZG9jLXguY29tL2F1dGgvcmVhbG1zL3dkeCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJkYzU4YmQ4Ni0wOTBkLTRlMmQtOTQ3Yy1jNzgzYjJkZTg2ZmEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3ZHgiLCJzZXNzaW9uX3N0YXRlIjoiZmI5NmU5NzQtM2JjZi00OGRmLTkwYjUtN2I1MGRlZGY4MmM0IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJtZWRpY2FsIiwiZGVmYXVsdC1yb2xlcy13ZHgiLCJvZmZsaW5lX2FjY2VzcyIsImhyX2FkbWluIiwidW1hX2F1dGhvcml6YXRpb24iLCJ1c2VyIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiZmI5NmU5NzQtM2JjZi00OGRmLTkwYjUtN2I1MGRlZGY4MmM0IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJncm91cF9pZCI6IjlkYjVlMmFmLTgxYTEtNDc2Yy04ZGRiLTQ1MTY4ZTAyZmM2ZSIsInVzZXJfaWQiOiI1OGUwMmRmOS02ZDZiLTQ5MzItODRjZS0yNDY1YzY3MWU2NmEiLCJvcmdfaWQiOiI5ZGI1ZTJhZi04MWExLTQ3NmMtOGRkYi00NTE2OGUwMmZjNmUiLCJuYW1lIjoiUm9iZXJ0IGRlIEJlc2NoZSIsInByZWZlcnJlZF91c2VybmFtZSI6InJvYmVydC5kZWJlc2NoZUBjaG9ydXMuc2UiLCJnaXZlbl9uYW1lIjoiUm9iZXJ0IiwiZmFtaWx5X25hbWUiOiJkZSBCZXNjaGUiLCJlbWFpbCI6InJvYmVydC5kZWJlc2NoZUBjaG9ydXMuc2UifQ.c8jIGbmhYH4axv06ovUuNiKxtrFFpOCwJlGPj3SKeOd7XTmkyjkABAEi5Z4iO2uxsSBP6rnfglOJAHltIkZGrWZSwPmUNu1nDeSd_z9--pEyXcYzU-KdP0xynoAZ5ewZQkKEYY7Fwscm0PYXuPu5gA3jr2ioBafsla8LPhPjp67Tvjx5E-nBITkihzsfByWgs8lpZH3orHkjNyitsV_gyTOE757Cxraw4P51G0WqSSZsj3JJ9FAU8EPDnGjKIw_S1wk0HH1DUKi-lr-XTRhtZWAIRiOmuJbKzwA8g6rciVtNrs6U_cnxLFF49ktfzyv9y8y8FAMAdNhH3XKfxkjN6Q"
#
#class TestCase(unittest.TestCase):
#    def setUp(self):
#        app.config['TESTING'] = True
#        app.config['WTF_CSRF_ENABLED'] = False
#        self.app = app.test_client()
#
#    def test_jwtRoles(self):
#        with self.app.test_client() as client:
#            client.get('/ping'),
#            data=None,
#            headers={'Authorization': jwt}
#
#if __name__ == '__main__':
#    unittest.main()

class TestWebApp(unittest.TestCase):
    # Invoked before every test
    def setup(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app_app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    # Invoked after every test
    def teardown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_get_ping(self):
        response = self.client.get('/ping')
        assert response.status_code == 200
        assert response.get_data(as_text=True)