# Cryptographic utilities will be defined here 

from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings

# Ensure the key is in bytes
ENCRYPTION_KEY = settings.DEVICE_CREDENTIAL_ENCRYPTION_KEY.encode()
_fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """Encrypts a string using Fernet symmetric encryption."""
    if not data:
        return ""
    encrypted_bytes = _fernet.encrypt(data.encode())
    return encrypted_bytes.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string using Fernet symmetric encryption."""
    if not encrypted_data:
        return ""
    try:
        decrypted_bytes = _fernet.decrypt(encrypted_data.encode())
        return decrypted_bytes.decode()
    except InvalidToken:
        # Handle cases where the token is invalid or tampered with
        # Log this event for security auditing
        print("Error: Failed to decrypt data. Token is invalid or tampered.")
        # Depending on policy, you might raise an exception or return an empty string/error indicator
        raise ValueError("Invalid encrypted data")
    except Exception as e:
        print(f"An unexpected error occurred during decryption: {e}")
        raise ValueError("Decryption failed due to an unexpected error")

# Placeholder for other crypto utils if needed 