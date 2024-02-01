import requests
import pandas as pd

def get_stock_news(api_key, query, total_results=100):
    base_url = "https://newsapi.org/v2/everything"
    articles = []
    page = 1
    pageSize = 100  # Adjust based on the maximum allowed by the API
    language = "en"
    domains = "finance.yahoo.com"

    while len(articles) < total_results:
        params = {
            "q": query,
            "pageSize": pageSize,
            "page": page,
            "apiKey": api_key,
            "language": language,
            "domains" : domains
        }
        response = requests.get(base_url, params=params).json()

        # Check if 'articles' key is in response
        if 'articles' in response:
            articles.extend(response['articles'])
        else:
            print("Error in API response:", response)
            break

        if len(articles) >= response.get('totalResults', 0):
            break  # Break if we have fetched all available results

        page += 1

    return articles[:total_results]  # Return only the requested number of articles


def main():
    api_key = "9de622d9afc5456dac6cdcb62ff76349"  # Replace with your NewsAPI key
    query = "Microsoft"    # Customize your query
    total_results = 100       # Specify the total number of results you want

    articles_json = get_stock_news(api_key, query, total_results)

    # Extracting article URLs
    articles = [article['url'] for article in articles_json]

    # Save to Excel
    df = pd.DataFrame({'Articles': articles})
    df.to_excel('stock_articles.xlsx', index=False)
    print("Articles saved to stock_articles.xlsx")

if __name__ == "__main__":
    main()
