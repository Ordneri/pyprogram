# This Python file uses the following encoding: utf-8
import sys
import mainwin
import res_mainwin
from styled_component import *
from PySide6.QtWidgets import QApplication, QStyleFactory,QLabel
from PySide6.QtGui import QPainter,QBrush
from PySide6.QtCore import QDir

class topbar(styled_bar):
    def __init__(self,parent,imgurl,w=0,h=0):

        super(topbar,self).__init__(parent,imgurl,w,h)
        self.p=parent
        self.setMouseTracking(True)
        self.startpos=QPoint()
        self.moves=QPoint()
        self.moving=False



    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.moving or (event.position().y()<10 and event.position().y()<self.size().height() and event.position().x()>0 and event.position().y()>0):
            if self.moving or event.buttons()==Qt.LeftButton:
                self.moves=event.globalPosition().toPoint()-self.startpos
                self.startpos=event.globalPosition().toPoint()
                self.p.move(self.p.pos()+self.moves)
                self.moving = True
            else:
                self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
    def mousePressEvent(self, event:QMouseEvent) -> None:
        if event.buttons()==Qt.LeftButton:
            self.startpos=event.globalPosition().toPoint()
            self.setCursor(Qt.ClosedHandCursor)
    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        self.startpos=event.globalPosition().toPoint()-self.parent().pos()
        self.setCursor(Qt.OpenHandCursor)
        self.moving = False



