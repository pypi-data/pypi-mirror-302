import os
import json
from datetime import datetime
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import torch
from unittest.mock import patch
from transformers.dynamic_module_utils import get_imports

# Simplified integrated mapping data
SEGMONTO_TO_FLORENCE_MAPPING = [
    {"segmonto_name": "TableZone-Cell", "florence_name": "data"},
    {"segmonto_name": "MainZone-P", "florence_name": "paragraph"},
    {"segmonto_name": "MainZone-Head", "florence_name": "title"},
    {"segmonto_name": "TableZone-RowName", "florence_name": "horizontal"},
    {"segmonto_name": "MainZone-List", "florence_name": "item"},
    {"segmonto_name": "RunningTitleZone", "florence_name": "paratext"},
    {"segmonto_name": "TableZone-ColName", "florence_name": "verticals"},
    {"segmonto_name": "TableZone", "florence_name": "table"},
    {"segmonto_name": "NumberingZone", "florence_name": "page number"},
    {"segmonto_name": "TableZone-ColNames", "florence_name": "vertical"},
    {"segmonto_name": "FormZone-Field", "florence_name": "form field"},
    {"segmonto_name": "GraphicZone", "florence_name": "image"},
    {"segmonto_name": "TableZone-Head", "florence_name": "table caption"},
    {"segmonto_name": "MarginTextZone-Notes", "florence_name": "footnote"},
    {"segmonto_name": "GraphicZone-Part", "florence_name": "image element"},
    {"segmonto_name": "MainZone-Signature", "florence_name": "signature"},
    {"segmonto_name": "MainZone-Entry", "florence_name": "entry"},
    {"segmonto_name": "MainZone-Date", "florence_name": "date"},
    {"segmonto_name": "MainZone-Form", "florence_name": "form"},
    {"segmonto_name": "ContactZone", "florence_name": "contact"},
    {"segmonto_name": "MainZone-Other", "florence_name": "other"},
    {"segmonto_name": "MainZone-P-Continued", "florence_name": "paragraph continued"},
    {"segmonto_name": "GraphicZone-Head", "florence_name": "image caption"},
    {"segmonto_name": "PageTitleZone", "florence_name": "front page"},
    {"segmonto_name": "GraphicZone-FigDesc", "florence_name": "image description"},
    {"segmonto_name": "DigitizationArtefactZone", "florence_name": "digital artifact"},
    {"segmonto_name": "DropCapitalZone", "florence_name": "uppercase"},
    {"segmonto_name": "GraphicZone-TextualContent", "florence_name": "image text"},
    {"segmonto_name": "GraphicZone-Math", "florence_name": "math"},
    {"segmonto_name": "AdvertisementZone", "florence_name": "advertising"},
    {"segmonto_name": "PageTitleZone-Index", "florence_name": "index"},
    {"segmonto_name": "MarginTextZone-ManuscriptAddendum", "florence_name": "manuscript text"},
    {"segmonto_name": "MainZone-Lg", "florence_name": "poem"},
    {"segmonto_name": "MainZone-List-Continued", "florence_name": "item continued"},
    {"segmonto_name": "FigureZone", "florence_name": "figure"},
    {"segmonto_name": "GraphicZone-Decoration", "florence_name": "decoration"},
    {"segmonto_name": "GraphicZone-Maths", "florence_name": "math"},
    {"segmonto_name": "StampZone", "florence_name": "stamp"},
    {"segmonto_name": "TableZone-Corner", "florence_name": "corner"},
    {"segmonto_name": "TableZone-Row", "florence_name": "row"},
    {"segmonto_name": "TableZone-Column", "florence_name": "column"},
    {"segmonto_name": "TableZone-Headers", "florence_name": "headers"},
    {"segmonto_name": "TableZone-SectionDiv", "florence_name": "sectiondivider"}
]

def get_reverse_category_mapping():
    return {item['florence_name']: item['segmonto_name'] for item in SEGMONTO_TO_FLORENCE_MAPPING}

