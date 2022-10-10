import requests
import praw


class RedditBot:
    def __init__(self):
        # Fighters' database in json
        morph_api_url = "https://api.morph.io/jasonchanhku/ufc_fighters_db/data.json"

        # Keep this key secret!
        morph_api_key = "[api_key]"

        r = requests.get(morph_api_url, params={
            'key': morph_api_key,
            'query': "select * from 'data'"
        })

        self.data = r.json()

    def find_match(self, comment):
        for i, dictionary in enumerate(self.data):
            if ("UfcStatBot " + dictionary['NAME']) in comment.body:
                print("Match found")
                self.make_reply(i, comment)

    def make_reply(self, i, comment):
        dictionary = self.data[i]
        with open("fighters.txt", "w") as f:
            for k, v in dictionary.items():
                f.write("%s: %s\n" % (k, str(v)))
        with open("fighters.txt", "r") as f:
            try:
                comment.reply(f.read())
            except Exception as e:
                print(e)


def main():
    # Authorization to Reddit
    # Put the needed information directly or use environment variables
    reddit = praw.Reddit(
        client_id="",
        client_secret="",
        username="",
        password="",
        user_agent=""
    )
    
    bot = RedditBot()
    subreddit = reddit.subreddit("ufc")
    for comment in subreddit.stream.comments(skip_existing=True):
        bot.find_match(comment)


if __name__ == __main__:
    main()


