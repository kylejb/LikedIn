"""Linkedin API Wrapper."""
__version__ = "0.1.0"

import collections
import contextlib
import hashlib
import random
import requests

from io import StringIO
from .utils import enum, raise_for_error, to_utf8
from urllib.parse import quote

__all__ = ["LinkedinAuthentication", "LinkedinAPI", "PERMISSIONS"]

PERMISSIONS = enum(
    "Permission",
    BASIC_PROFILE="r_liteprofile",
    EMAIL_ADDRESS="r_emailaddress",
    MEMBER_SOCIAL="w_membersocial",
)

ENDPOINTS = enum(
    "LinkedInURL",
    ME="https://api.linkedin.com/v2/me",
    REACTIONS="https://api.linkedin.com/v2/reactions?actor=",
)


class LinkedinSelector(object):
    @classmethod
    def parse(cls, selector):
        with contextlib.closing(StringIO()) as result:
            if type(selector) == dict:
                for k, v in selector.items():
                    result.write("%s:(%s)" % (to_utf8(k), cls.parse(v)))
            elif type(selector) in (list, tuple):
                result.write(",".join(map(cls.parse, selector)))
            else:
                result.write(to_utf8(selector))
            return result.getvalue()


class LinkedinAPI:
    def __init__(self, authentication=None, token=None):
        assert (
            authentication or token
        ), "Either authentication instance or access token is required"
        self.authentication = authentication
        if not self.authentication:
            self.authentication = LinkedinAuthentication("", "", "")
            self.authentication.token = AccessToken(token, None)

    def make_request(
        self, method, url, data=None, params=None, headers=None, timeout=60
    ):
        if headers is None:
            headers = {
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authentication.token.access_token}",
            }
        else:
            headers.update(
                {
                    "X-Restli-Protocol-Version": "2.0.0",
                    "Content-Type": "application/json",
                }
            )
        kw = {"data": data, "params": params, "headers": headers, "timeout": timeout}
        return requests.request(method.upper(), url, **kw)

    def get_basic_profile(self):
        response = self.make_request("GET", ENDPOINTS.ME)
        raise_for_error(response)
        return response.json()


AccessToken = collections.namedtuple("AccessToken", ["access_token", "expires_in"])


class LinkedinAuthentication:
    """Implement a standard OAuth 2.0 flow."""

    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

    def __init__(self, key, secret, redirect_uri, permissions=None):
        self.key = key
        self.secret = secret
        self.redirect_uri = redirect_uri
        self.permissions = permissions or []
        self.state = None
        self.authorization_code = None
        self.token = None
        self._error = None

    @property
    def authorization_url(self):
        qd = {
            "response_type": "code",
            "client_id": self.key,
            "scope": (" ".join(self.permissions)).strip(),
            "state": self.state or self._make_new_state(),
            "redirect_uri": self.redirect_uri,
        }

        qsl = ["%s=%s" % (quote(k), quote(v)) for k, v in qd.items()]
        return "%s?%s" % (self.AUTHORIZATION_URL, "&".join(qsl))

    @property
    def last_error(self):
        return self._error

    def _make_new_state(self):
        return hashlib.md5(
            "{}{}".format(random.randrange(0, 2 ** 63), self.secret).encode("utf8")
        ).hexdigest()

    def get_access_token(self, timeout=60):
        assert self.authorization_code, "You must first get the authorization code"
        qd = {
            "grant_type": "authorization_code",
            "code": self.authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.key,
            "client_secret": self.secret,
        }
        response = requests.post(self.ACCESS_TOKEN_URL, data=qd, timeout=timeout)
        raise_for_error(response)
        response = response.json()
        self.token = AccessToken(response["access_token"], response["expires_in"])
        return self.token
