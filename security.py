from cryptography.fernet import Fernet
from hashlib import blake2b
import base64
import pickle
import os.path
from getpass import getpass

def encrypt(password, message):
    key = blake2b(key=password.encode(), digest_size=16).hexdigest()
    key = base64.urlsafe_b64encode(key.encode())
    return Fernet(key).encrypt(message.encode()).decode('utf-8')

    
def decrypt(password, encrypted_message):
    key = blake2b(key=password.encode(), digest_size=16).hexdigest()
    key = base64.urlsafe_b64encode(key.encode())
    return Fernet(key).decrypt(encrypted_message.encode()).decode('utf-8')


def get_keys(key_file_name):
    
    if os.path.exists(key_file_name):
        key_file = open(key_file_name, 'rb')
        key = pickle.load(key_file)
        key_file.close()
        while True:
            try:
                entered_password = getpass('Please Enter Password: ')
                if entered_password == decrypt(entered_password, key['password']):
                    print('correct password')
                    x = dict()
                    x['api_key'] = decrypt(entered_password, key['api_key'])
                    x['api_secret'] = decrypt(entered_password, key['api_secret'])
                    return x
            except:
                pass
    else:
        print('No existing api key')
        return None


