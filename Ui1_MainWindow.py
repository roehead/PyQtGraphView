# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from res_rc import *

class Ui1_MainWindow(object):
    def setupUi1(self, GMainWindow):
        '''
        《QT5.9开发指南》示例代码"(C++)
            samp8_5GraphicsDraw之UI之desgner部分
        '''
        GMainWindow.setObjectName("GMainWindow")
        GMainWindow.resize(731, 460)
        self.centralWidget = QtWidgets.QWidget(GMainWindow)
        self.centralWidget.setObjectName("centralWidget")
        #view set code
        GMainWindow.setCentralWidget(self.centralWidget)

        #mainLayout = QHBoxLayout()
        #text = 'a button'
        #button = QPushButton(text)
        #mainLayout.addWidget(button)
        #mainLayout.addWidget(...);
        #mainLayout.addLayout(...);
        #self.centralWidget.setLayout(mainLayout)

        self.menuBar = QtWidgets.QMenuBar(GMainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 731, 23))
        self.menuBar.setObjectName("menuBar")
        GMainWindow.setMenuBar(self.menuBar)

        self.mainToolBar = QtWidgets.QToolBar(GMainWindow)
        self.mainToolBar.setIconSize(QtCore.QSize(16, 16))
        self.mainToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mainToolBar.setObjectName("mainToolBar")
        GMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(GMainWindow)
        self.statusBar.setObjectName("statusBar")
        GMainWindow.setStatusBar(self.statusBar)

        self.toolBar = QtWidgets.QToolBar(GMainWindow)
        self.toolBar.setAllowedAreas(QtCore.Qt.LeftToolBarArea)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        GMainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.actItem_Rect = QtWidgets.QAction(GMainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/RECTANGL.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Rect.setIcon(icon)
        #self.actItem_Rect.setObjectName("actItem_Rect")

        self.actItem_Ellipse = QtWidgets.QAction(GMainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/images/ELLIPSE.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Ellipse.setIcon(icon1)
        self.actItem_Ellipse.setObjectName("actItem_Ellipse")

        self.actItem_Line = QtWidgets.QAction(GMainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/images/LINE.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Line.setIcon(icon2)
        self.actItem_Line.setObjectName("actItem_Line")

        self.actEdit_Delete = QtWidgets.QAction(GMainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/images/108.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actEdit_Delete.setIcon(icon3)
        self.actEdit_Delete.setObjectName("actEdit_Delete")

        self.actQuit = QtWidgets.QAction(GMainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/images/132.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actQuit.setIcon(icon4)
        self.actQuit.setObjectName("actQuit")

        self.actItem_Pixmap = QtWidgets.QAction(GMainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/images/824.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Pixmap.setIcon(icon5)
        self.actItem_Pixmap.setObjectName("actItem_Pixmap")

        self.actItem_Text = QtWidgets.QAction(GMainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/images/800.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Text.setIcon(icon6)
        self.actItem_Text.setObjectName("actItem_Text")

        self.actEdit_Front = QtWidgets.QAction(GMainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/images/528.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actEdit_Front.setIcon(icon7)
        self.actEdit_Front.setObjectName("actEdit_Front")

        self.actEdit_Back = QtWidgets.QAction(GMainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/images/526.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actEdit_Back.setIcon(icon8)
        self.actEdit_Back.setObjectName("actEdit_Back")

        self.actItem_Polygon = QtWidgets.QAction(GMainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/images/FREEFORM.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Polygon.setIcon(icon9)
        self.actItem_Polygon.setObjectName("actItem_Polygon")

        self.actZoomIn = QtWidgets.QAction(GMainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/images/zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomIn.setIcon(icon10)
        self.actZoomIn.setObjectName("actZoomIn")

        self.actZoomOut = QtWidgets.QAction(GMainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/images/zoomout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actZoomOut.setIcon(icon11)
        self.actZoomOut.setObjectName("actZoomOut")

        self.actRotateLeft = QtWidgets.QAction(GMainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/images/rotateleft.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actRotateLeft.setIcon(icon12)
        self.actRotateLeft.setObjectName("actRotateLeft")

        self.actRotateRight = QtWidgets.QAction(GMainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/images/images/rotateright.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actRotateRight.setIcon(icon13)
        self.actRotateRight.setObjectName("actRotateRight")

        self.actRestore = QtWidgets.QAction(GMainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/images/images/420.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actRestore.setIcon(icon14)
        self.actRestore.setObjectName("actRestore")

        self.actGroup = QtWidgets.QAction(GMainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/images/images/UNGROUP.BMP"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actGroup.setIcon(icon15)
        self.actGroup.setObjectName("actGroup")

        self.actGroupBreak = QtWidgets.QAction(GMainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/images/images/128.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actGroupBreak.setIcon(icon16)
        self.actGroupBreak.setObjectName("actGroupBreak")

        self.actItem_Circle = QtWidgets.QAction(GMainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/images/images/08.JPG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Circle.setIcon(icon17)
        self.actItem_Circle.setObjectName("actItem_Circle")

        self.actItem_Triangle = QtWidgets.QAction(GMainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/images/images/Icon1242.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actItem_Triangle.setIcon(icon18)
        self.actItem_Triangle.setObjectName("actItem_Triangle")

        self.mainToolBar.addAction(self.actZoomIn)
        self.mainToolBar.addAction(self.actZoomOut)
        self.mainToolBar.addAction(self.actRestore)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actRotateLeft)
        self.mainToolBar.addAction(self.actRotateRight)
        self.mainToolBar.addAction(self.actEdit_Front)
        self.mainToolBar.addAction(self.actEdit_Back)
        self.mainToolBar.addAction(self.actGroup)
        self.mainToolBar.addAction(self.actGroupBreak)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actEdit_Delete)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actQuit)

        self.toolBar.addAction(self.actItem_Rect)
        self.toolBar.addAction(self.actItem_Ellipse)
        self.toolBar.addAction(self.actItem_Circle)
        self.toolBar.addAction(self.actItem_Triangle)
        self.toolBar.addAction(self.actItem_Polygon)
        self.toolBar.addAction(self.actItem_Line)
        self.toolBar.addAction(self.actItem_Text)

        self.retranslateUi(GMainWindow)
        self.actQuit.triggered.connect(GMainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(GMainWindow)  #会形成两次触发

        self.actItem_Rect.triggered.connect(self.on_actItem_Rect)  #_triggered
        '''
        self.actItem_Ellipse.triggered.connect(self.on_actItem_Ellipse_triggered)
        self.actItem_Circle.triggered.connect(self.on_actItem_Circle_triggered)
        self.actItem_Triangle.triggered.connect(self.on_actItem_Triangle_triggered)
        self.actItem_Polygon.triggered.connect(self.on_actItem_Polygon_triggered)
        self.actItem_Line.triggered.connect(self.on_actItem_Line_triggered)
        self.actItem_Text.triggered.connect(self.on_actItem_Text_triggered)

        self.actZoomIn.triggered.connect(self.on_actZoomIn_triggered)
        self.actZoomOut.triggered.connect(self.on_actZoomOut_triggered)
        self.actRestore.triggered.connect(self.on_actRestore_triggered)
        self.actRotateLeft.triggered.connect(self.on_actRotateLeft_triggered)
        self.actRotateRight.triggered.connect(self.on_actRotateRight_triggered)
        self.actEdit_Front.triggered.connect(self.on_actEdit_Front_triggered)
        self.actEdit_Back.triggered.connect(self.on_actEdit_Back_triggered)
        self.actGroup.triggered.connect(self.on_actGroup_triggered)
        self.actGroupBreak.triggered.connect(self.on_actGroupBreak_triggered)
        self.actEdit_Delete.triggered.connect(self.on_actEdit_Delete_triggered)
        #self.actQuit.triggered.connect(GMainWindow.close)
        '''


    def retranslateUi(self, GMainWindow):
        _translate = QtCore.QCoreApplication.translate
        GMainWindow.setWindowTitle(_translate("GMainWindow", "Graphics  View绘图"))
        self.toolBar.setWindowTitle(_translate("GMainWindow", "toolBar"))
        self.actItem_Rect.setText(_translate("GMainWindow", "矩形"))
        self.actItem_Rect.setToolTip(_translate("GMainWindow", "添加矩形"))
        self.actItem_Ellipse.setText(_translate("GMainWindow", "椭圆"))
        self.actItem_Ellipse.setToolTip(_translate("GMainWindow", "添加椭圆型"))
        self.actItem_Line.setText(_translate("GMainWindow", "直线"))
        self.actItem_Line.setToolTip(_translate("GMainWindow", "添加直线"))
        self.actEdit_Delete.setText(_translate("GMainWindow", "删除"))
        self.actEdit_Delete.setToolTip(_translate("GMainWindow", "删除选中的图元"))
        self.actQuit.setText(_translate("GMainWindow", "退出"))
        self.actQuit.setToolTip(_translate("GMainWindow", "退出本系统"))
        self.actItem_Pixmap.setText(_translate("GMainWindow", "图片"))
        self.actItem_Pixmap.setToolTip(_translate("GMainWindow", "添加图片"))
        self.actItem_Text.setText(_translate("GMainWindow", "文字"))
        self.actItem_Text.setToolTip(_translate("GMainWindow", "添加文字"))
        self.actEdit_Front.setText(_translate("GMainWindow", "前置"))
        self.actEdit_Front.setToolTip(_translate("GMainWindow", "居于最前面"))
        self.actEdit_Back.setText(_translate("GMainWindow", "后置"))
        self.actEdit_Back.setToolTip(_translate("GMainWindow", "居于最后面"))
        self.actItem_Polygon.setText(_translate("GMainWindow", "梯形"))
        self.actItem_Polygon.setToolTip(_translate("GMainWindow", "添加梯形"))
        self.actZoomIn.setText(_translate("GMainWindow", "放大"))
        self.actZoomIn.setToolTip(_translate("GMainWindow", "放大"))
        self.actZoomOut.setText(_translate("GMainWindow", "缩小"))
        self.actZoomOut.setToolTip(_translate("GMainWindow", "缩小"))
        self.actRotateLeft.setText(_translate("GMainWindow", "左旋转"))
        self.actRotateLeft.setToolTip(_translate("GMainWindow", "左旋转"))
        self.actRotateRight.setText(_translate("GMainWindow", "右旋转"))
        self.actRotateRight.setToolTip(_translate("GMainWindow", "右旋转"))
        self.actRestore.setText(_translate("GMainWindow", "恢复"))
        self.actRestore.setToolTip(_translate("GMainWindow", "恢复大小"))
        self.actGroup.setText(_translate("GMainWindow", "组合"))
        self.actGroup.setToolTip(_translate("GMainWindow", "组合"))
        self.actGroupBreak.setText(_translate("GMainWindow", "打散"))
        self.actGroupBreak.setToolTip(_translate("GMainWindow", "取消组合"))
        self.actItem_Circle.setText(_translate("GMainWindow", "圆形"))
        self.actItem_Circle.setToolTip(_translate("GMainWindow", "圆形"))
        self.actItem_Triangle.setText(_translate("GMainWindow", "三角形"))
        self.actItem_Triangle.setToolTip(_translate("GMainWindow", "三角形"))

