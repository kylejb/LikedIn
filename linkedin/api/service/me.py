"""Provide `/me` service class."""
from .base import ServiceBase
from ..constants import API_PATH
from ..utils import enum, raise_for_error, to_utf8  # noqa


class Me(ServiceBase):
    """Me is a Service class that represents the `/me` endpoint."""

    def get_basic_profile(self):
        response = self.make_request("GET", API_PATH["me"])
        raise_for_error(response)
        return response.json()
