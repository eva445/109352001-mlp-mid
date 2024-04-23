import cv2
import os

def resize_to_square(image, target_size, fill_color=(255, 255, 255)):
    # 獲取原始圖片的寬高
    height, width = image.shape[:2]
    
    # 確定 resize 的邊長
    target_length = max(height, width)
    
    # 計算填充後的邊界
    top_pad = (target_length - height) // 2
    bottom_pad = target_length - height - top_pad
    left_pad = (target_length - width) // 2
    right_pad = target_length - width - left_pad
    
    # 創建一個填充後的圖片
    padded_image = cv2.copyMakeBorder(image, top_pad, bottom_pad, left_pad, right_pad, 
                                       cv2.BORDER_CONSTANT, value=fill_color)
    
    # resize 圖片到目標大小
    resized_image = cv2.resize(padded_image, (target_size))
    return resized_image


def resize_data(brand):

    # 獲取當前工作目錄
    current_directory = os.getcwd()

    # 定義 "folder1" 資料夾的路徑
    folder_path = os.path.join(current_directory, brand)

    # 讀取 "folder1" 資料夾中的所有文件
    file_list = sorted(os.listdir(folder_path), key=lambda x: int(x.split('.')[0]))

    # 遍歷文件列表
    i = 1
    for file_name in file_list:
        image_path = os.path.join(folder_path, file_name)
        img = cv2.imread(image_path)

        resized_image = resize_to_square(img, target_size)

        image_filename = os.path.join(folder_path, f'{i}.jpg')
        cv2.imwrite(image_filename, resized_image)
        i += 1



target_size = (224,224)
# brands = ["INTO YOU", "CARSLAN","rom&nd"]
# for b in brands:
#     resize_data(b)


resize_data('testdata')