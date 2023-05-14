#!/usr/bin/python3
"""Unittests for testing the Review class."""

import models
import unittest
import os
from datetime import datetime
from models.review import Review
from models.base_model import BaseModel
from time import sleep


class TestReview_Instantiation(unittest.TestCase):
    """Unittest for testing the instantiation of a Review object."""
    review = Review()

    def test_no_arg(self):
        """Test review instantiation with no args"""
        self.assertEqual(Review, type(self.review))

    def test_new_instance_in_objects(self):
        """Test for review object in storage"""
        id = self.review.id
        key = "Review.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(self.review, models.storage.all().values())

    def test_attributes_are_public(self):
        """Test for public method atrributes"""
        self.review.name = "Lagos"
        self.assertEqual(datetime, type(Review().created_at))
        self.assertEqual(datetime, type(Review().updated_at))
        self.assertEqual(str, type(Review().id))
        self.assertEqual("Lagos", self.review.name)

    def test_unique_ids(self):
        """Test that review Ids of each review is not equal"""
        review_2 = Review()
        self.assertNotEqual(review_2.id, self.review.id)

    def test_user_created_at_difference(self):
        """Test that creation time of two users is different"""
        review = Review()
        review_2 = Review()
        self.assertLess(review.created_at, review_2.created_at)

    def test_user_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        review = Review()
        review_2 = Review()
        self.assertLess(review.updated_at, review_2.updated_at)

    def test_str_repr(self):
        self.review.id = "101010"
        date = datetime.now()
        self.review.created_at = self.review.updated_at = date
        review_str = f"[Review] ({self.review.id}) {self.review.__dict__}"
        self.assertEqual(review_str, str(self.review))

    def test_instantiate_with_kwargs(self):
        date = datetime.now().isoformat()
        review = Review(id="123456", created_at=date, updated_at=date)
        self.assertEqual("123456", review.id)
        self.assertEqual(date, review.created_at)
        self.assertEqual(date, review.updated_at)

    def test_instantiate_with_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None)


class TestReview_save(unittest.TestCase):
    """Unittest for testing the save() method."""
    review = Review()

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
        updated = self.review.to_dict()["updated_at"]
        self.review.save()
        save_update = self.review.to_dict()["updated_at"]
        self.assertIsInstance(updated, str)
        self.assertIsInstance(save_update, str)
        self.assertNotEqual(updated, save_update)

    def test_save_twice(self):
        self.review.save()
        update_1 = self.review.updated_at
        self.review.save()
        update_2 = self.review.updated_at
        self.assertLess(update_1, update_2)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.review.save(None)


class TestReview_to_dict(unittest.TestCase):
    """Unittest for testing the to_dict() method."""
    review = Review()

    def test_to_dict_type(self):
        self.assertIsInstance(self.review.to_dict(), dict)

    def test_to_dict_contains_necessary_elements(self):
        keys = self.review.to_dict().keys()
        self.assertIn("id", keys)
        self.assertIn("created_at", keys)
        self.assertIn("updated_at", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_can_add_attributes(self):
        self.review.email = "example@mail.org"
        self.review.age = 89
        self.assertIn("email", self.review.to_dict().keys())
        self.assertIn("age", self.review.to_dict().keys())

    def test_to_dict_datetime_keys_are_str(self):
        review_dict = self.review.to_dict()
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_instantiate(self):
        review = Review()
        review.my_school = "Alx SE Cohorts"
        review.number = 98
        to_dict = review.to_dict()
        review_2 = Review(**to_dict)
        self.assertDictEqual(to_dict, review_2.to_dict())
        self.assertNotEqual(review, review_2)

    def test_to_dict_output(self):
        review = Review()
        date = datetime.now()
        review.id = "123456"
        review.created_at = review.updated_at = date
        review_dict = review.to_dict()
        test_dict = {
            "id": "123456",
            "created_at": date.isoformat(),
            "updated_at": date.isoformat(),
            "__class__": "Review"
        }
        self.assertDictEqual(review_dict, test_dict)

    def test_from_dict_instances_of_two_instances(self):
        review = Review()
        to_dict = review.to_dict()
        review_1 = Review(**to_dict)
        self.assertDictEqual(review.to_dict(), review_1.to_dict())
        self.assertIsInstance(review, BaseModel)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
