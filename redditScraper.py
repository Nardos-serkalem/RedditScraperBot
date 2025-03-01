import praw
import json
import time
from textblob import TextBlob

# 🔹 Reddit API Credentials (Ensure correct credentials are set)
reddit = praw.Reddit(
    client_id="5kF3eMGlMTkLopBRcEgw3w",
    client_secret="Fao_Ga0ledGsDqDyaHsjUZdf660L2Q",
    user_agent="Bot/1.0 (by u/Dramatic_Forever_546)"
)

def fetch_saas_ideas(subreddit_name="entrepreneur", limit=50):
    """Fetches SaaS ideas from Reddit."""
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search("saas idea", limit=limit)

    saas_ideas = []
    
    for post in posts:
        try:
            # Load a few top-level comments (to prevent rate-limiting issues)
            post.comments.replace_more(limit=2)
            comments = [comment.body for comment in post.comments.list()[:10] if hasattr(comment, "body")]
            
            saas_ideas.append({
                "title": post.title,
                "upvotes": post.score,
                "num_comments": post.num_comments,
                "comments": comments
            })
            
            time.sleep(1)  # Prevent Reddit API rate-limiting
            
        except Exception as e:
            print(f"⚠️ Error processing post: {post.title} | {e}")

    return saas_ideas

def get_sentiment(text):
    """Calculates sentiment score using TextBlob (range: -1 to 1)."""
    return TextBlob(text).sentiment.polarity 

def rank_saas_ideas(saas_ideas):
    """Ranks SaaS ideas based on a weighted scoring system."""
    for idea in saas_ideas:
        comment_sentiments = [get_sentiment(c) for c in idea["comments"]]
        avg_sentiment = sum(comment_sentiments) / (len(comment_sentiments) or 1)  # Avoid division by zero

        idea["sentiment"] = avg_sentiment
        idea["score"] = idea["upvotes"] * 2 + idea["num_comments"] + avg_sentiment * 10  

    return sorted(saas_ideas, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    print("🔍 Fetching SaaS ideas from Reddit...")
    saas_ideas = fetch_saas_ideas()

    if not saas_ideas:
        print("❌ No SaaS ideas found. Try again later.")
    else:
        ranked_ideas = rank_saas_ideas(saas_ideas)

        # Save raw data
        with open("saas_ideas.json", "w") as f:
            json.dump(saas_ideas, f, indent=4)

        # Save sorted data
        with open("sorted_saas_ideas.json", "w") as f:
            json.dump(ranked_ideas, f, indent=4)

        print(f"✅ Successfully saved {len(ranked_ideas)} SaaS ideas to sorted_saas_ideas.json")

        # Display top 10 ideas
        for idea in ranked_ideas[:10]: 
            print(f"\n🔹 **{idea['title']}**\n   👍 Upvotes: {idea['upvotes']} | 💬 Comments: {idea['num_comments']} | 😃 Sentiment: {idea['sentiment']:.2f} | 📊 Score: {idea['score']:.2f}\n---")