def fixed_get_imports(filename: str | os.PathLike) -> list[str]:
    if not str(filename).endswith("modeling_florence2.py"):
        return get_imports(filename)
    imports = get_imports(filename)
    if "flash_attn" in imports:
        imports.remove("flash_attn")
    return imports

def apply_florence(image_directory, output_file, checkpoint, device="cpu"):
    """
    Apply Florence model to process images and generate COCO format annotations.

    Args:
    image_directory (str): Path to the directory containing images.
    output_file (str): Path to save the output COCO format JSON file.
    checkpoint (str): Path to the Florence model checkpoint.
    device (str): Device to run the model on. Default is "cpu".

    """
    print(f"Using device: {device}")

    prompt = "<OD>"

    try:
        with patch("transformers.dynamic_module_utils.get_imports", fixed_get_imports):
            model = AutoModelForCausalLM.from_pretrained(
                checkpoint,
                attn_implementation="sdpa",
                torch_dtype=torch.float32,
                trust_remote_code=True
            ).to(device)
        processor = AutoProcessor.from_pretrained(checkpoint, trust_remote_code=True)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    reverse_mapping = get_reverse_category_mapping()

    coco_dataset = {
        "info": {
            "year": datetime.now().year,
            "version": "1.0",
            "description": "Converted from custom format to COCO",
            "contributor": "Your Name",
            "url": "Your URL",
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "images": [],
        "annotations": [],
        "categories": []
    }

    category_id_map = {}
    next_category_id = 1
    next_annotation_id = 1
    image_id = 0

    for root, dirs, files in os.walk(image_directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, filename)
                image = Image.open(image_path)

                if image.mode != 'RGB':
                    image = image.convert('RGB')

                image_width, image_height = image.size

                inputs = processor(text=prompt, images=image, return_tensors="pt")
                inputs = {k: v.to(device) for k, v in inputs.items()}

                try:
                    with torch.no_grad():
                        generated_ids = model.generate(
                            input_ids=inputs["input_ids"],
                            pixel_values=inputs["pixel_values"],
                            max_new_tokens=1024,
                            do_sample=False,
                            num_beams=3
                        )

                    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
                    parsed_answer = processor.post_process_generation(generated_text, task="<OD>", image_size=(image_width, image_height))

                    coco_dataset["images"].append({
                        "id": image_id,
                        "file_name": os.path.relpath(image_path, image_directory),
                        "width": image_width,
                        "height": image_height
                    })

                    parsed_answer = parsed_answer["<OD>"]
                    bboxes = parsed_answer['bboxes']
                    labels = parsed_answer['labels']

                    for bbox, label in zip(bboxes, labels):
                        original_label = reverse_mapping.get(label, label)
                        if original_label not in category_id_map:
                            category_id_map[original_label] = next_category_id
                            next_category_id += 1

                        x, y, w, h = bbox
                        coco_dataset["annotations"].append({
                            "id": next_annotation_id,
                            "image_id": image_id,
                            "category_id": category_id_map[original_label],
                            "bbox": [x, y, w - x, h - y],
                            "area": (w - x) * (h - y),
                            "segmentation": [],
                            "iscrowd": 0
                        })
                        next_annotation_id += 1

                    print(f"Processed {image_path}")
                    image_id += 1
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")

    for original_label, category_id in category_id_map.items():
        coco_dataset["categories"].append({
            "id": category_id,
            "name": original_label,
            "supercategory": "none"
        })

    with open(output_file, 'w') as f:
        json.dump(coco_dataset, f, indent=4, ensure_ascii=False)

    print(f"COCO dataset saved to {output_file}")

if __name__ == "__main__":
    # This block allows you to run the script directly for testing
    image_directory = "/path/to/your/image/directory"
    output_file = "/path/to/your/output/boxescoco.json"
    checkpoint = "/path/to/your/model/checkpoint"
    apply_florence(image_directory, output_file, checkpoint)