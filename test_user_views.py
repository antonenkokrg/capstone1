"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, User, Trainings, Trainings_users
# from bs4 import BeautifulSoup
from app import app, CURR_USER_KEY, session

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class UserViewTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None,
                                    is_trainer=True)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("first_username", "test1@test.com", "password", None, True)
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.signup("testuser2", "test2@test.com", "password", None, False)
        self.u2_id = 884
        self.u2.id = self.u2_id
        self.u3 = User.signup("testuser3", "test3@test.com", "password", None, False)
        self.u4 = User.signup("testing", "test4@test.com", "password", None, True)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    # def test_users_index(self):
    #     with self.client as c:
    #         resp = c.get("/users/self.testuser_id")

    #         self.assertIn("@testuser", str(resp.data))
    #         self.assertIn("first_username", str(resp.data))
    #         self.assertIn("@testuser2", str(resp.data))
    #         self.assertIn("@testuser3", str(resp.data))
    #         self.assertIn("@testing", str(resp.data))

    def test_user_show_when_login(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                resp = c.get(f"/users/{self.testuser_id}")

                self.assertEqual(resp.status_code, 200)

                self.assertIn("@testuser2", str(resp.data))

    # def test_user_show(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser_id
    #             resp = c.get(f"/users/{self.testuser_id}")
    #             html = resp.get_data(as_text=True)

    #             self.assertEqual(resp.status_code, 200)
    #             self.assertIn("@testuser", html)

    # def test_user_show(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser_id
    #             resp = c.get(f"/users/{self.testuser_id}")
    #             html = resp.get_data(as_text=True)

    #             self.assertEqual(resp.status_code, 200)
    #             self.assertIn("@testuser", html)

    # def setup_followers(self):
    #     f1 = Follows(user_being_followed_id=self.u1_id, user_following_id=self.testuser_id)
    #     f2 = Follows(user_being_followed_id=self.u2_id, user_following_id=self.testuser_id)
    #     f3 = Follows(user_being_followed_id=self.testuser_id, user_following_id=self.u1_id)

    #     db.session.add_all([f1,f2,f3])
    #     db.session.commit()


    # def test_show_following(self):

    #     self.setup_followers()
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser_id

    #         resp = c.get(f"/users/{self.testuser_id}/following")
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("first_username", str(resp.data))
    #         self.assertIn("@testuser2", str(resp.data))
    #         self.assertNotIn("@testuser3", str(resp.data))
    #         self.assertNotIn("@testing", str(resp.data))

    # def test_show_followers(self):

    #     self.setup_followers()
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser_id

    #         resp = c.get(f"/users/{self.testuser_id}/followers")

    #         self.assertIn("first_username", str(resp.data))
    #         self.assertNotIn("@testuser2", str(resp.data))
    #         self.assertNotIn("@testuser3", str(resp.data))
    #         self.assertNotIn("@testing", str(resp.data))

    # def test_unauthorized_following_page_access(self):
    #     self.setup_followers()
    #     with self.client as c:

    #         resp = c.get(f"/users/{self.testuser_id}/following", follow_redirects=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("first_username", str(resp.data))
    #         self.assertIn("Access unauthorized", str(resp.data))

    # def test_unauthorized_followers_page_access(self):
    #     self.setup_followers()
    #     with self.client as c:

    #         resp = c.get(f"/users/{self.testuser_id}/followers", follow_redirects=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("first_username", str(resp.data))
    #         self.assertIn("Access unauthorized", str(resp.data))
