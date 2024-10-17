# generate_gmail_refresh_token.py
"""
This script helps you generate a refresh token for Gmail's API using OAuth 2.0.

Prerequisites:
1. Go to https://console.cloud.google.com/ and create a new project.
2. Enable the Gmail API for your project.
3. Create OAuth 2.0 credentials (choose "Desktop App" or "Web Application").
4. Download the 'client_secret.json' file and place it in the same directory as this script.

Steps to Run:
1. Ensure you have installed the necessary libraries:
   pip install google-auth-oauthlib

2. Run this script:
   python generate_gmail_refresh_token.py

3. Follow the instructions that appear in the browser window.
4. After granting permission, you will see the refresh token printed in your console.

Note:
- Keep your 'client_secret.json' and the generated refresh token secure.
- Do not share your refresh token publicly.
"""

from google_auth_oauthlib.flow import InstalledAppFlow

# Path to the client_secret.json file downloaded from Google Cloud Console
CLIENT_SECRETS_FILE = "/home/harnath/Desktop/Harnath/Harnath/alerthub/support_files/email_creds.json"

# The scopes define the level of access needed. Adjust the scopes as needed.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly', 
    'https://www.googleapis.com/auth/gmail.send'
]

def generate_refresh_token():
    """
    Generates a refresh token for Gmail API using OAuth 2.0 credentials.
    The token will be printed in the console once generated.
    """
    try:
        # Initialize the OAuth 2.0 flow
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        
        # Run local server to obtain the user's authorization
        creds = flow.run_local_server(port=0)
        
        # Print the obtained tokens
        print("\n--- Successfully Generated Tokens ---")
        print(f"Access Token: {creds.token}")
        print(f"Refresh Token: {creds.refresh_token}")
        print(f"Client ID: {creds.client_id}")
        print(f"Client Secret: {creds.client_secret}")
        print("\nNOTE: Keep these tokens secure and do not share them.")
    except Exception as e:
        print(f"Error generating refresh token: {e}")

if __name__ == "__main__":
    generate_refresh_token()
