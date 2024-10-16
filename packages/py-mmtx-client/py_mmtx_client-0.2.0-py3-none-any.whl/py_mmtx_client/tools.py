from typing import Literal, Tuple
from loguru import logger
from urllib3.util import parse_url
from py_mmtx_client import config
from py_mmtx_client.client.api_config_client import ConfigApiClient
from py_mmtx_client.models.config_models import AuthInternalUser, PathConfig, Permission


def _get_config_api_singleton() -> ConfigApiClient:
    if not hasattr(_get_config_api_singleton, "api"):
        _get_config_api_singleton.api = ConfigApiClient(
            config.MMTX_API_URL, config.MMTX_USER, config.MMTX_PASS
        )
    return _get_config_api_singleton.api


def add_path_to_config(path_name: str, source: str) -> bool:
    """Adds a path using the provided name and source to the MediaMTX server.

    Args:
        path_name (str): The name of the path to add
        source (str): Source URL to use when creating the path

    Returns:
        bool: True if the path was added successfully, False otherwise
    """
    assert path_name, "path_name is required"
    assert source, "source is required"
    # only letters and numbers are allowed in path names
    assert path_name.isalnum(), "path_name can only contain letters and numbers"

    new_path_config = PathConfig(name=path_name, source=source)
    return _get_config_api_singleton().add_path_config(new_path_config)


def remove_path_from_config(path_name: str) -> bool:
    """Removes the path with the given name from the MediaMTX server.

    Args:
        path_name (str): The name of the path to remove

    Returns:
        bool: True if the path was removed successfully, False otherwise
    """
    assert path_name, "path_name is required"
    # only letters and numbers are allowed in path names
    assert path_name.isalnum(), "path_name can only contain letters and numbers"

    return _get_config_api_singleton().delete_path_config(path_name)


def _revoke_access_to_path_for_user(path_name: str, user_name: str) -> bool:
    """Revokes access to the given user to the path with the given name."""
    assert path_name, "path_name is required"
    assert user_name, "user_name is required"
    # only letters and numbers are allowed in path names
    assert path_name.isalnum(), "path_name can only contain letters and numbers"
    api = _get_config_api_singleton()
    conf = api.get_global_config()
    for user in conf.authInternalUsers:
        if user.user == user_name:
            for permission in user.permissions:
                if permission.path == path_name:
                    user.permissions.remove(permission)
    return api.patch_global_config(conf)


def _grant_access_to_path_for_user(
    path_name: str, user_name: str, password: str
) -> bool:
    """Grants access to the given user to the path with the given name.

    Args:
        path_name (str): The name of the path to grant access to
        user_name (str): The name of the user to give access to the path to
        password (str): The password of the user to give access to the path to

    Returns:
        bool: True if the user was granted access to the path successfully, False otherwise
    """
    assert path_name, "path_name is required"
    assert user_name, "user_name is required"
    assert password, "password is required"
    # only letters and numbers are allowed in path names
    assert path_name.isalnum(), "path_name can only contain letters and numbers"

    api = _get_config_api_singleton()
    conf = api.get_global_config()
    permissions = [
        Permission(action="read", path=path_name),
        Permission(action="playback", path=path_name),
    ]
    new_auth_user = AuthInternalUser(
        **{
            "user": user_name,
            "pass": password,
            "ips": [],
            "permissions": permissions,
        }
    )
    logger.info(f"Adding user {user_name} to path {path_name}")
    conf.authInternalUsers.append(new_auth_user)
    return api.patch_global_config(conf)


def _get_port_from_address(address: str) -> int:
    """Extracts the port number from the given address.
    Address might be in the form of "host:port or :port".

    Args:
        address (str): host:port

    Returns:
        int: The port number extracted from the address. If no port is found, raise an exception.
    """
    if ":" in address:
        return int(address.rsplit(":", maxsplit=1)[1])
    raise ValueError("No port found in address")


