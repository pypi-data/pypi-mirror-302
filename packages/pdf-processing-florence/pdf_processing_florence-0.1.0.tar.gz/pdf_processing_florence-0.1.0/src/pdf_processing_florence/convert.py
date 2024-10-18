# src/pdf_processing_florence/convert.py

import os
from pathlib import Path
from pdf2image import convert_from_path

def convertpdf_jpg(input_dir, dpi=300):
    """
    Convert PDFs to JPGs in the given directory and its subdirectories.
    
    Args:
    input_dir (str): Path to the directory containing PDFs.
    dpi (int): DPI for the output JPG images. Default is 300.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                pdf_name = Path(file).stem
                
                subfolder_path = os.path.join(root, pdf_name)
                os.makedirs(subfolder_path, exist_ok=True)
                
                try:
                    images = convert_from_path(pdf_path, dpi=dpi)
                    for i, image in enumerate(images):
                        jpg_filename = f"{Path(file).stem}_page_{i+1}.jpg"
                        jpg_path = os.path.join(subfolder_path, jpg_filename)
                        image.save(jpg_path, "JPEG")
                        print(f"Saved: {jpg_path}")
                except Exception as e:
                    print(f"Failed to convert {pdf_path}: {e}")

if __name__ == "__main__":
    # This block allows you to run the script directly for testing
    input_directory = "/path/to/your/pdf/directory"
    convertpdf_jpg(input_directory)