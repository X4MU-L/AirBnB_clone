#!/usr/bin/env python3
"""Thisis the BaseModel Module"""

import re
import uuid
from datetime import datetime


class BaseModel:
    """This is the BaseModel class"""

    def __init__(self):
        """Instantiates a BaseModel object."""
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                elif k == "created_at":
                    self.created_at = datetime.fromisoformat(v)
                elif k == "updated_at":
                    self.updated_at = datetime.fromisoformat(v)
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Prints a string representaion of BaseModel"""
        return ("[{}] ({}) {}".format(type(self).__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Updates the time of of the updated_at"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary representation of BaseModel instance"""
        inst_dict = self.__dict__
        inst_dict = {
            key: value.isoformat() if re.search('.*_at', key) else value
            for key, value in inst_dict.items()
        }
        inst_dict["__class__"] = type(self).__name__
        return (inst_dict)
