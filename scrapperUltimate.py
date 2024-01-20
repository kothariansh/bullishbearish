import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited_urls = set()  # Keep track of visited URLs to avoid duplicates

def scrape_and_store_articles(url, search_term, max_depth=3):
    global visited_urls

    try:
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
                if href:
                    # Make relative URLs absolute
                    absolute_url = urljoin(url, href)

                    # Check if the link has already been visited
                    if absolute_url not in visited_urls:
                        # Check if the headline contains the search term
                        headline = link.get_text().strip()
                        if search_term.lower() in headline.lower():
                            # Store the filtered article link in a file
                            with open("article.txt", "a") as file:
                                file.write(absolute_url + '\n')

                            # Mark the current URL as visited
                            visited_urls.add(absolute_url)

                            # Continue scraping recursively
                            if max_depth > 0:
                                scrape_and_store_articles(absolute_url, search_term, max_depth=max_depth - 1)

    except KeyboardInterrupt:
        print("\nScraping interrupted by keyboard. Article links saved to article.txt")

if __name__ == "__main__":
    # Input the search term
    search_term = input("Enter the word to search in the headline: ")

    # List of URLs to scrape
    urls_to_scrape = [
        'https://www.google.com/finance/'
        # 'https://finance.yahoo.com/news/',
        # 'https://www.cnbc.com/world/',
        # 'https://www.bloomberg.com/markets',
        # 'https://www.reuters.com/business',
        # 'https://www.wsj.com/news/markets',
        # 'https://www.ft.com/markets',
        # 'https://www.investing.com/news/stock-market-news',
        # 'https://www.marketwatch.com/',
        # 'https://www.businessinsider.com/clusterstock',
        # 'https://www.forbes.com/business/',
        # 'https://www.nasdaq.com/',
        # 'https://www.barrons.com/',
        # 'https://www.thestreet.com/',
        # 'https://seekingalpha.com/',
        # 'https://www.fool.com/',
        # 'https://www.usnews.com/news/business',
        # 'https://www.moneycontrol.com/news/business/',
        # 'https://www.zacks.com/',
        # 'https://www.marketplace.org/',
        # 'https://www.npr.org/sections/business/'
    ]

    # Scrape articles and store links in a file until a keyboard interrupt
    for url in urls_to_scrape:
        scrape_and_store_articles(url, search_term)
