import pandas as pd
from transformers import pipeline
from newspaper import Article

# Load pre-trained sentiment analysis model
sentiment_analysis = pipeline('sentiment-analysis')

# Function to analyze sentiment for an article link
def analyze_article_sentiment(company, article_link):
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

        print(f"Company: {company}")
        print(f"Article Link: {article_link}")
        print(f"Sentiment: {sentiment} (Score: {score:.2f})\n")

        return sentiment

    except Exception as e:
        print(f"Error analyzing sentiment for {article_link}: {str(e)}")
        # Continue to the next iteration
        return None

# Function to parse and write URLs to an Excel file
def parse_and_write_to_excel(input_file, output_excel):
    data = {'Company': [], 'Link': [], 'Sentiment': []}

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Parse and extract company name and URLs from each line
    for line in lines:
        line_elements = line.split(';')
        if len(line_elements) > 1:
            company = line_elements[0].strip()
            link = line_elements[1].strip()
            sentiment = analyze_article_sentiment(company, link)
            data['Company'].append(company)
            data['Link'].append(link)
            data['Sentiment'].append(sentiment)

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    df.to_excel(output_excel, index=False)

# Read the links from 'results.txt' and store them in 'article.xlsx'
input_file_path = 'results.txt'
output_excel_path = 'article.xlsx'

parse_and_write_to_excel(input_file_path, output_excel_path)
