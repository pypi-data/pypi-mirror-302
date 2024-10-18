import os
import json
from json import JSONDecodeError

# We could have different places to look for credentials.
# They are sorted by priority, so for some projects
# it easy to have a local credentials file that overrides the global
CREDENTIALS_PATHS = map(
    os.path.expanduser,
    [
        "./.fleetglue_credentials",
        "~/.fleetglue/credentials",
        "~/.fleetglue_credentials",
    ]
)

ENVIRONMENTS = ["dev", "qa", "staging", "release"]  # TODO: Handle envs on credentials
URLS = {
    "local": "http://localhost:8001",
    "dev": "https://dev.api.fleetglue.com",
    "qa": "https://qa.api.fleetglue.com",
    "staging": "https://staging.api.fleetglue.com",
    "release": "https://api.fleetglue.com",
}
DEFAULT_URL = URLS["release"]


def get_credentials(path=None):
    if path is None:
        # If not path provided, check if any of the default locations exist
        for path in CREDENTIALS_PATHS:
            if os.path.exists(path):
                break
        else:
            raise NoCredentialsError(
                f"Credentials file is missing. Make sure any of the following paths exist: "
                f"{', '.join(CREDENTIALS_PATHS)}"
            )
    return Credentials.from_path(path=path)


class Credentials:

    def __init__(
        self, token=None, secret=None, url=DEFAULT_URL, path=None, **kwargs
    ):
        if token is None or secret is None:
            raise CredentialsParseError("Both `token` and `secret` cannot be empty")
        self.token = token
        self.secret = secret
        if url is None:
            url = DEFAULT_URL
        self.url = url
        self.path = path
        self.kwargs = kwargs

    def save(self):
        new_data = self.kwargs.copy()
        new_data.update({
            "token": self.token,
            "secret": self.secret,
        })
        if self.url is not None:
            new_data["url"] = self.url
        # Read previous content to update it without overriding other envs
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                data = json.load(f)
            data.update(new_data)
        else:
            data = new_data
        # Saves new file
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def from_path(cls, path):
        """Loads the credentials from a path."""

        with open(path, "r") as f:
            try:
                data = json.load(f)
            except JSONDecodeError as e:
                raise CredentialsParseError(f"Invalid JSON credentials on `{path}`. {e}")
        return cls(path=path, **data)


def validate_env(env):
    if env is not None and env not in ENVIRONMENTS:
        raise ValueError(f"Invalid environment `{env}`. Must be one of {ENVIRONMENTS}")


class CredentialsParseError(Exception):
    pass


class NoCredentialsError(Exception):
    pass
