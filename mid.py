import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# 資料前處理
import cv2,os
labels = []
train_data = []
train_labels = []
brand = ["INTO YOU","rom&nd","CARSLAN"]
label_dict = {"INTO YOU":0,"rom&nd":1,"CARSLAN":2}
i=0
for b in brand:
    for img_file in os.listdir(b):
        img = cv2.imread(b+'/'+img_file)
        train_data.append(img)
        train_labels.append(label_dict[b])

from tensorflow.keras.utils import to_categorical
train_labels = to_categorical(train_labels, num_classes=3)

# 正規化
import numpy as np
train_data = np.array(train_data)/255.0
train_labels = np.array(train_labels)


print(train_data.shape, train_labels.shape)



# 模型建置
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
# 宣告這是一個 Sequential 循序性的深度學習模型
model = Sequential()

# 輸入層捲基層加入
model.add(Conv2D(filters=32,kernel_size=(2,2),input_shape=(224,224,3),activation='relu',padding='same'))

model.add(Conv2D(filters=32, kernel_size=(2,2), activation='relu', padding='same'))

model.add(Conv2D(filters=32, kernel_size=(2,2), activation='relu', padding='same'))



# 池化層
model.add(MaxPooling2D(pool_size=(2,2)))
# 平坦層
model.add(Flatten())
# 全連接層
model.add(Dense(64,activation = 'relu'))
# 加入 dropout比例
model.add(Dropout(0.35))

# 隱藏層第二層
model.add(Dense(64,activation = 'relu'))
# 加入 dropout比例
model.add(Dropout(0.35))

# 輸出層模型
model.add(Dense(3, activation='softmax'))
print(model.summary())



from tensorflow.keras.optimizers import Adam
# 指定 loss function, optimizier, metrics
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['acc'])
history = model.fit(train_data,train_labels,validation_split=0.2,epochs=20,batch_size=128,verbose=1,shuffle=True)



#=========== 第五步 顯示訓練歷程 模型評估===========#
import matplotlib.pyplot as plt
def show_train_history(train_history):
    plt.plot(train_history.history['acc'])
    plt.plot(train_history.history['val_acc'])
    plt.xticks([i for i in range(0, len(train_history.history['acc']))])
    plt.title('Train History')
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    plt.plot(train_history.history['loss'])
    plt.plot(train_history.history['val_loss'])
    plt.xticks(range(len(train_history.history['loss'])))
    plt.title('Loss History')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'test'], loc='upper left')
    plt.show()
show_train_history(history)


model.save("mid_model.h5")
print("模型已成功儲存")