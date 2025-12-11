#!/usr/bin/env python3

import re
import time

from . import reddit

from datetime import datetime
from pprint import pprint


class RedditScraper:
    """Read submissions and comments from reddit subreddits and turn to
       json and store in s3"""

    def __init__(self, subreddit=None):
        self._subreddit = subreddit
        self._reddit = reddit.Reddit()


    def _clean_text(self, text):
        text = re.sub(r'http\S+', '', text)  # remove links
        text = re.sub(r'[^A-Za-z0-9$ .,!?\'"\-]+', ' ', text)
        return text.strip()


    def _process_comment_tree(self, parent_sub_id, comment_tree):
        """Process a comment tree into json to persist"""
        comment_tree.replace_more(limit=0) 
        comments = comment_tree.list()
        comment_data = [
                {
                    'id': c.id,
                    'author': c.author.name if c.author else None,
                    'body': self._clean_text(c.body),
                    'score': c.score,
                    'created_utc': c.created_utc,
                    'permalink': c.permalink,
                    'parent_id': c.parent_id,
                    'submission': parent_sub_id
                }
                for c in comments
        ]
        return comment_data


    def _process_submissions(self, submissions):
        """Iterate through the submissions and jsonify them
           while processing the comments therein"""
        date = datetime.now()

        data = {
               'collected_at': date.isoformat(),
               'subreddit': self._subreddit,
               'submissions': [
                   {
                       'id': sub.id,
                       'author': sub.author.name if sub.author else None,
                       'name': sub.name,
                       'title': sub.title,
                       'selftext': sub.selftext,
                       'created_utc': sub.created_utc,
                       'num_comments': sub.num_comments,
                       'score': sub.score,
                       'score_ration': sub.upvote_ratio,
                       'comments': self._process_comment_tree(sub.id, sub.comments)
                  }
                  for sub in submissions
               ]
        }

    def _do_something_with_data(self, data):
        """TODO: Replace this with a useful method"""
        pprint(data)



    def get_submissions(self):
        twenty_four_hours_ago =  time.time() - 24 * 60 * 60
        submissions = self._reddit.get_new_posts(self._subreddit, time_since = twenty_four_hours_ago)
        data = self._process_submissions(submissions)
        self._do_something_with_data(data)


def main():
    test_scraper = RedditScraper("test")
    test_scraper.get_submissions()


if __name__ == "__main__":
    main()
