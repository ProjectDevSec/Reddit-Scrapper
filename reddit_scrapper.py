import praw
import json
import os
import time
import requests  # Add this import for sending data to Discord webhook
from concurrent.futures import ThreadPoolExecutor  # For parallel processing

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",  # Replace with your Reddit app's client ID (Get it at https://old.reddit.com/prefs/apps) 
    client_secret="YOUR_CLIENT_SECRET",  # Replace with your Reddit app's client secret (Get it here too https://old.reddit.com/prefs/apps)
    user_agent="RedditCommentScraper/1.0"  # Replace with your user agent
)

# Target Reddit user
TARGET_USER = "USER_TARGET"  # Replace with the Reddit username you want to scrape / Ex: "reddit", not "u/reddit"

# Ensure the user exists
try:
    redditor = reddit.redditor(TARGET_USER)
    redditor.id  # Accessing the ID to ensure the user exists
    print(f"User @{TARGET_USER} found.")
except Exception as e:
    print(f"Failed to load user @{TARGET_USER}: {e}")
    exit(1)

# Scrape comments
comments = []
print(f"Fetching comments made by @{TARGET_USER}...")
max_comments = 11000  # Limit the number of comments to scrape (You can set it as much as you want)
retry_attempts = 3  # Reduce retry attempts
retry_delay = 2  # Reduce delay between retries

def fetch_comment_data(comment):
    """Fetch and format comment data."""
    return {
        "comment_id": comment.id,
        "subreddit": comment.subreddit.display_name,
        "body": comment.body,
        "created_utc": comment.created_utc,
        "score": comment.score,
        "permalink": f"https://www.reddit.com{comment.permalink}"
    }

try:
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        fetched_comments = redditor.comments.new(limit=max_comments)
        comments = list(executor.map(fetch_comment_data, fetched_comments))
except Exception as e:
    print(f"Error: {e}. Please try again later.")
    exit(1)

# Save to file
os.makedirs("output", exist_ok=True)
with open(f"output/{TARGET_USER}_comments.json", "w") as f:
    json.dump(comments, f, indent=2)

print(f"Saved {len(comments)} comments to output/{TARGET_USER}_comments.json")

# Save comments to a .txt file with proper formatting
comments_txt_path = f"output/{TARGET_USER}_comments.txt"
with open(comments_txt_path, "w", encoding="utf-8") as f:  # Specify UTF-8 encoding
    for comment in comments:
        f.write(f"Subreddit: {comment['subreddit']}\n")
        f.write(f"Score: {comment['score']}\n")
        f.write(f"Comment: {comment['body']}\n")
        f.write(f"Permalink: {comment['permalink']}\n")
        f.write(f"Created UTC: {comment['created_utc']}\n")
        f.write("-" * 80 + "\n")

print(f"Saved comments to {comments_txt_path}")

# Count total comments
try:
    total_comments = redditor.comment_karma  # Total comment karma (proxy for activity)
    print(f"Total comments made by @{TARGET_USER}: {total_comments}")
except Exception as e:
    print(f"Error fetching total comments for @{TARGET_USER}: {e}")
    total_comments = None

# Save total comments count to a separate JSON file
summary_data = {
    "username": TARGET_USER,
    "total_comments": total_comments,
    "scraped_comments_count": len(comments)
}

with open(f"output/{TARGET_USER}_summary.json", "w") as f:
    json.dump(summary_data, f, indent=2)

print(f"Saved summary to output/{TARGET_USER}_summary.json")

# Send data to Discord webhook
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK"  # Replace with your webhook URL

def send_to_discord_with_file(webhook_url, username, total_comments, scraped_count, file_path):
    """Send summary data and comments file to a Discord webhook."""
    message = {
        "content": f"Scraping completed for user @{username}.\n"
                   f"Total comments: {total_comments}\n"
                   f"Scraped comments: {scraped_count}"
    }
    try:
        with open(file_path, "rb") as file:
            response = requests.post(
                webhook_url,
                data=message,
                files={"file": (f"{username}_comments.txt", file)}
            )
        if response.status_code == 204:
            print("Successfully sent data and file to Discord webhook.")
        else:
            print(f"Failed to send data to Discord webhook. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to Discord webhook: {e}")

# Call the function to send data and file to Discord
send_to_discord_with_file(DISCORD_WEBHOOK_URL, TARGET_USER, total_comments, len(comments), comments_txt_path)

# Filtering example
def filter_comments(data, min_score=None, subreddit=None):
    filtered = data
    if min_score is not None:
        filtered = [c for c in filtered if c["score"] >= min_score]
    if subreddit is not None:
        filtered = [c for c in filtered if c["subreddit"].lower() == subreddit.lower()]
    return filtered

# Load saved comments
with open(f"output/{TARGET_USER}_comments.json") as f:
    saved_data = json.load(f)

# Example: Get comments with a score of at least 10 in a specific subreddit
filtered = filter_comments(saved_data, min_score=10, subreddit="example_subreddit")

print(f"Filtered count: {len(filtered)}")
for comment in filtered[:10]:  # Show first 10
    print(f"Subreddit: {comment['subreddit']}, Score: {comment['score']}, Comment: {comment['body']}")
