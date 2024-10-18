# url_extractor.py

import requests
from bs4 import BeautifulSoup
import csv
import os

def extract_urls_to_csv(website_url, folder_name):
    """
    Extracts all URLs (href) from the provided website and saves them to a CSV file.

    Args:
        website_url (str): The URL of the website to scrape.
        folder_name (str): The folder where the CSV will be saved.

    Returns:
        list: A list of URLs extracted from the website.
    """
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all href links on the webpage
    urls = [a['href'] for a in soup.find_all('a', href=True)]
    
    # Write the extracted URLs to a CSV file
    csv_file_name = os.path.join(folder_name, 'urls.csv')
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for url in urls:
            writer.writerow([url])
    
    print(f"Extracted {len(urls)} URLs and saved to {csv_file_name}")
    return urls
