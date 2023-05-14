#!/usr/bin/python3
"""Unittests for testing the State class."""

import models
import unittest
import os
from datetime import datetime
from models.state import State
from models.base_model import BaseModel
from time import sleep


class TestState_Instantiation(unittest.TestCase):
    """Unittest for testing the instantiation of a State object."""
    state = State()

    def test_no_arg(self):
        """Test state instantiation with no args"""
        self.assertEqual(State, type(self.state))

    def test_new_instance_in_objects(self):
        """Test for state object in storage"""
        id = self.state.id
        key = "State.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(self.state, models.storage.all().values())

    def test_attributes_are_public(self):
        """Test for public method atrributes"""
        self.state.name = "Lagos"
        self.assertEqual(datetime, type(State().created_at))
        self.assertEqual(datetime, type(State().updated_at))
        self.assertEqual(str, type(State().id))
        self.assertEqual("Lagos", self.state.name)

    def test_unique_ids(self):
        """Test that state Ids of each state is not equal"""
        state_2 = State()
        self.assertNotEqual(state_2.id, self.state.id)

    def test_user_created_at_difference(self):
        """Test that creation time of two users is different"""
        state = State()
        state_2 = State()
        self.assertLess(state.created_at, state_2.created_at)

    def test_user_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        state = State()
        state_2 = State()
        self.assertLess(state.updated_at, state_2.updated_at)

    def test_str_repr(self):
        self.state.id = "101010"
        date = datetime.now()
        self.state.created_at = self.state.updated_at = date
        amenity_str = f"[State] ({self.state.id}) {self.state.__dict__}"
        self.assertEqual(amenity_str, str(self.state))

    def test_instantiate_with_kwargs(self):
        date = datetime.now().isoformat()
        state = State(id="123456", created_at=date, updated_at=date)
        self.assertEqual("123456", state.id)
        self.assertEqual(date, state.created_at)
        self.assertEqual(date, state.updated_at)

    def test_instantiate_with_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None)


class TestState_save(unittest.TestCase):
    """Unittest for testing the save() method."""
    state = State()

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
        updated = self.state.to_dict()["updated_at"]
        self.state.save()
        save_update = self.state.to_dict()["updated_at"]
        self.assertIsInstance(updated, str)
        self.assertIsInstance(save_update, str)
        self.assertNotEqual(updated, save_update)

    def test_save_twice(self):
        self.state.save()
        update_1 = self.state.updated_at
        self.state.save()
        update_2 = self.state.updated_at
        self.assertLess(update_1, update_2)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.state.save(None)


class TestState_to_dict(unittest.TestCase):
    """Unittest for testing the to_dict() method."""
    state = State()

    def test_to_dict_type(self):
        self.assertIsInstance(self.state.to_dict(), dict)

    def test_to_dict_contains_necessary_elements(self):
        keys = self.state.to_dict().keys()
        self.assertIn("id", keys)
        self.assertIn("created_at", keys)
        self.assertIn("updated_at", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_can_add_attributes(self):
        self.state.email = "example@mail.org"
        self.state.age = 89
        self.assertIn("email", self.state.to_dict().keys())
        self.assertIn("age", self.state.to_dict().keys())

    def test_to_dict_datetime_keys_are_str(self):
        state_dict = self.state.to_dict()
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_instantiate(self):
        state = State()
        state.my_school = "Alx SE Cohorts"
        state.number = 98
        to_dict = state.to_dict()
        state_2 = State(**to_dict)
        self.assertDictEqual(to_dict, state_2.to_dict())
        self.assertNotEqual(state, state_2)

    def test_to_dict_output(self):
        state = State()
        date = datetime.now()
        state.id = "123456"
        state.created_at = state.updated_at = date
        state_dict = state.to_dict()
        test_dict = {
            "id": "123456",
            "created_at": date.isoformat(),
            "updated_at": date.isoformat(),
            "__class__": "State"
        }
        self.assertDictEqual(state_dict, test_dict)

    def test_from_dict_instances_of_two_instances(self):
        state = State()
        to_dict = state.to_dict()
        state_1 = State(**to_dict)
        self.assertDictEqual(state.to_dict(), state_1.to_dict())
        self.assertIsInstance(state, BaseModel)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.state.to_dict(None)

    def test_to_dict_return_value_not_same_as_self_dict(self):
        state = State()
        d = state.to_dict()
        self.assertNotEqual(d, state.__dict__)


if __name__ == "__main__":
    unittest.main()
