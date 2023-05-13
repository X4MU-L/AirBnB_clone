#!/usr/bin/env python3

import models
import unittest
import os
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
from time import sleep


class TestUser_Instantiation(unittest.TestCase):
    """Unittest for testing the attributes of the Amenity class"""
    amenity = Amenity()

    def test_no_arg(self):
        """Test amenity instantiation with no args"""
        self.assertEqual(Amenity, type(self.amenity))

    def test_new_instance_in_objects(self):
        """Test for amenity object in storage"""
        id = self.amenity.id
        key = "Amenity.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(self.amenity, models.storage.all().values())

    def test_attributes_are_public(self):
        """Test for public method atrributes"""
        self.amenity.email = "example@gmail.com"
        self.amenity.password = "123456"
        self.amenity.first_name = "Betty"
        self.amenity.last_name = "Holberton"
        self.assertEqual(datetime, type(Amenity().created_at))
        self.assertEqual(datetime, type(Amenity().updated_at))
        self.assertEqual(str, type(Amenity().id))
        self.assertEqual("example@gmail.com", self.amenity.email)
        self.assertEqual("123456", self.amenity.password)
        self.assertEqual("Betty", self.amenity.first_name)
        self.assertEqual("Holberton", self.amenity.last_name)

    def test_unique_ids(self):
        """Test that amenity Ids of each amenity is not equal"""
        amenity_2 = Amenity()
        self.assertNotEqual(amenity_2.id, self.amenity.id)

    def test_user_created_at_difference(self):
        """Test that creation time of two users is different"""
        d = Amenity()
        amenity_2 = Amenity()
        self.assertLess(d.created_at, amenity_2.created_at)

    def test_user_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        d = Amenity()
        amenity_2 = Amenity()
        self.assertLess(d.updated_at, amenity_2.updated_at)

    def test_str_repr(self):
        self.amenity.id = "101010"
        date = datetime.now()
        self.amenity.created_at = self.amenity.updated_at = date
        amenity_str = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(amenity_str, str(self.amenity))

    def test_instantiate_with_kwargs(self):
        date = datetime.now().isoformat()
        amenity = Amenity(id="123456", created_at=date, updated_at=date)
        self.assertEqual("123456", amenity.id)
        self.assertEqual(date, amenity.created_at)
        self.assertEqual(date, amenity.updated_at)

    def test_instantiate_with_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None)


class TestUser_save(unittest.TestCase):
    """Unittest for testing the save() method."""
    amenity = Amenity()

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
        updated = self.amenity.to_dict()["updated_at"]
        self.amenity.save()
        save_update = self.amenity.to_dict()["updated_at"]
        self.assertIsInstance(updated, str)
        self.assertIsInstance(save_update, str)
        self.assertNotEqual(updated, save_update)

    def test_save_twice(self):
        self.amenity.save()
        update_1 = self.amenity.updated_at
        self.amenity.save()
        update_2 = self.amenity.updated_at
        self.assertLess(update_1, update_2)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.amenity.save(None)


class TestUser_to_dict(unittest.TestCase):
    amenity = Amenity()

    def test_to_dict_type(self):
        self.assertIsInstance(self.amenity.to_dict(), dict)

    def test_to_dict_contains_necessary_elements(self):
        keys = self.amenity.to_dict().keys()
        self.assertIn("id", keys)
        self.assertIn("created_at", keys)
        self.assertIn("updated_at", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_can_add_attributes(self):
        self.amenity.email = "example@mail.org"
        self.amenity.age = 89
        self.assertIn("email", self.amenity.to_dict().keys())
        self.assertIn("age", self.amenity.to_dict().keys())

    def test_to_dict_datetime_keys_are_str(self):
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_instantiate(self):
        amenity = Amenity()
        amenity.my_school = "Alx SE Cohorts"
        amenity.number = 98
        to_dict = amenity.to_dict()
        d = Amenity(**to_dict)
        self.assertDictEqual(to_dict, d.to_dict())
        self.assertNotEqual(amenity, d)

    def test_to_dict_output(self):
        amenity = Amenity()
        date = datetime.now()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = date
        amenity_dict = amenity.to_dict()
        test_dict = {
            "id": "123456",
            "created_at": date.isoformat(),
            "updated_at": date.isoformat(),
            "__class__": "Amenity"
        }
        self.assertDictEqual(amenity_dict, test_dict)

    def test_from_dict_instances_of_two_instances(self):
        amenity = Amenity()
        to_dict = amenity.to_dict()
        amenity1 = Amenity(**to_dict)
        self.assertDictEqual(amenity.to_dict(), amenity1.to_dict())
        self.assertIsInstance(amenity, BaseModel)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
