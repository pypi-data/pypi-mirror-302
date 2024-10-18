import os 
import cv2 

img_path = r"D:\shelf_audit\obj_detection\dataset\sku110k\images\train"
label_path = r"D:\shelf_audit\obj_detection\dataset\sku110k\labels\train"

des_path = r"D:\shelf_audit\obj_detection\dataset\sku110k\bbox\train"
if not os.path.exists(des_path):
    os.makedirs(des_path, exits_ok = True)

for image in os.listdir(img_path):
    image_path = os.path.join(img_path, image)
    label_txt = os.path.join(label_path, f"{image[:-4]}.txt")

    img = cv2.imread(image_path)
    print(img.shape)
    img_width = img.shape[1]
    img_height = img.shape[0]

    with open(label_txt, "r") as f:
        annotations = [line.strip().split() for line in f.readlines()]

    for annot in annotations:
        cls, xc, yc, w, h= annot

        x_min = int(float(xc)*float(img_width) - float(w)*float(img_width) / 2)
        y_min = int(float(yc)*float(img_height) - float(h)*float(img_height) / 2)
        x_max = int(float(xc)*float(img_width) + float(w)*float(img_width) / 2)
        y_max = int(float(yc)*float(img_height) + float(h)*float(img_height) / 2)

        rect_img = cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color = (255, 255, 100), thickness = 2)
        cv2.imwrite(os.path.join(des_path, f"{image[:-4]}_bbox.jpg"), rect_img)
