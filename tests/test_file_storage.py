#!/usr/bin/python3
"""Unittest for testing the functionality of the FileStorage class"""

import unittest
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestStorage_Instantiation(unittest.TestCase):
    """Unittests for testing the instantiation of a Storage object."""

    @staticmethod
    def clear_file():
        file = open("file.json", "w")
        file.close()

    def test_check_for_instantiation(self):
        self.assertIsInstance(storage, FileStorage)

    def test_instance_of_filestorage_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_for_private_value(self):
        with self.assertRaises(AttributeError):
            FileStorage.__objects

    def test_all_method_returns(self):
        all_len = len(storage.all())
        base = BaseModel()
        to_dict = base.to_dict()
        new_base = BaseModel(**to_dict)
        all_new = storage.all()
        self.assertEqual(len(storage.all()), all_len + 1)
        self.assertEqual(base,
                         all_new[f"{type(new_base).__name__}.{new_base.id}"])
        self.assertIsInstance(
            all_new[f"{type(new_base).__name__}.{new_base.id}"], BaseModel)
        self.assertIs(base,
                      all_new[f"{type(new_base).__name__}.{new_base.id}"])
        self.assertIsNot(base, new_base)


if __name__ == "__main__":
    unittest.main()
