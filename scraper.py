import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_article_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all the anchor tags (links) in the HTML
        links = soup.find_all('a', href=True)
        
        # Extract and filter the article links
        article_links = []
        for link in links:
            href = link.get('href')
            
            # Filter out useless links (adjust as needed)
            if href and '/news/' in href and 'yahoo.com' in href:
                # Make relative URLs absolute
                absolute_url = urljoin(url, href)
                article_links.append(absolute_url)
                
        return article_links
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return []

# Example: Yahoo Finance News
yahoo_finance_news_url = 'https://finance.yahoo.com/news/'
article_links = get_article_links(yahoo_finance_news_url)

# Print the filtered article links
for link in article_links:
    print(link)
