from stream_listener.listener import MyStreamListener
import os
import tweepy
import logging
import datetime
import time
import csv

class master_stream:

    dem_handles = [
	"239548513",
	"20747881",
	"476256944",
	"30354991",
	"45645232",
	"278124059",
	"150078976",
	"381577682",
	"15324851",
	"47747074",
	"92186819",
	"247334603",
	"1058520120",
	"109071031",
	"18137749",
	"970207298",
	"1129029661",
	"76456274",
	"145292853",
	"33537967",
	"47724293",
	"515822213",
	"3145735852",
	"4749863113",
	"14125897",
	"946549322",
	"18695134",
	"15808765",
	"60828944",
	"1099199839",
	"17494010",
	"899978622416695297",
	"43910797",
	"250188760",
	"223166587",
	"171598736",
	"486694111",
	"242555999",
	"242836537",
	"7429102",
	"172858784",
	"293131808",
	"35567751",
	"234374703",
	"87510313", ]

    rep_handles = [
        "21111098",
	"18061669",
	"2891210047",
	"2964949642",
	"968650362",
	"968650362",
	"235217558",
	"15745368",
	"306389855",
	"2863210809",
	"1200451909406121984",
	"600463589",
	"1096059529",
	"234128524",
	"1080870981877534720",
	"10615232",
	"2856787757",
	"75364211",
	"18632666",
	"1249982359",
	"216881337",
	"55677432",
	"816683274076614656",
	"19726613",
	"264219447",
	"262192574",
	"21269970",
	"2352629311",
	"11651202",
	"323490669",
	"1480852568",
	"21157904",
	"22195441",
	"382791093",
	"1048784496",
	"18915145",
	"7270292",
	"27044466",
	"221162525",
	"432895323",
	"217543151",
	"296361085",
	"2955485182",
	"76649729",
	"278145569",
	"1648117711",
	"23022687",
	"88784440",
	"50055701",
	"193794406",
	"233737858",
	"291756142", ]

    consumer_key = os.environ["CONSUMER_KEY"]
    consumer_secret = os.environ["CONSUMER_SECRET"]

    key = os.environ["KEY"]
    secret = os.environ["SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStreamListener.load(dem_handles, rep_handles)

    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    def __init__(self):
        logging.basicConfig(filename="logs/logs.log")

        open("stream_data/rep_tweets.csv", "a").close()
        open("stream_data/dem_tweets.csv", "a").close()

        self.check_headers()

        while(1):
            try:
                print("connecting to stream...")
                master_stream.myStream.filter(master_stream.dem_handles + master_stream.rep_handles)
            except:
                logging.error(f"Stream Failed {datetime.datetime.now()}")
                time.sleep(10)


    def check_headers(self):
        with open("stream_data/rep_tweets.csv", newline='') as csv_file:
            rea = csv.reader(csv_file)
            has_header = False
            for x in rea:
                if x == ['user_name', 'status', 'datetime']:
                    has_header = True
                break

        if not has_header:
            with open("stream_data/rep_tweets.csv", "w") as csv_file:
                    fieldnames = ["user_name", "status", "datetime"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()

        has_header = False
        with open("stream_data/dem_tweets.csv", newline='') as csv_file:
            rea = csv.reader(csv_file)
            has_header = False
            for x in rea:
                if x == ['user_name', 'status', 'datetime']:
                    has_header = True
                break

        if not has_header:
            with open("stream_data/dem_tweets.csv", "w") as csv_file:
                    fieldnames = ["user_name", "status", "datetime"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
