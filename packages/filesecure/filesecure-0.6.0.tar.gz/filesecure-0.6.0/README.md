# FileSecure Tool

**FileSecure** is a command-line utility for encrypting and decrypting files using AES-256-CBC encryption. This tool allows you to securely protect your files with a password, ensuring that sensitive data is not exposed.

## Features

- **Encrypt Files**: Secure your files with AES-256-CBC encryption.
- **Decrypt Files**: Restore encrypted files back to their original state.
- **Easy to Use**: Simple command-line interface with straightforward commands.
- **Password-Based Encryption**: Utilize a password to derive a strong encryption key.

## Installation

To use the FileSecure tool, you need to have Python and `pip` installed on your system.

```bash
pip install filesecure
```

## Usage

### Encrypting a File

To encrypt a file, use the following command:

```bash
filesecure encrypt --password "your_password" yourfile.txt
```
#### Parameters

- `--password "your_password"`: The password used to encrypt the file. Make sure to use a strong password.
- `yourfile.txt`: The name of the file you want to encrypt.

#### Important Notes

- The original file will be overwritten with the encrypted content.
- If the file is already encrypted (i.e., it starts with `FILE_SECURE`), a message will indicate that the file is already encrypted.

### Decrypting a File

To decrypt a file, use the following command:

```bash
filesecure decrypt --password "your_password" yourfile.txt
```

#### Parameters

- `--password "your_password"`: The password used to decrypt the file. It must match the password used during encryption.
- `yourfile.txt`: The name of the file you want to decrypt.

#### Important Notes

- The original file will be overwritten with the decrypted content.
- If the file is not encrypted (i.e., it does not start with `FILE_SECURE`), an error message will indicate that the file is not encrypted or is in an invalid format.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.