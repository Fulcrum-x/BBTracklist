import win32crypt
import base64
import json
import os

class CredentialsManager:
    def __init__(self, filename="spotify_credentials.enc"):
        self.filename = filename
    
    def encrypt_data(self, data):
        """Encrypt data using Windows DPAPI"""
        byte_data = json.dumps(data).encode('utf-8')
        # CryptProtectData takes (DataIn, DataDescr, OptionalEntropy, Reserved, PromptStruct, Flags)
        encrypted_data = win32crypt.CryptProtectData(
            byte_data,
            "Spotify API Credentials",  # Description
            None,  # Optional entropy
            None,  # Reserved
            None,  # Prompt struct
            0     # Flags
        )
        # Convert to base64 for file storage
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_data(self, encrypted_str):
        """Decrypt data using Windows DPAPI"""
        try:
            encrypted_data = base64.b64decode(encrypted_str)
            # CryptUnprotectData returns (Description, Data)
            decrypted_byte_data = win32crypt.CryptUnprotectData(
                encrypted_data,
                None,  # Optional entropy
                None,  # Reserved
                None,  # Prompt struct
                0     # Flags
            )[1]  # [1] contains the decrypted data
            return json.loads(decrypted_byte_data.decode('utf-8'))
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return None
    
    def save_credentials(self, client_id, client_secret):
        """Save encrypted credentials to file"""
        creds = {
            'client_id': client_id,
            'client_secret': client_secret
        }
        encrypted_data = self.encrypt_data(creds)
        with open(self.filename, 'w') as f:
            f.write(encrypted_data)
    
    def load_credentials(self):
        """Load and decrypt credentials from file"""
        if not os.path.exists(self.filename):
            return None
            
        try:
            with open(self.filename, 'r') as f:
                encrypted_str = f.read()
            return self.decrypt_data(encrypted_str)
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return None
            
    def delete_credentials(self):
        """Delete the credentials file"""
        if os.path.exists(self.filename):
            os.remove(self.filename)