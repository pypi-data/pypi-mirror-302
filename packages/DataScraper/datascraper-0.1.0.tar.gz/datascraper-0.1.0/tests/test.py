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

# Example usage:

# Initialize the converter (setting keep_word_active to True keeps Word open after conversion)
converter = DocxToPdfConverter(keep_word_active=False)

# Convert a single file
input_file_path = r"C:\Users\MukhtarULIslam\Downloads\srap_Data\www.iana.org_domains_example.docx"
output_file_path = r"C:\Users\MukhtarULIslam\Downloads\srap_Data\output.pdf"
converter.convert_single_docx(input_file_path, output_file_path)

# Convert all .docx files in a directory
# input_directory_path = r"C:\path\to\your\input_directory"
# output_directory_path = r"C:\path\to\output_directory"
# converter.convert_directory(input_directory_path, output_directory_path)
