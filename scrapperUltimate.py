from transformers import pipeline
from newspaper import Article

# Load pre-trained sentiment analysis model
sentiment_analysis = pipeline('sentiment-analysis')

# Function to analyze sentiment for an article link
def analyze_article_sentiment(article_link):
    try:
        # Download and parse the article
        article = Article(article_link)
        article.download()
        article.parse()

        # Get the article text
        article_text = article.text

        # Limit the article text to the model's maximum sequence length
        max_sequence_length = 512
        truncated_text = article_text[:max_sequence_length]

        # Analyze sentiment for the truncated article
        result = sentiment_analysis(truncated_text)
        label = result[0]['label']
        score = result[0]['score']

        sentiment = "positive" if label == "POSITIVE" else "negative"

        print(f"Article Link: {article_link}")
        print(f"Sentiment: {sentiment} (Score: {score:.2f})\n")

    except Exception as e:
        print(f"Error analyzing sentiment for {article_link}: {str(e)}")
        # Continue to the next iteration

# Example article links
file_path = 'article.txt'  # Replace 'your_file.txt' with the actual file path

# Read the file and store each line in an array
with open(file_path, 'r') as file:
    lines_array = [line.strip() for line in file if 'company_name' in line]

# Display the array of lines
print(lines_array)

article_links = lines_array

# Analyze sentiment for each article link
for link in article_links:
    analyze_article_sentiment(link)
