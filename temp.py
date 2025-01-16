import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# gamma < 1: 어두운 영역이 밝아짐
# gamma > 1: 밝은 영역이 어두워짐
brightened = adjust_gamma(image, gamma=0.5)
