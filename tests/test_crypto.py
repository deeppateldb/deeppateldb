"""Tests for encryption module"""

import unittest
import sys
sys.path.insert(0, '../src')

from encryption.crypto import CryptoUtils

class TestCryptoUtils(unittest.TestCase):
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "secure_password_123"
        hashed, salt = CryptoUtils.hash_password(password)
        
        # Verify correct password
        self.assertTrue(CryptoUtils.verify_password(password, hashed, salt))
        
        # Verify incorrect password
        self.assertFalse(CryptoUtils.verify_password("wrong_password", hashed, salt))
    
    def test_aes_encryption(self):
        """Test AES encryption and decryption"""
        plaintext = "This is a secret message"
        key = "my_secret_key_32_chars_long!"
        
        encrypted = CryptoUtils.encrypt_aes(plaintext, key)
        decrypted = CryptoUtils.decrypt_aes(encrypted, key)
        
        self.assertEqual(plaintext, decrypted)

if __name__ == "__main__":
    unittest.main()
