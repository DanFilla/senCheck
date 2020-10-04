from keys import secret_keys
import threading
import tweepy
from stream_classes.master_stream import master_stream

if __name__ == "__main__":
    go = master_stream()
