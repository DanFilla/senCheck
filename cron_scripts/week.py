#!/usr/bin/env python3

import sys
path_to_root = __file__[:27]
sys.path.append(path_to_root)

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
from trending_words import trending_words

plt.close('all')
matplotlib.use('Agg')

consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

key = os.environ["KEY"]
secret = os.environ["SECRET"]

dem_df = pd.read_csv(path_to_root + "/stream_data/dem_tweets.csv")
rep_df = pd.read_csv(path_to_root + "/stream_data/rep_tweets.csv")

today = datetime.datetime.today()
today = today.strftime(today.strftime("%b-%d-%Y"))

#Get week range.
week_end = datetime.datetime.today()
week_start = week_end - datetime.timedelta(days=7)
week_range = range(week_start.day, week_end.day)

#Republican day and hour tweet dataframe. key = day
#                                             value = array of the hours each tweet was tweeted.


#collecting tweet data for Republicans
rep_date_list = {}
for j in range(len(rep_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(rep_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
    if day == week_start.day-1:
        break
    rep_date_list[day] = []

for i in range(len(rep_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
    hour = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
    if day == week_start.day-1:
        break
    rep_date_list[day] = rep_date_list.get(day) + [hour]

#Collecting tweet data for Democrats
dem_date_list = {}
for j in range(len(dem_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
    if day == week_start.day-1:
        break
    dem_date_list[day] = []

for i in range(len(dem_df['datetime'])-1, 0, -1):
    day = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
    hour = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
    if day == week_start.day-1:
        break
    dem_date_list[day] = dem_date_list.get(day) + [hour]

rep_week_plot = []
dem_week_plot = []
for day_add in range(7):
    num = (week_start + datetime.timedelta(days=day_add)).day
    try:
        rep_week_plot.append(len(rep_date_list.get(num)))
    except TypeError:
        rep_week_plot.append(0)

    try:
        dem_week_plot.append(len(dem_date_list.get(num)))
    except TypeError:
        dem_week_plot.append(0)


#save graph
plt.plot(range(1, 8), rep_week_plot, label="Republicans", color="r")
plt.plot(range(1, 8), dem_week_plot, label="Democrats", color="b")
plt.legend(loc="upper left")
plt.xlabel("Days")
plt.ylabel("Number of Tweets")
plt.savefig(f"{today}_weekplt.png", bbox_inches="tight")

#tweet the graph
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

api.update_with_media(f"{today}_weekplt.png", status=trending_words(rep_df, dem_df))

os.remove(f"{today}_weekplt.png")
#rep_df = pd.DataFrame(columns=rep_df.columns)
#dem_df = pd.DataFrame(columns=dem_df.columns)

