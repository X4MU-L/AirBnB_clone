#!/usr/bin/env python3
"""Unittest for testing the BaseModel class."""

import unittest
from datetime import datetime
from models.base_model import BaseModel


class Test_Instantiation(unittest.TestCase):
    """Unittest for testing the functionalities of the Basemodel class."""
    def test_instantiation_without_arg(self):
        base = BaseModel()
        self.assertEqual(type(base).__name__, "BaseModel")

    def test_instantiation_with_one_str_arg(self):
        with self.assertRaises(TypeError):
            BaseModel("arg1")

    def test_instantiation_with_more_than_one_arg_of_diffferent_type(self):
        with self.assertRaises(TypeError):
            BaseModel(89, "arg2", [98, "Betty"], (1, 2, 3))

    def test_attr_type_after_instantiation(self):
        base = BaseModel()
        self.assertEqual(type(base.id), str)
        self.assertEqual(type(base.created_at).__name__,
                         type(datetime.now()).__name__)
        self.assertEqual(type(base.updated_at).__name__,
                         type(datetime.now()).__name__)

    def test_public_attr(self):
        base = BaseModel()
        base.id = 98
        date = "2023-05-09T00:00:00.00000"
        base.created_at = date
        base.updated_at = date
        self.assertEqual(base.id, 98)
        self.assertEqual(date, base.created_at)
        self.assertEqual(date, base.updated_at)


class Test_String_Rep(unittest.TestCase):
    """Unittest for testing the string representation of a BaseModel object."""

    def test_str(self):
        base = BaseModel()
        result = "[{}] ({}) {}".format(type(base).__name__,
                                       base.id, base.__dict__)
        self.assertEqual(result, str(base))


class Test_Save(unittest.TestCase):
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


class Test_Dict_Rep(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
