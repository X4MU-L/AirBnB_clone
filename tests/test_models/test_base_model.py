#!/usr/bin/python3
"""Unittest for testing the BaseModel class."""

import models
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel_Instantiation(unittest.TestCase):
    """Unittest for testing the functionalities of the Basemodel class."""
    def test_instantiation_without_arg(self):
        base = BaseModel()
        self.assertIsInstance(base, BaseModel)

    def test_new_instance_in_objects(self):
        base = BaseModel()
        id = base.id
        key = "BaseModel.{}".format(id)
        self.assertIn(key, models.storage.all().keys())
        self.assertIn(base, models.storage.all().values())

    def test_instantiation_from_dict(self):
        date = "2023-05-09T00:00:00.000000"
        d = {'id': 8998, 'updated_at': date, 'created_at': date}
        base = BaseModel(**d)
        self.assertIsInstance(base, BaseModel)

    def test_unique_ids(self):
        base = BaseModel()
        base_2 = BaseModel()
        self.assertNotEqual(base_2.id, base.id)

    def test_base_created_at_difference(self):
        """Test that creation time of two users is different"""
        base = BaseModel()
        base_2 = BaseModel()
        self.assertLess(base.created_at, base_2.created_at)

    def test_base_updated_at_difference(self):
        """Test that the updated_at of two users are different"""
        base = BaseModel()
        base_2 = BaseModel()
        self.assertLess(base.updated_at, base_2.updated_at)

    def test_base_str_repr(self):
        base = BaseModel()
        base.id = "101010"
        date = datetime.now()
        base.created_at = base.updated_at = date
        base_str = f"[BaseModel] ({base.id}) {base.__dict__}"
        self.assertEqual(base_str, str(base))

    def test_pass_args_with_kwargs(self):
        d = {'id': '06af571e-a3de-478a-b6f0-ba0a9cffe0b0',
             'created_at': '2023-05-10T00:00:46.509762',
             'updated_at': '2023-05-10T00:00:46.509775',
             'name': 'My_First_Model', 'my_number': 89,
             '__class__': 'BaseModel'}
        base = BaseModel(98, 'Betty', [1, 2, 3], **d)
        self.assertEqual(base.id, '06af571e-a3de-478a-b6f0-ba0a9cffe0b0')
        self.assertEqual(base.created_at.isoformat(),
                         '2023-05-10T00:00:46.509762')
        self.assertEqual(base.updated_at.isoformat(),
                         '2023-05-10T00:00:46.509775')
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)

    def test_instantiation_with_dict(self):
        date = "2023-05-09T00:00:00.000000"
        d = {'id': 8998, 'updated_at': date, 'created_at': date}
        base = BaseModel(**d)
        self.assertEqual(8998, base.id)
        self.assertEqual(date, datetime.strftime(base.created_at,
                                                 "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(date, datetime.strftime(base.updated_at,
                                                 "%Y-%m-%dT%H:%M:%S.%f"))

    def test_attr_type_after_instantiation(self):
        base = BaseModel()
        self.assertEqual(type(base.id), str)
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)

    def test_public_attr(self):
        base = BaseModel()
        base.id = 98
        date = datetime.now()
        base.created_at = date
        base.updated_at = date
        self.assertEqual(base.id, 98)
        self.assertEqual(date, base.created_at)
        self.assertEqual(date, base.updated_at)


class TestBaseModel_save(unittest.TestCase):
    """Unittest to testing the public save method."""
    def test_attr_value_after_save(self):
        base = BaseModel()
        id = base.id
        created_at = base.created_at
        updated_at = base.updated_at
        base.save()
        self.assertEqual(id, base.id)
        self.assertEqual(created_at, base.created_at)
        self.assertNotEqual(updated_at, base.updated_at)


class TestBaseModel_dict(unittest.TestCase):
    """Unittest for testing the to_dict() public method."""
    def test_to_dict_method_returns(self):
        base = BaseModel()
        base.author = "samuel"
        to_dict = base.to_dict()
        self.assertIsInstance(to_dict, dict)
        self.assertEqual(to_dict.get("author"), base.author)
        self.assertEqual(to_dict["__class__"], type(base).__name__)
        self.assertIsInstance(to_dict["created_at"], str)
        self.assertIsInstance(to_dict["updated_at"], str)

    def test_same_dict_from_two_instances_with_same_attr(self):
        base1 = BaseModel()
        base1.my_school = "Alx SE Cohorts"
        base1.number = 98
        to_dict1 = base1.to_dict()
        base2 = BaseModel(**to_dict1)
        self.assertEqual(to_dict1, base2.to_dict())
        self.assertNotEqual(base1, base2)

    def test_dict_repr(self):
        date = "2023-05-09T00:59:59.123450"
        d = {'id': 8998, 'updated_at': date, 'created_at': date,
             'name': 'Betty', 'number': 98, '__class__': 'BaseModel'}
        base = BaseModel(**d)
        self.assertEqual(base.to_dict(), d)

    def test_to_dict_return_value_not_same_as_self_dict(self):
        base = BaseModel()
        d = base.to_dict()
        self.assertNotEqual(d, base.__dict__)


if __name__ == "__main__":
    unittest.main()
