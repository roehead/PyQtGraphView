#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import random

from PyQt5.QtCore import QDataStream, QFile, QFileInfo, QIODevice
from PyQt5.QtGui import QCursor, QPixmap, QImage
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from BoxItem import *
from TextItem import *
from PixmapItem import *
from Slot_MainWindow import *
from Ui1_MainWindow import *
from Ui2_MainWindow import *

#global in Ui2_MainWindow
#MAC = True
#try:
#    from PyQt5.QtGui import qt_mac_set_native_menubar
#except ImportError:
#    MAC = False

#PageSize = (595, 842) # A4 in points
PageSize = (600, 400) # US Letter in points
#PointSize = 10

MagicNumber = 0x70616765
Dirty = False

FileVersion = 1

#ItemId = 1  #绘图项自定义数据的key
#ItemDesciption = 2  #绘图项自定义数据的key

#seqNum=0
#backZ=0
#frontZ=0


class GMainWindow(QMainWindow, Ui1_MainWindow, Ui2_MainWindow, Slot_MainWindow): #QDialog
    
    #global frontZ,seqNum,backZ,ItemId,ItemDesciption
    #global MAC, PageSize, PointSize
    
    def __init__(self, parent=None):
        super(GMainWindow,self).__init__()
        self.setupUi1(self)
        self.setupUi2(self)
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageSize(QPrinter.Letter)
        
        #self.addBorders()

    def addBorders(self):
        self.borders = []
        rect = QRectF(-PageSize[0]/2, -PageSize[1]/2, PageSize[0], PageSize[1])
        #rect = QRectF(-PageSize[0], -PageSize[1], PageSize[0], PageSize[1])
        #rect = QRectF(PageSize[0]/2, PageSize[1]/2,-PageSize[0]/2, -PageSize[1]/2 )

        item = self.scene.addRect(rect, Qt.blue)
        #item.setPos(-PageSize[0]/4, -PageSize[1]/4)
        self.borders.append(item)
        self.view.set_item_index(item,"矩形3")

        margin = 5.25 * PointSize
        item = self.scene.addRect(
                rect.adjusted(margin, margin, -margin, -margin),
                Qt.blue)
        #item.setPos(-PageSize[0]/4, -PageSize[1]/4)
        self.borders.append(item)
        self.view.set_item_index(item,"矩形3")
        self.view.resize(PageSize[0], PageSize[1])


    def removeBorders(self):
        while self.borders:
            item = self.borders.pop()
            self.scene.removeItem(item)
            del item


    def reject(self):
        self.accept()


    def accept(self):
        self.offerSave()
        #QDialog.accept(self)


    def offerSave(self):
        if (Dirty and QMessageBox.question(self,
                            "Page Designer - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No) == 
           QMessageBox.Yes):
            self.save()


    def position(self):
        point = self.mapFromGlobal(QCursor.pos())
        if not self.view.geometry().contains(point):
            coord = random.randint(360,444)
            point = QPoint(coord, coord)
        else:
            if point == self.prevPoint:
                point += QPoint(self.addOffset, self.addOffset)
                self.addOffset += 5
            else:
                self.addOffset = 5
                self.prevPoint = point
        return self.view.mapToScene(point)


    def addText(self):
        dialog = TextItemDlg(position=self.position(),
                             scene=self.scene, parent=self)
        dialog.exec_()  
        self.view.set_item_index(dialog.item,"文字2")


    def addBox(self):
        item = BoxItem(self.position(), self.scene)
        self.view.set_item_index(item,"矩形2")

    def addPixmap(self):
        path = (QFileInfo(self.filename).path()
            if self.filename else ".")
        fname,filetype = QFileDialog.getOpenFileName(self,
                "Page Designer - Add Pixmap", path,
                "Pixmap Files (*.bmp *.jpg *.png *.xpm)")
        if not fname:
            return
        item = GraphicsPixmapItem(self.scene, QPixmap(fname), 
                                  self.position(), 
                                  matrix=QTransform())
        self.view.set_item_index(item,"图片")
        
        
    def selectedItem(self):
        items = self.scene.selectedItems()
        if len(items) == 1:
            return items[0]
        return None
        
        
    def copy(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copiedItem.clear()
        self.pasteOffset = 5
        stream = QDataStream(self.copiedItem, QIODevice.WriteOnly)
        self.writeItemToStream(stream, item)
        
        
    def cut(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copy()
        self.scene.removeItem(item)
        del item
        
        
    def paste(self):
        if self.copiedItem.isEmpty():
            return
        stream = QDataStream(self.copiedItem, QIODevice.ReadOnly)
        self.readItemFromStream(stream, self.pasteOffset)
        self.pasteOffset += 5
        
        
    def setAlignment(self, alignment):
        # Items are returned in arbitrary order
        items = self.scene.selectedItems()
        if len(items) <= 1:
            return
        # Gather coordinate data
        leftXs, rightXs, topYs, bottomYs = [], [], [], []
        for item in items:
            rect = item.sceneBoundingRect()
            leftXs.append(rect.x())
            rightXs.append(rect.x() + rect.width())
            topYs.append(rect.y())
            bottomYs.append(rect.y() + rect.height())
        # Perform alignment
        if alignment == Qt.AlignLeft:
            xAlignment = min(leftXs)
            for i, item in enumerate(items):
                item.moveBy(xAlignment - leftXs[i], 0)
        elif alignment == Qt.AlignRight:
            xAlignment = max(rightXs)
            for i, item in enumerate(items):
                item.moveBy(xAlignment - rightXs[i], 0)
        elif alignment == Qt.AlignTop:
            yAlignment = min(topYs)
            for i, item in enumerate(items):
                item.moveBy(0, yAlignment - topYs[i])
        elif alignment == Qt.AlignBottom:
            yAlignment = max(bottomYs)
            for i, item in enumerate(items):
                item.moveBy(0, yAlignment - bottomYs[i])
        global Dirty
        Dirty = True
        
        
    def rotate(self):
        for item in self.scene.selectedItems():
            item.setRotation(item.rotation()+30)
        
    def delete(self):
        items = self.scene.selectedItems()
        if (len(items) and QMessageBox.question(self,
                "Page Designer - Delete",
                "Delete {0} item{1}?".format(len(items),
                "s" if len(items) != 1 else ""),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            global Dirty
            Dirty = True
        
        
    def print_(self):
        dialog = QPrintDialog(self.printer)
        if dialog.exec_():
            painter = QPainter(self.printer)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.TextAntialiasing)
            self.scene.clearSelection()
            self.removeBorders()
            self.scene.render(painter)
            self.addBorders()
        
        
    def open(self):
        self.offerSave()
        path = (QFileInfo(self.filename).path()
                if self.filename else ".")
        fname,filetype = QFileDialog.getOpenFileName(self,
                "Page Designer - Open", path,
                "Page Designer Files (*.pgd)")
        if not fname:
            return
        self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            items = self.scene.items()
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            self.addBorders()
            stream = QDataStream(fh)
            stream.setVersion(QDataStream.Qt_5_7)
            magic = stream.readInt32()
            if magic != MagicNumber:
                raise IOError("not a valid .pgd file")
            fileVersion = stream.readInt16()
            if fileVersion != FileVersion:
                raise IOError("unrecognised .pgd file version")
            while not fh.atEnd():
                self.readItemFromStream(stream)
        except IOError as e:
            QMessageBox.warning(self, "Page Designer -- Open Error",
                    "Failed to open {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False
    
    def save(self):
        if not self.filename:
            path = "."
            fname,filetype = QFileDialog.getSaveFileName(self,
                    "Page Designer - Save As", path,
                    "Page Designer Files (*.pgd)")
            if not fname:
                return
            self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            self.scene.clearSelection()
            stream = QDataStream(fh)
            stream.setVersion(QDataStream.Qt_5_7)
            stream.writeInt32(MagicNumber)
            stream.writeInt16(FileVersion)
            for item in self.scene.items():
                self.writeItemToStream(stream, item)
        except IOError as e:
            QMessageBox.warning(self, "Page Designer -- Save Error",
                    "Failed to save {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        QMessageBox.warning(self, "debug","Save file!")
        global Dirty
        Dirty = False
        
        
    def readItemFromStream(self, stream, offset=0):
        type = ""
        position = QPointF()
        matrix = QTransform()

        rotateangle=0#add by yangrongdong
        type=stream.readQString()
        stream >> position >> matrix
        if offset:
            position += QPointF(offset, offset)
        if type == "Text":
            text = ""
            font = QFont()
            text=stream.readQString()
            stream >> font
            item=TextItem(text, position, self.scene, font, matrix)
        elif type == "Box":
            rect = QRectF()
            stream >> rect
            style = Qt.PenStyle(stream.readInt16())
            item=BoxItem(position, self.scene, style, rect, matrix)
        elif type == "Pixmap":
            pixmap = QPixmap()
            stream >> pixmap
            item = GraphicsPixmapItem(self.scene, pixmap, 
                                      position, matrix)
        if type in ('Text','Box','Pixmap'):
            sc          = stream.readFloat()
            rotateangle = stream.readFloat()
            item_Zvalue = stream.readInt16()
            item_order  = stream.readInt16()
            item_desc   = stream.readQString()
            item.setRotation(rotateangle)
            item.setScale(sc)
            QMessageBox.warning(self, "read"+type, "ItemDesciption: "+item_desc)
            item.setZValue(item_Zvalue)
            item.setData(self.view.ItemId,item_order)
            item.setData(self.view.ItemDesciption, item_desc)


    def writeItemToStream(self, stream, item):
        if isinstance(item, TextItem):
            stream.writeQString("Text")
            stream<<item.pos()<< item.transform() 
            stream.writeQString(item.toPlainText())
            stream<< item.font()
        elif isinstance(item, GraphicsPixmapItem):
            stream.writeQString("Pixmap")
            stream << item.pos() << item.transform() << item.pixmap()
        elif (isinstance(item, BoxItem) or (isinstance(item, QGraphicsRectItem) 
                             and item.data(self.view.ItemDesciption)!=('矩形3'))):
            stream.writeQString("Box")
            stream<< item.pos() << item.transform() << item.rect
            stream.writeInt16(item.style)

        if item.data(self.view.ItemDesciption)in ('矩形','矩形2','图片','文字2'): # ,'椭圆','圆形','梯形','直线','文字'):
            #QMessageBox.warning(self, "debug", item.data(self.view.ItemDesciption))
            stream.writeFloat(item.scale())
            stream.writeFloat(item.rotation())#add by yangrongdong
            stream.writeInt16(item.zValue())
            stream.writeInt16(item.data(self.view.ItemId))
            stream.writeQString(item.data(self.view.ItemDesciption))

    def save_pic(self):
        self.filename = None
        if not self.filename:
            path = "."
            fname,filetype = QFileDialog.getSaveFileName(self,
                    "Page Designer - Save As", path,
                    "Page Designer Files (*.png)")
            if not fname:
                return
            self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            ##################################################
            self.image1 = QImage(self.view.width(),self.view.height(), QImage.Format_ARGB32)
            if  self.image1:
                self.image_painter=QPainter(self.image1)
                self.scene.clearSelection()
                self.removeBorders()
                #self.scene.render(self.image_painter)
                self.view.render(self.image_painter)
                self.image_painter= None
                self.image1.save(self.filename)
                self.addBorders()
                QMessageBox.warning(self, "Page Designer -- Save Success",
                                    "Image be saved!")
            else:
                QMessageBox.warning(self, "Page Designer -- Save Error",
                                    "Failed to Save!")
            #self.scene.clearSelection()
            #self.removeBorders()
            #self.scene.render(painter)
            ###################################################
        
        except IOError as e:
            QMessageBox.warning(self, "Page Designer -- Save Error",
                    "Failed to save {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False

