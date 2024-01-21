import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Function to scrape a news article
def scrape_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        return article_text
    except Exception as e:
        print("Error scraping the article:", e)
        return None

# Initialize data list
data = []

# Training phase
while True:
    print("\n--- Training Mode ---")
    url = input("Enter article URL (or type 'done' to end training): ")
    if url == 'done':
        break

    sentiment = input("Enter article sentiment ('positive' or 'negative'): ").lower()
    if sentiment not in ['positive', 'negative']:
        print("Invalid sentiment. Please enter 'positive' or 'negative'.")
        continue

    article_text = scrape_article(url)
    if article_text:
        data.append((article_text, sentiment))
    else:
        print("Failed to scrape the article or the article is empty.")

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
