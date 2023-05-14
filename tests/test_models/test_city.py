#!/usr/bin/python3
"""Unittests for testing the City class."""

import models
import unittest
import os
from datetime import datetime
from models.city import City
from models.base_model import BaseModel
from time import sleep


class TestCity_Instantiation(unittest.TestCase):
    """Unittest for testing the instantiation of a City object."""
    city = City()

    def test_no_arg(self):
        """Test city instantiation with no args"""
        self.assertEqual(City, type(self.city))

    def test_new_instance_in_objects(self):
        """Test for city object in storage"""
        id = self.city.id
        key = "City.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(self.city, models.storage.all().values())

    def test_attributes_are_public(self):
        """Test for public method atrributes"""
        self.city.name = "Lagos"
        self.city.state_id = "1001"
        self.assertEqual(datetime, type(City().created_at))
        self.assertEqual(datetime, type(City().updated_at))
        self.assertEqual(str, type(City().id))
        self.assertEqual("Lagos", self.city.name)
        self.assertEqual("1001", self.city.state_id)

    def test_unique_ids(self):
        """Test that city Ids of each city is not equal"""
        city_2 = City()
        self.assertNotEqual(city_2.id, self.city.id)

    def test_user_created_at_difference(self):
        """Test that creation time of two users is different"""
        city = City()
        city_2 = City()
        self.assertLess(city.created_at, city_2.created_at)

    def test_user_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        city = City()
        city_2 = City()
        self.assertLess(city.updated_at, city_2.updated_at)

    def test_str_repr(self):
        self.city.id = "101010"
        date = datetime.now()
        self.city.created_at = self.city.updated_at = date
        city_str = f"[City] ({self.city.id}) {self.city.__dict__}"
        self.assertEqual(city_str, str(self.city))

    def test_instantiate_with_kwargs(self):
        date = datetime.now().isoformat()
        city = City(id="123456", created_at=date, updated_at=date)
        self.assertEqual("123456", city.id)
        self.assertEqual(date, city.created_at)
        self.assertEqual(date, city.updated_at)

    def test_instantiate_with_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None)


class TestCity_save(unittest.TestCase):
    """Unittest for testing the save() method."""
    city = City()

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
        updated = self.city.to_dict()["updated_at"]
        self.city.save()
        save_update = self.city.to_dict()["updated_at"]
        self.assertIsInstance(updated, str)
        self.assertIsInstance(save_update, str)
        self.assertNotEqual(updated, save_update)

    def test_save_twice(self):
        self.city.save()
        update_1 = self.city.updated_at
        self.city.save()
        update_2 = self.city.updated_at
        self.assertLess(update_1, update_2)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.city.save(None)


class TestCity_to_dict(unittest.TestCase):
    """Unittest for testing the to_dict() method."""
    city = City()

    def test_to_dict_type(self):
        self.assertIsInstance(self.city.to_dict(), dict)

    def test_to_dict_contains_necessary_elements(self):
        keys = self.city.to_dict().keys()
        self.assertIn("id", keys)
        self.assertIn("created_at", keys)
        self.assertIn("updated_at", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_can_add_attributes(self):
        self.city.email = "example@mail.org"
        self.city.age = 89
        self.assertIn("email", self.city.to_dict().keys())
        self.assertIn("age", self.city.to_dict().keys())

    def test_to_dict_datetime_keys_are_str(self):
        city_dict = self.city.to_dict()
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_instantiate(self):
        city = City()
        city.my_school = "Alx SE Cohorts"
        city.number = 98
        to_dict = city.to_dict()
        city_2 = City(**to_dict)
        self.assertDictEqual(to_dict, city_2.to_dict())
        self.assertNotEqual(city, city_2)

    def test_to_dict_output(self):
        city = City()
        date = datetime.now()
        city.id = "123456"
        city.created_at = city.updated_at = date
        city_dict = city.to_dict()
        test_dict = {
            "id": "123456",
            "created_at": date.isoformat(),
            "updated_at": date.isoformat(),
            "__class__": "City"
        }
        self.assertDictEqual(city_dict, test_dict)

    def test_from_dict_instances_of_two_instances(self):
        city = City()
        to_dict = city.to_dict()
        city_1 = City(**to_dict)
        self.assertDictEqual(city.to_dict(), city_1.to_dict())
        self.assertIsInstance(city, BaseModel)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.city.to_dict(None)

    def test_to_dict_return_value_not_same_as_self_dict(self):
        city = City()
        d = city.to_dict()
        self.assertNotEqual(d, city.__dict__)


if __name__ == "__main__":
    unittest.main()
