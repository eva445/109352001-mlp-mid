
# 資料前處理
import cv2,os
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
labels = []
test_data = []
train_labels = []
label_dict = {"INTO YOU":0,"rom&nd":1,"CARSLAN":2}
i=0
for img_file in sorted(os.listdir('testdata'), key=lambda x: int(x.split('.')[0])):
    img = cv2.imread('testdata/'+img_file)
    test_data.append(img)
    # cv2.imshow(f"{img_file}", img)
    # cv2.waitKey(0)
result_img = test_data
test_data = np.array(test_data)/255.0


# 在需要時加載模型
from tensorflow.keras.models import load_model

# 加載模型
model = load_model("mid_model.h5")
print("模型已成功加載")


#=========== 預測結果 ===========#

#並將字串轉為整數，正規化並預測
pred= model.predict(test_data)

#CSV格式
submit='ImageId,Label\n'

rev_label_dict = {label_dict[key] : key for key in label_dict}

for i in range(len(pred)):    
    # # 找出概率最大的類別索引作為預測結果
    predicted_label_index = np.argmax(pred[i])

    # 使用索引對應的字典中的值作為預測的類別名稱
    predicted_label_name = rev_label_dict[predicted_label_index]

    submit += str(i+1) + ',' + str(np.argmax(pred[i])) + '\n'
    cv2.imshow(f"{predicted_label_name}{i}", result_img[i])


#存成CSV檔
open('submit.csv', 'w').write(submit)
cv2.waitKey(0)