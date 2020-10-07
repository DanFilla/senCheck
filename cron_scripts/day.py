#!/usr/bin/env python3

import sys
sys.path.append("../")

import tweepy

import matplotlib

import logging

import os
import numpy as np
import pandas as pd
import datetime
import nltk; nltk.download('popular')
from collections import defaultdict
import matplotlib.pyplot as plt
import schedule
import time
from keys import secret_keys


plt.close('all')
matplotlib.use('Agg')

consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

key = os.environ["KEY"]
secret = os.environ["SECRET"]

logging.basicConfig(filename="../logs/logs.log")

dem_df = pd.read_csv("../stream_data/dem_tweets.csv")
rep_df = pd.read_csv("../stream_data/rep_tweets.csv")

current_day = datetime.datetime.today().day
hour_range = range(0, 24)

#Democrate day and hour tweet dataframe. key = day value = hour.

dem_date_list = {}

for j in range(len(dem_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
    if day == current_day-1:
        break
    dem_date_list[day] = []

for i in range(len(dem_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
    hour = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
    if day == current_day-1:
        break
    dem_date_list[day] = dem_date_list.get(day) + [hour]

#Republican day and hour tweet dataframe. key = day
#                                         value = array of the hours each tweet was tweeted.
rep_date_list = {}

for j in range(len(rep_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(rep_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
    if day == current_day-1:
        break
    rep_date_list[day] = []

for i in range(len(rep_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
    hour = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
    if day == current_day-1:
        break
    rep_date_list[day] = rep_date_list.get(day) + [hour]

rep_temp = set(rep_date_list.get(current_day))
dem_temp = set(dem_date_list.get(current_day))

rep_tweet_count = []
dem_tweet_count = []

for num in hour_range:
    if num not in rep_temp:
        rep_tweet_count.append(0)
    else:
        rep_tweet_count.append(rep_date_list.get(current_day).count(num))

    if num not in dem_temp:
        dem_tweet_count.append(0)
    else:
        dem_tweet_count.append(dem_date_list.get(current_day).count(num))

#Save the plot
plt.plot(hour_range, rep_tweet_count, label="Republican", color="r")
plt.plot(hour_range, dem_tweet_count, label="Democrats", color="b")
plt.legend(loc="upper left")
plt.xlabel("Hours")
plt.ylabel("Number of Tweets")

today = datetime.datetime.today()
today = today.strftime(today.strftime("%b-%d-%Y"))

plt.savefig(f"{today}_hourplt.png", bbox_inches="tight")

# Tweet the plot.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

api.update_with_media(f"{today}_hourplt.png")

os.remove(f"{today}_hourplt.png")
