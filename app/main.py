import asyncio
import os
from fastapi import FastAPI, Header, HTTPException
from twscrape import API, gather
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize the API (You can also pass a custom database path)
api = API()

# Add accounts to the API pool (usually, you would load these from a secure source)
# For demonstration purposes, you can hardcode or use env variables

@app.on_event("startup")
async def startup_event():
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    email = os.environ.get("EMAIL") 
    # Load accounts (In a real scenario, you might load these from a secure source)
    await api.pool.add_account(username, password, email, password)
    await api.pool.login_all()

@app.get("/search")
async def search_tweets(query: str):
    # (In this example, assume login and account management is already handled at startup)
    try:
        # Fetch tweets using the search query
        tweets = await gather(api.search(query, limit=20, kv={"product": "Top"}))

        # Filter and return only the required information
        filtered_tweets = []
        for tweet in tweets:
            filtered_tweet = {
                "date": tweet.date,
                "username": tweet.user.username,
                "displayname": tweet.user.displayname,
                "followers_count": tweet.user.followersCount,
                "raw_content": tweet.rawContent,
                "reply_count": tweet.replyCount,
                "quote_count": tweet.quoteCount,
                "like_count": tweet.likeCount,
                "bookmark_count": tweet.bookmarkedCount,
            }
            filtered_tweets.append(filtered_tweet)

        return {"query": query, "tweets": filtered_tweets}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# To run the API, use the command: uvicorn script_name:app --reload