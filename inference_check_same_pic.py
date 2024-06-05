import argparse
import os
import tqdm
import cv2
import numpy as np
import torch
import glob
from backbones import get_model
from numpy import dot
from numpy.linalg import norm
import torch.nn.functional as F
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
# CUDA_VISIBLE_DEVICES=4 python inference_check_same_pic.py --img_path /Storage/221Backup/backup/kc/crawled_data/dt_general_SR --idx 3
# CUDA_VISIBLE_DEVICES=5 python inference_check_same_pic.py --img_path /Storage/221Backup/backup/kc/crawled_data/dt_general_SR --idx 4
# CUDA_VISIBLE_DEVICES=6 python inference_check_same_pic.py --img_path /Storage/221Backup/backup/kc/crawled_data/dt_general_SR --idx 5
# CUDA_VISIBLE_DEVICES=7 python inference_check_same_pic.py --img_path /Storage/221Backup/backup/kc/crawled_data/dt_general_SR --idx 6
# CUDA_VISIBLE_DEVICES=1 python inference_check_same_pic.py --img_path /Storage/221Backup/backup/kc/crawled_data/dt_general_SR --idx 7
# CUDA_VISIBLE_DEVICES=2 python inference_check_same_pic.py --img_path /Storage/221Backup/backup/kc/crawled_data/dt_general_SR --idx 8

@torch.no_grad()
def inference(weight, name, img_path, idx):
   
    fld_path    = sorted(glob.glob(img_path + '/*'))[500*idx:500*(idx+1)]
       
    net = get_model(name, fp16=False)
    net.load_state_dict(torch.load(weight))
    net.eval()
    net.cuda()
    for fld in tqdm.tqdm(fld_path):
        fld_name = fld.split('/')[-1]
        img_list = sorted(glob.glob(fld + '/*'))
        feat     = None
        print(f'{fld_name} : 폴더 처리를 시작합니다.')
        for img_dir in img_list:
            img   = cv2.imread(img_dir)
            img   = cv2.resize(img, (112, 112))
            img   = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img   = np.transpose(img, (2, 0, 1))
            img   = torch.from_numpy(img).unsqueeze(0).float() # 0 ~ 255
            # img.div_(255)
            img.div_(255).sub_(0.5).div_(0.5) # -1 ~ 1
            feat1 = net(img.cuda())
            feat1 = F.normalize(feat1, p=2, dim=1)
            feat1 = feat1.detach().cpu().numpy()
            if feat is None:
                feat = feat1
            else:
                feat = np.concatenate((feat, feat1), axis=0)

        if feat is not None:
            cosim_all = None 
            for i in range(feat.shape[0]):
                cosim = cosine_similarity(feat[i:i+1,:],feat)
                cosim = [1 if x>0.8 else 0 for x in cosim[0,:]]
                cosim = np.array(cosim).reshape((1,-1))
                if cosim_all is None:
                    cosim_all = cosim
                else:
                    cosim_all = np.concatenate((cosim_all, cosim), axis=0)

            labels = DBSCAN(min_samples=1).fit_predict(cosim_all)
            print(f'클러스터 개수 : {1+labels.max()} / 파일 개수 : {len(img_list)}')
            for i in range(labels.max()):
                if sum(labels == i) > 1:
                    print(f'Label {i}에 중복 케이스가 존재합니다.')
                    idx_same = np.where(labels == i)
                    print(f'동일사진 index : {idx_same[0]}')

                    for idx in idx_same[0][1:]:
                        print(f'Delete file : {img_list[idx]}')
                        os.remove(img_list[idx])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyTorch ArcFace Training')
    parser.add_argument('--network', type=str, default='r100', help='backbone network')
    parser.add_argument('--weight', type=str, default='pretrained/partial_fc_glint360k_r100.pth')
    parser.add_argument('--img_path', type=str, default='/Storage/221Backup/backup/kc/crawled_data/dt_side_SR')
    parser.add_argument("--idx", type=int, default=0, help="Range index")

    args = parser.parse_args()
    inference(args.weight, args.network, args.img_path, args.idx)