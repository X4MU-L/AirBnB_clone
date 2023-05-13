#!/usr/bin/env python3

import models
import os
import unittest
from datetime import datetime
from models.amenity import Amenity
from models.user import User
from models.base_model import BaseModel
from time import sleep


class TestUser_Instantiation(unittest.TestCase):
    """Unittest for testing the attributes of the User class"""
    user = User()

    def test_no_arg(self):
        """Test user instantiation with no args"""
        self.assertEqual(User, type(self.user))

    def test_new_instance_in_objects(self):
        """Test for user object in storage"""
        id = self.user.id
        key = "User.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(self.user, models.storage.all().values())

    def test_attributes_are_public(self):
        """Test for public method atrributes"""
        self.user.email = "example@gmail.com"
        self.user.password = "123456"
        self.user.first_name = "Betty"
        self.user.last_name = "Holberton"
        self.assertEqual(datetime, type(User().created_at))
        self.assertEqual(datetime, type(User().updated_at))
        self.assertEqual(str, type(User().id))
        self.assertEqual("example@gmail.com", self.user.email)
        self.assertEqual("123456", self.user.password)
        self.assertEqual("Betty", self.user.first_name)
        self.assertEqual("Holberton", self.user.last_name)

    def test_unique_ids(self):
        """Test that user Ids of each user is not equal"""
        user2 = User()
        self.assertNotEqual(user2.id, self.user.id)

    def test_user_created_at_difference(self):
        """Test that creation time of two users is different"""
        user1 = User()
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_user_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        user1 = User()
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_repr(self):
        self.user.id = "101010"
        date = datetime.now()
        self.user.created_at = self.user.updated_at = date
        user_str = f"[User] ({self.user.id}) {self.user.__dict__}"
        self.assertEqual(user_str, str(self.user))

    def test_instantiate_with_kwargs(self):
        date = datetime.now().isoformat()
        user = User(id="123456", created_at=date, updated_at=date)
        self.assertEqual("123456", user.id)
        self.assertEqual(date, user.created_at)
        self.assertEqual(date, user.updated_at)

    def test_instantiate_with_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None)


class TestUser_save(unittest.TestCase):
    """Unittest for testing the save() method."""
    user = User()

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "temp_file")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("temp_file", "file.json")
        except FileNotFoundError:
            pass

    def test_after_save_updated_time_different(self):
        updated = self.user.to_dict()["updated_at"]
        self.user.save()
        save_update = self.user.to_dict()["updated_at"]
        self.assertIsInstance(updated, str)
        self.assertIsInstance(save_update, str)
        self.assertNotEqual(updated, save_update)

    def test_save_twice(self):
        self.user.save()
        update_1 = self.user.updated_at
        self.user.save()
        update_2 = self.user.updated_at
        self.assertLess(update_1, update_2)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.user.save(None)


class TestUser_to_dict(unittest.TestCase):
    user = User()

    def test_to_dict_type(self):
        self.assertIsInstance(self.user.to_dict(), dict)

    def test_to_dict_contains_necessary_elements(self):
        keys = self.user.to_dict().keys()
        self.assertIn("id", keys)
        self.assertIn("created_at", keys)
        self.assertIn("updated_at", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_can_add_attributes(self):
        self.user.email = "example@mail.org"
        self.user.age = 89
        self.assertIn("email", self.user.to_dict().keys())
        self.assertIn("age", self.user.to_dict().keys())

    def test_to_dict_datetime_keys_are_str(self):
        user_dict = self.user.to_dict()
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_instantiate(self):
        user = User()
        user.my_school = "Alx SE Cohorts"
        user.number = 98
        to_dict = user.to_dict()
        user1 = User(**to_dict)
        self.assertDictEqual(to_dict, user1.to_dict())
        self.assertNotEqual(user, user1)

    def test_to_dict_output(self):
        user = User()
        date = datetime.now()
        user.id = "123456"
        user.created_at = user.updated_at = date
        user_dict = user.to_dict()
        test_dict = {
            "id": "123456",
            "created_at": date.isoformat(),
            "updated_at": date.isoformat(),
            "__class__": "User"
        }
        self.assertDictEqual(user_dict, test_dict)

    def test_from_dict_instances_of_two_instances(self):
        user = User()
        to_dict = user.to_dict()
        user1 = User(**to_dict)
        self.assertDictEqual(user.to_dict(), user1.to_dict())
        self.assertIsInstance(user, BaseModel)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
