# main.py
import os
import sys
import base64
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding

# Constant for the encryption header
ENCRYPTION_HEADER = "FILE_SECURE;AES-256-CBC;0.4.0;"

# Function to derive a key from a password and a salt
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    key = kdf.derive(password.encode())
    return key

# Function to encrypt a file
def encrypt_file(password: str, input_file: str):
    with open(input_file, 'rb') as f:
        data = f.read()

    # Check if the file is already encrypted
    if data.startswith(ENCRYPTION_HEADER.encode()):
        print(f"Error: the file '{input_file}' is already encrypted.")
        return

    # Generate a salt and derive the key
    salt = os.urandom(16)
    key = derive_key(password, salt)

    # Generate an initialization vector (IV)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Add padding to ensure data is a multiple of the block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Base64 encode the encrypted data
    b64_encrypted_data = base64.b64encode(salt + iv + encrypted_data).decode('utf-8')

    # Format the output file with FILE_CRYPT
    encrypted_content = f"{ENCRYPTION_HEADER}\n"

    # Add Base64 while limiting lines to 80 characters
    for i in range(0, len(b64_encrypted_data), 80):
        encrypted_content += b64_encrypted_data[i:i + 80] + "\n"

    # Save to the same file
    with open(input_file, 'w') as f:
        f.write(encrypted_content)

    print(f"File '{input_file}' encrypted.")

# Function to decrypt a file
def decrypt_file(password: str, input_file: str):
    with open(input_file, 'r') as f:
        content = f.read()

    if not content.startswith(ENCRYPTION_HEADER):
        print(f"Error: the file '{input_file}' is not encrypted or is in an invalid format.")
        sys.exit(1)

    # Extract Base64 encrypted data
    encrypted_data_b64 = content.split(';')[3].strip()
    encrypted_data = base64.b64decode(encrypted_data_b64)

    # Extract the salt and IV
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    encrypted_data = encrypted_data[32:]

    # Derive the key from the password and the salt
    key = derive_key(password, salt)

    # Decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    # Save to the same file, replacing the encrypted content with the decrypted content
    with open(input_file, 'wb') as f:
        f.write(data)

    print(f"File '{input_file}' decrypted.")

# Main function to handle arguments and execute commands
def filesecure():
    parser = argparse.ArgumentParser(description='Encrypt and decrypt files with a password.')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Subcommand to encrypt a file
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('--password', required=True, help='Password to encrypt the file')
    encrypt_parser.add_argument('file', help='Name of the file to encrypt')

    # Subcommand to decrypt a file
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('--password', required=True, help='Password to decrypt the file')
    decrypt_parser.add_argument('file', help='Name of the file to decrypt')

    # Parse the arguments
    args = parser.parse_args()

    if args.command == 'encrypt':
        encrypt_file(args.password, args.file)
    elif args.command == 'decrypt':
        decrypt_file(args.password, args.file)
    else:
        parser.print_help()
