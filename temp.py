import lpips
import torch
import torch.nn as nn

# LPIPS 모델 로드 (VGG16 사용)
lpips_loss = lpips.LPIPS(net='vgg').to('cuda' if torch.cuda.is_available() else 'cpu')

# VGG16에서 특정 Low-Level Feature만 활성화하기 위해 나머지 Layer를 제거
lpips_loss.net.slice3 = nn.Identity()  # conv3_x 제거
lpips_loss.net.slice4 = nn.Identity()  # conv4_x 제거
lpips_loss.net.slice5 = nn.Identity()  # conv5_x 제거

print(lpips_loss)
