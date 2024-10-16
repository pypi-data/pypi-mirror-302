"""
API client for the path(s) API.
"""

from loguru import logger
from py_mmtx_client.client.api_base import ApiClient, join_url_parts
from py_mmtx_client.models.path_models import Path, PathList


class PathApiClient(ApiClient):
    """Path API client"""

    def __init__(self, api_base_url: str, api_user: str, api_password: str):
        super().__init__(join_url_parts(api_base_url, "paths"), api_user, api_password)

    def get_all_paths(self):
        """"""
        url = join_url_parts(self.api_base_url, "list")
        logger.trace(f"Fetching paths: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched paths")
            return PathList(**res.json())
        else:
            logger.error(f"Error getting config: {res.text}")

    def get_path_by_name(self, name: str):
        url = join_url_parts(self.api_base_url, "get", name)
        logger.trace(f"Fetching path for {name}: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched path")
            return Path(**res.json())
        else:
            logger.error(f"Error getting config: {res.text}")
