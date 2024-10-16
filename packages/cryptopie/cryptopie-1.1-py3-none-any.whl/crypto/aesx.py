from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from enum import Enum

class AesAlg(Enum):
    CBC = 'cbc'
    CFB = 'cfb'
    GCM = 'gcm'

def pkcs5_padding(data: bytes) -> bytes:
    padding_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([padding_len] * padding_len)

def pkcs5_unpadding(data: bytes) -> bytes:
    padding_len = data[-1]
    return data[:-padding_len]

class AESChiper:
    def __init__(self, key: str, data: str, alg: AesAlg):
        self.data = data.encode()
        self.alg = alg
        self.key = key.encode()

    def encrypt(self) -> str:
        if self.alg == AesAlg.CBC:
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padded_data = pkcs5_padding(self.data)
            encrypted = cipher.encrypt(padded_data)
            return (iv + encrypted).hex()
        elif self.alg == AesAlg.CFB:
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            encrypted = cipher.encrypt(self.data)
            return (iv + encrypted).hex()
        elif self.alg == AesAlg.GCM:
            cipher = AES.new(self.key, AES.MODE_GCM)
            encrypted, tag = cipher.encrypt_and_digest(self.data)
            return (cipher.nonce + encrypted + tag).hex()
        else:
            raise ValueError("Invalid algorithm")

    def decrypt(self, encrypted_hex: str) -> str:
        encrypted_data = bytes.fromhex(encrypted_hex)
        if self.alg == AesAlg.CBC:
            iv = encrypted_data[:AES.block_size]
            encrypted = encrypted_data[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padded_data = cipher.decrypt(encrypted)
            data = pkcs5_unpadding(padded_data)
            return data.decode()
        elif self.alg == AesAlg.CFB:
            iv = encrypted_data[:AES.block_size]
            encrypted = encrypted_data[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            data = cipher.decrypt(encrypted)
            return data.decode()
        elif self.alg == AesAlg.GCM:
            nonce = encrypted_data[:AES.block_size]
            tag = encrypted_data[-16:]
            encrypted = encrypted_data[AES.block_size:-16]
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            data = cipher.decrypt_and_verify(encrypted, tag)
            return data.decode()
        else:
            raise ValueError("Invalid algorithm")
