#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from CvImage import *
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, Qt, pyqtSlot,QEvent
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QTransform, QImage, QPixmap,QTransform
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsRectItem,QApplication,
                             QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsLineItem, QGraphicsItemGroup,
                             QGraphicsTextItem, QMessageBox, QInputDialog, QColorDialog, QFontDialog)
from PixmapItem import GraphicsPixmapItem
MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

class Slot_MainWindow(object):  # QDialog
        '''
    本模块基于以下原代码修改：
        一）《QT5.9开发指南》示例代码"(C++)
             samp8_5GraphicsDraw之槽函数部分
        二）http://blog.sina.com.cn/s/blog_c22e36090102x1p3.html
           《python3+PyQt5 图形项的自定义和交互--实现page Designer应用程序》
            by basisworker in 2017-03-06 09:58:31
        修改记录：
            1.原主对话框类QDialog改为QMainWindow
            2.图形像类拆分为独立模块文件
            4.界面部分代码移到Ui2_MainWindow模块（类）
            5.槽函数部分Slot——MainWindow模块（类）
        '''
    def setBrushColor(self, item):
        # 函数模板
        color = item.brush().color()
        color = QColorDialog.getColor(color, self, "选择填充颜色")
        if color.isValid():
            item.setBrush(QBrush(color))
    def onCbChanged(self,CbIndex):
        item = self.scene.selectedItems()[0]
        assert isinstance(item,GraphicsPixmapItem), "The item must be GraphicsPixmapItem" 
        CompMod = self.comboBox.itemData(CbIndex)
        item.setCompMode(CompMod)
        #QMessageBox.warning(self, "onCbChanged", "CbIndex=%d,CompMod=%d"%(CbIndex,CompMod))

    def on_mouseMovePoint(self, point, event):  # 鼠标移动事件，point是 GraphicsView的坐标,物理坐标

        pointScene = self.view.mapToScene(point)  # 转换到Scene坐标

        #在状态栏显示坐标
        self.labViewCord.setText("View%d,%d" % (point.x(), point.y()))
        self.labSceneCord.setText("Scene%.0f,%.0f" % (pointScene.x(), pointScene.y()))

        

        #item = self.scene.itemAt(pointScene, self.view.transform())  # 获取光标下的绘图项
        #鼠标左键按下时移动图片
        if ((self.view.m_mouse_press == True) and (self.view.m_start_draw == False)): 
            # and (QApplication.mouseButtons() == QEvent.MouseButtonPress)):
            # and (QApplication.keyboardModifiers() == Qt.ShiftModifier)):
            #QMessageBox.warning(self, "debug clicked", "mouse_button%d"%QApplication.mouseButtons())
            self.view.m_point2 = pointScene #记录鼠标移动时最新的坐标位置
            point_item = self.view.m_point_item
            point1 = self.view.m_point1
            point2 = self.view.m_point2
            self.view.m_drag_item.setPos(point_item.x()+(point2.x()-point1.x()),
                        point_item.y()+(point2.y()-point1.y()))

        #鼠标左键按下并且按住Ctrl键时动态显示剪切框
        if ((self.view.m_start_draw == True)
                and (QApplication.keyboardModifiers() == Qt.ControlModifier)):

            rect_item = self.view.m_drag_item.boundingRect()
            point_item = self.view.m_drag_item.mapFromScene(pointScene)
            #if rect_item.containsPoint(point_item, Qt.OddEvenFill):
            if rect_item.contains(point_item):
                self.view.m_point2 = pointScene #记录鼠标移动时最新的坐标位置
                #删除移动剪切框
                while self.view.m_rect_items:
                  item1 = self.view.m_rect_items.pop()
                  if item1:
                      self.scene.removeItem(item1)
                      del item1
                point1 = self.view.m_point1
                point2 = self.view.m_point2

                points = QPolygonF()
                points.append(point1)
                points.append(QPointF(point1.x(),point2.y()))
                points.append(point2)
                points.append(QPointF(point2.x(),point1.y()))

                item1 = self.scene.addPolygon(points,Qt.red)
                item1.style=Qt.SolidLine
                self.view.m_rect_items.append(item1)
        return

    def on_mouseClicked(self, point):  # 鼠标单击事件

        pointScene = self.view.mapToScene(point)  # 转换到Scene坐标
        item = self.scene.itemAt(pointScene, self.view.transform())  # 获取光标下的绘图项

        self.view.m_point1 = pointScene  #记录鼠标单击时坐标位置

        if item != None and item.data(self.view.ItemId) != None:  # 有绘图项
            pointItem = item.mapFromScene(pointScene)  # 转换为绘图项的局部坐标
            self.labItemCord.setText("Item%.0f,%.0f" % (pointItem.x(), pointItem.y()))
            self.labItemInfo.setText(item.data(self.view.ItemDesciption) + ", ItemId=%d" % item.data(self.view.ItemId))

        if isinstance(item,GraphicsPixmapItem): #有图片绘图项
            self.view.m_mouse_press = True
            self.view.m_drag_item = item
            self.view.m_point_item = item.mapToScene(QPoint(0,0))
            self.comboBox.setEnabled(True)
        else:
            self.comboBox.setEnabled(False)

        if (isinstance(item,GraphicsPixmapItem) 
                and (QApplication.keyboardModifiers() == Qt.ControlModifier)
                and (self.view.m_start_draw == False)): #有图版绘图项，并且按下Ctrl键
            #QMessageBox.warning(self, "debug", "Is a Pixmap!")
            self.view.m_start_draw = True

        return

    def on_mouseRelease(self, point):  # 鼠标释放事件

        self.view.m_mouse_press = False
        self.view.m_drag_item = None
        
        while self.view.m_rect_items:
           item1 = self.view.m_rect_items.pop()
           if item1:
              self.scene.removeItem(item1)
              del item1

        pointScene = self.view.mapToScene(point)  # 转换到Scene坐标
        item = self.scene.itemAt(pointScene, self.view.transform())  # 获取光标下的绘图项
        if (    (self.view.m_start_draw == True)      and 
                (isinstance(item,GraphicsPixmapItem)) and
                (QApplication.keyboardModifiers() == Qt.ControlModifier)):
            
            img=QImage(item.pixmap())
            angle = item.rotation()
            h = img.height()
            w = img.width()
            
            #利用cv2旋转图片
            img_cv = convertQImageToMat(img)
            img_cv = rotate_bound(img_cv,angle)
            
            #转换Qt格式
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGBA)
            imgRotate = QImage(img_cv,img_cv.shape[1], img_cv.shape[0],QImage.Format_RGBA8888)
            #imgRotate = np2qimage(imgR)  #调用不成功，用上面两行代替
            
            i_point1 = self.view.m_point1
            i_point2 = self.view.m_point2
            
            #计算选择框在scence中的左上角位置与长宽尺寸
            top_left = QPoint()
            top_left.setX(min(i_point1.x(),i_point2.x()))
            top_left.setY(min(i_point1.y(),i_point2.y()))
            h1 = abs(i_point1.y() - i_point2.y())
            w1 = abs(i_point1.x() - i_point2.x())
            rect1 = QRect(top_left.x(), top_left.y(),w1,h1)

            #img.save("temp.png")  #仅用于测试

            #计算旋转后的图片尺寸
            (cX, cY) = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
            cosA = np.abs(M[0, 0])
            sinA = np.abs(M[0, 1])
         
            nW = int((h * sinA) + (w * cosA))
            nH = int((h * cosA) + (w * sinA))
         
            M[0, 2] += (nW / 2) - cX
            M[1, 2] += (nH / 2) - cY
            
            #通过旋转计算左上角的偏移
            matrix1 = QTransform()
            matrix1.rotate(angle)      #再旋转   （顺序是倒的？）
            matrix1.translate(-cX,-cY) #先移到放大图片的中心
            topleft = matrix1.map(QPoint(0,0))
            #topleft = matrix1.map(QPoint(-cX,-cY))
            #QMessageBox.warning(self, "debug clicked", "(nW,nH)=(%d,%d),topleft=(%d,%d),dw,dh=(%d,%d)"
            #                %((nW/2),(nH/2),topleft.x()+nW/2,topleft.y()+nH/2,sinA*h,sinA*w))

            #将选择框映射到item（可以是任意图片）局部坐标后，计算在旋转后图片（已扩展）中的顶点位置
            matrix = QTransform()
            matrix.translate(topleft.x()+nW/2,topleft.y()+nH/2) #sinA*h,0)  #必须先平移，先旋转坐标方向变化
            matrix.rotate(angle)

            #matrix.rotateAround(QPoint(img.width()/2,img.height()/2),item.rotation())
            polygon1 = item.mapFromScene(QRectF(rect1))  #转换为item局部坐标（即image坐标）
            polygon1 = matrix.map(polygon1)   #利用Qt矩阵映射选择柜局部坐标
            pos_point = self.position()

            #imgRotate = img.transformed(matrix)

            polygon2 = polygon1.toPolygon()
            assert polygon2.at(0).y() == polygon2.at(1).y(), "The polygon must be a Horizon Rectangle!" 

            rect1 = QRect(polygon2.at(0),polygon2.at(2))
            rect1 = polygon2.boundingRect()
            img = imgRotate.copy(rect1)
            item = GraphicsPixmapItem(self.scene, QPixmap(img), 
                                      pos_point, 
                                      matrix=QTransform())
            self.view.set_item_index(item,"图片")

            #显示剪切位置（用于调试）
            if False:
                item = GraphicsPixmapItem(self.scene, QPixmap(img), 
                                          pos_point, 
                                          matrix=QTransform())
                self.view.set_item_index(item,"图片")

                polygon3 = item.mapToScene(polygon1) #从未旋转的item局部坐标映射到场景坐标

                self.scene.removeItem(item)
                del item

                itemR = GraphicsPixmapItem(self.scene, QPixmap(imgRotate), 
                                          pos_point, 
                                          matrix=QTransform())
                self.view.set_item_index(itemR,"图片")

                #self.scene.removeItem(itemR)
                #del itemR

                item = self.scene.addPolygon(polygon3,Qt.red) #显示剪切位置
                item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
                self.view.set_item_index(item,"剪切框")

            self.view.m_start_draw = False
        return

    def on_keyPress(self, event):  # 按键事件
        if len(self.scene.selectedItems()) != 1:
            QMessageBox.warning(self, "debug clicked", "No item found!")
            return  # 没有选中的绘图项，或选中的多于1个
        item = self.scene.selectedItems()[0]  # QGraphicsItem

        if event.key() == Qt.Key_Delete:  # 删除
            self.scene.removeItem(item)

        elif event.key() == Qt.Key_Space:  # 顺时针旋转90度
            item.setRotation(30 + item.rotation())

        elif event.key() == Qt.Key_PageUp:  # 放大
            item.setScale(0.1 + item.scale())
        elif event.key() == Qt.Key_PageDown:  # 缩小
            item.setScale(-0.1 + item.scale())

        elif event.key() == Qt.Key_Left:  # 左移
            item.setX(-10 + item.x())

        elif event.key() == Qt.Key_Right:  # 右移
            item.setX(10 + item.x())

        elif event.key() == Qt.Key_Up:  # 上移
            item.setY(-10 + item.y())

        elif event.key() == Qt.Key_Down:  # 下移
            item.setY(10 + item.y())

    def on_mouseDoubleClick(self, point):  # 鼠标双击事件,调用相应的对话框，设置填充颜色、线条颜色或字体
        # QMessageBox.warning(self, "debug","on_mouseDoubleClick!")
        pointScene = self.view.mapToScene(point)  # 转换到Scene坐标
        # QGraphicsItem  *item=NULL
        item = self.scene.itemAt(pointScene, self.view.transform())  # 获取光标下的绘图项

        item_type = item.type()
        # QMessageBox.warning(self, "debug",str(item_type)+'<==>'+str(QGraphicsLineItem.Type))
        if item == None or item_type == None:  # 没有绘图项
            QMessageBox.warning(self, "debug", "No item found!")
            return
        # switch (item_type):  #绘图项的类型
        if item_type == 3:  # QGraphicsRectItem.Type:    #矩形框
            # 强制类型转换
            theItem = QGraphicsRectItem(item)
            self.setBrushColor(theItem)
            return

        elif item_type == 4:  # QGraphicsEllipseItem.Type:    #椭圆和圆都是 QGraphicsEllipseItem
            theItem = QGraphicsEllipseItem(item)
            self.setBrushColor(theItem)
            return

        elif item_type == 5:  # QGraphicsPolygonItem.Type:    #梯形和三角形
            theItem = QGraphicsPolygonItem(item)
            self.setBrushColor(theItem)
            return

        elif item_type == 6:  # QGraphicsLineItem.Type:    #直线，设置线条颜色
            theItem = QGraphicsLineItem(item)
            pen = theItem.pen()
            color = theItem.pen().color()
            color = QColorDialog.getColor(color, self, "选择线条颜色")
            if color.isValid():
                pen.setColor(color)
                theItem.setPen(pen)
            return

        elif item_type == 8:  # QGraphicsTextItem.Type:    #文字，设置字体
            theItem = QGraphicsTextItem(item)
            font = theItem.font()
            ok = False
            font, ok = QFontDialog.getFont(self)
            if ok:
                theItem.setFont(font)
            return

    #@pyqtSlot()
    def on_actItem_Rect(self):  # 添加一个矩形  _triggered
        rect = QRectF(-50, -25, 100, 50)
        item = QGraphicsRectItem(rect)  # x,y 为左上角的图元局部坐标，图元中心点为0,0
        item.rect = rect
        item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        item.brush = Qt.yellow
        item.setBrush(QBrush(item.brush))
        item.style = Qt.SolidLine
        #item.setTransform(QTransform())
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))
        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)
        item.setData(self.view.ItemDesciption, "矩形")

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    @pyqtSlot()
    def on_actItem_Ellipse_triggered(self):  # 添加一个椭圆
        item = QGraphicsEllipseItem(-50, -30, 100, 60)
        item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        item.setBrush(QBrush(Qt.blue))  # //填充颜色
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)  # //用于叠放顺序
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))  # //初始位置
        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)  # //自定义数据，ItemId键
        item.setData(self.view.ItemDesciption, "椭圆")  # //自定义数据，ItemDesciption键

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)
        #self.disconnect()
        #self.blockSignals(True)

    @pyqtSlot()
    def on_actItem_Polygon_triggered(self):  # 添加一个梯形

        item = QGraphicsPolygonItem()
        points = QPolygonF()

        points.append(QPointF(-40, -40))
        points.append(QPointF(40, -40))
        points.append(QPointF(100, 40))
        points.append(QPointF(-100, 40))

        item.setPolygon(points)
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))

        item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        item.setBrush(QBrush(Qt.green))
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)

        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)  # //自定义数据，ItemId键
        item.setData(self.view.ItemDesciption, "梯形")

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    @pyqtSlot()
    def on_actItem_Circle_triggered(self):  # 添加圆形
        item = QGraphicsEllipseItem(-50, -50, 100, 100)
        item.setFlags(QGraphicsItem.ItemIsMovable
                      | QGraphicsItem.ItemIsSelectable
                      | QGraphicsItem.ItemIsFocusable)
        item.setBrush(QBrush(Qt.cyan))
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))

        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)  # //自定义数据，ItemId键
        item.setData(self.view.ItemDesciption, "圆形")

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    @pyqtSlot()
    def on_actItem_Triangle_triggered(self):  # 添加三角形
        item = QGraphicsPolygonItem()
        points = QPolygonF()
        points.append(QPointF(0, -40))
        points.append(QPointF(60, 40))
        points.append(QPointF(-60, 40))
        item.setPolygon(points)
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))

        item.setFlags(QGraphicsItem.ItemIsMovable
                      | QGraphicsItem.ItemIsSelectable
                      | QGraphicsItem.ItemIsFocusable)
        item.setBrush(QBrush(Qt.magenta))
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)

        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)  # //自定义数据，ItemId键
        item.setData(self.view.ItemDesciption, "三角形")

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    @pyqtSlot()
    def on_actItem_Line_triggered(self):  # 添加直线
        item = QGraphicsLineItem(-100, 0, 100, 0)  # x,y 为左上角的图元局部坐标，图元中心点为0,0
        item.setFlags(QGraphicsItem.ItemIsMovable
                      | QGraphicsItem.ItemIsSelectable
                      | QGraphicsItem.ItemIsFocusable)

        pen = QPen(Qt.red)
        pen.setWidth(3)
        item.setPen(pen)
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))

        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)  # //自定义数据，ItemId键
        item.setData(self.view.ItemDesciption, "直线")

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    @pyqtSlot()
    def on_actItem_Text_triggered(self):  # 添加文字
        str, okPressed = QInputDialog.getText(self, "输入文字", "请输入文字")
        if okPressed == False or not str:
            return ()

        item = QGraphicsTextItem(str)

        font = self.font()
        font.setPointSize(20)
        font.setBold(True)
        item.setFont(font)

        item.setFlags(QGraphicsItem.ItemIsMovable
                      | QGraphicsItem.ItemIsSelectable
                      | QGraphicsItem.ItemIsFocusable)
        item.setPos(-50 + (QtCore.qrand() % 100), -50 + (QtCore.qrand() % 100))
        self.view.frontZ = self.view.frontZ + 1
        item.setZValue(self.view.frontZ)

        self.view.seqNum = self.view.seqNum + 1
        item.setData(self.view.ItemId, self.view.seqNum)  # //自定义数据，ItemId键
        item.setData(self.view.ItemDesciption, "文字")

        self.scene.addItem(item)
        self.scene.clearSelection()
        item.setSelected(True)

    @pyqtSlot()
    def on_actItem_Pixmap_triggered(self):
        point = QPoint()

    @pyqtSlot()
    def on_actZoomIn_triggered(self):  # 放大
        cnt = len(self.scene.selectedItems())
        if cnt == 1:
            # QGraphicsItem   *item
            item = self.scene.selectedItems()[0]
            item.setScale(0.1 + item.scale())
        else:
            self.view.scale(1.1, 1.1)

    @pyqtSlot()
    def on_actZoomOut_triggered(self):  # 缩小
        cnt = len(self.scene.selectedItems())
        if cnt == 1:
            # QGraphicsItem   *item
            item = self.scene.selectedItems()[0]
            item.setScale(item.scale() - 0.1)
        else:
            self.view.scale(0.9, 0.9)

    @pyqtSlot()
    def on_actRestore_triggered(self):  # 取消所有变换
        cnt = len(self.scene.selectedItems())
        if cnt == 1:
            # QGraphicsItem   *item
            item = self.scene.selectedItems()[0]
            item.resetTransform()
        else:
            self.view.resetTransform()

    @pyqtSlot()
    def on_actRotateLeft_triggered(self):  # 逆时针旋转
        cnt = len(self.scene.selectedItems())
        if cnt == 1:
            # QGraphicsItem   *item
            item = self.scene.selectedItems()[0]
            # frontZ++
            item.setRotation(-30 + item.rotation())
        else:
            self.view.rotate(-30)

    @pyqtSlot()
    def on_actRotateRight_triggered(self):  # 顺时针旋转
        cnt = len(self.scene.selectedItems())
        if cnt == 1:
            item = self.scene.selectedItems()[0]
            # frontZ++
            item.setRotation(+30 + item.rotation())
        else:
            self.view.rotate(+30)

    @pyqtSlot()
    def on_actEdit_Front_triggered(self):  # bring to front,前置
        cnt = len(self.scene.selectedItems())
        if cnt > 0:  # 只处理选中的第1个绘图项
            # QGraphicsItem   *item
            item = self.scene.selectedItems()[0]
            # frontZ++
            self.view.frontZ = self.view.frontZ + 1
            item.setZValue(self.view.frontZ)

    @pyqtSlot()
    def on_actEdit_Back_triggered(self):  # bring to back，后置
        cnt = len(self.scene.selectedItems())
        if cnt > 0:  # 只处理选中的第1个绘图项
            # QGraphicsItem   *item
            item = self.scene.selectedItems()[0]
            # backZ--
            self.view.backZ = self.view.backZ - 1
            item.setZValue(self.view.backZ)

    @pyqtSlot()
    def on_actGroup_triggered(self):  # 组合
        cnt = len(self.scene.selectedItems())
        if cnt > 1:
            # group=self.scene.createItemGroup(self.scene.selectedItems())
            group = QGraphicsItemGroup()  # 创建组合
            self.scene.addItem(group)  # 组合添加到场景中

            for i in range(0, cnt):
                item = self.scene.selectedItems()[0]
                item.setSelected(False)  # 清除选择虚线框
                item.clearFocus()
                group.addToGroup(item)  # 添加到组合
            group.setFlags(QGraphicsItem.ItemIsMovable
                           | QGraphicsItem.ItemIsSelectable
                           | QGraphicsItem.ItemIsFocusable)

            self.view.frontZ = self.view.frontZ + 1
            group.setZValue(self.view.frontZ)
            # group.clearFocus()
            self.scene.clearSelection()
            group.setSelected(True)

    @pyqtSlot()
    def on_actGroupBreak_triggered(self):  # break group,打散组合
        cnt = len(self.scene.selectedItems())
        if cnt == 1:
            # QGraphicsItemGroup  *group
            group = self.scene.selectedItems()[0]
            if isinstance(group,QGraphicsItemGroup):
                self.scene.destroyItemGroup(group)

    @pyqtSlot()
    def on_actEdit_Delete_triggered(self):  # 删除所有选中的绘图项
        cnt = len(self.scene.selectedItems())
        # QGraphicsItem   *item
        if cnt > 0:
            for i in range(0, cnt):
                item = self.scene.selectedItems()[0]
                self.scene.removeItem(item)  # 删除绘图项
