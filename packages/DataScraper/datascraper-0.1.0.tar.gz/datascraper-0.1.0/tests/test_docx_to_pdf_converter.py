
from data_scraper.docx_to_pdf_converter import DocxToPdfConverter
converter = DocxToPdfConverter()
# Define input and output directories
input_directory = "folder_word_file"
output_directory = "folder_pdf_file"

# Convert all .docx files to .pdf
converter.convert_multiple_docx_to_pdf(input_directory, output_directory)