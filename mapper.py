import re
from collections import defaultdict

# List of companies to check for matches
company_list = ['Microsoft', 'Apple', 'Amazon', 'Alphabet', 'Meta', 'Tesla', 'Johnson', 'AMD', 'Walmart', 'Netflix', 'Verizon', 'Pfizer', 'AT&T', 'IBM']

# Input and output file paths
input_file_path = 'impact1.txt'
output_file_path = 'matched_companies.txt'
occurrences_file_path = 'your_data.txt'

# Regular expression patterns to extract sentiment and company names within parentheses
sentiment_pattern = r"Sentiment: (\w+),"
company_pattern = r"\('([^']+)', \d+\)"

# Dictionary to store occurrences of other companies for each primary company
company_occurrences = defaultdict(lambda: defaultdict(int))

# Function to find and write matching companies and sentiment
def find_and_write_matching_info(line):
    sentiment_match = re.search(sentiment_pattern, line)
    if sentiment_match:
        sentiment = sentiment_match.group(1)
        matches = re.findall(company_pattern, line)
        matching_companies = [match.strip() for match in matches if match.strip() in company_list]
        if matching_companies:
            primary_company = matching_companies[0]
            for other_company in matching_companies[1:]:
                if sentiment == 'positive':
                    company_occurrences[primary_company][other_company] += 1
                elif sentiment == 'negative':
                    company_occurrences[primary_company][other_company] -= 1

            with open(output_file_path, 'a') as output_file:
                output_file.write(f"Sentiment: {sentiment}, Impacted Companies: {matching_companies}\n")

# Main script
with open(input_file_path, 'r') as input_file:
    for line in input_file:
        find_and_write_matching_info(line)

# Write company occurrences to the occurrences file
with open(occurrences_file_path, 'w') as occurrences_file:
    for primary_company, occurrences_dict in company_occurrences.items():
        occurrences_line = f"{primary_company} - "
        occurrences_line += "; ".join([f"{other_company},{count}" for other_company, count in occurrences_dict.items()])
        occurrences_file.write(occurrences_line + '\n')
