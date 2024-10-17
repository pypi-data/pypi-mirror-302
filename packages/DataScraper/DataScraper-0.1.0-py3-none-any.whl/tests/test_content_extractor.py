from data_scraper.content_extractor import extract_content_from_urls
urls = ["https://www.iana.org/domains/example"]  # List of URLs
folder_name = "Ouput_folder"  # Output folder for DOCX files
extract_content_from_urls(urls, folder_name)