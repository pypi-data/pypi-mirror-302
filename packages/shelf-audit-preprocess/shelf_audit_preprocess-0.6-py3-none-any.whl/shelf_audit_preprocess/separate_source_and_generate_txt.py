########################## separate image , json and find prediction txt #############################################
import os
import json
import cv2
import shutil
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool


root_dir = './set1'
des_root = "./results"

des_img_path = os.path.join(des_root, 'images')
os.makedirs(des_img_path, exist_ok=True)

des_json_path = os.path.join(des_root, 'yolo_labels')
os.makedirs(des_json_path, exist_ok=True)

des_norm_txt_path = os.path.join(des_root, 'labels')
os.makedirs(des_norm_txt_path, exist_ok=True)

des_txt_path = os.path.join(des_root, 'original_labels')
os.makedirs(des_txt_path, exist_ok=True)


# reference json file to identity what obj is in the labelling json file 
obj_class_json = "/mnt/sfs-shelfaudit-data/Nithish/data_preparation/classes.json"
classes = json.load(open(obj_class_json))

# function to convert json annotations to yolo(txt) format 
def yolo_annotations(product, product_class, annotations, classes, width, height):
    x1, y1 = product["points"][0]["x"], product["points"][0]["y"]
    x2, y2 = product["points"][2]["x"], product["points"][2]["y"]
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    cx_rel = cx / width
    cy_rel = cy / height
    w_rel = w / width
    h_rel = h / height

    #product_class = product["attributes"]["object"]
    if product_class in classes:
        class_id = classes[product_class]
    else:
        # Update the JSON and assign the new class ID
        classes[product_class] = classes["next_value"]
        classes["next_value"] += 1
        class_id = classes[product_class]

    annotation = f"{class_id} {cx_rel} {cy_rel} {w_rel} {h_rel}"
    # print(annotation)
    annotations.append(annotation)


def process_file(file_path, root):
    json_data = json.load(open(file_path))
    img_path = os.path.join(root, os.path.splitext(os.path.basename(file_path))[0]) + ".jpg"

    if "jobid" in json_data and "labels" in json_data:
        jobid = json_data["jobid"]

        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to read image: {img_path}")
            return

        img_w = img.shape[1]
        img_h = img.shape[0]

        annotations_norm_txt = []
        annotations_original_txt = []
        dest_img_path = os.path.join(des_img_path, os.path.splitext(jobid)[0] + ".jpg")
        dest_json_path = os.path.join(des_json_path, os.path.splitext(jobid)[0] + ".json")
        if len(json_data["labels"]) == 0:
            shutil.copy(img_path, dest_img_path)
            shutil.copy(file_path, dest_json_path)
            
            pass 

        else:
            for product in json_data["labels"]:
                if (len(product) != 0) and "object" in product:
                    if "name" in product and product["name"] == "Empty1":
                        continue
                    else:
                        product_class = product["object"]
                        if product_class == "EMPTY":
                            continue
                    yolo_annotations(product, product_class, annotations_norm_txt, classes, width = img_w, height = img_h)
                    yolo_annotations(product, product_class, annotations_original_txt,classes, width = 1, height = 1)
                else:
                    continue
            if len(annotations_norm_txt) == 0:
                return
            else:
                shutil.copy(img_path, dest_img_path)
                shutil.copy(file_path, dest_json_path)

        norm_txt_file_path = os.path.join(des_norm_txt_path, os.path.splitext(jobid)[0] + ".txt")
        txt_file_path = os.path.join(des_txt_path, os.path.splitext(jobid)[0] + ".txt")

        # print(dest_img_path)
        # print(txt_file_path)
        with open(norm_txt_file_path, "w") as f:
            f.write("\n".join(annotations_norm_txt))
        
        with open(txt_file_path, "w") as f:
            f.write("\n".join(annotations_original_txt))
        


def process_files_in_dir(args):
    root, files = args
    for file in files:
        file_path = os.path.join(root, file)
        try:
            if file_path.endswith(".json") and os.path.exists(os.path.join(root, os.path.splitext(file)[0]) + ".jpg"):
                process_file(file_path, root)

        except Exception as e:
            print(file_path)
    
    # Save the updated JSON file
with open(obj_class_json, 'w') as file:
    json.dump(classes, file, indent=4)

def main():
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(root_dir):
            executor.submit(process_files_in_dir, (root, files))

if __name__ == "__main__":
    main()
