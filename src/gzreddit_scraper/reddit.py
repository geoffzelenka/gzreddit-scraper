import os
import praw

from dotenv import load_dotenv



# Expects a '.env' file in the current working directory 
#   REDDIT_KEY="reddit app client id"
#   REDDIT_SECRET="reddit app secret"
#   USER_AGENT="this apps user agent"

class Reddit:
    def __init__(self):
        load_dotenv()
        required_vars = ['REDDIT_KEY', 'REDDIT_SECRET', 'USER_AGENT']
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_KEY'),
            client_secret=os.getenv('REDDIT_SECRET'),
            user_agent=os.getenv('USER_AGENT')
        )

    def get_test_posts(self):
        for p in self.reddit.subreddit("test").hot(limit=10):
            print(p.title)


if __name__ == "__main__":
    r = Reddit()

    r.get_test_posts()


