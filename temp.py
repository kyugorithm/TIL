import os
import requests
from bs4 import BeautifulSoup
from google_images_download import google_images_download
import cv2
import numpy as np

def download_images(query, limit=100, output_directory='downloaded_images'):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": query,
        "limit": limit,
        "format": "jpg",
        "output_directory": output_directory,
        "no_directory": True,
        "silent_mode": True
    }
    paths = response.download(arguments)
    return paths[0][query]

def is_logo(image_path, min_edge_ratio=0.1, max_edge_ratio=0.9):
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    
    edge_ratio = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    return min_edge_ratio < edge_ratio < max_edge_ratio

def crawl_logo_images(brand_names, images_per_brand=100):
    for brand in brand_names:
        print(f"Crawling images for: {brand}")
        
        # 로고 특화 키워드 추가
        queries = [
            f"{brand} logo",
            f"{brand} brand logo",
            f"{brand} official logo",
            f"{brand} symbol"
        ]
        
        for query in queries:
            output_dir = os.path.join('logo_images', brand)
            os.makedirs(output_dir, exist_ok=True)
            
            downloaded_images = download_images(query, limit=images_per_brand // len(queries), output_directory=output_dir)
            
            for img_path in downloaded_images:
                if is_logo(img_path):
                    print(f"  Kept logo image: {img_path}")
                else:
                    os.remove(img_path)
                    print(f"  Removed non-logo image: {img_path}")

# 브랜드 리스트
brand_names = ["Apple", "Nike", "Coca-Cola", "Microsoft", "Amazon"]

# 크롤링 실행
crawl_logo_images(brand_names)
