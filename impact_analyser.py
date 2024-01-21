import requests
from bs4 import BeautifulSoup
import spacy
from transformers import pipeline
from collections import Counter

def get_article_text(url):
    # Fetch the HTML content of the article
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text content from the article
    article_text = ' '.join([p.get_text() for p in soup.find_all('p')])

    return article_text

def extract_companies_from_text(text):
    # Load the spaCy English NER model
    nlp = spacy.load('en_core_web_sm')

    # Process the text using spaCy
    doc = nlp(text)

    # Extract organizations (companies) from the processed text
    companies = [ent.text for ent in doc.ents if ent.label_ == 'ORG']

    return companies

def analyze_impact(article_text):
    # Load the pre-trained BERT sentiment analysis model
    sentiment_model = pipeline("sentiment-analysis")

    # Split the article text into segments that fit within the model's limit
    max_segment_length = 512
    article_segments = [article_text[i:i+max_segment_length] for i in range(0, len(article_text), max_segment_length)]

    # Analyze sentiment of each segment
    sentiment_results = []
    for segment in article_segments:
        segment_results = sentiment_model(segment)
        sentiment_results.extend([(segment, result['label']) for result in segment_results])

    # Extract companies from each statement
    companies_impacted = []
    for segment, label in sentiment_results:
        companies = extract_companies_from_text(segment)
        companies_impacted.extend(companies)

    return companies_impacted

if __name__ == "__main__":
    # Replace 'article_url' with the link to the stock news article
    article_url = 'https://www.investopedia.com/meta-vr-headset-announcement-preempts-apple-7507006'

    # Get the text content of the article
    article_text = get_article_text(article_url)

    # Analyze the impact of the article and extract companies for each segment
    impacted_companies = analyze_impact(article_text)

    # Rank companies by frequency
    company_counts = Counter(impacted_companies)
    ranked_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)

    # Display the ranked companies impacted by the news
    print("Ranked Companies Impacted by the News:")
    for company, count in ranked_companies:
        print(f"{company}: {count} times")

