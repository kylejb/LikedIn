#!/usr/bin/env python

"""LikedIn."""
__author__ = "Kyle J. Burda"
__version__ = "0.1.0"
import os
import sys
import pawl

from dotenv import load_dotenv
from pawl.utils.token_manager import FileTokenManager

load_dotenv()

ACCESS_TOKEN_FILENAME = "app/tokens/access_token.txt"
API_SECRET = "LINKEDIN_API_SECRET"
API_CLIENT = "LINKEDIN_API_CLIENT_ID"


def initialize_token_manager_file():
    if os.path.isfile(ACCESS_TOKEN_FILENAME):
        return
    raise RuntimeError(
        "access_token.txt needs to be initialized. Please run setup/initial_setup.py"
    )


def initialize_linkedin_client(token_manager=None):
    _client_id = os.environ[API_CLIENT]
    _client_secret = os.environ[API_SECRET]

    return pawl.Linkedin(
        token_manager=token_manager,
        client_id=_client_id,
        client_secret=_client_secret,
        redirect_uri="http://localhost:8000",
    )


def main():
    initialize_linkedin_client(token_manager=FileTokenManager(ACCESS_TOKEN_FILENAME))
    # TODO: Iteratively like last 5-10 posts on page


if __name__ == "__main__":
    sys.exit(main())
