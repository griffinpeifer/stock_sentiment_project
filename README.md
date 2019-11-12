# stock_sentiment_project

This repository contains files which connect to the Twitter API using tweepy, and collect 1% of all tweets while the tweepy script is run. VaderSentiment was used in conjuction with the collected Tweets to provide a sentiment score for each tweet depending on the contents and structure of the text.

A webpage was created using Dash which allows a user to type in a stock symbol and date range to view a stocks performance over time, and show a line graph displaying the stocks performance over time. Additionally users are prompted to type in a Twitter search word of their choice to view the overall sentiment of a topic on Twitter in real time. Using these two charts, a user could speculate on the influence of the sentiment on twitter for a given topic  the performance of a stock.
