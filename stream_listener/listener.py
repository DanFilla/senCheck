import tweepy
import datetime
import csv

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

class MyStreamListener(tweepy.StreamListener):
    dem_handles = []
    rep_handles = []

    def load(self, dem_handles, rep_handles):
        self.dem_handles = dem_handles
        self.rep_handles = rep_handles

    def on_status(self, status):

        if (from_creator(status)):
            #find what part the id is from and open that file.
            if status.user._json['id_str'] in self.dem_handles:
                party = "Democrate"
                opened_file = open("stream_data/dem_tweets.csv", "a")
            elif status.user._json['id_str'] in self.rep_handles:
                party = "Republican"
                opened_file = open("stream_data/rep_tweets.csv", "a")

            fieldnames = ["user_name", "status", "datetime"]
            tweet_data = csv.DictWriter(opened_file, fieldnames=fieldnames)

            user_name = status._json['user']['name']
            date_time = datetime.datetime.now()

            print(f"Senator {user_name} has tweeted from the {party} party.")

            #Save tweet to csv file
            if hasattr(status, "retweeted_status"):
                try:
                    extended_user_status = status.retweeted_status.extended_tweet["full_text"]
                    tweet_data.writerow({"user_name": user_name, 'status': extended_user_status, 'datetime': date_time})
                except AttributeError:
                    user_status = status.retweeted_status.text
                    tweet_data.writerow({"user_name": user_name, 'status': user_status, 'datetime': date_time})

            else:
                try:
                    extended_user_status = status.extended_tweet["full_text"]
                    tweet_data.writerow({"user_name": user_name, 'status': extended_user_status, 'datetime': date_time})
                except AttributeError:
                    user_status = status.text
                    tweet_data.writerow({"user_name": user_name, 'status': user_status, 'datetime': date_time})
        else:
            print(f"ignored Democrate status {datetime.datetime.now()}")
            print(f"{status.user._json['id']}")
