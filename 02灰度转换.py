#导入cv图片
import cv2 as cv
#读取图片
img = cv.imread('data/1_001.jpg')
#灰度转换
grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#显示灰度
cv.imshow('grey', grey_img)
#显示图片
cv.imshow('read_img', img)
#等待
cv.waitKey(0)
#释放内存
cv.destroyAllWindows()







