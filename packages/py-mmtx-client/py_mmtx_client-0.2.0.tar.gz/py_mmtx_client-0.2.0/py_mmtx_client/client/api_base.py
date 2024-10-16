"""
Description: Base class for API clients. Handles authentication and provides a session object.
"""

import requests


class ApiClient:
    """Base class for API clients. Handles authentication and provides a session object."""

    def __init__(self, api_base_url: str, api_user: str, api_password: str):
        self.api_base_url = api_base_url
        self.api_user = api_user
        self.api_password = api_password
        self.session = requests.Session()
        self.session.auth = (api_user, api_password)


def join_url_parts(*args: tuple[str, ...]) -> str:
    """Join parts of a URL with a slash; strips leading/trailing slashes from parts

    Returns:
        str: Joined URL
    """
    # Join parts of a URL with a slash; strips leading/trailing slashes from parts
    return "/".join([str(arg).strip("/") for arg in args])
