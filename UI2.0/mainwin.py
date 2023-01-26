# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwin.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(957, 567)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(586, 424))
        Form.setBaseSize(QSize(0, 0))
        Form.setMouseTracking(True)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.W_Buttons = QWidget(Form)
        self.W_Buttons.setObjectName(u"W_Buttons")
        self.W_Buttons.setGeometry(QRect(760, 30, 99, 25))
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.W_Buttons.sizePolicy().hasHeightForWidth())
        self.W_Buttons.setSizePolicy(sizePolicy1)
        self.W_Buttons.setMinimumSize(QSize(0, 0))
        self.LO_Buttons = QHBoxLayout(self.W_Buttons)
        self.LO_Buttons.setSpacing(0)
        self.LO_Buttons.setObjectName(u"LO_Buttons")
        self.LO_Buttons.setContentsMargins(0, 0, 0, 0)
        self.W_topbar = QWidget(Form)
        self.W_topbar.setObjectName(u"W_topbar")
        self.W_topbar.setGeometry(QRect(0, 0, 309, 37))
        self.LO_topbar = QVBoxLayout(self.W_topbar)
        self.LO_topbar.setSpacing(0)
        self.LO_topbar.setObjectName(u"LO_topbar")
        self.LO_topbar.setContentsMargins(0, 0, 0, 0)
        self.W_bottombar = QWidget(Form)
        self.W_bottombar.setObjectName(u"W_bottombar")
        self.W_bottombar.setGeometry(QRect(0, 540, 158, 24))
        self.LO_bottombar = QHBoxLayout(self.W_bottombar)
        self.LO_bottombar.setSpacing(0)
        self.LO_bottombar.setObjectName(u"LO_bottombar")
        self.LO_bottombar.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

