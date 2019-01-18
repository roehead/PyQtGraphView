#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PyQt5.QtCore import  pyqtSignal,QPoint, Qt, QEvent
from PyQt5.QtGui import QPainter, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView
#from MainWindow import*

class GraphicsView(QGraphicsView):
    #item属性变量
    PointSize = 10
    ItemId         = 1  #绘图项自定义数据的key
    ItemDesciption = 2  #绘图项自定义数据的key
    seqNum=0
    backZ=0
    frontZ=0

    #信号定义
    mouseMovePoint   = pyqtSignal(QPoint,QMouseEvent) #鼠标移动
    mouseClicked     = pyqtSignal(QPoint) #鼠标单击
    mouseRelease     = pyqtSignal(QPoint) #鼠标释放
    mouseDoubleClick = pyqtSignal(QPoint) #双击事件
    keyPress         = pyqtSignal(QKeyEvent) #按键事件

    m_point1 = QPoint(0,0)
    m_point2 = QPoint(0,0)
    m_rect_items = []
    m_start_draw = False

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        #self.m_Path= None
        #self.isEnd = False

    def set_item_index(self,item,item_name):

        self.frontZ = self.frontZ +1
        item.setZValue(self.frontZ)

        self.seqNum = self.seqNum + 1
        item.setData(self.ItemId,self.seqNum)

        item.setData(self.ItemDesciption,item_name)

    def wheelEvent(self, event):
        #factor = 1.41 ** (-event.delta() / 240.0) 
        factor = event.angleDelta().y()/120.0
        if event.angleDelta().y()/120.0 > 0:
            factor=2
        else:
            factor=0.5
        self.scale(factor, factor)

    def mouseMoveEvent(self, event): #鼠标移动事件
        point = QPoint()
        point=event.pos() #QGraphicsView的坐标
        self.mouseMovePoint.emit(point,event) #释放信号
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event): #鼠标左键按下事件
        if (event.button()==Qt.LeftButton):
            point = QPoint()
            point=event.pos() #QGraphicsView的坐标
            self.mouseClicked.emit(point) #释放信号
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event): #鼠标双击事件
        if (event.button()==Qt.LeftButton):
            point = QPoint()
            point=event.pos() #QGraphicsView的坐标
            self.mouseDoubleClick.emit(point) #释放信号
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event): #按键事件
        self.keyPress.emit(event)
        super().keyPressEvent(event)


    def mouseReleaseEvent(self, event):
        if (event.button()==Qt.LeftButton):
            point = QPoint()
            self.m_start_draw = False
            point=event.pos() #QGraphicsView的坐标
            self.mouseRelease.emit(point) #释放信号
        super().mouseReleaseEvent(event)
