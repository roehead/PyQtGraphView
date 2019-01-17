# -*- coding: utf-8 -*-
import functools

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QByteArray, QPoint, Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QMenu, QVBoxLayout,
                             QGraphicsScene, QGraphicsView)

from GraphicsView import GraphicsView

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False
#PageSize = (595, 842) # A4 in points
#PageSize = (612, 792) # US Letter in points
#PointSize = 10

class Ui2_MainWindow(object):

    global PageSize

    def setupUi2(self, GMainWindow):
        self.labViewCord = QLabel("View:") 
        self.labViewCord.setMinimumWidth(150)
        self.statusBar.addWidget(self.labViewCord)
        
        self.labSceneCord = QLabel("Scene:")
        self.labSceneCord.setMinimumWidth(150)
        self.statusBar.addWidget(self.labSceneCord)
        
        self.labItemCord = QLabel("Item:")
        self.labItemCord.setMinimumWidth(150)
        self.statusBar.addWidget(self.labItemCord)
        
        self.labItemInfo = QLabel("ItemInfo:")
        self.labItemInfo.setMinimumWidth(200)
        self.statusBar.addWidget(self.labItemInfo)
        
        #self.statusBar=QStatusBar()
        #self.labItemInfo.setMinimumSize(self.labItemInfo.sizeHint())
        #self.labItemInfo.setAlignment(Qt.AlignHCenter)
        
        self.filename = ""
        self.copiedItem = QByteArray()
        self.pasteOffset = 5
        self.prevPoint = QPoint()
        self.addOffset = 5
        self.borders = []
        
        
        #self.view = GraphicsView()
        self.view = GraphicsView(self.centralWidget)
        self.view.setGeometry(QtCore.QRect(10, 10, 641, 351))
        self.view.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.view.setObjectName("view")
        
        self.view.setCursor(Qt.CrossCursor)  #设置鼠标
        self.view.setMouseTracking(True)  # //
        self.view.setDragMode(QGraphicsView.RubberBandDrag)

        self.scene = QGraphicsScene(-300,-200,600,200) #self #//创建QGraphicsScene
        #self.scene.setSceneRect(-PageSize[0]/2, -PageSize[1]/2, PageSize[0]/2, PageSize[1]/2)

        self.view.setScene(self.scene) #//与view关联

        self.addBorders()

        
        
        #slef.setCentralWidget(self.view)

        #设置槽函数
        #button.clicked.connect(slot)
        self.view.mouseMovePoint.connect(self.on_mouseMovePoint)
        
        self.view.mouseClicked.connect(self.on_mouseClicked)
        
        self.view.keyPress.connect(self.on_keyPress)
        
        self.view.mouseDoubleClick.connect(self.on_mouseDoubleClick)
        
        #qsrand(QTime.currentTime().second())
        
        self.wrapped = [] # Needed to keep wrappers alive
         
        buttonLayout = QVBoxLayout()
        for text, slot in (
                ("Add &Text", self.addText),
                ("Add &Box", self.addBox),
                ("Add Pi&xmap", self.addPixmap),
                ("&Align", None),
                ("&Copy", self.copy),
                ("C&ut", self.cut),
                ("&Paste", self.paste),
                ("&Delete...", self.delete),
                ("&Rotate", self.rotate),
                ("Pri&nt...", self.print_),
                ("&Open...", self.open),
                ("&Save", self.save),
                ("&Save As Pic", self.save_pic),
                ("&Quit", self.accept)):
            button = QPushButton(text)
            if not MAC:
                button.setFocusPolicy(Qt.NoFocus)
            if slot is not None:
                button.clicked.connect(slot)
            if text == "&Align":
                menu = QMenu(self)
                for text, arg in (
                        ("Align &Left", Qt.AlignLeft),
                        ("Align &Right", Qt.AlignRight),
                        ("Align &Top", Qt.AlignTop),
                        ("Align &Bottom", Qt.AlignBottom)):
                    wrapper = functools.partial(self.setAlignment, arg)
                    self.wrapped.append(wrapper)
                    menu.addAction(text, wrapper)
                button.setMenu(menu)
            if text == "Pri&nt...":
                buttonLayout.addStretch(5)
            if text == "&Quit":
                buttonLayout.addStretch(1)
            buttonLayout.addWidget(button) #逐个添加
        
        buttonLayout.addStretch()
        
        layout = QHBoxLayout()
        layout.addWidget(self.view, 1)
        layout.addLayout(buttonLayout)
        self.centralWidget.setLayout(layout) #主对话框
        
        fm = QFontMetrics(self.font())
        #self.resize(self.scene.width() + fm.width(" Delete... ") + 50,
        #            self.scene.height() + 50)
        self.setWindowTitle("Page Designer")
