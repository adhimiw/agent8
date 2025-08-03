"""
Security and encryption utilities for the Autonomous Personal Assistant.
Handles secure storage of API keys and sensitive data.
"""

import base64
import os
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config.settings import Settings
from core.logger import get_security_logger

logger = get_security_logger()

class SecurityManager:
    """Manages security and encryption for the assistant."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cipher_suite: Optional[Fernet] = None
        
    async def initialize(self):
        """Initialize security components."""
        logger.info("Initializing security manager")
        
        # Initialize encryption
        self._setup_encryption()
        
        logger.info("Security manager initialized")
    
    def _setup_encryption(self):
        """Setup encryption cipher."""
        try:
            # Use the encryption key from settings
            key = self.settings.app.encryption_key.encode()
            
            # Derive a proper encryption key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'autonomous_assistant_salt',
                iterations=100000,
            )
            derived_key = base64.urlsafe_b64encode(kdf.derive(key))
            
            self.cipher_suite = Fernet(derived_key)
            logger.info("Encryption setup complete")
            
        except Exception as e:
            logger.error("Failed to setup encryption", error=str(e))
            raise
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        if not self.cipher_suite:
            raise RuntimeError("Encryption not initialized")
        
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        if not self.cipher_suite:
            raise RuntimeError("Encryption not initialized")
        
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(decoded_data)
        return decrypted_data.decode()
