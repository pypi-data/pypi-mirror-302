"""Test the ai4_api_keys.keys module."""

import pytest

from ai4_api_keys import exceptions
from ai4_api_keys import keys


@pytest.fixture
def key():
    """Return a Fernet key."""
    return "D5muj8QWVvkzDLRA0iPITxjGGYF22U2AA6eopxIWX2M="


def test_create_key(key):
    """Test the fernet.create function."""
    scope = "ai4eosc"
    level = keys.APILevels.BRONZE

    new_key = keys.create(key, scope, level)
    assert new_key

    assert keys.validate(key, new_key, scope) is None


@pytest.fixture()
def valid_api_key():
    """Return a valid API key."""
    return (
        "gAAAAABnDh1srDPSh7F3R8f3dhNVR1_t8pGX_pOc8RZRq0j_0UWIluMjxttgieXdfihMUChb"
        "smz5ByfRw4K3t_N8Nhp_pbsi7KbBFw9H-AK7qqMRAZvef527SEkHP-j0S8TLYoE93WD_PkqQI"
        "Oe4N0ShUnd8wHrSrI1QzOBlsWnzmPv3lkUV0uI="
    )


def test_validate_key(key, valid_api_key):
    """Test the keys.validate function."""
    scope = "ai4eosc"

    assert keys.validate(key, valid_api_key, scope) is None


def test_validate_key_invalid(key):
    """Test the keys.validate function with an invalid key."""
    scope = "ai4eosc"

    # This raises an exception
    with pytest.raises(exceptions.InvalidKeyError):
        keys.validate(key, "invalid_key", scope)


def test_validate_key_invalid_scope(key, valid_api_key):
    """Test the keys.validate function with an invalid scope."""
    scope = "invalid_scope"

    with pytest.raises(exceptions.InvalidScopeError):
        keys.validate(key, valid_api_key, scope)
