import unittest
import subprocess
import os

class TestFileSecureCLI(unittest.TestCase):

    def setUp(self):
        """Create a temporary test file before each test."""
        self.test_file = 'testfile.txt'
        self.encrypted_file = 'testfile_encrypted.txt'
        self.decrypted_file = 'testfile_decrypted.txt'

        # Write some dummy content to the test file
        with open(self.test_file, 'w') as f:
            f.write('This is a test file for encryption.')

    def tearDown(self):
        """Remove test files after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.encrypted_file):
            os.remove(self.encrypted_file)
        if os.path.exists(self.decrypted_file):
            os.remove(self.decrypted_file)

    def test_encryption(self):
        """Test that the file is encrypted correctly."""
        password = "test_password"

        # Run the encryption command
        result = subprocess.run(
            ['filesecure', 'encrypt', '--password', password, self.test_file, '--output-file', self.encrypted_file],
            capture_output=True,
            text=True
        )

        # Check that the command ran successfully
        self.assertEqual(result.returncode, 0)

        # Check if the output file exists and is encrypted
        self.assertTrue(os.path.exists(self.encrypted_file))

        with open(self.encrypted_file, 'r') as f:
            encrypted_content = f.read()

        # The encrypted file should start with the encryption header
        self.assertTrue(encrypted_content.startswith("FILE_SECURE"))

    def test_decryption(self):
        """Test that the file is decrypted correctly."""
        password = "test_password"

        # Encrypt the file first
        subprocess.run(
            ['filesecure', 'encrypt', '--password', password, self.test_file, '--output-file', self.encrypted_file],
            capture_output=True,
            text=True
        )

        # Now decrypt the file
        result = subprocess.run(
            ['filesecure', 'decrypt', '--password', password, self.encrypted_file, '--output-file', self.decrypted_file],
            capture_output=True,
            text=True
        )

        # Check that the command ran successfully
        self.assertEqual(result.returncode, 0)

        # Check if the decrypted file exists
        self.assertTrue(os.path.exists(self.decrypted_file))

        # Check that the content matches the original file content
        with open(self.decrypted_file, 'r') as f:
            decrypted_content = f.read()

        self.assertEqual(decrypted_content, 'This is a test file for encryption.')

    def test_encryption_on_already_encrypted_file(self):
        """Test that encrypting an already encrypted file returns an error."""
        password = "test_password"

        # First encrypt the file
        subprocess.run(
            ['filesecure', 'encrypt', '--password', password, self.test_file, '--output-file', self.encrypted_file],
            capture_output=True,
            text=True
        )

        # Try to encrypt the already encrypted file
        result = subprocess.run(
            ['filesecure', 'encrypt', '--password', password, self.encrypted_file],
            capture_output=True,
            text=True
        )

        # Check that the command returns an error
        self.assertNotEqual(result.returncode, 0)

        # Check that the error message indicates the file is already encrypted
        self.assertIn("already encrypted", result.stderr)

    def test_decryption_with_wrong_password(self):
        """Test that decryption fails with an incorrect password."""
        password = "test_password"
        wrong_password = "wrong_password"

        # Encrypt
