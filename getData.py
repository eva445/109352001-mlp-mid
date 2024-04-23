from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import requests
# 從網頁下載圖片
brand = "rom&nd"
url = "https://www.amazon.com/s?k=rom%26nd&crid=VV6Q1XF6KMOH&sprefix=rom%26nd%2Caps%2C264&ref=nb_sb_noss_1"


def download_image(url, folder, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 檢查目標文件夾是否存在，如果不存在就創建它
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            # 構建文件路徑
            file_path = os.path.join(folder, filename)
            
            # 將圖片保存到文件中
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("圖片下載成功！")
        else:
            print("無法下載圖片：狀態碼", response.status_code)
    except Exception as e:
        print("發生錯誤：", e)



# 使用Selenium啟動一個瀏覽器
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 在後台運行瀏覽器
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

driver.get(url)

# 等待網頁加載完成
time.sleep(5)

# 獲取網頁源代碼
html_content = driver.page_source

driver.quit()  # 關閉瀏覽器

# 使用Beautiful Soup解析HTML
soup = BeautifulSoup(html_content, "html.parser")
img_tags = soup.find_all("img", class_="s-image")

img_urls = []
# 提取前21張圖片的src屬性
for img_tag in img_tags:
    alt_text = img_tag.get("alt")
    print(alt_text)
    if (brand in alt_text):
        src = img_tag.get("src")
        img_urls.append(src)
        print(src)

# 目標文件夾
folder = os.path.join(os.path.dirname(__file__), brand)

# 下載每張圖片
for i, url in enumerate(img_urls):
    filename = f"{i + 1}.jpg"  # 文件名可以根據需要進行修改
    download_image(url, folder, filename)