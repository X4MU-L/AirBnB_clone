#!/usr/bin/python3
"""Defines the Review class."""

from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a Review object.

    Attributes:
        place_id (str): The place id.
        user_id (str): The user id.
        text (str): The review text.
    """

    place_id = ""
    user_id = ""
    text = ""
