"""
API client for the config API.
"""

from loguru import logger
from py_mmtx_client.client.api_base import ApiClient, join_url_parts
from py_mmtx_client.models.config_models import (
    GlobalConfig,
    OptionalGlobalConfig,
    OptionalPathConfig,
    PathConfig,
    PathConfigList,
)


class ConfigApiClient(ApiClient):
    """Config API client"""

    def __init__(self, api_base_url: str, api_user: str, api_password: str):
        super().__init__(join_url_parts(api_base_url, "config"), api_user, api_password)

    def get_global_config(self) -> GlobalConfig:
        """Get the global config"""
        url = join_url_parts(self.api_base_url, "global", "get")
        logger.trace(f"Fetching config: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched config")
            return GlobalConfig(**res.json())
        else:
            logger.error(f"Error getting config: {res.text}")

    def patch_global_config(self, global_config: OptionalGlobalConfig) -> bool:
        """
        Patch the global config;
        only the fields that are set in the OptionalGlobalConfig object will be patched
        """
        url = join_url_parts(self.api_base_url, "global", "patch")
        logger.trace(f"Patching config: {url}")
        res = self.session.patch(url, json=global_config.model_dump())
        if res.ok:
            logger.debug("successfully patched config")
            return True
        else:
            logger.error(f"Error patching config: {res.text}")
            return False

    def get_default_path_config(self) -> PathConfig:
        """Get the default path config"""
        url = join_url_parts(self.api_base_url, "pathdefaults", "get")
        logger.trace(f"Fetching default path config: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched default path config")
            return PathConfig(**res.json())
        else:
            logger.error(f"Error getting default path config: {res.text}")

    def get_all_path_configs(self) -> PathConfigList:
        """Get all path configs"""
        url = join_url_parts(self.api_base_url, "paths", "list")
        logger.trace(f"Fetching all path configs: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug("successfully fetched all path configs")
            return PathConfigList(**res.json())
        else:
            logger.error(f"Error getting all path configs: {res.text}")

    def get_path_config_by_name(self, name: str) -> PathConfig:
        """Get a path config by name"""
        url = join_url_parts(self.api_base_url, "paths", "get", name)
        logger.trace(f"Fetching path config for {name}: {url}")
        res = self.session.get(url)
        if res.ok:
            logger.debug(f"successfully fetched path config for {name}")
            return PathConfig(**res.json())
        else:
            logger.error(f"Error getting path config for {name}: {res.text}")

    def add_path_config(self, path_config: PathConfig) -> bool:
        """Add a path config; name is mandatory"""
        if not path_config.name:
            logger.error("Path config name is mandatory")
            return False
        url = join_url_parts(self.api_base_url, "paths", "add", path_config.name)
        logger.debug(f"Adding path config for {path_config.name}: {url}")
        res = self.session.post(url, json=path_config.model_dump())
        if res.ok:
            logger.debug(f"successfully added path config for {path_config.name}")
            return True
        else:
            logger.error(f"Error adding path config for {path_config.name}: {res.text}")
            return False

    def patch_path_config(self, path_config: OptionalPathConfig) -> bool:
        """Patch a path config; name is mandatory"""
        if not path_config.name:
            logger.error("Path config name is mandatory")
            return False
        url = join_url_parts(self.api_base_url, "paths", "patch", path_config.name)
        logger.trace(f"Patching path config for {path_config.name}: {url}")
        res = self.session.patch(url, json=path_config.model_dump())
        if res.ok:
            logger.debug(f"successfully patched path config for {path_config.name}")
            return True
        else:
            logger.error(
                f"Error patched path config for {path_config.name}: {res.text}"
            )
            return False

    def replace_path_config(self, path_config: PathConfig) -> bool:
        """Replace a path config; name is mandatory"""
        if not path_config.name:
            logger.error("Path config name is mandatory")
            return False
        url = join_url_parts(self.api_base_url, "paths", "replace", path_config.name)
        logger.trace(f"Replacing path config for {path_config.name}")
        res = self.session.put(url, json=path_config.model_dump())
        if res.ok:
            logger.debug(f"successfully replaced path config for {path_config.name}")
            return True
        else:
            logger.error(
                f"Error replacing path config for {path_config.name}: {res.text}"
            )
            return False

    def delete_path_config(self, name: str) -> bool:
        """Delete a path config by name"""
        url = join_url_parts(self.api_base_url, "paths", "delete", name)
        logger.trace(f"Deleting path config for {name}: {url}")
        res = self.session.delete(url)
        if res.ok:
            logger.debug(f"successfully deleted path config for {name}")
            return True
        else:
            logger.error(f"Error deleting path config for {name}: {res.text}")
            return False
