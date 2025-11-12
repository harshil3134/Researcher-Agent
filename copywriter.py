from dotenv import load_dotenv
from typing import Annotated
import operator
from langchain_core.tools import tool
from pydantic import BaseModel
from langgraph.graph import StateGraph, add_messages,END
from langgraph.prebuilt import InjectedState
from datetime import datetime
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import tweepy
import json
import requests
import json
import os


load_dotenv()

copywriter_prompt=open("prompts/copywriter.md","r").read()
linkedin_example=open("example_content/linkedin.md","r").read()
x_example=open("example_content/x.md","r").read()
blog_example=open("example_content/blog.md","r").read()

class CopyWriterState(BaseModel):
    """The state of the copywriter agent."""
    messages:Annotated[list,add_messages]=[]
    research_reports:Annotated[list,operator.add]=[]

@tool
async def review_research_reports(
    state:Annotated[CopyWriterState,InjectedState]):
    """Use this tool to review available research reports to inform your writing."""
    return [report.model_dump_json() for report in state.research_reports]

@tool
async def generate_linkedin_post(
    title:str,
    content:str,
):
    """Use this tool to generate a LinkedIn post and save it to a file."""
    filename=f"ai_files/{title}.md"
    with open(filename,"w") as f:
        f.write(content)
    return f"The linkedIn post has been generated and saved to {filename}"

@tool
async def generate_x_post(
    title:str,
    content:str,
):
    """Use this tool to generate a x post and save it to a file."""
    filename=f"ai_files/{title}.md"
    with open(filename,"w") as f:
        f.write(content)
    return f"The x post has been generated and saved to {filename}"

@tool
async def generate_blog_post(
    title:str,
    content:str,
):
    """Use this tool to genrate a blog post."""
    filename=f"ai_files/{title}.md"
    with open(filename,"w") as f:
        f.write(content)
    return f"The blog post has been generated and saved to {filename}"

@tool
async def post_to_linkedin(content: str) -> str:
    """Posts a message to LinkedIn.

    Args:
        content: The content of the post to be published on LinkedIn.

    Returns:
        A string indicating the status of the post.
    """

    access_token=os.getenv('LINKEDIN_AUTH_TOKEN')
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
   
    author_urn=os.getenv('LINKEDIN_AUTHOR_URN')
    print('access token',access_token," ----",author_urn)

    post_data = {
        "author": "urn:li:person:37ubxIoEWo",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    try:
        post_response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, data=json.dumps(post_data))
        post_response.raise_for_status()
        print("✅ Post was successful!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to LinkedIn: {e}")
        print(f"Response from LinkedIn: {post_response.text}")

    # This tool now calls the reusable function from our module
    return post_response

key = os.getenv("GOOGLE_API_KEY_2")
print(key)
llm=ChatGoogleGenerativeAI(
    name="CopyWriter",
    model="gemini-2.0-flash",
    api_key=key
)

tools=[
    review_research_reports,
    generate_linkedin_post,
    generate_x_post,
    generate_blog_post,
    post_to_linkedin

    ,
    # publish_x_thread posts a list of strings as a thread to X (Twitter)
    # use dry_run=True to preview payloads without sending
    # requires X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET in env
    
]


@tool
async def publish_x_thread(posts: list, dry_run: bool = True):
    # Minimal, easy-to-read implementation.
    consumer_key = os.getenv("X_API_KEY")
    consumer_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not posts or not isinstance(posts, list):
        return {"ok": False, "error": "posts must be a non-empty list"}

    # Dry-run simply echoes the posts back so callers can preview payloads.
    if dry_run:
        return {"ok": True, "dry_run": True, "posts": posts}

    if not (consumer_key and consumer_secret and access_token and access_token_secret):
        return {"ok": False, "error": "Missing X credentials in environment"}

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    posted_ids = []
    try:
        # Post the first tweet
        resp = client.create_tweet(text=posts[0])
        data = getattr(resp, "data", {}) or {}
        tweet_id = data.get("id") if isinstance(data, dict) else getattr(data, "id", None)
        posted_ids.append(tweet_id)

        # Post replies (if any)
        for text in posts[1:]:
            resp = client.create_tweet(text=text, reply={"in_reply_to_tweet_id": tweet_id})
            data = getattr(resp, "data", {}) or {}
            tweet_id = data.get("id") if isinstance(data, dict) else getattr(data, "id", None)
            posted_ids.append(tweet_id)

    except Exception as e:
        return {"ok": False, "error": str(e)}

    return {"ok": True, "posted_ids": posted_ids}

llm_with_tools=llm.bind_tools(tools)

async def copywriter(state:CopyWriterState):
    """The main copywriter agent."""
    system_prompt=SystemMessage(content=copywriter_prompt.format(
        current_datetime=datetime.now(),
        linkedin_example=linkedin_example,
        x_example=x_example,
        blog_example=blog_example,
    ))
    response=llm_with_tools.invoke([system_prompt]+state.messages)
    return {"messages":[response]}

async def copywriter_router(state:CopyWriterState)->str:
    """Route to the tools node if the copywriter makes a tool call."""
    if state.messages[-1].tool_calls:
        return "tools"
    return END

builder=StateGraph(CopyWriterState)

builder.add_node(copywriter)
builder.add_node("tools",ToolNode(tools))

builder.set_entry_point("copywriter")

builder.add_conditional_edges(
    "copywriter",
    copywriter_router,
    {
        "tools":"tools",
        END:END,
    }
)
builder.add_edge("tools","copywriter")

graph=builder.compile()
