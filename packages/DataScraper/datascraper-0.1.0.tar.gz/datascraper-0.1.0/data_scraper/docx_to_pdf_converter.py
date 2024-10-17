# # docx_to_pdf_converter.py

# from docx import Document
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import os

# def convert_docx_to_pdf(docx_file, pdf_file):
#     """
#     Converts a .docx file to a PDF file using ReportLab.

#     Args:
#         docx_file (str): The path to the .docx file to be converted.
#         pdf_file (str): The path where the PDF will be saved.

#     Returns:
#         None
#     """
#     # Load the .docx document
#     doc = Document(docx_file)

#     # Create a new PDF canvas
#     c = canvas.Canvas(pdf_file, pagesize=letter)
#     width, height = letter
#     y = height - 40  # Start at the top of the page
#     margin=40    #set margins

#     # Iterate through paragraphs in the .docx file
#     for para in doc.paragraphs:
#         if not para.text.strip():  # Skip empty paragraphs
#             continue

#         # Set font size and style based on the paragraph style (header or normal text)
#         if para.style.name == 'Heading 1':
#             c.setFont("Helvetica-Bold", 16)
#         elif para.style.name == 'Heading 2':
#             c.setFont("Helvetica-Bold", 14)
#         else:
#             c.setFont("Helvetica", 12)
        
#         # wrap text to fit page width
#         text= para.text
#         # text_width= c.stringWidth(text,c.getFont(),c.getFontSize())

#         #check if we need new page
#         if y < margin +12:  # keep some space for the margin
#             c.showPage()
#             c.setFont("Helvetica",12) # Reset to normal font for new page
#             y=height-margin # reset y position
        
#         #draw the text on the pdf
#         c.drawString(margin,y,text)
#         y-= 14 # move down for the next line , adjusting spacing as needed


#         # Start a new page if the current page is full
#         # if y < 40:  
#         #     c.showPage()
#         #     y = height - 40

#         # Draw the paragraph text on the PDF
#         # c.drawString(40, y, para.text)
#         # y -= 14  # Adjust spacing for next line

#     # Save the PDF file
#     c.save()

# def convert_multiple_docx_to_pdf(docx_folder, output_folder):
#     """
#     Converts all .docx files in a folder to PDF files.

#     Args:
#         docx_folder (str): The folder containing .docx files to be converted.
#         output_folder (str): The folder where the converted PDF files will be saved.

#     Returns:
#         None
#     """
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Iterate through .docx files in the input folder and convert each to PDF
#     for filename in os.listdir(docx_folder):
#         if filename.endswith('.docx'):
#             docx_file = os.path.join(docx_folder, filename)
#             pdf_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
#             convert_docx_to_pdf(docx_file, pdf_file)
#             print(f"Converted {docx_file} to {pdf_file}")





#==============================update the code===========================

import os
import pythoncom
from win32com import client as win32

class DocxToPdfConverter:
    def __init__(self, keep_word_active=False):
        """
        Initialize the converter. Optionally, set whether to keep Microsoft Word active after conversion.

        :param keep_word_active: If True, Microsoft Word will remain open after the conversion process.
        """
        self.keep_word_active = keep_word_active
        self.word_app = None

    def open_word(self):
        """Open Microsoft Word using COM interface."""
        if self.word_app is None:
            self.word_app = win32.Dispatch("Word.Application")
            self.word_app.Visible = False  # Hide the Word window during conversion

    def close_word(self):
        """Close Microsoft Word if not keeping it active."""
        if self.word_app and not self.keep_word_active:
            self.word_app.Quit()
            self.word_app = None

    def convert_single_docx(self, input_file, output_file):
        """
        Convert a single .docx file to .pdf.

        :param input_file: Path to the input .docx file.
        :param output_file: Path to the output .pdf file.
        """
        self.open_word()
        try:
            doc = self.word_app.Documents.Open(input_file)
            doc.SaveAs(output_file, FileFormat=17)  # FileFormat 17 is PDF
            doc.Close()
            print(f"Converted: {input_file} -> {output_file}")
        except Exception as e:
            print(f"Error converting {input_file} -> {output_file}: {e}")
        finally:
            self.close_word()

    def convert_directory(self, input_dir, output_dir):
        """
        Batch convert all .docx files in a directory to .pdf.

        :param input_dir: Path to the directory containing .docx files.
        :param output_dir: Path to the directory to save the .pdf files.
        """
        assert os.path.isdir(input_dir), f"Input path '{input_dir}' is not a directory"
        assert os.path.isdir(output_dir), f"Output path '{output_dir}' is not a directory"

        files = [f for f in os.listdir(input_dir) if f.endswith('.docx')]

        self.open_word()
        for file in files:
            input_file = os.path.join(input_dir, file)
            output_file = os.path.join(output_dir, file.replace('.docx', '.pdf'))
            try:
                self.convert_single_docx(input_file, output_file)
            except Exception as e:
                print(f"Error converting {input_file}: {e}")
        self.close_word()

    def convert_multiple_docx_to_pdf(self, docx_folder, output_folder):
        """
        Converts all .docx files in a folder to PDF files.

        Args:
            docx_folder (str): The folder containing .docx files to be converted.
            output_folder (str): The folder where the converted PDF files will be saved.

        Returns:
            None
        """
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through .docx files in the input folder and convert each to PDF
        for filename in os.listdir(docx_folder):
            if filename.endswith('.docx'):
                docx_file = os.path.join(docx_folder, filename)
                pdf_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
                self.convert_single_docx(docx_file, pdf_file)
                print(f"Converted {docx_file} to {pdf_file}")
