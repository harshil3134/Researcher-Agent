import os
import requests
import webbrowser
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# --- Configuration ---
# Make sure your Client ID is set as an environment variable
CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
# For debugging, we have hardcoded the secret. Remember to remove this for production.
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"
TOKEN_FILE = "linkedin_token.txt"

# This global variable will hold the authorization code sent by LinkedIn
authorization_code = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """A simple HTTP request handler to catch the OAuth 2.0 callback."""
    def do_GET(self):
        global authorization_code
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get('code', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if code:
            authorization_code = code
            self.wfile.write(b"<html><body><h1>Authentication Successful!</h1><p>You can close this browser tab and return to your script.</p></body></html>")
        else:
            self.wfile.write(b"<html><body><h1>Authentication Failed</h1><p>Could not find an authorization code in the request from LinkedIn.</p></body></html>")

def get_access_token():
    """Guides the user through the OAuth 2.0 flow by running a temporary web server."""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Please set the LINKEDIN_CLIENT_ID environment variable and ensure the Client Secret is in the script.")
        return

    server = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()
    print("--- Step 1: Temporary server started at http://localhost:8080 ---")

    # We are requesting all scopes we need: to read the profile and to post.
    scopes = "openid profile w_member_social"
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=some_random_string&scope={scopes}"

    print("--- Step 2: Opening browser for authorization ---")
    webbrowser.open(auth_url)

    print("--- Step 3: Waiting for you to authorize in the browser... ---")
    thread.join()

    if not authorization_code:
        print("\nError: Could not retrieve authorization code. Please try again.")
        return
    
    print("Authorization code received successfully!")

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        token_response = requests.post(token_url, data=token_payload)
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if access_token:
            with open(TOKEN_FILE, "w") as f:
                f.write(access_token)
            print(f"\n--- Step 4: Success! ---")
            print(f"Access token saved to {TOKEN_FILE}")
        else:
            print("\nError: Could not retrieve access token.")
            print("Response from LinkedIn:", token_data)

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred during token exchange: {e}")
        if 'token_response' in locals():
            print("Response from LinkedIn:", token_response.text)

if __name__ == "__main__":
    get_access_token()
