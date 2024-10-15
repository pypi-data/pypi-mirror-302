"""Models for the HLS muxer API of the MediaMTX server."""

# pylint: disable=missing-class-docstring # noqa


from typing import List

from pydantic import BaseModel

from py_mmtx_client.models.base_models import ListModel


class HlsMuxer(BaseModel):
    path: str
    created: str
    lastRequest: str
    bytesSent: int


class HlsMuxerList(ListModel):
    items: List[HlsMuxer]
