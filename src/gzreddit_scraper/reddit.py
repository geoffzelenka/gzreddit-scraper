import os
import praw
import time

from datetime import datetime
from dotenv import load_dotenv



# Expects a '.env' file in the current working directory 
#   REDDIT_KEY="reddit app client id"
#   REDDIT_SECRET="reddit app secret"
#   USER_AGENT="this apps user agent"

class Reddit:
    def __init__(self):
        """Initialize our PRAW wrapper using our .env creds"""
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

        #some stats of what we've done
        self.submissions = 0
        self.comments = 0

    def get_test_posts(self):
        """Get the last 10 posts from the "hot" sort of the "test" subreddit"""
        for p in self.reddit.subreddit("test").hot(limit=10):
            print(p.title)


    def get_new_posts(self, subreddit, time_since = 0, max_posts=None):
        """Get posts from a specified subreddit, can limit by number of posts or number of seconds back to go"""
        sub = self.reddit.subreddit(subreddit)
        posts = []

        for submission in sub.new(limit=max_posts):
            if submission.created_utc > time_since:
                posts.append(submission)
            else:
                break

        self.submissions += len(posts)
        print(f"Found {len(posts)} since {datetime.fromtimestamp(time_since)}")

        return posts

    def get_stickied_posts(self, subreddit_name, title_filter=None):
        """Get the pinned posts of a particular subreddit, with optional title filter"""
        subreddit = self.reddit.subreddit(subreddit_name)

        stickied_posts = []
        for i in [1, 2]:
            try:
                stickied_posts.append(subreddit.sticky(number=i))
            except praw.exceptions.NotFound:
                pass

        if title_filter:
            stickied_posts = [ post for post in stickied_posts if title_filter in post.title ]

        return stickied_posts




if __name__ == "__main__":
    r = Reddit()

    ten_mins_ago = time.time() - (10 * 60)
    ten_hours_ago = time.time() - (10 * 60 * 60)

    new_posts = r.get_new_posts("test",ten_hours_ago)

    print(new_posts[0])

    for p in new_posts:
        print(f"{p.title} ({p.num_comments}) - {datetime.fromtimestamp(p.created_utc)} - {p.subreddit.display_name}")
