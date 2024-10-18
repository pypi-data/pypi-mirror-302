import os
from pdf_processing_florence import convertpdf_jpg, apply_florence, extract_text

def test_convertpdf_jpg():
    input_directory = "./test_files"
    convertpdf_jpg(input_directory)
    
    # Check if JPG files were created
    pdf_name = [f for f in os.listdir(input_directory) if f.endswith('.pdf')][0]
    jpg_folder = os.path.join(input_directory, os.path.splitext(pdf_name)[0])
    assert os.path.exists(jpg_folder), f"JPG folder not created for {pdf_name}"
    assert any(f.endswith('.jpg') for f in os.listdir(jpg_folder)), "No JPG files created"
    print("convertpdf_jpg test passed")

def test_apply_florence():
    image_directory = "./test_files"
    output_file = "./test_files/annotations.json"
    checkpoint = "/Users/rosas/edunat/model"  # Update this path
    
    apply_florence(image_directory, output_file, checkpoint)
    
    # Check if the annotations file was created
    assert os.path.exists(output_file), "Annotations file not created"
    print("apply_florence test passed")

def test_extract_text():
    document_folder = "./test_files"
    coco_file = "./test_files/annotations.json"
    output_json_file = "./test_files/extracted_text.json"
    
    extract_text(document_folder, coco_file, output_json_file)
    
    # Check if the output JSON file was created
    assert os.path.exists(output_json_file), "Extracted text JSON file not created"
    print("extract_text test passed")

if __name__ == "__main__":
    test_convertpdf_jpg()
    test_apply_florence()
    test_extract_text()
    print("All tests passed successfully!")