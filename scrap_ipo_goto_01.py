import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "IPO GOTO OR saham GOTO OR IHSG lang:id since:2022-04-09 until:2022-04-14"
tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 1000:  # batasi 1000 tweet maksimal
        break
    tweets.append([tweet.date, tweet.content, tweet.user.username,
                   tweet.likeCount, tweet.retweetCount, tweet.replyCount])

df = pd.DataFrame(tweets, columns=["date","content","username","likeCount","retweetCount","replyCount"])
df.to_csv("ipo_goto_tweets.csv", index=False)
df.head()
