import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=T&interval=5min&apikey=7P2FY1GOD9JYF2TW'
r = requests.get(url)
data = r.json()

# Specify the output file path
output_file_path = 'alphavantage_metadata.txt'

# Write metadata to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(str(data))

print(f"Metadata has been written to {output_file_path}")
