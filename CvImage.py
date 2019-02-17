#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import copy
from PyQt5.QtGui import QImage, QTransform



# view.ItemId = 1  #绘图项自定义数据的key
# view.ItemDesciption = 2  #绘图项自定义数据的key

# view.seqNum=0
# view.backZ=0
# view.frontZ=0
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
    #(cX, cY) = (0.0, 0.0)
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

def QImage2cvMat(image): #(QImage image)
    mat =  None #cv2.Mat 
    #qDebug() << image.format();
    img_frm = image.format()

    if ((img_frm == QImage.Format_ARGB32)
     or (img_frm == QImage.Format_RGB32)
     or (img_frm == QImage.Format_ARGB32_Premultiplied)):
        mat = np.array(image.height(), image.width(), cv2.CV_8UC4, image.constBits(), image.bytesPerLine())

    if (img_frm == QImage.Format_RGB888):
        mat = np.array(image.height(), image.width(), cv2.CV_8UC3, image.constBits(), image.bytesPerLine())
        cv2.cvtColor(mat, mat, cv2.CV_BGR2RGB)

    if (img_frm == QImage.Format_Indexed8):
        mat = np.array(image.height(), image.width(), cv2.CV_8UC1, image.constBits(), image.bytesPerLine())

    return mat;

def qt_image_to_array(img, share_memory=False):
    """ Creates a numpy array from a QImage.

        If share_memory is True, the numpy array and the QImage is shared.
        Be careful: make sure the numpy array is destroyed before the image, 
        otherwise the array will point to unreserved memory!!
    """
    assert isinstance(img, QImage), "img must be a QtGui.QImage object" 
    assert img.format() == QImage.Format.Format_RGB32, \
        "img format must be QImage.Format.Format_RGB32, got: {}".format(img.format())

    img_size = img.size()
    buffer = img.constBits()
    buffer = img.bits()
    print(buffer[0]) 
    # Sanity check
    n_bits_buffer = len(buffer) * 8
    n_bits_image  = img_size.width() * img_size.height() * img.depth()
    assert n_bits_buffer == n_bits_image, \
        "size mismatch: {} != {}".format(n_bits_buffer, n_bits_image) 

    assert img.depth() == 32, "unexpected image depth: {}".format(img.depth())

    # Note the different width height parameter order!
    arr = np.ndarray(shape  = (img_size.height(), img_size.width(), img.depth()//8),
                     buffer = buffer, 
                     dtype  = np.uint8)

    if share_memory:
        return arr
    else:
        return copy.deepcopy(arr)
def np2qimage(np_img):
    #frame = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGBA)
    #frame = copy.deepcopy(np_img)
    frame = np_img
    print("framelenght=%d,(%d,%d),%",(frame.size,frame.shape[0],frame.shape[1],frame.shape[0]*frame.shape[1]*4))
    img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB32) #  , frame.shape[1] * 4 RGBA8888
    print("byteCount()=%d"%img.byteCount())
    return img #QPixmap.fromImage(img)


def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(QImage.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

def QImageToCvMat(self,incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(QtGui.QImage.Format.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.constBits()
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr