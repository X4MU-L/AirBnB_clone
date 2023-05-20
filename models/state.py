#!/usr/bin/python3
"""Defines State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a State object.

    Attributes:
        name (str): The name of the state.
    """

    name = ""
