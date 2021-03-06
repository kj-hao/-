
# =============================================================================
# # -*- coding: utf-8 -*-
# """
# Created on Thu Mar 19 15:18:30 2020
# 
# @author: kjhao
# """
# 
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np
#  
# 
# #读取图片
# img_eg = mpimg.imread("2.jpg")
# print(img_eg.shape)
# #(650, 650, 3)
# 
# #奇异值分解
# img_temp = img_eg.reshape(650, 650* 3)#先将图片变成600×1200，再做奇异值分解。
# U,Sigma,VT = np.linalg.svd(img_temp)#从svd函数中得到的奇异值sigma它是从大到小排列的。
# #取前部分奇异值重构图片
# # 取前60个奇异值
# sval_nums = 60
# img_restruct1 = (U[:,0:sval_nums]).dot(np.diag(Sigma[0:sval_nums])).dot(VT[0:sval_nums,:])
# img_restruct1 = img_restruct1.reshape((650, 650, 3))
#  
# # 取前120个奇异值
# sval_nums = 120
# img_restruct2 = (U[:,0:sval_nums]).dot(np.diag(Sigma[0:sval_nums])).dot(VT[0:sval_nums,:])
# img_restruct2 = img_restruct2.reshape((650, 650, 3))
# 
# #将照片显示出来，对比效果
# fig, ax = plt.subplots(1,3,figsize = (24,32))
#  
# ax[0].imshow(img_eg)
# ax[0].set(title = "src")
# ax[1].imshow(img_restruct1.astype(np.uint8))
# ax[1].set(title = "nums of sigma = 60")
# ax[2].imshow(img_restruct2.astype(np.uint8))
# ax[2].set(title = "nums of sigma = 120")
# =============================================================================


import numpy as np
import pandas as pd
from scipy.io import loadmat
 
# 读取数据，使用自己数据集的路径。
train_data_mat = loadmat("train_data2.mat")
train_data = train_data_mat["Data"]
print(train_data.shape)

# 数据必需先转为浮点型，否则在计算的过程中会溢出，导致结果不准确
train_dataFloat = train_data / 255.0

def SVD(train_dataFloat):
    # 计算特征值和特征向量
    eval_sigma1,evec_u = np.linalg.eigh(train_dataFloat.dot(train_dataFloat.T))

    #降序排列后，逆序输出
    eval1_sort_idx = np.argsort(eval_sigma1)[::-1]
    # 将特征值对应的特征向量也对应排好序
    eval_sigma1 = np.sort(eval_sigma1)[::-1]
    evec_u = evec_u[:,eval1_sort_idx]

    # 计算奇异值矩阵的逆
    eval_sigma1 = np.diag(np.sqrt(eval_sigma1))
    eval_sigma1_inv = np.linalg.inv(eval_sigma1)
    # 计算右奇异矩阵
    evec_part_vT = eval_sigma1_inv.dot((evec_u.T).dot(train_dataFloat))
    evec_part_v=np.transpose(evec_part_vT)
    return evec_u,eval_sigma1,evec_part_vT

evec_u,eval_sigma1,evec_part_vT=SVD(train_dataFloat)