def _get_scheme_and_port_for_stream_type(
    stream_type: Literal["rtsp", "rtmp", "hls", "webrtc", "srt"] = "hls"
) -> Tuple[str, int]:
    config = _get_config_api_singleton().get_global_config()
    if stream_type == "rtsp":
        if not config.rtsp:
            raise ValueError("RTSP is not enabled in the config")
        if config.encryption == "strict":
            return "rtsps", _get_port_from_address(config.rtspsAddress)
        return "rtsp", _get_port_from_address(config.rtspAddress)
    elif stream_type == "rtmp":
        if not config.rtmp:
            raise ValueError("RTMP is not enabled in the config")
        if config.rtmpEncryption == "strict":
            return "rtmps", _get_port_from_address(config.rtmpsAddress)
        return "rtmp", _get_port_from_address(config.rtmpAddress)
    elif stream_type == "hls":
        if not config.hls:
            raise ValueError("HLS is not enabled in the config")
        if config.hlsEncryption:
            return "https", _get_port_from_address(config.hlsAddress)
        return "http", _get_port_from_address(config.hlsAddress)
    elif stream_type == "webrtc":
        if not config.webrtc:
            raise ValueError("WebRTC is not enabled in the config")
        if config.webrtcEncryption:
            return "https", _get_port_from_address(config.webrtcAddress)
        return "http", _get_port_from_address(config.webrtcAddress)
    elif stream_type == "srt":
        if not config.srt:
            raise ValueError("SRT is not enabled in the config")
        return "srt", _get_port_from_address(config.srtAddress)
    else:
        raise ValueError(f"Invalid stream type: {stream_type}")


def add_stream_path_for_user(
    path_name: str,
    source: str,
    user_name: str,
    password: str,
    stream_type: Literal["rtsp", "rtmp", "hls", "webrtc", "srt"] = "hls",
) -> str | None:
    """Adds a stream path to media MTX and allows access to this path to the given user.

    Args:
        path_name (str): The name of the path to add
        source (str): Source URL to use when creating the path
        user_name (str): The name of the user to give access to the path to
        password (str): The password of the user to give access to the path to

    Returns:
        str | None: returns the URL for the path; but without scheme if successful, None otherwise
    """
    assert path_name, "path_name is required"
    assert source, "source is required"
    assert user_name, "user_name is required"
    assert password, "password is required"
    # only letters and numbers are allowed in path names
    assert path_name.isalnum(), "path_name can only contain letters and numbers"
    path_config = _get_config_api_singleton().get_path_config_by_name(path_name)
    if not path_config:
        if not add_path_to_config(path_name, source):
            logger.error("Failed to add path to config")
            return None

        ok = _grant_access_to_path_for_user(path_name, user_name, password)
        if not ok:
            logger.error("Failed to grant access to path for user")
            return None
    else:
        logger.info(f"Path {path_name} already exists; skipping path creation!")
    # parse the URL and return all except the path
    u = parse_url(config.MMTX_API_URL)
    scheme, port = _get_scheme_and_port_for_stream_type(stream_type)
    return f"{scheme}://{u.host}:{port}/{path_name}"


def remove_path_for_user(path_name: str, user_name: str) -> bool:
    """Removes the path with the given name and revokes access to the given user.

    Args:
        path_name (str): _description_
        user_name (str): _description_

    Returns:
        bool: True if the path was removed successfully, False otherwise
    """
    assert path_name, "path_name is required"
    assert user_name, "user_name is required"
    revoked = _revoke_access_to_path_for_user(path_name, user_name)
    if not revoked:
        logger.warning("Failed to revoke access to path for user")
    removed = remove_path_from_config(path_name)
    if not removed:
        logger.warning("Failed to remove path from config")
    return revoked and removed

def list_paths_and_user_permissions():
    """List all paths and their associated user permissions."""
    conf = _get_config_api_singleton().get_global_config()
    paths = _get_config_api_singleton().get_all_path_configs()
    for path in paths.items:
        logger.info(f"Path: {path.name}")
        for user in conf.authInternalUsers:
            logger.info(user)
            for perm in user.permissions:
                if perm.path == path.name:
                    logger.info(f"User: {user.user}, Permissions: {perm.action}")
        logger.info("----")
    return True