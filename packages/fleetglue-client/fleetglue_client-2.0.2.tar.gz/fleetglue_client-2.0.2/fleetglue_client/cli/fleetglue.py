import click

from fleetglue_client import __version__
from fleetglue_client.cli.commands.setup import setup
from fleetglue_client.cli.commands.device import (
    device,
)


@click.group()
@click.version_option(version=__version__, prog_name="FleetGlue CLI")
def cli(args=None):
    pass


cli.add_command(setup)
cli.add_command(device)

if __name__ == "__main__":
    cli()
