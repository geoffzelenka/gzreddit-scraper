import json
import praw


# Expects a json file in the current working directory 
# that is named '.creds' and contains the following fields
#   REDDIT_KEY: reddit app client id
#   REDDIT_SECRET: reddit app secret
#   USER_AGENT: this apps user agent

class Reddit:
    def __init__(self):
        with open('.creds', 'r') as credfile:
            self.creds = json.load(credfile)

        print(self.creds)

        self.reddit = praw.Reddit(
            client_id=self.creds['REDDIT_KEY'],
            client_secret=self.creds['REDDIT_SECRET'],
            user_agent=self.creds['USER_AGENT']
        )

        print(f"Reddit instance is read-only: {self.reddit.read_only}")

    def get_test_posts(self):
        for p in self.reddit.subreddit("test").hot(limit=10):
            print(p.title)


if __name__ == "__main__":
    r = Reddit()

    r.get_test_posts()


