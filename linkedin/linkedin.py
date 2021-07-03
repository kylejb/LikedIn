"""Provide the Linkedin class."""
from .api import Auth


class Linkedin:
    """The Linkedin class provides convenient access to Linkedin's API."""

    def __init__(self):
        self.auth = Auth()
