import asyncio
import logging
import os
import platform
import ssl

import os.path
import stat
import sys
import certifi
from collections.abc import Coroutine
from typing import Any

import click
from exponent.core.remote_execution.git import get_git_info
import httpx
from dotenv import load_dotenv

from exponent.commands.utils import ConnectionTracker
from exponent.core.config import (
    Settings,
    get_settings,
)
from exponent.core.remote_execution.client import RemoteExecutionClient
from exponent.core.remote_execution.exceptions import ExponentError
from exponent.core.remote_execution.types import UseToolsConfig

load_dotenv()


def set_log_level() -> None:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level), stream=sys.stdout)


def redirect_to_login(settings: Settings, cause: str = "detected") -> None:
    if inside_ssh_session():
        click.echo(f"No API Key {cause}, run 'exponent login --key <API-KEY>'")
    else:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/cli")


def inside_ssh_session() -> bool:
    return (os.environ.get("SSH_TTY") or os.environ.get("SSH_TTY")) is not None


def inside_git_repo() -> bool:
    git_info = get_git_info(os.getcwd())

    return git_info is not None


def missing_ssl_certs() -> bool:
    if platform.system().lower() != "darwin":
        return False

    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile
    )

    return not os.path.exists(os.path.join(openssl_dir, openssl_cafile))


def install_ssl_certs() -> None:
    STAT_0o775 = (
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )

    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile
    )

    cwd = os.getcwd()
    # change working directory to the default SSL directory
    os.chdir(openssl_dir)
    relpath_to_certifi_cafile = os.path.relpath(certifi.where())

    try:
        os.remove(openssl_cafile)
    except FileNotFoundError:
        pass

    click.echo(" -- creating symlink to certifi certificate bundle")
    os.symlink(relpath_to_certifi_cafile, openssl_cafile)
    click.echo(" -- setting permissions")
    os.chmod(openssl_cafile, STAT_0o775)
    click.echo(" -- update complete")
    os.chdir(cwd)


def check_ssl() -> None:
    if missing_ssl_certs():
        click.confirm(
            "Missing root SSL certs required for python to make HTTP requests, "
            "install certifi certificates now?",
            abort=True,
            default=True,
        )

        install_ssl_certs()


def check_inside_git_repo() -> None:
    if not inside_git_repo():
        click.confirm(
            f"No git repository detected in {os.getcwd()}, make sure to run "
            "exponent from the root of your project. Continue?",
            abort=True,
            default=True,
        )


def run_until_complete(coro: Coroutine[Any, Any, Any]) -> Any:
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass
    except ExponentError as e:
        click.secho(f"Encountered error: {e}", fg="red")
        click.secho(
            "The Exponent team has been notified, "
            "please try again and reach out if the problem persists.",
            fg="yellow",
        )
        sys.exit(1)


async def benchmark_mode_exit(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        await asyncio.sleep(5)
        if await client.check_remote_end_event(chat_uuid):
            sys.exit(0)


async def run_client_connection(
    client: RemoteExecutionClient,
    chat_uuid: str,
    connection_tracker: ConnectionTracker | None = None,
) -> None:
    await client.run_connection(chat_uuid, connection_tracker)


async def start_chat(
    client: RemoteExecutionClient,
    chat_uuid: str,
    prompt: str,
    use_tools_config: UseToolsConfig,
) -> None:
    click.secho("Starting chat...")
    await client.start_chat(chat_uuid, prompt, use_tools_config=use_tools_config)
    click.secho("Chat started. Open the link to join the chat.")


async def start_client(
    api_key: str,
    base_api_url: str,
    chat_uuid: str,
    prompt: str | None = None,
    benchmark: bool = False,
    connection_tracker: ConnectionTracker | None = None,
) -> None:
    if benchmark is True and prompt is None:
        click.secho("Error: Benchmark mode requires a prompt.", fg="red")
        return

    current_working_directory = os.getcwd()

    use_tools_config = UseToolsConfig()
    async with RemoteExecutionClient.session(
        api_key, base_api_url, current_working_directory
    ) as client:
        if benchmark:
            assert prompt is not None
            await asyncio.gather(
                start_chat(
                    client, chat_uuid, prompt, use_tools_config=use_tools_config
                ),
                run_client_connection(client, chat_uuid, connection_tracker),
                benchmark_mode_exit(client, chat_uuid),
            )
        elif prompt:
            await asyncio.gather(
                start_chat(
                    client, chat_uuid, prompt, use_tools_config=use_tools_config
                ),
                run_client_connection(client, chat_uuid, connection_tracker),
            )
        else:
            await run_client_connection(client, chat_uuid, connection_tracker)


# Helper functions
async def create_chat(api_key: str, base_api_url: str) -> str | None:
    try:
        async with RemoteExecutionClient.session(
            api_key, base_api_url, os.getcwd()
        ) as client:
            chat = await client.create_chat()
            return chat.chat_uuid
    except (httpx.ConnectError, ExponentError) as e:
        click.secho(f"Error: {e}", fg="red")
        return None
