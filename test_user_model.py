"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Trainings, Trainings_users

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None, True)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password",None, True)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    ######SIGNUP#############
    def test_valid_signup(self):
        new_user = User.signup("newUser", "test@mail.com", "StrongPassword", None, True)
        uid = 555
        new_user.id = uid
        db.session.commit()

        new_user = User.query.get(uid)
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.username, "newUser")
        self.assertEqual(new_user.email, "test@mail.com")
        self.assertNotEqual(new_user.password, "StrongPassword")
        self.assertTrue(new_user.password.startswith("$2b$12$"))

    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None, True)


    #######authenticate########
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("invalidusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "worngpassword"))

    ########Create Trainig########
    def test_create_training(self):
        
        new_training = Trainings(title="Yoga", description="For your health", date=None,trainer_users_id=self.uid1)
        tid = 777
        new_training.id = tid
        db.session.commit()

        new_training = Trainings.query.get(tid)
        self.assertEqual(new_training.title, "Yoga")
        self.assertEqual(new_training.description, "For your health")
        self.assertEqual(new_training.trainer_users_id, self.uid1)


    # #####Follow test#####
    # def test_user_follows(self):
    #     self.u1.following.append(self.u2)
    #     db.session.commit()

    #     self.assertEqual(len(self.u2.following), 0)
    #     self.assertEqual(len(self.u2.followers), 1)
    #     self.assertEqual(len(self.u1.followers), 0)
    #     self.assertEqual(len(self.u1.following), 1)

    #     self.assertEqual(self.u2.followers[0].id, self.u1.id)
    #     self.assertEqual(self.u1.following[0].id, self.u2.id)


    # def test_user_unfollows(self):
    #     self.u1.following.append(self.u2)
    #     if self.u2 in self.u1.following:
    #         self.u1.following = [follower for follower in self.u1.following if follower != self.u2]
    #     db.session.commit()
    #     self.assertEqual(len(self.u2.followers), 0)