class mainw(styled_win):
    def __init__(self):
        self.rw=957
        self.rh=567

        super().__init__(mainwin.Ui_Form(),':/mainw/res_mainw/minw.png',self.rw,self.rh)
        #创建控件
        self.BT_close=styled_button(':/mainw/res_mainw/BT_close_normal.png',':/mainw/res_mainw/BT_close_select.png',self,34,25,True,':/mainw/res_mainw/BT_close_normal_maxed.png',':/mainw/res_mainw/BT_close_select_maxed.png')
        self.BT_scale=styled_button(':/mainw/res_mainw/BT_scale_normal_not_switch.png',':/mainw/res_mainw/BT_scale_select_not_switch.png',self,34,25,True,':/mainw/res_mainw/BT_scale_normal_switched.png',':/mainw/res_mainw/BT_scale_select_switched.png')
        self.BT_min=styled_button(':/mainw/res_mainw/BT_min_normal.png',':/mainw/res_mainw/BT_min_Select.png',self,34,25)
        self.Bar_top=topbar(self,':/mainw/res_mainw/topbar.png',309,37)
        self.Bar_Bottom=styled_bar(self,':/mainw/res_mainw/bottombar.png',158,24,0.50)
        self.stiper=corner_tip_single(self,':/mainw/res_mainw/BT_cotip_uncheck.png',':/mainw/res_mainw/BT_cotip_checked.png',True,15,15)
        self.tipl=corner_tip_list(self,':/mainw/res_mainw/BT_cotip_uncheck.png',':/mainw/res_mainw/BT_cotip_checked.png',15,15,corner_tip_list.limit_by_parent,gaptoparent=20)
        self.testbutton = QPushButton('T1',self)
        self.testbutton2 = QPushButton('T2', self)
        self.testbutton3 = QPushButton('T3', self)
        self.testbutton.setFixedSize(25,25)
        self.testbutton2.setFixedSize(25, 25)
        self.testbutton3.setFixedSize(25, 25)
        self.tiptest=0
        self.tiptest1=0

        #添加到UI
        self.ui.LO_Buttons.addWidget(self.BT_min)
        self.ui.LO_Buttons.addWidget(self.BT_scale)
        self.ui.LO_Buttons.addWidget(self.BT_close)
        self.ui.LO_topbar.addWidget(self.Bar_top)
        self.ui.LO_bottombar.addWidget(self.Bar_Bottom)
        self.Bar_top.layout.addWidget(self.testbutton)
        self.Bar_top.layout.addWidget(self.testbutton2)
        self.Bar_top.layout.addWidget(self.testbutton3)

        #设置锚点
        self.anchorwidget(anchor.topright,self.ui.W_Buttons,anchor.righttop,adjust_x=2)
        self.anchorwidget(anchor.topmid,self.ui.W_topbar,anchor.topmid)
        self.anchorwidget(anchor.leftbottom,self.ui.W_bottombar,anchor.leftbottom,-2,1)
        #绑定信号和槽
        self.BT_scale.clicked.connect(self.scalewindow)
        self.BT_close.clicked.connect(self.close)
        self.BT_min.clicked.connect(self.showMinimized)
        self.testbutton.clicked.connect(self.warningmode)
        self.testbutton2.clicked.connect(self.test_tip)
        self.testbutton3.clicked.connect(self.test_tip1)

        #窗口初始化
        self.geo=[0,0,self.rw,self.rh]
        self.drawd=3
        self.maxed=False
        self.warning=False
        self.wincolor=QColor(104, 154, 214)
        self.winmask=QPixmap(self.rw*self.drawd,self.rh*self.drawd)
        self.winmask.fill(QColor(255, 255, 255, 0))
        self.paintwin=QPainter(self.winmask)
        self.paintwin.setBrush(QColor(0,0,0))
        self.paintwin.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)
        self.paintwin.setBrush(QColor(0,0,0))
        self.paintwin.drawRoundedRect(0,0,self.rw*self.drawd,self.rh*self.drawd,20*self.drawd,20*self.drawd)
        self.paintwin.drawRect(1060*self.drawd, 620*self.drawd,20*self.drawd,20*self.drawd)
        self.paintwin.end()
        self.winmask= self.winmask.scaled(self.rw,self.rw)
        self.winimg.fill(QColor(104,154,214))
        self.winimg.setMask(self.winmask.mask())
        #self.winimg.fill(QColor(104,154,214))
        self.setMask(self.winmask.mask())
        self.setuppal()
        self.adjustcomponentposition()

    def scalewindow(self):
        if self.BT_scale.switched:
            self.geo=[self.geometry().x(),self.geometry().y(),self.geometry().width(),self.geometry().height()]
            self.Bar_Bottom.changestyle(':/mainw/res_mainw/bottombar_maxed.png')
            self.scaleable = False
            self.maxed=True
            self.BT_close.switched=True
            self.showMaximized()
        else:
            self.maxed=False
            self.BT_close.switched=False
            self.Bar_Bottom.changestyle(':/mainw/res_mainw/bottombar.png')
            self.setGeometry(self.geo[0],self.geo[1],self.geo[2],self.geo[3])
            self.scaleable=True

    def warningmode(self):
        self.warning = not self.warning
        if self.warning: #del latter
            self.wincolor=QColor(255,0,0)
            self.Bar_top.changestyle(':/mainw/res_mainw/topbar_warning.png')
            self.winimg.fill(self.wincolor)
            self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
            if self.maxed:
                self.showMaximized()
            else:
                self.show()
        else:
            self.restore()
        self.setuppal()

    def restore(self):
        self.warning=False
        self.wincolor = QColor(104,154,214)
        self.Bar_top.changestyle(':/mainw/res_mainw/topbar.png')
        self.winimg.fill(self.wincolor)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if self.maxed:
            self.showMaximized()
        else:
            self.show()
        self.setuppal()

    def resizeEvent(self, event:QResizeEvent):
        if self.maxed:
            self.winimg.scaled(self.size())
            self.winimg.fill(self.wincolor)
            self.winmask.scaled(self.size())
            self.winmask.fill(Qt.white)
            #self.ui.resize(self.size())
            self.clearMask()
        else:
            w=self.size().width()
            h=self.size().height()
            self.winimg = self.winimg.scaled(w,h)
            self.winmask = self.winmask.scaled(w*self.drawd,h*self.drawd)
            self.winmask.fill(QColor(0,0,0,0))
            self.paintwin.begin(self.winmask)
            self.paintwin.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)
            self.paintwin.setBrush((QColor(0,0,0)))
            self.paintwin.drawRoundedRect(0, 0, w*self.drawd , h*self.drawd , 15*self.drawd, 15*self.drawd)
            self.paintwin.drawRect((w-20)*self.drawd, (h-20)*self.drawd, 20*self.drawd,  20*self.drawd)
            self.paintwin.end()
            self.winmask=self.winmask.scaled(w,h)
            self.winimg.fill(self.wincolor)
            self.winimg.setMask(self.winmask.mask())
            #self.ui.resize(self.size())
            self.setMask(self.winmask.mask())
        self.setuppal()
        self.adjustcomponentposition()

    def test_tip(self):
        if self.tiptest==0:
            self.tiptest+=1
            self.stiper.tip('this is a tip')
        elif self.tiptest==1:
            self.tiptest+=1
            self.stiper.operate('and it is used to\ntip some info')
        else:
            self.tiptest=0
            self.stiper.warn('or used to report some bug')

    def test_tip1(self):
        if self.tiptest1==0:
            self.tiptest1+=1
            self.tipl.tip('进阶版提示')
        elif self.tiptest1<3:
            self.tiptest1+=1
            self.tipl.operate('我来两次\n:)\n:）\n:)\n:)\n:)')
        else:
            self.tiptest1=0
            self.tipl.warn('蓟\n县\n2\n3\n3\n3\n3\n3\n3\n3\n3\n3\n3\n3\n3\n3\n3\n3')

if __name__ == "__main__":
    app = QApplication([])
    w=mainw()
    app.setStyle(QStyleFactory.create("fusion"))
    w.show()
    sys.exit(app.exec())
