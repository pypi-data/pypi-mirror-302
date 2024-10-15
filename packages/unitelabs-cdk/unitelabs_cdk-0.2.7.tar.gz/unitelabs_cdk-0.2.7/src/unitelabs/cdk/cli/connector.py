import importlib
import importlib.machinery
import importlib.metadata
import importlib.util
import logging
import os
import pathlib

import click
import dotenv

from unitelabs.cdk import AppFactory, compose_app, utils


class TLSConfigurationError(Exception):
    pass


@click.group()
def connector() -> None:
    """Base cli"""

    dotenv.load_dotenv()


@connector.command()
@click.option(
    "--app",
    type=str,
    metavar="IMPORT",
    default=utils.find_factory,
    help="The application factory function to load, in the form 'module:name'.",
)
@click.option(
    "--tls/--no-tls",
    required=False,
    default=None,
    envvar="SILA_SERVER__TLS",
    help="Use TLS encryption. Alone, this will assume cert and key exist in `certificate.generate` default location.",
)
@click.option(
    "-C",
    "--cert",
    required=False,
    envvar="SILA_SERVER__CERT",
    default=None,
    help="The path to the certificate chain file, overriding .env setting of `SILA_SERVER__CERT`, default: ./cert.pem",
)
@click.option(
    "-K",
    "--key",
    required=False,
    envvar="SILA_SERVER__KEY",
    default=None,
    help="The path to the private key file, overriding .env setting of `SILA_SERVER__KEY`, default: ./key.pem",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase the verbosity of to debug.",
)
@utils.coroutine
async def start(app, tls, cert, key, verbose: int):
    """Application Entrypoint."""
    if tls is not None:
        os.environ["SILA_SERVER__TLS"] = str(tls)

    if tls:
        cert = pathlib.Path(cert) if cert else pathlib.Path("./cert.pem")
        key = pathlib.Path(key) if key else pathlib.Path("./key.pem")
        cert = cert.resolve()
        key = key.resolve()

        msg = ""
        if not cert.exists():
            msg += f"Certificate file at {cert} does not exist. Specify path with --cert. "

        if not key.exists():
            msg += f"Private key file at {key} does not exist. Specify path with --key."

        if msg:
            raise TLSConfigurationError(msg)

        os.environb[b"SILA_SERVER__CERT"] = cert.read_bytes()
        os.environb[b"SILA_SERVER__KEY"] = key.read_bytes()

    log_level = logging.DEBUG if verbose > 0 else logging.INFO

    create_app = await load_create_app(app)
    app = await compose_app(create_app, log_level=log_level)

    await app.start()


async def load_create_app(location: str) -> AppFactory:
    """
    Dynamically import the application factory from the given location.

    Args:
      location: Where to find the app factory formatted as "module:name".
    """

    module_name, _, factory_name = location.partition(":")

    module = importlib.import_module(module_name)
    create_app = getattr(module, factory_name)

    return create_app


if __name__ == "__main__":
    connector()
