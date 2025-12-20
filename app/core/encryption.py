from cryptography.fernet import Fernet
from app.core.config import settings

# Initialize Fernet with the key from settings
# Ensure settings.ENCRYPTION_KEY is a base64-encoded 32-byte key
# If not, generate one using Fernet.generate_key().decode() and store it securely
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(plaintext: str) -> str:
    """
    Encrypts a plaintext string using AES256 (Fernet).
    Returns the ciphertext as a URL-safe base64-encoded string.
    """
    if not isinstance(plaintext, str):
        raise TypeError("Plaintext must be a string.")
    
    # Fernet operates on bytes, so encode the string
    encrypted_bytes = fernet.encrypt(plaintext.encode('utf-8'))
    # Return as string
    return encrypted_bytes.decode('utf-8')

def decrypt_data(ciphertext: str) -> str:
    """
    Decrypts a URL-safe base64-encoded ciphertext string using AES256 (Fernet).
    Returns the plaintext string.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext must be a string.")
        
    # Fernet operates on bytes, so encode the string
    decrypted_bytes = fernet.decrypt(ciphertext.encode('utf-8'))
    # Return as string
    return decrypted_bytes.decode('utf-8')
