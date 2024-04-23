from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Pentagoan Chart // Radar Chart


# Load CSV file containing tweets
# import os
# csv_file_path = os.path.abspath('./application/cooking.csv')
# df = pd.read_csv(csv_file_path)


# # Extract tweets from the second column named 'tweet'
# tweets = df['tweet']

# Initialize the Vader sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to categorize words based on sentiment scores
def categorize_words(tweet):
    words = word_tokenize(tweet)
    sentiments = [analyzer.polarity_scores(word) for word in words]
    positive_words = [word for word, sentiment in zip(words, sentiments) if sentiment['compound'] > 0]
    negative_words = [word for word, sentiment in zip(words, sentiments) if sentiment['compound'] < 0]
    neutral_words = [word for word, sentiment in zip(words, sentiments) if sentiment['compound'] == 0]
    return positive_words, negative_words, neutral_words



def raderdata(df):
    tweets = df['tweet']
    # Initialize counters for positive, negative, and neutral words
    positive_counter = Counter()
    negative_counter = Counter()
    neutral_counter = Counter()

    # Perform sentiment analysis for each tweet and count words
    for tweet in tweets:
        positive_words, negative_words, neutral_words = categorize_words(tweet)
        positive_counter.update(positive_words)
        negative_counter.update(negative_words)
        neutral_counter.update(neutral_words)



    # Get the top 5 positive, negative, and neutral words
    top_positive_words = dict(positive_counter.most_common(5))
    top_negative_words = dict(negative_counter.most_common(5))
    top_neutral_words = dict(neutral_counter.most_common(5))

    # Print or do anything you need with these top words
    print("Top 5 Positive Words:", top_positive_words)
    print("Top 5 Negative Words:", top_negative_words)
    print("Top 5 Neutral Words:", top_neutral_words)

    return top_positive_words,top_negative_words,top_neutral_words

# data = raderdata()

# print(data)