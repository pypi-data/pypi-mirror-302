import click

from fleetglue_client.cli.commands.base import (
    add_options,
    common_options,
    error_message_catch,
)

from fleetglue_client import FleetGlueClient
from fleetglue_client.credentials import (
    get_credentials,
    NoCredentialsError,
    Credentials,
)


@click.command()
@add_options(common_options)
@click.option("--force", default=False, is_flag=True)
def setup(**kwargs):
    user = kwargs.get("user")
    env = kwargs.get("env")
    force = kwargs.get("force")
    from fleetglue_client.api_handler import login

    try:
        credentials = get_credentials()
        if not force:
            click.confirm(
                click.style(
                    f"There are already existent credentials on {credentials.path}. "
                    f"Are you sure you want to override them?",
                    fg="yellow",
                ),
                abort=True,
            )
    except NoCredentialsError:
        # If no credentials already exist, we will create them
        pass

    # Gather user information
    click.echo("OK, let's first login to the application in order to generate a token.")
    if not user:
        user = click.prompt("Insert user/email", type=str)

    password = click.prompt(f"Insert password for [{user}]", hide_input=True)

    with error_message_catch("Login"):
        url, token_id, secret = login(username=user, password=password, env=env)

    client = FleetGlueClient(token=token_id, secret=secret, url=url, env=env)

    # Create a token without expiration with same permissions
    with error_message_catch("New token creation"):
        token = client.get_token(token_id)
        description = f"FleetGlue CLI token created for user {user}"
        # TODO change this for policies
        result = client.create_token(
            token._data.get("allowed_actions"),
            token._data.get("accounts"),
            token._data.get("devices"),
            description,
            create_secret=True,
            raw=True,
            type="fleetglue_cli",
        )
        new_token_id = result["token"]
        new_secret = result["secret"]

    # Save the new credentials
    with error_message_catch("Credentials generation"):
        Credentials(token=new_token_id, secret=new_secret, url=url).save()
