import os
import asyncio
from fastapi import FastAPI, HTTPException, Query
from twscrape import API, gather
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize the API (You can also pass a custom database path)
api = API()

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

@app.on_event("startup")
async def startup_event():
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    email = os.environ.get("EMAIL") 

    # Add accounts at startup
    await api.pool.add_account(username, password, email, password)
    await api.pool.login_all()

def classify_sentiment(compound_score):
    if compound_score >= 0.05:
        return "pos"
    elif compound_score <= -0.05:
        return "neg"
    else:
        return "neu"

@app.get("/search")
async def search_tweets(query: str, limit: int = Query(20, ge=1, le=100), product: str = Query("Top")):
    """
    Search tweets with optional limit and product query parameters.

    Args:
        query (str): The search query.
        limit (int): The maximum number of tweets to fetch (default is 20).
        product (str): The search type, can be "Top", "Latest", or "Media" (default is "Top").

    Returns:
        JSON response containing the tweets and their sentiment analysis.
    """
    try:
        # Fetch tweets using the search query with the given limit and product type
        tweets = await gather(api.search(query, limit=limit, kv={"product": product}))

        filtered_tweets = []
        sentiment_scores = {"pos": 0, "neu": 0, "neg": 0}

        for tweet in tweets:
            sentiment = analyzer.polarity_scores(tweet.rawContent)
            score = classify_sentiment(sentiment["compound"])

            # Update sentiment count for overall sentiment calculation
            sentiment_scores[score] += 1

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
                "sentiment": {
                    "neg": sentiment["neg"],
                    "neu": sentiment["neu"],
                    "pos": sentiment["pos"],
                    "compound": sentiment["compound"],
                    "score": score
                }
            }
            filtered_tweets.append(filtered_tweet)

        # Determine overall sentiment based on majority
        if sentiment_scores["pos"] > sentiment_scores["neg"] and sentiment_scores["pos"] > sentiment_scores["neu"]:
            overall_sentiment = "pos"
        elif sentiment_scores["neg"] > sentiment_scores["pos"] and sentiment_scores["neg"] > sentiment_scores["neu"]:
            overall_sentiment = "neg"
        else:
            overall_sentiment = "neu"

        return {
            "query": query,
            "overall_sentiment": overall_sentiment,
            "tweets": filtered_tweets
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))