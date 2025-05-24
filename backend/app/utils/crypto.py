# Cryptographic utilities will be defined here 

from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings

# Ensure the key is in the correct format (bytes, URL-safe base64 encoded)
# Fernet.generate_key() can be used to create a suitable key
# For now, we assume settings.DEVICE_CREDENTIAL_ENCRYPTION_KEY is already a valid Fernet key
# or can be encoded into one. If it's a simple string, it needs to be
# base64 encoded and of the correct length.
# A more robust solution would involve key derivation if the raw key isn't suitable.

# For simplicity, let's assume settings.DEVICE_CREDENTIAL_ENCRYPTION_KEY is a URL-safe base64 encoded string.
# If it's not, this will need adjustment (e.g., using a KDF like PBKDF2HMAC).
try:
    # Attempt to decode the key from settings.
    # Ensure it is a URL-safe base64 encoded string representing 32 bytes.
    key = settings.DEVICE_CREDENTIAL_ENCRYPTION_KEY.encode() # Ensure it's bytes
    if len(key) < 44: # A 32-byte key base64 encoded is typically 44 bytes with padding
        # This is a simplified check. Proper key validation or generation is crucial.
        # For a production system, generate a key using Fernet.generate_key() and store it securely.
        # Example: key = base64.urlsafe_b64encode(settings.DEVICE_CREDENTIAL_ENCRYPTION_KEY.ljust(32)[:32].encode())
        # This example pads/truncates the key to 32 bytes and encodes it. This is NOT cryptographically secure for arbitrary strings.
        # A better approach if the key is a passphrase, is to use a KDF.
        # For now, we proceed with the assumption that the key from settings is correctly formatted or a placeholder.
        # To generate a proper key for .env:
        # from cryptography.fernet import Fernet
        # key = Fernet.generate_key()
        # print(key.decode()) # Store this in .env
        pass # Placeholder for more robust key handling if needed
    
    cipher_suite = Fernet(key)
except Exception as e:
    # Fallback or error logging if key is invalid.
    # This is critical for security. For now, we'll print a warning.
    # In a real app, this should prevent startup or use a known fallback if appropriate.
    print(f"WARNING: DEVICE_CREDENTIAL_ENCRYPTION_KEY may not be a valid Fernet key. Error: {e}")
    print("Please generate a valid key using Fernet.generate_key() and set it in your .env file.")
    # As a VERY INSECURE fallback for the app to run during development if no key is set,
    # generating a temporary key. THIS IS NOT FOR PRODUCTION.
    temp_key = Fernet.generate_key()
    print(f"DEVELOPMENT ONLY: Using temporary encryption key: {temp_key.decode()}")
    cipher_suite = Fernet(temp_key)


def encrypt_data(data: str) -> str:
    """Encrypts a string using Fernet symmetric encryption."""
    if not data:
        return ""
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string using Fernet symmetric encryption."""
    if not encrypted_data:
        return ""
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

# Example of how to generate a key if you need one for your .env:
# if __name__ == "__main__":
# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(f"Generated Fernet key for .env: {key.decode()}")

# Placeholder for other crypto utils if needed 