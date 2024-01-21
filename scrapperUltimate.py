import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

visited_urls = set()  # Keep track of visited URLs to avoid duplicates

def scrape_and_store_articles(url, search_term, results_file, max_depth=3, timeout=3):
    global visited_urls

    try:
        start_time = time.time()
        
        # Send a GET request to the URL with timeout
        response = requests.get(url, timeout=timeout)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the anchor tags (links) in the HTML
            links = soup.find_all('a', href=True)

            # Extract and filter the article links
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
                            # Store the filtered article link in the results file
                            with open(results_file, "a") as file:
                                file.write(f"{search_term} - {absolute_url}\n")

                            # Mark the current URL as visited
                            visited_urls.add(absolute_url)

                            # Continue scraping recursively
                            if max_depth > 0:
                                scrape_and_store_articles(absolute_url, search_term, results_file, max_depth=max_depth - 1)

        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time} seconds")

    except requests.Timeout:
        print(f"Request to {url} timed out after {timeout} seconds. Skipping to the next search term.")
    except KeyboardInterrupt:
        print("\nScraping interrupted by keyboard. Data saved to results.txt")
        raise  # Re-raise the KeyboardInterrupt to stop the program
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Read search terms from a txt file
    with open("search_terms.txt", "r") as terms_file:
        search_terms = [term.strip() for term in terms_file]

    # List of URLs to scrape
    urls_to_scrape = [
        'https://www.google.com/finance/'
    ]

    # Scrape articles and store links for each search term until a keyboard interrupt
    try:
        results_file = "results.txt"
        for url in urls_to_scrape:
            for term in search_terms:
                scrape_and_store_articles(url, term, results_file)
                time.sleep(2)  # Add a 2-second delay between requests to avoid being blocked
    except KeyboardInterrupt:
        pass  # Handle KeyboardInterrupt gracefully
