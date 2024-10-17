
# from data_scraper.url_extractor import extract_urls_to_csv
# # from Datascrapper.data_scraper.data_scraper.url_extractor import extract_urls_to_csv

# website_url = r"https://smallpage.io/"  # Replace with your target website
# folder_name = r"C:\Users\MukhtarULIslam\Downloads\srap_Data"  # Output folder for CSV
# extract_urls_to_csv(website_url, folder_name)

import pytest
from data_scraper.url_extractor import extract_urls_to_csv

def test_extract_urls_to_csv():
    # Example test code
    website_url = "https://example.com"  # Use a valid test URL
    folder_name = r'C:\Users\MukhtarULIslam\Downloads\srap_Data'
    result = extract_urls_to_csv(website_url, folder_name)
    assert isinstance(result, list)  # Check that the result is a list
    # You can add more assertions to check the URLs' correctness
