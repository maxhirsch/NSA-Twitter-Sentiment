import got3 as got
import datetime as dt
from tqdm import tqdm

def printTweet(descr, t):
        print(descr)
        print("Username: %s" % t.username)
        print("Date: %s" % t.date)
        print("Retweets: %d" % t.retweets)
        print("Text: %s" % t.text)
        print("Mentions: %s" % t.mentions)
        print("Hashtags: %s\n" % t.hashtags)

#start_date = dt.datetime(2008, 6, 6)
start_date = dt.datetime(2016, 10, 22)
end_date = dt.datetime(2016, 10, 23) # not inclusive

tweetCriteria = got.manager.TweetCriteria()
tweetCriteria = tweetCriteria.setQuerySearch('nsa')
tweetCriteria = tweetCriteria.setLang("en")
tweetCriteria = tweetCriteria.setMaxTweets(100)
tweetCriteria = tweetCriteria.setTopTweets(True)

with open('twitter_data4.csv', 'w') as f:
    f.write("date,text,retweets,favorites")
    for i in tqdm(range((end_date - start_date).days)):
        cur_start = start_date + dt.timedelta(i)
        cur_end = cur_start + dt.timedelta(1)

        tweetCriteria = tweetCriteria.setSince(str(cur_start)[:10])
        tweetCriteria = tweetCriteria.setUntil(str(cur_end)[:10])

        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        for tweet in tweets:
            try:
                f.write(str(tweet.date) + "," + str(tweet.text).replace(",", "") + "," + \
                    str(tweet.retweets) + "," + str(tweet.favorites) + "\n")
            except: pass