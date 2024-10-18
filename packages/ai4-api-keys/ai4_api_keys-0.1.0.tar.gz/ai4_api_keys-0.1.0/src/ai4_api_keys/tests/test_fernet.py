"""Test the ai4_api_keys.fernet module."""

import pytest

from ai4_api_keys import fernet


@pytest.fixture
def key():
    """Return a Fernet key."""
    return "D5muj8QWVvkzDLRA0iPITxjGGYF22U2AA6eopxIWX2M="


def test_generate_key():
    """Test the fernet.generate function."""
    key = fernet.generate()
    assert key
    assert len(key) == 44


def test_encrypt_decrypt(key):
    """Test the fernet.encrypt and fernet.decrypt functions."""
    data = "Hello, World!"
    encrypted_data = fernet.encrypt(key, data)
    assert encrypted_data

    decrypted_data = fernet.decrypt(key, encrypted_data)
    assert decrypted_data == data
