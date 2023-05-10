#!/usr/bin/env python3
"""Thisis the BaseModel Module"""

import models
import re
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """This is the BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Instantiates a BaseModel object."""
        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    if k == "created_at" or k == "updated_at":
                        v = datetime.fromisoformat(v)
                    setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Prints a string representaion of BaseModel"""
        return ("[{}] ({}) {}".format(type(self).__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Updates the time of of the updated_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of BaseModel instance"""
        inst_dict = self.__dict__
        inst_dict = {
            key: value.isoformat() if re.search('.*_at', key) else value
            for key, value in inst_dict.items()
        }
        inst_dict["__class__"] = type(self).__name__
        return (inst_dict)
