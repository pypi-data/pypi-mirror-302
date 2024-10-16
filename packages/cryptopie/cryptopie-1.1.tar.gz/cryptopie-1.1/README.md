# go-encrypt

This project focuses on encrypting Personally Identifiable Information (PII) using the Go programming language.

## Features

- Encryption and decryption of PII data
- Easy integration with go applications

## Getting Started

To give Git credentials, you’ll need to have a .netrc that includes gitlab.playcourt.id in your home directory.

### Installation

```sh
pip install cryptopie
```

The below example will print the contents:

```py
from crypto import Crypto
from crypto import AesAlg

crypto = Crypto(aes_key=aes_key, hmac_key=hmac_key)

encrypted_data = crypto.encrypt('Hello, World!', AesAlg.CBC)
print(f'Encrypted Data: {encrypted_data}')

decrypted_data = crypto.decrypt("87eb6382b98f41d7897fcf919e887e08c106c341402fe3ac598de9ab4c35a43959eb4ead70bf355cc2bc2a54d1b506bc", AesAlg.CBC)
print(f'Decrypted Data: {decrypted_data}')
```
