import time
import random
from script import get_image_from_google, get_languages

def get_images_with_delay(keyword, save_path, max_num, min_delay=1, max_delay=5):
    for _ in range(max_num):
        get_image_from_google(keyword, save_path=save_path, max_num=1)
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

# 사용 예시
get_images_with_delay("Apple", save_path="temp/Apple", max_num=50)
