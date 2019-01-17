#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QPointF, QRectF, Qt, pyqtSlot
from PyQt5.QtGui import QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsLineItem, QGraphicsItemGroup,
                             QGraphicsTextItem, QMessageBox, QInputDialog, QColorDialog, QFontDialog)

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


# view.ItemId = 1  #绘图项自定义数据的key
# view.ItemDesciption = 2  #绘图项自定义数据的key

# view.seqNum=0
# view.backZ=0
# view.frontZ=0


class Slot_MainWindow(object):  # QDialog
    def setBrushColor(self, item):
        # 函数模板
        color = item.brush().color()
        color = QColorDialog.getColor(color, self, "选择填充颜色")
        if color.isValid():
            item.setBrush(QBrush(color))

    def on_mouseMovePoint(self, point):  # 鼠标移动事件，point是 GraphicsView的坐标,物理坐标

        point1 = QPoint()
        point1 = point
        self.labViewCord.setText("View%d,%d" % (point1.x(), point1.y()))
        pointScene = self.view.mapToScene(point)  # 转换到Scene坐标
        self.labSceneCord.setText("Scene%.0f,%.0f" % (pointScene.x(), pointScene.y()))

    def on_mouseClicked(self, point):  # 鼠标单击事件

        pointScene = self.view.mapToScene(point)  # 转换到Scene坐标
        # item=QGraphicsItem()
        item = self.scene.itemAt(pointScene, self.view.transform())  # 获取光标下的绘图项
        if item != None and item.data(self.view.ItemId) != None:  # 有绘图项
            pointItem = item.mapFromScene(pointScene)  # 转换为绘图项的局部坐标
            self.labItemCord.setText("Item%.0f,%.0f" % (pointItem.x(), pointItem.y()))
            self.labItemInfo.setText(item.data(self.view.ItemDesciption) + ", ItemId=%d" % item.data(self.view.ItemId))

    def on_keyPress(self, event):  # 按键事件
        if len(self.scene.selectedItems()) != 1:
            QMessageBox.warning(self, "debug", "No item found!")
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
            item.setX(-1 + item.x())

        elif event.key() == Qt.Key_Right:  # 右移
            item.setX(1 + item.x())

        elif event.key() == Qt.Key_Up:  # 上移
            item.setY(-1 + item.y())

        elif event.key() == Qt.Key_Down:  # 下移
            item.setY(1 + item.y())

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
        item.setBrush(QBrush(Qt.yellow))
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
