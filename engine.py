import os
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from stegano import lsb
import random
import string

class Hider:
    keys = None

    def __init__(self):
        self.keys = {}

    def add_key(self, dialog, password, salt=''):
        """ Add a key to the Hider's keys dictionary if it does not exist.
        """
        if not dialog in self.keys:
            encoded_password = str.encode(password)
            encoded_salt = str.encode(salt)
            key = self.gen_key(encoded_password, encoded_salt)
            self.keys[dialog] = key
        else:
            print('Key already exists!')
    
    def del_key(self, dialog):
        """ Remove a key from the Hider's keys dictionary if it exists.
        """
        if dialog in self.keys:
            del self.keys[dialog]
        else:
            print('Key does not exist!')

    @staticmethod
    def gen_key(password, salt=b''):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return Fernet(key)

    def hide(self, dialog, plaintext, file_path_plaintext, directory_path_hidden):
        """ Encrypt a message and hide its contents in a file, then return its path.
        Returns path to image with encrypted text.

        dialog: A combination of the client prefix and chat/channel, used to get key
        plaintext: Message to be hidden
        file_path_plaintext: Path to an image file to hide message in
        directory_path_hidden: The directory of where to save the steg file
        """
        try:
            plaintext = base64.b64encode(str.encode(plaintext)) # Encode message into a bytes-like base64 string
            ciphertext = self.keys[dialog].encrypt(plaintext).decode()
            secret = lsb.hide(file_path_plaintext, ciphertext)
            file_extension = file_path_plaintext.split('.')[-1]
            random_filename = directory_path_hidden +\
                              ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randint(10, 12))) +\
                              '.' +\
                              file_extension
            secret.save(random_filename)
            return random_filename
        except KeyError:
            print('Key does not exist!')
        except FileNotFoundError:
            print('File does not exist!')

    def show(self, dialog, file_path_ciphertext):
        """ Pull the text out of a picture which uses LSB steganography, then decrypt it.
        Returns plaintext.
        
        dialog: A combination of the client previx and chat/channel, used to get key
        file_path_ciphertext: Path to an image file with hidden, encrypted text
        """
        try:
            ciphertext = str.encode(lsb.reveal(file_path_ciphertext))
            plaintext = self.keys[dialog].decrypt(ciphertext)
            plaintext = base64.b64decode(plaintext).decode()
            return plaintext
        except KeyError:
            print('Key does not exist!')
        except FileNotFoundError:
            print('File does not exist!')

def main():
    # Create a Hider object for the cryptostego engine.
    engine = Hider()

    # Process requests
    

    
if __name__ == '__main__':
    main()