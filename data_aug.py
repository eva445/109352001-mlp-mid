import numpy as np
import cv2
from imgaug import augmenters as iaa
import os


def aug(brand):
    i = 1
    # 獲取當前工作目錄
    current_directory = os.getcwd()

    # 定義 "folder1" 資料夾的路徑
    folder_path = os.path.join(current_directory, brand)

    # 讀取 "folder1" 資料夾中的所有文件
    file_list = sorted(os.listdir(folder_path), key=lambda x: int(x.split('.')[0]))
    n = len(file_list)
    # 遍歷文件列表
    for file_name in file_list:
        image_path = os.path.join(folder_path, file_name)
        img = cv2.imread(image_path)

        img = cv2.resize(img, (224,224)) ## 改變圖片尺寸
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Cv2讀進來是BGR，轉成RGB
        img_origin = img.copy()
        img = np.array(img, dtype=np.float32)

        images = np.random.randint(0, 255, (45, 224, 224, 3), dtype=np.uint8)##創造一個array size==(45, 224, 224, 3)

        flipper = iaa.Fliplr(1.0) # 水平翻轉機率==1.0
        images[0] = flipper.augment_image(img) 

        vflipper = iaa.Flipud(0.4) # 垂直翻轉機率40%
        images[1] = vflipper.augment_image(img) 

        blurer = iaa.GaussianBlur(3.0)
        images[2] = blurer.augment_image(img) # 高斯模糊圖像( sigma of 3.0)

        for j in range(0,10):
            translater = iaa.Affine(translate_px={"x": -16*j}) # 向左橫移16個像素
            images[3+j] = translater.augment_image(img) 
        j += 1
        for k in range(j,j + 10):
            translater = iaa.Affine(translate_px={"x": 16*(k-j)}) # 向右橫移16個像素
            images[3+k] = translater.augment_image(img) 


        scaler = iaa.Affine(scale={"x":0.5, "y": 0.5}) # 縮放
        images[23] = scaler.augment_image(img)

        scaler = iaa.Affine(scale={"x": 2.0, "y": 2.0})
        images[24] = scaler.augment_image(img)

        for j in range(0, 10):
            rotater = iaa.Affine(rotate=(15*(j+1)))
            images[25 + j] = rotater.augment_image(img)
        for j in range(0, 10):
            rotater = iaa.Affine(rotate=(-15*(j+1)))
            images[35 + j] = rotater.augment_image(img)

        for image in images:
            image_filename = os.path.join(folder_path, f'{i + n}.jpg')
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Cv2讀進來是BGR，轉成RGB
            cv2.imwrite(image_filename, image)
            i += 1

brand = ["INTO YOU", "CARSLAN","rom&nd"]
for b in brand:
    aug(b)