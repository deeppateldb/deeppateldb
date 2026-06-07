"""Encryption and decryption utilities"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import hashlib
import base64

class CryptoUtils:
    """Cryptographic utilities for encryption and hashing"""
    
    @staticmethod
    def hash_password(password: str, salt: bytes = None) -> tuple:
        """Hash password using PBKDF2"""
        if salt is None:
            salt = get_random_bytes(32)
        hashed = PBKDF2(password, salt, dkLen=64, count=100000)
        return base64.b64encode(hashed).decode(), base64.b64encode(salt).decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Verify password against hash"""
        salt_bytes = base64.b64decode(salt)
        new_hash = PBKDF2(password, salt_bytes, dkLen=64, count=100000)
        return base64.b64encode(new_hash).decode() == hashed
    
    @staticmethod
    def encrypt_aes(plaintext: str, key: str) -> str:
        """Encrypt text using AES"""
        cipher = AES.new(key.encode().ljust(32)[:32], AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    
    @staticmethod
    def decrypt_aes(ciphertext: str, key: str) -> str:
        """Decrypt AES encrypted text"""
        data = base64.b64decode(ciphertext)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext_bytes = data[32:]
        cipher = AES.new(key.encode().ljust(32)[:32], AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext_bytes, tag)
        return plaintext.decode()
