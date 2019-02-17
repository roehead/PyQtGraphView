#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import cv2
from MainWindow import *
from PyQt5.QtWidgets import  QApplication

#MAC = True
#try:
#    from PyQt5.QtGui import qt_mac_set_native_menubar
#except ImportError:
#    MAC = False

#PageSize = (595, 842) # A4 in points
PageSize = (612, 792) # US Letter in points
PointSize = 10

#MagicNumber = 0x70616765
#FileVersion = 1

#Dirty = False

#ItemId = 1          #绘图项自定义数据的key
#ItemDesciption = 2  #绘图项自定义数据的key

#seqNum=0   #绘图项索引
#backZ=0    #绘图项索引
#frontZ=0   #绘图项索引


app = QApplication(sys.argv)
form = GMainWindow()
rect = QApplication.desktop().availableGeometry()
form.resize(int(rect.width() * 0.6), int(rect.height() * 0.9))
form.show()
app.exec_()