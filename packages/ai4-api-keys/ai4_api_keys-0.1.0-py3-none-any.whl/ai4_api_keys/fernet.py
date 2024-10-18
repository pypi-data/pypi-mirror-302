"""Manage AI4 Fernet signing keys."""

import cryptography.fernet


def generate() -> bytes:
    """Generate a new Fernet key."""
    key = cryptography.fernet.Fernet.generate_key()
    return key


def encrypt(key: str, data: str) -> str:
    """Encrypt data using a Fernet key."""
    fernet = cryptography.fernet.Fernet(key.encode())
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt(key: str, data: str) -> str:
    """Decrypt data using a Fernet key."""
    fernet = cryptography.fernet.Fernet(key.encode())
    decrypted_data = fernet.decrypt(data.encode())
    return decrypted_data.decode()
