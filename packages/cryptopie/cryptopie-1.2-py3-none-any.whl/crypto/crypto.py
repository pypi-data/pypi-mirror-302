from typing import Optional
from crypto.aesx import AESChiper, AesAlg
from crypto.hmacx import HMACX

AES_128_KEY_SIZE = 16
AES_192_KEY_SIZE = 24
AES_256_KEY_SIZE = 32

class Crypto:
    def __init__(self, aes_key: Optional[str] = None, hmac_key: Optional[str] = None):
        self.AESKey = aes_key
        self.HMACKey = hmac_key

        if not self.AESKey or not self.HMACKey:
            raise ValueError("AES_KEY and HMAC_KEY are required")
        
    def is_valid_aes_key(self, key: str) -> bool:
        key_len = len(key)
        aes_keys= [AES_128_KEY_SIZE, AES_192_KEY_SIZE, AES_256_KEY_SIZE]
        if key_len not in aes_keys: 
            return False
        return True
    
    def encrypt(self, data: str, alg: AesAlg) -> str:
        aes_cipher = AESChiper(self.AESKey, data, alg)
        return aes_cipher.encrypt()

    def decrypt(self, encrypted_data: str, alg: AesAlg) -> str:
        aes_cipher = AESChiper(self.AESKey, '', alg)
        return aes_cipher.decrypt(encrypted_data)
    
    def hash(self, data: str) -> str:
        hmac_instance = HMACX(self.HMACKey)
        return hmac_instance.hash(data)
    
    def verify(self, data: str, signature: str) -> bool:
        hmac_instance = HMACX(self.HMACKey)
        return hmac_instance.verify(data, signature)
    
    def heap(self, data: str) -> str:
        return self.hash(data)[-8:]
