import re
import pandas as pd
from textblob import TextBlob

def clean_tweet(tweet): 
    return re.sub("(@ \S+ )|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", str(tweet))

def get_tweet_polarity(tweet): 
    analysis = TextBlob(clean_tweet(tweet)) 
    return analysis.sentiment.polarity

def get_tweet_subjectivity(tweet): 
    analysis = TextBlob(clean_tweet(tweet)) 
    return analysis.sentiment.subjectivity

df = pd.read_csv("aggregated_twitter_data.csv", encoding = "ISO-8859-1")
df["text"] = df["text"].map(lambda tweet: clean_tweet(tweet))
df["polarity"] = df["text"].map(lambda tweet: get_tweet_polarity(tweet))
df["subjectivity"] = df["text"].map(lambda tweet: get_tweet_subjectivity(tweet))

df.to_csv("./cleaned_twitter_data.csv", index = None, header = True)