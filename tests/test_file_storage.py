#!/usr/bin/python3
"""The unnittest for FileStorage"""
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class Test_Storage_Instantiation(unittest.TestCase):

    # create a setUp create and get a file for use
    @staticmethod
    def clear_file():
        file = open("file.json", "w")
        file.close()

    # check if is of FileStorage Class
    def test_check_for_instantiation(self):
        self.assertIsInstance(storage, FileStorage)

    # check instantiation with argument - should give ValueError
    def test_instance_of_filestorage_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage({"id": 12, "created_at": "2023-05-09T00:00:00.000000"})

    # check for if private attributes are private
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
