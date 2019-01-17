#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import functools

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QTransform, QPen
from PyQt5.QtWidgets import QMenu, QStyle, QGraphicsItem

#PointSize = 10

Dirty = False

class BoxItem(QGraphicsItem):

    def __init__(self, position, scene, style=Qt.SolidLine,
                 rect=None, matrix=QTransform()):
        super(BoxItem, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable|
                      QGraphicsItem.ItemIsFocusable)
        if rect is None:
            PointSize = scene.views()[0].PointSize
            rect = QRectF(-10 * PointSize, -PointSize, 20 * PointSize,
                          2 * PointSize)
        self.rect = rect
        self.style = style
        self.setPos(position)
        self.setTransform(matrix)
        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        self.setFocus()
        global Dirty
        Dirty = True


    def parentWidget(self):
        return self.scene().views()[0]


    def boundingRect(self):
        return self.rect.adjusted(-2, -2, 2, 2)


    def paint(self, painter, option, widget):
        pen = QPen(self.style)
        pen.setColor(Qt.black)
        pen.setWidth(1)
        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawRect(self.rect)


    def itemChange(self, change, variant):
        if change != QGraphicsItem.ItemSelectedChange:
            global Dirty
            Dirty = True
        return QGraphicsItem.itemChange(self, change, variant)


    def contextMenuEvent(self, event):
        wrapped = []
        menu = QMenu(self.parentWidget())
        for text, param in (
                ("&Solid", Qt.SolidLine),
                ("&Dashed", Qt.DashLine),
                ("D&otted", Qt.DotLine),
                ("D&ashDotted", Qt.DashDotLine),
                ("DashDo&tDotted", Qt.DashDotDotLine)):
            wrapper = functools.partial(self.setStyle, param)
            wrapped.append(wrapper)
            menu.addAction(text, wrapper)
        menu.exec_(event.screenPos())


    def setStyle(self, style):
        self.style = style
        self.update()
        global Dirty
        Dirty = True


    def keyPressEvent(self, event):
        factor = self.parentWidget().PointSize / 4
        changed = False
        if event.modifiers() & Qt.ShiftModifier:
            if event.key() == Qt.Key_Left:
                self.rect.setRight(self.rect.right() - factor)
                changed = True
            elif event.key() == Qt.Key_Right:
                self.rect.setRight(self.rect.right() + factor)
                changed = True
            elif event.key() == Qt.Key_Up:
                self.rect.setBottom(self.rect.bottom() - factor)
                changed = True
            elif event.key() == Qt.Key_Down:
                self.rect.setBottom(self.rect.bottom() + factor)
                changed = True
        if changed:
            self.update()
            #QMessageBox.warning(None, "debug","BoxItem be changed!")
            global Dirty
            Dirty = True
        else:
            #QMessageBox.warning(None, "debug","BoxItem do not be changed!")
            QGraphicsItem.keyPressEvent(self, event)

