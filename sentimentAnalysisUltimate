from transformers import pipeline

# Load pre-trained sentiment analysis model
sentiment_analysis = pipeline('sentiment-analysis')

# Function to analyze sentiment for an article link
def analyze_article_sentiment(article_line):
    try:
        # Split the line using semicolons and take the second index (URL)
        article_link = article_line.split(';')[1].strip()

        # Analyze sentiment for the article link
        result = sentiment_analysis(article_link)
        label = result[0]['label']
        score = result[0]['score']

        sentiment = "positive" if label == "POSITIVE" else "negative"

        print(f"Article Link: {article_link}")
        print(f"Sentiment: {sentiment} (Score: {score:.2f})\n")

    except Exception as e:
        print(f"Error analyzing sentiment for {article_line}: {str(e)}")
        # Continue to the next iteration

# Example article links
file_path = 'results.txt'  # Replace 'your_file.txt' with the actual file path

# Read the file and store each line in an array
with open(file_path, 'r') as file:
    lines_array = [line.strip() for line in file if 'company_name' in line]

# Display the array of lines
print(lines_array)

# Analyze sentiment for each article link
for line in lines_array:
    analyze_article_sentiment(line)
