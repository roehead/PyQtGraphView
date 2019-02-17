import cv2
import numpy as np
import copy
from PyQt5.QtGui import QImage

def rotate_bound(image, angle):
    '''
    --------------------- 
    作者：hui3909 
    来源：CSDN 
    原文：https://blog.csdn.net/hui3909/article/details/78854387 
    版权声明：本文为博主原创文章，转载请附上博文链接！
    --------------------- 
    '''
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)

    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH),borderValue=125)

def QImageToCvMat(incomingImage):

    '''  Converts a QImage into an opencv MAT format  '''
    #PySide ?? 测试没通过

    incomingImage = incomingImage.convertToFormat(QImage.Format.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.constBits()
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(QImage.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

def np2qpixmap(np_img):
    #frame = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGBA)
    #frame = copy.deepcopy(frame1)
    frame = np_img
    print("framelenght=%d,(%d,%d),%",(frame.size,frame.shape[0],frame.shape[1],frame.shape[0]*frame.shape[1]*4))
    img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB32) #  , frame.shape[1] * 4 RGBA8888
    print("byteCount()=%d"%img.byteCount())
    return img #QPixmap.fromImage(img)
    '''
    img=cv2.resize(src=img,dsize=None,fx=0.2,fy=0.2)
    img2=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    self._image = QtGui.QImage(img2[:],img2.shape[1], img2.shape[0],img2.shape[1] * 3, QtGui.QImage.Format_RGB888)
    注意:QImage(uchar * data, int width, int height, int bytesPerLine, Format format) 中的bytesPerLine 参数不能省略,负责造成Qimage数据错误,显示图片不正常,此参数设置为image的width*image.channels
    --------------------- 
    作者：Lynn_Chan 
    来源：CSDN 
    原文：https://blog.csdn.net/ccchen706/article/details/71425653 
    版权声明：本文为博主原创文章，转载请附上博文链接！
    '''
def main():
    
    img = QImage("D:\\Tulips.jpg")
    print("byteCount()=%d"%img.byteCount())
    print("bytesPerLine()=%d"%img.bytesPerLine())
    cv_np = convertQImageToMat(img)
    #cv_np = QImageToCvMat(img)  #测试没通过
    cv_img = cv_np
    print("%d,%d,%d"%(cv_img.shape[0],cv_img.shape[1],cv_img.shape[2]))

    
    cv_img = rotate_bound(cv_img,30)    

    cv2.imwrite("D:\\tulips_cv.jpg",cv_img)
    #cv2.imshow("OpenCV",cv_img)
    #cv2.waitKey()

    #cv_img = cv2.cvtColor(cv_np, cv2.COLOR_BGR2RGB)
    #w = cv_img.shape[0]
    #h = cv_img.shape[1]
    print("lenght=%d,(%d,%d)",(cv_img.size,cv_img.shape[0],cv_img.shape[1]))
    print("bit[1]=%d,bit[2]=%d,bit[3]=%d",(cv_img[0][0][0],cv_img[0][0][1],cv_img[0][0][2]))



    #qt_img = QImage(cv_img, w, h, w * 4, QImage.Format_RGB32)
    
    qt_img = np2qpixmap(cv_img)
    print("byteCount()=%d"%qt_img.byteCount())
    qt_img.save("D:\\tulips_qt.jpg")
    return cv_img
    
if __name__ == '__main__':
    main()
'''
cv::cvtColor()支持多种颜色空间之间的转换，其支持的转换类型和转换码如下：

1、RGB和BGR（opencv默认的彩色图像的颜色空间是BGR）颜色空间的转换

cv::COLOR_BGR2RGB
cv::COLOR_RGB2BGR
cv::COLOR_RGBA2BGRA
cv::COLOR_BGRA2RGBA

2、向RGB和BGR图像中增添alpha通道

cv::COLOR_RGB2RGBA
cv::COLOR_BGR2BGRA

3、从RGB和BGR图像中去除alpha通道

cv::COLOR_RGBA2RGB
cv::COLOR_BGRA2BGR

4、从RBG和BGR颜色空间转换到灰度空间

cv::COLOR_RGB2GRAY
cv::COLOR_BGR2GRAY

cv::COLOR_RGBA2GRAY
cv::COLOR_BGRA2GRAY

5、从灰度空间转换到RGB和BGR颜色空间

cv::COLOR_GRAY2RGB
cv::COLOR_GRAY2BGR

cv::COLOR_GRAY2RGBA
cv::COLOR_GRAY2BGRA

6、RGB和BGR颜色空间与BGR565颜色空间之间的转换

cv::COLOR_RGB2BGR565
cv::COLOR_BGR2BGR565
cv::COLOR_BGR5652RGB
cv::COLOR_BGR5652BGR
cv::COLOR_RGBA2BGR565
cv::COLOR_BGRA2BGR565
cv::COLOR_BGR5652RGBA
cv::COLOR_BGR5652BGRA

7、灰度空间域BGR565之间的转换

cv::COLOR_GRAY2BGR555
cv::COLOR_BGR5552GRAY

8、RGB和BGR颜色空间与CIE XYZ之间的转换

cv::COLOR_RGB2XYZ
cv::COLOR_BGR2XYZ
cv::COLOR_XYZ2RGB
cv::COLOR_XYZ2BGR

9、RGB和BGR颜色空间与uma色度（YCrCb空间）之间的转换

cv::COLOR_RGB2YCrCb
cv::COLOR_BGR2YCrCb
cv::COLOR_YCrCb2RGB
cv::COLOR_YCrCb2BGR

10、RGB和BGR颜色空间与HSV颜色空间之间的相互转换

cv::COLOR_RGB2HSV
cv::COLOR_BGR2HSV
cv::COLOR_HSV2RGB
cv::COLOR_HSV2BGR

11、RGB和BGR颜色空间与HLS颜色空间之间的相互转换

cv::COLOR_RGB2HLS
cv::COLOR_BGR2HLS
cv::COLOR_HLS2RGB
cv::COLOR_HLS2BGR

12、RGB和BGR颜色空间与CIE Lab颜色空间之间的相互转换


cv::COLOR_RGB2Lab
cv::COLOR_BGR2Lab
cv::COLOR_Lab2RGB
cv::COLOR_Lab2BGR

13、RGB和BGR颜色空间与CIE Luv颜色空间之间的相互转换

cv::COLOR_RGB2Luv
cv::COLOR_BGR2Luv
cv::COLOR_Luv2RGB
cv::COLOR_Luv2BGR

14、Bayer格式（raw data）向RGB或BGR颜色空间的转换

cv::COLOR_BayerBG2RGB
cv::COLOR_BayerGB2RGB
cv::COLOR_BayerRG2RGB
cv::COLOR_BayerGR2RGB
cv::COLOR_BayerBG2BGR
cv::COLOR_BayerGB2BGR
cv::COLOR_BayerRG2BGR
cv::COLOR_BayerGR2BGR
--------------------- 
作者：PHILOS_THU 
来源：CSDN 
原文：https://blog.csdn.net/guduruyu/article/details/68941554 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''