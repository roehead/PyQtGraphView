#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import functools

from PyQt5.Qt import Qt,QImage
from PyQt5.QtGui import QTransform, QPainter, QPen, QPainterPath, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QMenu

Dirty = False

class GraphicsPixmapItem(QGraphicsPixmapItem):        #add by yangrongdong
    def __init__(self,scene, pixmap, position, matrix=QTransform()):
        super(QGraphicsPixmapItem, self).__init__(pixmap)
        self.setFlags(QGraphicsItem.ItemIsSelectable) #|QGraphicsItem.ItemIsMovable)
        self.setPos(position)
        #self.setOpacity(0.8)
        self.setTransform(matrix)

        scene.clearSelection()
        scene.addItem(self)

        self.setSelected(True)

        self.CompMode = QPainter.CompositionMode_SourceOver
        self.m_Path= None
        self.isEnd = False

        global Dirty
        Dirty = True

    def contextMenuEvent(self, event):
        wrapped = []
        menu = QMenu(self.parentWidget())
        for text, param in (
                ("&SourceOver]", QPainter.CompositionMode_SourceOver),
                ("&Xor", QPainter.CompositionMode_Xor),
                ("&Multiply", QPainter.CompositionMode_Multiply),
                ("&Darken]", QPainter.CompositionMode_Darken),
                ("&Lighten]", QPainter.CompositionMode_Lighten)):
            wrapper = functools.partial(self.setCompMode, param)
            wrapped.append(wrapper)
            menu.addAction(text, wrapper)
        menu.exec_(event.screenPos())

    def setCompMode(self,nCompMode):
        self.CompMode = nCompMode
        self.update()

    def paint(self, painter, option, widget):
        pixmap = self.pixmap()
        painter.setCompositionMode(self.CompMode)
        painter.drawPixmap(0,0,pixmap)

        #if self.m_Path:
        #    painter.drawPath(self.m_Path)
        #else:
        #    self.m_Path = QPainterPath()
        #    self.m_Path.moveTo(1, 20)
        #    self.m_Path.lineTo(20, 20)
        #    self.m_Path.lineTo(20, 1)
        #    pen=QPen(QColor(255, 0, 0), 2)
        #    painter.setPen(pen)
        #    painter.drawPath(self.m_Path)
        #    self.m_Path=None
        #    pen=None

