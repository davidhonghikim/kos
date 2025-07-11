import json, os
from pathlib import Path
from cryptography.fernet import Fernet

VAULT_PATH = Path(".vault/secure.json")
KEY_PATH = Path(".vault/key")

def get_key():
    if not KEY_PATH.exists():
        key = Fernet.generate_key()
        KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        KEY_PATH.write_bytes(key)
    return KEY_PATH.read_bytes()

fernet = Fernet(get_key())

def load_secrets():
    if not VAULT_PATH.exists():
        return {}
    encrypted = VAULT_PATH.read_bytes()
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted)

def save_secrets(secrets):
    encrypted = fernet.encrypt(json.dumps(secrets).encode())
    VAULT_PATH.write_bytes(encrypted)

def get_secret(key):
    return load_secrets().get(key)

def set_secret(key, value):
    secrets = load_secrets()
    secrets[key] = value
    save_secrets(secrets) 