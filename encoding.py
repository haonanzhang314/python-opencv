import os

from retinaface import Retinaface
# 将所有人脸编码的结果放在一个列表中，得到的就是已知的所有人脸的特征列表，在之后获得的实时图片中的人脸都需要与已知的列表进行对比，就能知道谁是谁
'''
在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
'''
retinaface = Retinaface(1)

list_dir = os.listdir("face_dataset")
image_paths = []
names = []
for name in list_dir:
    image_paths.append("face_dataset/"+name)
    names.append(name.split("_")[0])

retinaface.encode_face_dataset(image_paths,names)