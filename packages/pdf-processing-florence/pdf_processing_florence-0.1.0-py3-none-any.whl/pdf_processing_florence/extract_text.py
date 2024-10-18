# src/pdf_processing_florence/extract_text.py

import os
import csv
import json
import re
import fitz  # PyMuPDF
from collections import defaultdict

def load_coco_annotations(coco_file):
    with open(coco_file, 'r') as f:
        coco_data = json.load(f)
    
    image_annotations = defaultdict(list)
    categories = {cat['id']: cat['name'] for cat in coco_data['categories']}
    
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category = categories[annotation['category_id']]
        bbox = annotation['bbox']
        image_annotations[image_id].append((category, bbox))
    
    return coco_data['images'], image_annotations, categories

def extract_text_from_boxes(pdf_document, page_index, annotations, image_width, image_height):
    page = pdf_document[page_index]
    results = []
    
    for category, bbox in annotations:
        try:
            # Convert COCO bbox (x, y, width, height) to PyMuPDF rect (x0, y0, x1, y1)
            x, y, w, h = bbox
            x0 = x / image_width * page.rect.width
            y0 = y / image_height * page.rect.height
            x1 = (x + w) / image_width * page.rect.width
            y1 = (y + h) / image_height * page.rect.height
            
            rect = fitz.Rect(x0, y0, x1, y1)
            text = page.get_text("text", clip=rect).strip()
            y_center = (y0 + y1) / 2
            results.append((category, text, y_center))
        except Exception as e:
            print(f"Error processing a box on page {page_index}: {e}")

    return results

def create_entry(main_title, section, text, document_name, page_num):
    full_text = f"{main_title} {section} {text}".strip()
    return {
        "main_title": main_title,
        "section": section,
        "text": full_text,
        "file": document_name,
        "page": page_num,
        "word_count": len(re.findall(r'\w+', full_text))
    }

def extract_text(document_folder, coco_file, output_json_file):
    """
    Extract text from PDFs using COCO annotations and save the results to a JSON file.

    Args:
    document_folder (str): Path to the folder containing PDF documents.
    coco_file (str): Path to the COCO annotation file.
    output_json_file (str): Path to save the output JSON file.

    """
    images, image_annotations, categories = load_coco_annotations(coco_file)
    
    print(f"Processing folder: {document_folder}")

    pdf_documents = {}
    pdf_results = defaultdict(list)

    for image_data in images:
        image_id = image_data['id']
        filename = image_data['file_name']
        
        # Extract PDF name from the image filename
        pdf_name = filename.split('/')[0]  # Get the first part of the path
        pdf_path = os.path.join(document_folder, f"{pdf_name}.pdf")
        page_num = int(filename.split('_page_')[-1].split('.')[0])

        print(f"Processing: {filename}")
        
        if pdf_path not in pdf_documents:
            if not os.path.exists(pdf_path):
                print(f"Error: PDF file not found: {pdf_path}")
                continue
            try:
                pdf_documents[pdf_path] = fitz.open(pdf_path)
            except Exception as e:
                print(f"Error opening PDF {pdf_path}: {e}")
                continue

        pdf_document = pdf_documents[pdf_path]
        
        if page_num > len(pdf_document):
            print(f"Warning: Page {page_num} does not exist in the PDF {pdf_path}. Skipping.")
            continue

        try:
            annotations = image_annotations[image_id]
            results = extract_text_from_boxes(pdf_document, page_num - 1, annotations, image_data['width'], image_data['height'])
            
            results = [(label, text, y_coord, page_num) for label, text, y_coord in results]
            
            pdf_results[pdf_path].extend(results)

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    # Close all opened PDF documents
    for pdf_doc in pdf_documents.values():
        pdf_doc.close()

    all_entries = []

    # Create a specific folder for CSV files
    csv_folder = os.path.join(document_folder, "csv_output")
    os.makedirs(csv_folder, exist_ok=True)

    for pdf_path, results in pdf_results.items():
        results.sort(key=lambda x: (x[3], x[2]))

        csv_results = []
        seen_texts = set()
        for label, text, _, page_num in results:
            if text not in seen_texts or label in ["MainZone-Head", "TableZone-Head", "TableZone-Header", "TableZone-Row"]:
                csv_results.append((label, text, page_num))
                seen_texts.add(text)

        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        csv_path = os.path.join(csv_folder, f"{pdf_name}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Label', 'Extracted Text', 'Page'])
            writer.writerows(csv_results)
        
        print(f"CSV file created: {csv_path}")

        main_title = ""
        section = ""
        current_text = ""
        last_mainzone_p = ""
        cumulated_list_text = ""

        for label, text, page_num in csv_results:
            if label == "PageTitleZone" and not main_title:
                main_title = text.replace("\n", " ").strip()
            elif label == "MainZone-Head":
                if current_text:
                    entry = create_entry(main_title, section, current_text, pdf_name, page_num)
                    all_entries.append(entry)
                if cumulated_list_text:
                    list_entry = create_entry(main_title, section, f"{last_mainzone_p} {cumulated_list_text}", pdf_name, page_num)
                    all_entries.append(list_entry)
                section = text.replace("\n", " ").strip()
                current_text = ""
                cumulated_list_text = ""
            elif label == "MainZone-P":
                if current_text:
                    entry = create_entry(main_title, section, current_text, pdf_name, page_num)
                    all_entries.append(entry)
                if cumulated_list_text:
                    list_entry = create_entry(main_title, section, f"{last_mainzone_p} {cumulated_list_text}", pdf_name, page_num)
                    all_entries.append(list_entry)
                    cumulated_list_text = ""
                current_text = text.strip()
                last_mainzone_p = current_text
            elif label == "MainZone-List":
                cumulated_list_text += f" {text.strip()}"
            elif label in ["TableZone-Row", "ContactZone"]:
                if current_text:
                    entry = create_entry(main_title, section, current_text, pdf_name, page_num)
                    all_entries.append(entry)
                if cumulated_list_text:
                    list_entry = create_entry(main_title, section, f"{last_mainzone_p} {cumulated_list_text}", pdf_name, page_num)
                    all_entries.append(list_entry)
                    cumulated_list_text = ""
                current_text = text.strip()

        if current_text:
            entry = create_entry(main_title, section, current_text, pdf_name, page_num)
            all_entries.append(entry)
        if cumulated_list_text:
            list_entry = create_entry(main_title, section, f"{last_mainzone_p} {cumulated_list_text}", pdf_name, page_num)
            all_entries.append(list_entry)

    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(all_entries, json_file, indent=4, ensure_ascii=False)
    
    print(f"JSON file created: {output_json_file}")

if __name__ == "__main__":
    # This block allows you to run the script directly for testing
    document_folder = "/path/to/your/document/folder"
    coco_file = "/path/to/your/coco_annotations.json"
    output_json_file = "/path/to/your/output/final_output.json"
    extract_text(document_folder, coco_file, output_json_file)