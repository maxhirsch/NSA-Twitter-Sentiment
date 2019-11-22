import requests
import got3
session = requests.session()
keyword = 'nsa'
start_date = '2010-01-01'
end_date = '2019-11-01'

#response = session.get(f'https://twitter.com/search?l=&q=%23{keyword}%20since%3A\
#                        {start_date}%20until%3A{end_date}&src=typd')

response = session.get("https://twitter.com/search?q=%23surveillance%20since%3A2015-05-01%20until%3A2019-07-31&src=typed_query")

tweets = response.content
#print(tweets)

print("Writing tweets to file")
with open('twitter_data.txt', 'w') as f:
    # get new line characters good
    s = ""
    for c in str(tweets):
        s += c
    s = s.split('\\n')
    
    for line in s:
        f.write(line + '\n')
