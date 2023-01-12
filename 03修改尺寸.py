#导入cv图片
import cv2 as cv
#读取图片
img = cv.imread('data/001.jpg')
#灰度转换
grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#修改尺寸
resize_img = cv.resize(img, dsize=(200, 200))
#显示原图
cv.imshow('img', img)
#显示修改后的图片
cv.imshow('resize_img', resize_img)
#打印原图尺寸
print('未修改', img.shape)
#打印修改后的尺寸
print('修改后', resize_img.shape)
#等待
while True:
    if ord('q')== cv.waitKey(0):
        break
# #显示灰度
# cv.imshow('grey', grey_img)
# #显示图片
# cv.imshow('read_img', img)
#等待
cv.waitKey(0)
#释放内存
cv.destroyAllWindows()