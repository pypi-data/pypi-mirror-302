''' code for old json annotation format to convert into yolo(txt) format '''

import os
import json
import cv2
import shutil

# root dir where images and labels are downloaded from the blob 
root_dir = r'D:\shelf_audit\data\ShelfAudit\set1'

# des path to save the converted image and labels in yolo format 
des_root = r"D:\shelf_audit\data\ShelfAudit"

des_img_path = os.path.join(des_root, 'images')
if not os.path.exists(des_img_path):
    os.makedirs(des_img_path, exist_ok=True)

des_txt_path = os.path.join(des_root, 'labels1')
if not os.path.exists(des_txt_path):
    os.makedirs(des_txt_path, exist_ok=True)

# reference json file to identity what obj is in the labelling json file 
obj_class_json = r"D:\shelf_audit\data\ShelfAudit\classes.json"
classes = json.load(open(obj_class_json))

# function to convert json annotations to yolo(txt) format 
def yolo_annotations(product, product_class):
    x1, y1 = product["points"][0]["x"], product["points"][0]["y"]
    x2, y2 = product["points"][2]["x"], product["points"][2]["y"]
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    cx_rel = cx / img_w
    cy_rel = cy / img_h
    w_rel = w / img_w
    h_rel = h / img_h

    #product_class = product["attributes"]["object"]
    if product_class in classes:
        class_id = classes[product_class]
    else:
        # Update the JSON and assign the new class ID
        classes[product_class] = classes["next_value"]
        classes["next_value"] += 1
        class_id = classes[product_class]

    annotation = f"{class_id} {cx_rel} {cy_rel} {w_rel} {h_rel}"
    print(annotation)
    annotations.append(annotation)




for root, dirs, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(root, file)

        '''take only the data's have both json and image'''
        if file_path.endswith(".json") and os.path.exists(os.path.join(root, os.path.splitext(file)[0]) + ".jpg"):
            json_data = json.load(open(file_path))
            img_path = os.path.join(root, os.path.splitext(file)[0]) + ".jpg"

            ''' select only the files which have both jobid and labels key in the json files '''
            if "jobid" in json_data and "labels" in json_data: #and 'labels' in json_data:
                jobid = json_data["jobid"]

                img = cv2.imread(img_path)
                if img is None:
                    print(f"Failed to read image: {img_path}")
                    continue

                img_w = img.shape[1]
                img_h = img.shape[0]

                annotations = []
                dest_img_path = os.path.join(des_img_path, os.path.splitext(jobid)[0] + ".jpg")
                if len(json_data["labels"]) == 0:
                    shutil.copy(img_path, dest_img_path)
                    pass 
                else:
                    for product in json_data["labels"]:
                        if (len(product) != 0) and "object" in product:
                            if not os.path.exists(dest_img_path):
                                shutil.copy(img_path, dest_img_path)
                            if product["name"] == "Empty1":
                                product_class = "EMPTY"
                            else:
                                product_class = product["object"]
                            yolo_annotations(product, product_class)
                        else:
                            continue
                    
                txt_file_path = os.path.join(des_txt_path, os.path.splitext(jobid)[0] + ".txt")
                with open(txt_file_path, "w") as f:
                    f.write("\n".join(annotations))
            
            else:
                continue


# Save the updated JSON file
with open(obj_class_json, 'w') as file:
    json.dump(classes, file, indent=4)
