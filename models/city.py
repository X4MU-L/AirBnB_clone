#!/usr/bin/python3
"""Represents a City class."""

from models.base_model import BaseModel


class City(BaseModel):
    """Represents a City object.

    Attributes:
        state_id (str): The state identity of the city.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""
