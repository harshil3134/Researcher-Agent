import os, tweepy
from dotenv import load_dotenv

load_dotenv()

# DEV ONLY: allow http redirect_uri like http://localhost:3000/callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_ID = os.getenv("X_ACCESS_TOKEN")
CLIENT_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")  # include if app is "confidential"
REDIRECT_URI = "http://localhost:3000/callback"
SCOPES = ["tweet.read","users.read","tweet.write","offline.access"]

auth = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=SCOPES,
    client_secret=CLIENT_SECRET,   # keep same handler alive!
)

auth_url = auth.get_authorization_url()
print("Open in browser:\n", auth_url)

callback_url = input("\nPaste FULL redirect URL here:\n> ")
token = auth.fetch_token(callback_url)  # uses the SAME handler's code_verifier
print("Access token (start):", token["access_token"])
