from credentials_manager import CredentialsManager
import sys

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else 'check'
    cred_manager = CredentialsManager()
    
    if action == 'save':
        client_id = sys.argv[2]
        client_secret = sys.argv[3]
        cred_manager.save_credentials(client_id, client_secret)
        print("SUCCESS")
        
    elif action == 'load':
        creds = cred_manager.load_credentials()
        if creds:
            print(f"CLIENT_ID={creds['client_id']}")
            print(f"CLIENT_SECRET={creds['client_secret']}")
        else:
            print("NO_CREDS")
            
    elif action == 'delete':
        cred_manager.delete_credentials()
        print("DELETED")
        
    elif action == 'check':
        if cred_manager.load_credentials():
            print("EXISTS")
        else:
            print("NO_CREDS")

if __name__ == "__main__":
    main()