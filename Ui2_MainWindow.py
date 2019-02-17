# -*- coding: utf-8 -*-
import functools

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QByteArray, QPoint, Qt
from PyQt5.QtGui import QFontMetrics, QPainter
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QMenu, QVBoxLayout,
                             QGraphicsScene, QGraphicsView)

from GraphicsView import GraphicsView
#from PixmapItem import GraphicsPixmapItem
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
        '''
        《QT5.9开发指南》示例代码(C++)
            samp8_5GraphicsDraw之UI手工部分
        '''
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

        self.scene = QGraphicsScene(-300,-200,600,400) #self #//创建QGraphicsScene
        #self.scene.setSceneRect(-PageSize[0]/2, -PageSize[1]/2, PageSize[0], PageSize[1])

        self.view.setScene(self.scene) #//与view关联

        self.addBorders()

        
        
        #slef.setCentralWidget(self.view)

        #设置view中自定义事件对应的槽函数
        #button.clicked.connect(slot)
        self.view.mouseMovePoint.connect(self.on_mouseMovePoint)
        
        self.view.mouseClicked.connect(self.on_mouseClicked)
        
        self.view.mouseRelease.connect(self.on_mouseRelease)
        
        self.view.keyPress.connect(self.on_keyPress)
        
        self.view.mouseDoubleClick.connect(self.on_mouseDoubleClick)
        
        #qsrand(QTime.currentTime().second())
        
        self.wrapped = [] # Needed to keep wrappers alive
         
        lebal1 = QLabel("CompositionMode:")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(70, 40, 87, 122))
        self.comboBox.setObjectName("self.comboBox")  
        self.comboBox.addItem("SourceOver",QPainter.CompositionMode_SourceOver)
        self.comboBox.addItem("DestinationOverlist1",QPainter.CompositionMode_DestinationOver)
        self.comboBox.addItem("Clear",QPainter.CompositionMode_Clear)
        self.comboBox.addItem("Source",QPainter.CompositionMode_Source)
        self.comboBox.addItem("Destination",QPainter.CompositionMode_Destination)
        self.comboBox.addItem("SourceIn",QPainter.CompositionMode_SourceIn)
        self.comboBox.addItem("DestinationIn",QPainter.CompositionMode_DestinationIn)
        self.comboBox.addItem("SourceOut",QPainter.CompositionMode_SourceOut)
        self.comboBox.addItem("DestinationOut",QPainter.CompositionMode_DestinationOut)
        self.comboBox.addItem("SourceAtop",QPainter.CompositionMode_SourceAtop)
        self.comboBox.addItem("DestinationAtoplist1",QPainter.CompositionMode_DestinationAtop)
        self.comboBox.addItem("Xor",QPainter.CompositionMode_Xor)
        self.comboBox.addItem("Plus",QPainter.CompositionMode_Plus)
        self.comboBox.addItem("Multiply",QPainter.CompositionMode_Multiply)
        self.comboBox.addItem("Screen",QPainter.CompositionMode_Screen)
        self.comboBox.addItem("Overlay",QPainter.CompositionMode_Overlay)
        self.comboBox.addItem("Darken",QPainter.CompositionMode_Darken)
        self.comboBox.addItem("Lighten",QPainter.CompositionMode_Lighten)
        self.comboBox.addItem("ColorDodge",QPainter.CompositionMode_ColorDodge)
        self.comboBox.addItem("ColorBurn",QPainter.CompositionMode_ColorBurn)
        self.comboBox.addItem("HardLight",QPainter.CompositionMode_HardLight)
        self.comboBox.addItem("SoftLight",QPainter.CompositionMode_SoftLight)
        self.comboBox.addItem("Difference",QPainter.CompositionMode_Difference)
        self.comboBox.addItem("Exclusion",QPainter.CompositionMode_Exclusion)
        self.comboBox.currentIndexChanged.connect(self.onCbChanged) #para is (int)
        self.comboBox.setEnabled(False)  #变灰

        '''
        以下部分原代码（QPushButton部分）复制来源：
            http://blog.sina.com.cn/s/blog_c22e36090102x1p3.html
            《python3+PyQt5 图形项的自定义和交互--实现page Designer应用程序》
            by basisworker in 2017-03-06 09:58:31
        修改记录：
            1.原主对话框类QDialog改为QMainWindow
            2.图形像类拆分为独立模块文件
            4.界面部分代码移到Ui2_MainWindow模块（类）
        '''
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
                buttonLayout.addWidget(lebal1)
                buttonLayout.addWidget(self.comboBox)
                buttonLayout.addStretch(5)
            if text == "&Quit":
                buttonLayout.addStretch(1)
            buttonLayout.addWidget(button) #逐个添加 in for loop
        
        buttonLayout.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(self.view, 1)
        layout.addLayout(buttonLayout)
        self.centralWidget.setLayout(layout) #主对话框
        
        #fm = QFontMetrics(self.font())
        #self.resize(self.scene.width() + fm.width(" Delete... ") + 50,
        #            self.scene.height() + 50)
        self.setWindowTitle("Page Designer")
