# Reddit Comment Scraper

This Python program scrapes comments from a specific Reddit user and saves the data in both JSON and text formats. It also provides functionality to filter comments based on specific criteria and send the scraped data to a Discord webhook.

## Features

- Scrapes up to 11,000 _(or how much you want to set it too)_ comments from a specified Reddit user.
- Saves the scraped comments in:
  - A JSON file (`output/<username>_comments.json`).
  - A formatted text file (`output/<username>_comments.txt`).
- Generates a summary file (`output/<username>_summary.json`) with:
  - Total comments made by the user.
  - Number of comments scraped.
- Sends the scraped data to a Discord webhook.
- Allows filtering of comments based on:
  - Minimum score.
  - Specific subreddit.

## Requirements

- Python 3.7 or higher
- The following Python libraries:
  - `praw`
  - `json`
  - `os`
  - `time`
  - `requests`
  - `concurrent.futures`

## Setup

1. Clone or download this repository.
2. Install the required Python libraries:
   ```bash
   pip install praw requests
3. Replace the placeholders in the code with your own credentials:
- **client_id**: Your Reddit app's client ID.
- **client_secret**: Your Reddit app's client secret.
- **user_agent**: A user agent string for your Reddit app.
- **DISCORD_WEBHOOK_URL**: Your Discord webhook URL.

## Usage
Open the script file reddit_scrapper.py.
Set the TARGET_USER variable to the Reddit username you want to scrape.
Run the script:
`python reddit_scrapper.py`

4. The program will:
- Fetch comments from the specified user.
- Save the comments in JSON and text formats in the output directory.
- Generate a summary file with the total and scraped comment counts.
- Send the data to the specified Discord webhook.

## Filtering Comments
The program includes a filtering function to extract comments based on specific criteria:

- Minimum score.
- Subreddit.
Example usage:
`filtered = filter_comments(saved_data, min_score=10, subreddit="example_subreddit")`

## Output Files
- **JSON File**: Contains all scraped comments in structured JSON format.
- **Text File**: Contains all scraped comments in a human-readable format.
- **Summary File**: Contains metadata about the scraping process.

### Example Output
JSON File (output/<username>_comments.json):
```[
  {
    "comment_id": "abc123",
    "subreddit": "example_subreddit",
    "body": "This is a comment.",
    "created_utc": 1670000000.0,
    "score": 10,
    "permalink": "https://www.reddit.com/r/example_subreddit/comments/abc123"
  }
]
```
```
Text File (output/<username>_comments.txt):
Subreddit: example_subreddit
Score: 10
Comment: This is a comment.
Permalink: https://www.reddit.com/r/example_subreddit/comments/abc123
Created UTC: 1670000000.0
```
--------------------------------------------------------------------------------

Summary File (output/<username>_summary.json):
```
{
  "username": "example_user",
  "total_comments": 500,
  "scraped_comments_count": 100
}
```
### Notes
- The program uses the Reddit API via the praw library to fetch comments.
- Ensure your Reddit app credentials are valid and have the necessary permissions.
- The Discord webhook URL must be valid to send data successfully.
