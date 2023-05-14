#!/usr/bin/python3
"""Unittests for testing the Place class."""

import models
import unittest
import os
from datetime import datetime
from models.place import Place
from models.base_model import BaseModel
from time import sleep


class TestPlace_Instantiation(unittest.TestCase):
    """Unittest for testing the instantiation of a Place object."""
    place = Place()

    def test_no_arg(self):
        """Test place instantiation with no args"""
        self.assertEqual(Place, type(self.place))

    def test_new_instance_in_objects(self):
        """Test for place object in storage"""
        id = self.place.id
        key = "Place.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(self.place, models.storage.all().values())

    def test_attributes_are_public(self):
        """Test for public method atrributes"""
        self.place.city_id = "101"
        self.place.user_id = "001"
        self.place.name = "Lagos"
        self.place.description = "Beach Town"
        self.place.number_rooms = 4
        self.place.number_bathrooms = 4
        self.place.max_guest = 2
        self.place.price_by_night = 800
        self.place.latitude = 0.0
        self.place.longitude = 0.0
        self.place.amenity_ids = ["001", "002", "003", "004"]
        self.assertEqual(datetime, type(Place().created_at))
        self.assertEqual(datetime, type(Place().updated_at))
        self.assertEqual(str, type(Place().id))
        self.assertEqual("101", self.place.city_id)
        self.assertEqual("001", self.place.user_id)
        self.assertEqual("Lagos", self.place.name)
        self.assertEqual("Beach Town", self.place.description)
        self.assertEqual(4, self.place.number_rooms)
        self.assertEqual(4, self.place.number_bathrooms)
        self.assertEqual(2, self.place.max_guest)
        self.assertEqual(800, self.place.price_by_night)
        self.assertEqual(0.0, self.place.latitude)
        self.assertEqual(0.0, self.place.longitude)
        self.assertEqual(["001", "002", "003", "004"], self.place.amenity_ids)

    def test_unique_ids(self):
        """Test that place Ids of each place is not equal"""
        place_2 = Place()
        self.assertNotEqual(place_2.id, self.place.id)

    def test_user_created_at_difference(self):
        """Test that creation time of two users is different"""
        place = Place()
        place_2 = Place()
        self.assertLess(place.created_at, place_2.created_at)

    def test_user_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        place = Place()
        place_2 = Place()
        self.assertLess(place.updated_at, place_2.updated_at)

    def test_str_repr(self):
        self.place.id = "101010"
        date = datetime.now()
        self.place.created_at = self.place.updated_at = date
        amenity_str = f"[Place] ({self.place.id}) {self.place.__dict__}"
        self.assertEqual(amenity_str, str(self.place))

    def test_instantiate_with_kwargs(self):
        date = datetime.now().isoformat()
        place = Place(id="123456", created_at=date, updated_at=date)
        self.assertEqual("123456", place.id)
        self.assertEqual(date, place.created_at)
        self.assertEqual(date, place.updated_at)

    def test_instantiate_with_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittest for testing the save() method."""
    place = Place()

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
        updated = self.place.to_dict()["updated_at"]
        self.place.save()
        save_update = self.place.to_dict()["updated_at"]
        self.assertIsInstance(updated, str)
        self.assertIsInstance(save_update, str)
        self.assertNotEqual(updated, save_update)

    def test_save_twice(self):
        self.place.save()
        update_1 = self.place.updated_at
        self.place.save()
        update_2 = self.place.updated_at
        self.assertLess(update_1, update_2)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.place.save(None)


class TestPlace_to_dict(unittest.TestCase):
    """Unittest for testing the to_dict() method."""
    place = Place()

    def test_to_dict_type(self):
        self.assertIsInstance(self.place.to_dict(), dict)

    def test_to_dict_contains_necessary_elements(self):
        keys = self.place.to_dict().keys()
        self.assertIn("id", keys)
        self.assertIn("created_at", keys)
        self.assertIn("updated_at", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_can_add_attributes(self):
        self.place.email = "example@mail.org"
        self.place.age = 89
        self.assertIn("email", self.place.to_dict().keys())
        self.assertIn("age", self.place.to_dict().keys())

    def test_to_dict_datetime_keys_are_str(self):
        place_dict = self.place.to_dict()
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_instantiate(self):
        place = Place()
        place.my_school = "Alx SE Cohorts"
        place.number = 98
        to_dict = place.to_dict()
        place_2 = Place(**to_dict)
        self.assertDictEqual(to_dict, place_2.to_dict())
        self.assertNotEqual(place, place_2)

    def test_to_dict_output(self):
        place = Place()
        date = datetime.now()
        place.id = "123456"
        place.created_at = place.updated_at = date
        place_dict = place.to_dict()
        test_dict = {
            "id": "123456",
            "created_at": date.isoformat(),
            "updated_at": date.isoformat(),
            "__class__": "Place"
        }
        self.assertDictEqual(place_dict, test_dict)

    def test_from_dict_instances_of_two_instances(self):
        place = Place()
        to_dict = place.to_dict()
        place_1 = Place(**to_dict)
        self.assertDictEqual(place.to_dict(), place_1.to_dict())
        self.assertIsInstance(place, BaseModel)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.place.to_dict(None)

    def test_to_dict_return_value_not_same_as_self_dict(self):
        place = Place()
        d = place.to_dict()
        self.assertNotEqual(d, place.__dict__)


if __name__ == "__main__":
    unittest.main()
