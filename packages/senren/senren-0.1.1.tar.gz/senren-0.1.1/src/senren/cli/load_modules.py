import importlib
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Tuple

from senren.custom_exceptions import ConfigurationError
from senren.data_source import DataSource
from senren.entity import Entity
from senren.feature_service import FeatureService
from senren.feature_view import FeatureView
from senren.logging_config import get_logger
from senren.online_store import OnlineStore
from senren.repo import RepoSpec

logger = get_logger(__name__)


def load_modules(directory: Path) -> Tuple[Dict[str, Any], List[str]]:
    """
    Load Python modules from the specified directory.

    Args:
        directory (Path): The directory containing the modules to load.

    Returns:
        Tuple[Dict[str, Any], List[str]]: A tuple containing a dictionary of loaded modules
        and a list of error messages.

    Raises:
        ConfigurationError: If there's an issue with the directory configuration.
    """
    modules = {}
    errors = []

    logger.debug(f"Starting to load modules from directory: {directory}")

    if not directory.exists() or not directory.is_dir():
        error_msg = f"The specified directory does not exist or is not a directory: {directory}"
        logger.error(error_msg)
        raise ConfigurationError(error_msg)

    for file in directory.rglob("*.py"):
        if file.name.startswith("__"):
            continue
        module_name = f"{directory.name}.{file.relative_to(directory).with_suffix('').as_posix().replace('/', '.')}"

        logger.debug(f"Attempting to load module: {module_name}")

        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            if spec is None or spec.loader is None:
                error_msg = f"Failed to create spec for module: {module_name}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue

            module = importlib.util.module_from_spec(spec)
            logger.debug(f"Created module object for: {module_name}")

            try:
                logger.debug(f"Executing module: {module_name}")
                spec.loader.exec_module(module)
                logger.debug(f"Successfully executed module: {module_name}")
            except RecursionError as re:
                error_msg = f"RecursionError in module {module_name}: {str(re)}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
                continue
            except Exception as e:
                error_msg = f"Error executing module {module_name}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
                continue

            modules[module_name] = module
            logger.debug(f"Successfully loaded and executed module: {module_name}")

        except Exception as e:
            error_msg = f"Unexpected error loading module {module_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            errors.append(error_msg)

    logger.debug(f"Finished loading modules. Total loaded: {len(modules)}, Total errors: {len(errors)}")

    return modules, errors


def parse_user_repo(modules: Dict[str, Any]) -> RepoSpec:
    """
    Parse the user repository from loaded modules.

    Args:
        modules (Dict[str, Any]): Dictionary of loaded modules.

    Returns:
        RepoSpec: The parsed repository specification.
    """
    entities = {}
    data_sources = {}
    feature_views = {}
    feature_services = {}
    online_stores = {}

    logger.info("Parsing user repository")
    for module_name, module in modules.items():
        logger.debug(f"Parsing module: {module_name}")
        for name, obj in module.__dict__.items():
            if isinstance(obj, Entity):
                entities[f"{obj.metadata.namespace}::{obj.metadata.name}"] = obj
                logger.debug(f"Found Entity: {obj.metadata.name}")
            elif isinstance(obj, DataSource):
                key = f"{obj.metadata.namespace}::{obj.metadata.name}"
                data_sources[key] = obj
                logger.debug(f"Found DataSource: {key}")
            elif isinstance(obj, FeatureView):
                key = f"{obj.metadata.namespace}::{obj.metadata.name}"
                feature_views[key] = obj
                logger.debug(f"Found FeatureView: {key}")
            elif isinstance(obj, FeatureService):
                key = f"{obj.metadata.namespace}::{obj.metadata.name}"
                feature_services[key] = obj
                logger.debug(f"Found FeatureService: {key}")
            elif isinstance(obj, OnlineStore):
                online_stores[obj.metadata.name] = obj
                logger.debug(f"Found OnlineStore: {obj.metadata.name}")

    user_repo = RepoSpec(
        entities=entities,
        data_sources=data_sources,
        feature_views=feature_views,
        feature_services=feature_services,
        online_stores=online_stores,
    )

    logger.info(
        f"Parsed user repository: "
        f"{len(entities)} entities, "
        f"{len(data_sources)} data sources, "
        f"{len(feature_views)} feature views, "
        f"{len(feature_services)} feature services, "
        f"{len(online_stores)} online stores"
    )

    return user_repo
