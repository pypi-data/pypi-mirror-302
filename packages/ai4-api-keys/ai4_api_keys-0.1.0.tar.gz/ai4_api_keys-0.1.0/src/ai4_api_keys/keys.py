"""Module to generate API keys."""

import enum
import json
import secrets

from ai4_api_keys import exceptions
from ai4_api_keys import fernet


class APILevels(str, enum.Enum):
    """Levels of API keys."""

    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    PLATINUM = "platinum"

    def __str__(self):
        """Return the name of the level."""
        return f"{self.name}"


def create(key: str, scope: str, level: APILevels) -> str:
    """Create a new API key.

    :param key: The Fernet key to use.
    :param scope: The scope of the API key.
    :param level: The level of the API key.
    :return: The new API key.
    """
    message = {
        "nonce": secrets.token_hex(8),
        "scope": scope,
        "level": level.value,
    }

    return fernet.encrypt(key, json.dumps(message))


def validate(key: str, api_key: str, scope: str) -> None:
    """Validate an API key.

    :param key: The Fernet key to use.
    :param api_key: The API key to validate.
    :param scope: The scope of the API key.

    This function raises an exception if the key is invalid.
    """
    try:
        decrypted = fernet.decrypt(key, api_key)
    except Exception:
        raise exceptions.InvalidKeyError(api_key)

    message = json.loads(decrypted)
    if message["scope"] != scope:
        raise exceptions.InvalidScopeError(message["scope"], scope)

    # NOTE(aloga): we need to use this, "level in Enum" does not work with member values
    # before Python 3.12
    levels = [i.value for i in dict(APILevels.__members__).values()]
    if message["level"] not in levels:
        # MyPy complains about this line, but it's correct with
        # "InvalidLevelError" has incompatible type "type[APILevels]"; expected "Enum"
        raise exceptions.InvalidLevelError(message["level"], APILevels)  # type: ignore
