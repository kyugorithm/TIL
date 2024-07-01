import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import hashlib

# 로고 이미지를 저장할 디렉토리 생성
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 이미지 해시값으로 중복 이미지 체크
def get_image_hash(image):
    return hashlib.md5(image.tobytes()).hexdigest()

# 이미지를 다운로드하고 저장
def save_image(url, directory, brand_name, seen_hashes):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image_hash = get_image_hash(image)
        
        if image_hash not in seen_hashes:
            seen_hashes.add(image_hash)
            image_path = os.path.join(directory, f"{brand_name}_{len(seen_hashes)}.jpg")
            image.save(image_path)
            print(f"Saved image: {image_path}")
        else:
            print("Duplicate image found, skipping.")
    except Exception as e:
        print(f"Failed to save image from {url}: {e}")

# 메인 크롤링 함수
def crawl_images(brand_name, num_images=100):
    # Selenium 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    search_url = f"https://www.google.com/search?q={brand_name}+logo&tbm=isch"

    driver.get(search_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    image_tags = soup.find_all("img", {"class": "rg_i"})
    
    if not image_tags:
        print("No images found.")
        return

    directory = f"logos/{brand_name}"
    create_directory(directory)
    seen_hashes = set()

    for img_tag in image_tags[:num_images]:
        try:
            img_url = img_tag['src']
            save_image(img_url, directory, brand_name, seen_hashes)
        except KeyError:
            continue

# 사용 예제
brand_names = ["Nike", "Adidas", "Apple"]
for brand in brand_names:
    crawl_images(brand, num_images=50)
