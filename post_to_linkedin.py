import requests
import json
import os

TOKEN_FILE = "linkedin_token.txt"
POST_MESSAGE = "Hello from my Agentic Post Generator! This is a test post sent via the LinkedIn API. #Python #API #Automation"

def post_to_linkedin():
    """
    Reads the access token from a file and posts a message to LinkedIn.
    """
    # 1. Read the Access Token
    try:
        with open(TOKEN_FILE, "r") as f:
            access_token = f.read().strip()
        if not access_token:
            print(f"Error: {TOKEN_FILE} is empty. Please run linkdin_call.py to get a new token.")
            return
    except FileNotFoundError:
        print(f"Error: {TOKEN_FILE} not found. Please run linkdin_call.py first.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # 2. Get your LinkedIn Member ID (URN) from the /userinfo endpoint
    try:
        userinfo_response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
        userinfo_response.raise_for_status()
        userinfo_data = userinfo_response.json()
        # For the /userinfo endpoint, the URN is the value of the 'sub' field
        author_urn = userinfo_data['sub']
        print(f"Successfully fetched author URN: {author_urn}")
    except requests.exceptions.RequestException as e:
        print(f"Error getting your LinkedIn profile: {e}")
        print("Your access token might be invalid or lack the correct permissions (openid, profile).")
        return

    # 3. Construct the Post
    post_data = {
        "author": "urn:li:person:37ubxIoEWo",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": POST_MESSAGE
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # 4. Make the API Request to Post
    try:
        post_response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, data=json.dumps(post_data))
        post_response.raise_for_status()
        print("✅ Post was successful!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to LinkedIn: {e}")
        print(f"Response from LinkedIn: {post_response.text}")


if __name__ == "__main__":
    post_to_linkedin()
