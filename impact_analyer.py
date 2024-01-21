import requests
from bs4 import BeautifulSoup
import spacy
from transformers import pipeline
from collections import Counter
import re  # Import the re module for regular expressions

# Download spaCy model if not already installed
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

def get_article_text(url):
    # Fetch the HTML content of the article
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article content for {url}: {str(e)}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text content from the article
    article_text = ' '.join([p.get_text() for p in soup.find_all('p')])

    return article_text

def extract_companies_from_text(text):
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
    # Open "impact1.txt" in append mode
    with open('impact1.txt', 'a') as impact_file:
        # Open "errors.txt" in append mode for logging errors
        with open('errors.txt', 'a') as errors_file:
            # Read URLs from the input file and process each one
            with open('results.txt', 'r') as file:
                for line in file:
                    # Split the line by semicolon to get elements
                    elements = line.strip().split(';')

                    try:
                        # Get the URL from the second element
                        article_url = elements[1]

                        # Get the text content of the article
                        article_text = get_article_text(article_url)

                        if article_text is not None:
                            # Analyze the impact of the article and extract companies for each segment
                            impacted_companies = analyze_impact(article_text)

                            # Rank companies by frequency
                            company_counts = Counter(impacted_companies)
                            ranked_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)

                            # Write results to "impact.txt" on a new line and flush the file
                            impact_file.write(f"{article_url} - {', '.join([f'{company}: {count} times' for company, count in ranked_companies])}\n")
                            impact_file.flush()

                            print(f"Results for {article_url} have been appended to impact1.txt")

                    except Exception as e:
                        # Log the error to "errors.txt"
                        errors_file.write(f"Error processing {article_url}: {str(e)}\n")
                        errors_file.flush()

                        print(f"Error processing {article_url}: {str(e)}")

    print("All results have been written to impact1.txt. Errors, if any, have been logged to errors.txt.")
