"""
API client for the HLS muxers API.
"""

from loguru import logger
from py_mmtx_client.client.api_base import ApiClient, join_url_parts
from py_mmtx_client.models.hls_models import HlsMuxer, HlsMuxerList


class HlsApiClient(ApiClient):
    """HLS muxer API client"""

    def __init__(self, api_base_url: str, api_user: str, api_password: str):
        super().__init__(
            join_url_parts(api_base_url, "hlsmuxers"), api_user, api_password
        )

    def get_all_hls_muxers(self):
        """Get all HLS muxers"""
        url = join_url_parts(self.api_base_url, "list")
        logger.trace(f"Fetching hls muxer: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched hls muxers")
            return HlsMuxerList(**res.json())
        else:
            logger.error(f"Error getting config: {res.text}")

    def get_hls_muxer_by_name(self, name: str):
        """Get an HLS muxer by name"""
        url = join_url_parts(self.api_base_url, "get", name)
        logger.trace(f"Fetching hls muxer for {name}: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched hls muxer")
            return HlsMuxer(**res.json())
        else:
            logger.error(f"Error getting config: {res.text}")
