#!/usr/bin/env python

import argparse
import json
import sys
import time
import os
import twitter
from dateutil.parser import parse

__author__ = "Hakan Ozalan"
__version__ = "0.1"

def delete(api, date, r):
    with open("tweet.js") as file:
	d = json.load(file)
        count = 0
        for row in d:
            tweet_id = int(row["id"])
            tweet_date = parse(row["created_at"], ignoretz=True).date()

            if date != "" and tweet_date >= parse(date).date():
                continue

            if (r == "retweeted" and row["retweeted_status_id"] == "" or
                    r == "reply" and row["in_reply_to_status_id"] == ""):
                continue

            try:
                print "Deleting tweet #{0} ({1})".format(tweet_id, tweet_date)

                api.DestroyStatus(tweet_id)
                count += 1
                time.sleep(0.1)

            except twitter.TwitterError, err:
                print "Exception: %s\n" % err.message

    print "Number of deleted tweets: %s\n" % count

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")

    args = parser.parse_args()

    api = twitter.Api(consumer_key="",
                      consumer_secret="",
                      access_token_key="",
                      access_token_secret="")

    delete(api, args.date, args.restrict)


if __name__ == "__main__":
    main()
