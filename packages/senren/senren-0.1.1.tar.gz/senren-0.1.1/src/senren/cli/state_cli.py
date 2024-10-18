from pathlib import Path
from typing import Optional

import grpc
import typer

from senren.cli.load_modules import load_modules, parse_user_repo
from senren.config import get_config
from senren.custom_exceptions import ConfigurationError, RegistryError
from senren.feature_store.v1 import registry_pb2, registry_pb2_grpc
from senren.logging_config import get_logger

state_app = typer.Typer()
logger = get_logger(__name__)


@state_app.command("init")
def init(example: bool = typer.Option(False, "--example", help="Initialize with example")):
    """Initialize project"""
    if example:
        typer.echo("Initializing project with example")
    else:
        typer.echo("Initializing project")
    # TODO: Implement initialization logic


@state_app.command("show")
def show():
    """Show current state"""
    logger.info("Running `senren state show`")


@state_app.command("plan")
def plan(directory: Optional[str] = typer.Argument(None)):
    """Plan changes"""
    typer.echo(f"Planning changes for directory: {directory}")
    # TODO: Implement plan logic


@state_app.command("apply")
def apply(
    repo: Path = typer.Argument(Path.cwd(), help="Path to repository directory"),
    plan: Optional[str] = typer.Option(None, "--plan", help="Path to plan file"),
):
    """Apply changes to the feature store"""
    logger.info(f"Running `senren state apply` for repo: {repo.absolute()}")

    try:
        if not repo.is_dir():
            raise ConfigurationError(f"Invalid repo path: {repo}. Must be a directory.")

        modules, errors = load_modules(repo)

        if errors:
            logger.error("Errors occurred while loading modules:")
            for error in errors:
                logger.error(error)
            raise typer.Abort()

        if not modules:
            logger.error("No modules were loaded successfully. Aborting apply operation.")
            raise typer.Abort()

        repo_spec = parse_user_repo(modules)
        repo_spec_proto = repo_spec.to_proto()
        logger.debug(f"Converted RepoSpec to protobuf: {repo_spec_proto}")

        config = get_config()
        with grpc.insecure_channel(config.REGISTRY_SERVICE_URL) as channel:
            stub = registry_pb2_grpc.RegistryServiceStub(channel=channel)
            try:
                request = registry_pb2.ApplyRequest(spec=repo_spec_proto)
                stub.Apply(request)
                logger.info("Apply operation completed successfully")
            except grpc.RpcError as rpc_error:
                logger.error(f"RPC failed: {rpc_error}")
                raise RegistryError(f"Failed to apply repository: {rpc_error}")
    except Exception as e:
        logger.error(f"An error occurred during the apply operation: {str(e)}")
        raise typer.Abort()


@state_app.command("destroy")
def destroy():
    """Destroy the current feature store configuration"""
    logger.info("Running 'senren state destroy'...")

    config = get_config()
    with grpc.insecure_channel(config.REGISTRY_SERVICE_URL) as channel:
        stub = registry_pb2_grpc.RegistryServiceStub(channel=channel)
        try:
            stub.Destroy(registry_pb2.DestroyRequest())
            logger.info("Destroy operation completed successfully")
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                logger.error(f"Destroy operation was cancelled: {rpc_error}")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logger.error(f"Registry service is unavailable: {rpc_error}")
            else:
                logger.error(f"Received unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
            raise RegistryError(f"Failed to destroy repository: {rpc_error}")


@state_app.command("rollback-to")
def rollback_to(state_id: str):
    """Rollback to a specific state"""
    typer.echo(f"Rolling back to state: {state_id}")
    # TODO: Implement rollback logic
