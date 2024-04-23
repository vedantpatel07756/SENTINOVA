import pandas as pd
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Load the CSV file
# csv_file_path = './application/cooking.csv'
# df = pd.read_csv(csv_file_path)

# Extract tweets from the 'tweet' column
# tweets = df['tweet']

# Function to extract hashtags from tweets
def extract_hashtags(tweet):
    return re.findall(r'#(\w+)', tweet)

# Function to extract mentions from tweets
def extract_mentions(tweet):
    return re.findall(r'@(\w+)', tweet)

# Function to calculate character count distribution
def calculate_char_count_distribution(tweet):
    # Remove whitespaces from the tweet
    tweet = tweet.replace(" ", "")
    # Calculate character count distribution
    char_count_distribution = Counter(len(word) for word in tweet)
    return char_count_distribution



def bar_data(df):
    tweets = df['tweet']
    # Initialize counters for hashtag, mention, and URL frequencies
    hashtag_counter = Counter()
    mention_counter = Counter()
    # Initialize counter for character count distribution
    char_count_distribution_counter = Counter()
    total_char_count = 0
    total_tweets = 0  # Counter for total tweets
    total_hashtags = 0  # Counter for total hashtags
    total_mentions = 0  # Counter for total mentions

# Extract and count hashtags, mentions, and URLs from each tweet
    for tweet in tweets:
        total_tweets += 1  # Increment total_tweets counter
        hashtags = extract_hashtags(tweet)
        mentions = extract_mentions(tweet)
        hashtag_counter.update(hashtags)
        mention_counter.update(mentions)
        char_count_distribution = calculate_char_count_distribution(tweet)
        char_count_distribution_counter.update(char_count_distribution)
        total_char_count += sum(char_count_distribution.values())
        total_hashtags += len(hashtags)
        total_mentions += len(mentions)

    return total_tweets,total_hashtags,total_mentions


# data=bar_data()
# print("data=",data)
# # Print the total number of tweets, hashtags, mentions, and character count distribution
# print("Total Tweets:", total_tweets)
# print("Total Hashtags:", total_hashtags)
# print("Total Mentions:", total_mentions)
# print("Character Count Distribution:", dict(char_count_distribution_counter))
