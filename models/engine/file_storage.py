#!/usr/bin/python3
"""Defines a FileStorage Class."""

import json
from models.base_model import BaseModel
from json.decoder import JSONDecodeError


class FileStorage:
    """Represents a FileStorage object/instance."""
    __objects = {}
    __file_path = "file.json"

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj as value with key as <obj class name>.id
           Args:
                obj (any): The object to be added to the dictionary.
        """
        k = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[k] = obj

    def save(self):
        """Serializes __objects to the JSON file <__file_path>."""
        o_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(o_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path) as f:
                try:
                    o_dict = json.load(f)
                    for v in o_dict.values():
                        cls_name = v["__class__"]
                        self.new(eval(cls_name)(**v))
                except JSONDecodeError:
                    pass
        except FileNotFoundError:
            return
