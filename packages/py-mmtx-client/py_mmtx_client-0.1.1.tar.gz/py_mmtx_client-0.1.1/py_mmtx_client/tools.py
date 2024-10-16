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


def grant_access_to_path_for_user(
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
        Permission(action="read", path="test"),
        Permission(action="playback", path="test"),
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


def add_stream_path_for_user(
    path_name: str, source: str, user_name: str, password: str
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
    if not add_path_to_config(path_name, source):
        logger.error("Failed to add path to config")
        return None
    
    ok = grant_access_to_path_for_user(path_name, user_name, password)
    if not ok:
        logger.error("Failed to grant access to path for user")
        return None
    
    # parse the URL and return all except the path
    u = parse_url(config.MMTX_API_URL)
    return f"{u.s}/stream/{path_name}"
