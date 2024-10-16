"""Models for the path API of the MediaMTX server."""

# pylint: disable=missing-class-docstring # noqa

from typing import List

from pydantic import BaseModel

from py_mmtx_client.models.base_models import ListModel


class Source(BaseModel):
    type: str
    id: str


class Reader(BaseModel):
    type: str
    id: str


class Path(BaseModel):
    name: str
    confName: str
    source: Source
    ready: bool
    readyTime: str
    tracks: List[str]
    bytesReceived: int
    bytesSent: int
    readers: List[Reader]


class PathList(ListModel):
    items: List[Path]
