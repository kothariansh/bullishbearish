import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Function to scrape a news article
def scrape_article(url):
    try:
        response = requests.get(url, timeout=10)  # Adding a 10-second timeout
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        return article_text
    except requests.exceptions.Timeout:
        print(f"Request timed out for URL: {url}")
        return None
    except Exception as e:
        print(f"Error scraping the article at {url}: {e}")
        return None

# Read the Excel file
excel_file = 'scrapped.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(excel_file)

# Initialize data list
data = []

# Process each row in the Excel file
for index, row in df.iterrows():
    url = row[0]  # Assuming the first column contains URLs
    sentiment = row[1].lower()  # Assuming the second column contains sentiment labels

    # Validate sentiment
    if sentiment not in ['positive', 'negative']:
        print(f"Invalid sentiment '{sentiment}' in row {index + 1}. Skipping.")
        continue

    article_text = scrape_article(url)
    if article_text:
        data.append((article_text, sentiment))
    else:
        print(f"Failed to scrape article or article is empty for URL in row {index + 1}.")

# Check if there is enough data to train the model
if len(data) < 2:
    print("Not enough data to train the model.")
    exit()

# Separate the data and labels
texts, labels = zip(*data)

# Create and train the model
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(texts, labels)

# Prediction phase
print("\n--- Prediction Mode ---")
while True:
    url = input("\nEnter article URL for sentiment prediction (or type 'done' to exit): ")
    if url == 'done':
        break

    article_text = scrape_article(url)
    if article_text:
        predicted_sentiment = model.predict([article_text])[0]
        print(f"Predicted sentiment for the article: {predicted_sentiment}")
    else:
        print("Failed to scrape the article or the article is empty.")
