import praw
import json
from textblob import TextBlob
import streamlit as st

reddit = praw.Reddit(
    client_id="5kF3eMGlMTkLopBRcEgw3w",
    client_secret="Fao_Ga0ledGsDqDyaHsjUZdf660L2Q",
    user_agent="Bot/1.0 (by u/Dramatic_Forever_546)"
)
subreddit = reddit.subreddit("entrepreneur")  
posts = subreddit.search("saas idea", limit=100)  

saas_ideas = []

for post in posts:
    saas_ideas.append({
        "title": post.title,
        "upvotes": post.score,
        "comments": [comment.body for comment in post.comments if hasattr(comment, "body")],
        "num_comments": post.num_comments
    })

with open("saas_ideas.json", "w") as f:
    json.dump(saas_ideas, f, indent=4)

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity 

for idea in saas_ideas:
    idea["sentiment"] = sum(get_sentiment(c) for c in idea["comments"]) / (len(idea["comments"]) or 1)
    idea["score"] = idea["upvotes"] * 2 + idea["num_comments"] + idea["sentiment"] * 10  

saas_ideas = sorted(saas_ideas, key=lambda x: x["score"], reverse=True)

with open("sorted_saas_ideas.json", "w") as f:
    json.dump(saas_ideas, f, indent=4)

for idea in saas_ideas[:10]: 
    print(f"Title: {idea['title']}\nUpvotes: {idea['upvotes']}\nComments: {idea['num_comments']}\nSentiment: {idea['sentiment']:.2f}\nScore: {idea['score']:.2f}\n---")