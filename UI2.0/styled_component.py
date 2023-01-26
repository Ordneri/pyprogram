'''
自定义窗口，按demo操作就好，有一定的上手难度，不知道用的UTF-8还是什么编码，在极特别情况下会出错，自己解决一下
Styled widgets and components,the 'main.py' is a example of using it,hope you like it,this code may cause 'UnicodeDecodeError' in some situations,solve it by deleting chinese character
'''
from PySide6.QtCore import Qt,QPoint,QSize,QFile,Signal,QPropertyAnimation,QRect,QTimer,Slot
from PySide6.QtWidgets import  QWidget, QPushButton,QHBoxLayout,QGraphicsOpacityEffect,QLabel,QFrame
from PySide6.QtGui import QPalette, QColor,QPixmap,QMouseEvent,QResizeEvent,QCloseEvent,QPainter
from PySide6.QtUiTools import QUiLoader

from enum import Enum
import res_mainwin
class anchor(Enum):
    topleft=0
    topmid=1
    topright=2
    bottomleft=3
    bottonright=4
    bottonmid=5
    leftmid=6
    rightmid=7
    lefttop=8
    leftbottom=9
    rightbottom=10
    righttop=11
    mid=12
    midtop=13
    midbottom=14
    midleft=15
    midright=16
anchordict={\
    anchor.topleft:[0,0], \
    anchor.topmid:[1,0], \
    anchor.topright:[2,0], \
    anchor.bottomleft:[0,2], \
    anchor.bottonright:[2,2], \
    anchor.bottonmid: [1,2],\
    anchor.leftmid:[0,1],\
    anchor.rightmid:[2,1],\
    anchor.lefttop:[0,0],\
    anchor.leftbottom:[0,2],\
    anchor.rightbottom:[2,2],\
    anchor.righttop:[2,0],\
    anchor.mid:[1,1], \
    anchor.midtop :[1,0],\
    anchor.midbottom :[1,2],\
    anchor.midleft :[0,1],\
    anchor.midright :[2,1]}
'''
锚点布局类（widgetanchor）和styled_win里面的widgetanchor方法基本上是一模一样的，之所以会出现这种情况，
是因为一开始这个东西就是做给styled_win用的，挺好用的，干脆单独拿出来了，但styled_win里面那个高级些
the 'styled_win' class has function 'anchorwidget' similar to this 'widgetanchor' class because
it is first used in 'styled_win' and it does a nice job,so I made it to a new class named 'widgetanchor'
however 'anchorwidget' has more functions
'''

class widgetanchor:
    '''
    用于把一个窗口连接到另外一个窗口上，目前设定了9个连接部位，见anchor类
    例如：把Button的左下角锚接到Widget的左下角，再调用place_widget方法，就可以在Widget的左下角找到Button了
    想法来源于虚幻5
    '''
    def __init__(self):
        self.anchorcomponent=[]
    def add_anchor(self,widget1:QWidget,w1pos:anchor,widget2:QWidget,w2pos:anchor,adjust_x,adjust_y):
        self.anchoredcomponents.append(
            [widget1, anchordict[w1pos], widget2,anchordict[w2pos], adjust_x, adjust_y])
    def place_widget(self):
        for comp in self.anchorcomponent:
            wx, wy = anchorpos(comp[0], comp[1])
            cx, cy = anchorpos(comp[2], comp[3])
            move_x = wx - cx + int(comp[-2])
            move_y = wy - cy + int(comp[-1])
            comp[2].move(move_x, move_y)


def anchorpos(widget:QWidget,pos:[]):
    w=0
    h=0
    if pos[0]==0:
        w=0
    if pos[0]==1:
        w=widget.width()/2
    if pos[0]==2:
        w=widget.width()
    if pos[1]==0:
        h=0
    if pos[1]==1:
        h=widget.height()/2
    if pos[1]==2:
        h=widget.height()
    return w,h
class styled_win(QWidget):
    '''
    自定义窗口，真是太快乐了，不过目前只支持由UI文件转，因为我做毕设时就是这么写了，懒得改:)
    默认情况下是关闭按钮都没有的(Alt+F4，不客气）
    '''
    def __init__(self,uimodule=None,imageurl='',w=0,h=0,has_scale=True):
        super(styled_win,self).__init__()
        self.winimg = QPixmap(100,100)
        self.winimg.fill(QColor(0,0,0))
        if imageurl:
            self.winimg = QPixmap(imageurl)
        self.scaleable=has_scale
        if w*h==0:
            self.resize(self.winimg.width(),self.winimg.height())
        else:
            self.resize(w,h)
            self.winimg=self.winimg.scaled(w,h,Qt.IgnoreAspectRatio)
        if has_scale:
            self.setMouseTracking(True)
            self.mousestartpos=QPoint()


        self.resizing=False
        if uimodule:
            self.ui=uimodule
            self.ui.setupUi(self)
        self.setAutoFillBackground(True)
        self.setMask(self.winimg.mask())
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.anchoredcomponents = []


    def resizeEvent(self, event:QResizeEvent):
        self.winimg = self.winimg.scaled(self.size().width(), self.size().height(), Qt.IgnoreAspectRatio)
        self.resize(self.size())
        self.setMask(self.winimg.mask())


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.resizing:
            moveto=event.globalPosition().toPoint()
#            self.mousestartpos=event.globalPosition().toPoint()
            resizetow=min(max(moveto.x()-self.x(),self.minimumWidth()),self.maximumWidth())
            resizetoh=min(max(moveto.y()-self.y(),self.minimumHeight()),self.maximumHeight())
            self.resize(resizetow,resizetoh)
        elif self.scaleable and (self.size().width()+self.size().height()-event.position().x()-event.y()<36 and event.position().x()<self.size().width() and event.position().y()<self.size().height()):
            self.setCursor(Qt.SizeFDiagCursor)
            if event.buttons()==Qt.LeftButton:
                self.resizing=True
        else:
            self.setCursor(Qt.ArrowCursor)
    def anchorwidget(self,window_anchor:anchor,widget:QWidget,widget_anchor:anchor,adjust_x=0,adjust_y=0):
        for x in self.anchoredcomponents:
            if x[1]==widget:
                self.anchoredcomponents.remove(x)
        self.anchoredcomponents.append([widget,anchordict[window_anchor],anchordict[widget_anchor],adjust_x,adjust_y])


    def removeanchorwidget(self,widget:QWidget):
        for x in self.anchoredcomponents:
            if widget in x:
                self.anchoredcomponents.remove(x)

    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     self.mousestartpos=event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.resizing=False

    def adjustcomponentposition(self):
        for comp in self.anchoredcomponents:
            wx, wy = anchorpos(self, comp[1])
            cx, cy = anchorpos(comp[0], comp[2])
            move_x = wx - cx + int(comp[-2])
            move_y = wy - cy + int(comp[-1])
            comp[0].move(move_x, move_y)


    def setuppal(self):
        pal = self.palette()
        pal.setBrush(QPalette.Window, self.winimg)
        self.setPalette(pal)

class styled_button(QWidget):
    '''
    额，貌似和原装的QPushButton没有太大区别，想用就用吧
    '''
    clicked = Signal()
    def __init__(self,normal_imgurl,select_imgurl,paren,w=100,h=50,has_switch=False,switch_imgurl='',switch_select_imgurl='',cursor_change=True):
        super(styled_button,self).__init__()
        self.setParent(paren)
        self.setFixedSize(w,h)
        self.setAutoFillBackground(True)
        self.cursor_change=cursor_change
        self.normlstyle=QPixmap(normal_imgurl).scaled(w,h)
        self.selectstyle=QPixmap(select_imgurl).scaled(w,h)

        self.select=False
        self.switched = False
        self.has_switch=has_switch
        if has_switch:
            self.norml_switched = QPixmap(switch_imgurl).scaled(w, h)
            self.select_switched = QPixmap(switch_select_imgurl).scaled(w, h)
        self.setstyle()

    def mousePressEvent(self, event):
        if self.has_switch:
            self.switched = not self.switched
        self.clicked.emit()
    def enterEvent(self, event):
        self.select=True
        if self.cursor_change:
            self.setCursor(Qt.PointingHandCursor)
        self.setstyle()
    def leaveEvent(self, event):
        self.select=False
        if self.cursor_change:
            self.setCursor(Qt.PointingHandCursor)
        self.setstyle()

    def setstyle(self):
        pal = self.palette()
        if self.select:
            if self.switched:
                pal.setBrush(QPalette.Window, self.select_switched)
                self.setMask(self.select_switched.mask())
            else:
                pal.setBrush(QPalette.Window, self.selectstyle)
                self.setMask(self.selectstyle.mask())
        else:
            if self.switched:
                pal.setBrush(QPalette.Window, self.norml_switched)
                self.setMask(self.norml_switched.mask())
            else:
                pal.setBrush(QPalette.Window, self.normlstyle)
                self.setMask(self.normlstyle.mask())
        self.setPalette(pal)
    def setuppal(self):
        pal = self.palette()
        pal.setBrush(QPalette.Window, self.winimg)
        self.setPalette(pal)

class styled_check_button(QWidget):
    '''
    写corner_tip时的附赠品，喜欢吗
    '''
    check = Signal(bool)
    def __init__(self, uncheck_imgurl, checked_imgurl, parent, w=100, h=50, has_switch=True,cursor_change=True):
        super(styled_check_button, self).__init__()
        self.setParent(parent)
        self.setFixedSize(w, h)
        self.setAutoFillBackground(True)
        self.cursor_change = cursor_change
        self.uncheckstyle = QPixmap(uncheck_imgurl).scaled(w, h)
        self.checkedstyle = QPixmap(checked_imgurl).scaled(w, h)

        self.checked=False
        self.switched = False
        self.has_switch = has_switch
        self.setstyle()

    def mousePressEvent(self, event):
        if self.checked:
            if self.has_switch:
                self.checked=False
                self.check.emit(False)
                self.setstyle()
        else:
            self.checked = True
            self.check.emit(True)
            self.setstyle()
            # self.clicked.emit(True)
    def setstyle(self):
        pal = self.palette()
        if self.checked:
            pal.setBrush(QPalette.Window, self.checkedstyle)
            self.setMask(self.checkedstyle.mask())
        else:
            pal.setBrush(QPalette.Window, self.uncheckstyle)
            self.setMask(self.uncheckstyle.mask())
        self.setPalette(pal)


    def enterEvent(self, event):
        self.select = True
        if self.cursor_change:
            self.setCursor(Qt.PointingHandCursor)
        self.update()

    def leaveEvent(self, event):
        self.select = False
        if self.cursor_change:
            self.setCursor(Qt.PointingHandCursor)
        self.update()

    def set_checked(self,checked:bool):
        self.checked=checked
        self.setstyle()
class styled_bar(QWidget):
    def __init__(self,parent:QWidget,imgurl='',w=0,h=0,opacity=1.0):
        super(styled_bar,self).__init__(parent=parent)
        #self.setParent(parent)
        self.opeffect = QGraphicsOpacityEffect()
        self.opeffect.setOpacity(opacity)
        self.layout=QHBoxLayout()
        self.setLayout(self.layout)
        self.winimg = QPixmap(imgurl).scaled(w,h)
        self.setAutoFillBackground(True)
        self.setGraphicsEffect(self.opeffect)
        self.rw=w
        self.rh=h
        if w*h != 0:
            self.setFixedSize(w,h)
        if imgurl != '':
            self.pal=self.palette()
            self.pal.setBrush(QPalette.Window,self.winimg)
            self.setPalette(self.pal)
            self.setMask(self.winimg.mask())

    def changestyle(self, newimgurl: str):
        self.winimg = QPixmap(newimgurl).scaled(self.rw, self.rh)
        self.pal = self.palette()
        self.pal.setBrush(QPalette.Window, self.winimg)
        self.setPalette(self.pal)
        self.setMask(self.winimg.mask())


class corner_tip_single(styled_win):
    '''
    默认用的在展示时计算夫窗口大小然后布置，所以夫窗口突然变大小的话它不会跟着走
    single_use和corner_tip_list相对立，corner_tip_list会自动调用corner_tip_single的plus模式
    谁不喜欢角落里的小提示呢?总比黑窗提示好吧?
    这里面最长的一个类了，我这个编程小白写了整整一天（90%的时间在修BUG）
    运行起来会报QPainter之类的错误，不影响使用
    It runs with QPainter wrong,but it doesn't matter.
    '''
    wclosed=Signal(QWidget)
    wshow=Signal()
    def __init__(self,parent : QWidget , button_img_uncheck,button_img_checked,single_use=True,buttonw=10,buttonh=10,tipcolor:QColor=QColor(0,255,0)):
        super(corner_tip_single,self).__init__()
        # self.setAutoFillBackground(True)
        self.setParent(parent)
        self.parent=parent
        self.tipcolor=tipcolor
        self.opeffect = QGraphicsOpacityEffect()
        self.bopeff=QGraphicsOpacityEffect()
        # self.noeff=QGraphicsOpacityEffect()
        self.winmask = QPixmap(100,100)
        self.winmask.fill(QColor(255, 255, 255, 0))
        self.winimg = QPixmap(100,100)
        self.winimg.fill(QColor(255, 255, 255, 0))
        self.paintwin = QPainter(self.winmask)
        self.single=single_use
        self.drawd=2
        self.frame=QFrame(self)
        self.wincolor=QColor(117,127,147)
        #components:
        self.BT_close=styled_check_button(button_img_uncheck,button_img_checked,self,buttonw,buttonh,False)
        self.BT_close.setToolTip('已读')
        self.refreshtime=20
        self.ani_o=QTimer()
        self.ani_o.setInterval(self.refreshtime)
        self.ani_p=QTimer()
        self.ani_p.setInterval(self.refreshtime)
        self.opacitysylelast=3500
        self.movestep =0
        self.movedstep = 0
        self.movestylelast=300
        self.currentopacity=1
        self.currentmove=0
        self.pal=self.palette()
        self.tpal=QPalette()

        self.lable=QLabel(self)

        self.checked=False
        self.is_closed=False
        self.BT_close.check.connect(self.closew)
        self.ani_p.timeout.connect(self.moves)
        if single_use:
            self.hide()
        self.ani_o.timeout.connect(self.setwopacity)
        self.setGraphicsEffect(self.opeffect)
        self.BT_close.setGraphicsEffect(self.bopeff)
        self.contentchange=False
        self.paintwin.end()

    # def __del__(self):
    #     print(f'released')


    def tip(self,text:str):
        self.BT_close.set_checked(False)
        self.pal.setColor(QPalette.WindowText , self.tipcolor)
        self.lable.setText(text)
        self.display()

    def warn(self,text:str):
        self.BT_close.set_checked(False)
        self.pal.setColor(QPalette.WindowText , QColor(255,0,0))
        self.lable.setText(text)
        self.display()
    def operate(self,text:str):
        self.BT_close.set_checked(False)
        self.pal.setColor(QPalette.WindowText ,QColor(0,0,255))
        self.lable.setText(text)
        self.display()

    def resizeEvent(self, event:QResizeEvent):
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
        self.anchorwidget(anchor.leftmid,self.BT_close,anchor.leftmid,5,2)
        self.anchorwidget(anchor.rightmid,self.lable,anchor.rightmid,-5,2)
        self.setuppal()
        self.adjustcomponentposition()
    def display(self):
        self.ani_o.stop()
        self.ani_p.stop()
        self.currentopacity=1
        self.is_closed=False
        self.lable.adjustSize()
        self.resize(self.lable.size()+QSize(self.BT_close.x()+25,25))
        self.lable.setPalette(self.pal)
        self.ani_o.start()
        if self.single:
            self.show()
            #if do not use anchor,use move:
            self.move(self.parent.width()-self.width(),self.parent.height()-self.height())
        elif not self.contentchange:
            self.wshow.emit()

    def enterEvent(self, event):
        if not self.is_closed:
            self.currentopacity=1
            self.opeffect.setOpacity(self.currentopacity)
            self.bopeff.setOpacity(self.currentopacity)
            self.adjustcomponentposition()
            self.ani_o.stop()
            # self.setWindowOpacity(1)
    def leaveEvent(self, event):
        if not self.is_closed:
            self.ani_o.start()
    def closew(self):
        self.is_closed=True
        self.movestep= int(self.width()*self.refreshtime/self.movestylelast)
        self.ani_p.start()

    def moves(self):
        if self.movedstep<self.width():
            self.move(self.x()+self.movestep,self.y())
            self.movedstep+=self.movestep
        else:
            self.ani_p.stop()
            self.movedstep=0
            self.hidew()

    def setwopacity(self):
        self.currentopacity -= self.refreshtime/self.opacitysylelast
        if self.currentopacity>0:
            self.opeffect.setOpacity(self.currentopacity)
            self.bopeff.setOpacity(self.currentopacity)
        else:
            self.currentopacity=1
            self.ani_o.stop()
            self.hidew()

    def setuppal(self):
        pal = self.palette()
        pal.setBrush(QPalette.Window, self.winimg)
        self.setPalette(pal)

    def hidew(self):
        if self.single:
            self.hide()
        else:
            # self.hide()
            self.wclosed.emit(self)


class corner_tip_list(styled_win):
    limit_by_quantity= b'quan'
    limit_by_height=b'h'
    limit_by_parent=b'p'
    def __init__(self ,parent : styled_win , button_img_uncheck,button_img_checked,buttonw=10,buttonh=10,limit_method:bytes=limit_by_height,limit_qaun=3,limit_h=100,interval=10,gaptoparent=20):
        super(corner_tip_list,self).__init__()
        self.setParent(parent)
        self.parent=parent
        self.tiplist=[]
        if limit_method== b'quan':
            self.addtip=self.addtip_q
        elif limit_method== b'h':
            self.addtip=self.addtip_h
        else:
            self.addtip=self.addtip_p
        self.b_c_img=button_img_checked
        self.b_unc_img=button_img_uncheck
        self.bw=buttonw
        self.bh=buttonh
        self.limit_height=limit_h
        self.sumheight=0
        self.interval=interval
        self.gap=gaptoparent
        self.limit_q=limit_qaun


    def removetip(self,w:QWidget):
        for a in self.tiplist:
            if a == w:
                self.sumheight -= w.height()
                a.wshow.disconnect()
                a.wclosed.disconnect()
                a.close()
                self.parent.removeanchorwidget(w)
                self.tiplist.remove(a)
                # a.deleteLater()
        self.rearrange()
        '''貌似python会把没有变量指向的值给删掉，（我是C++过来的），corner_tip_single里面注释掉的__del__就是我原来用来验证这个结论用的,重点来了，
        我创造的corner_tip_single是QObject的对象，所有者是Qt，所以python在这里不会清理掉，而我用deleteLater的话又会把新创建出来的，不应该被清理掉的corner_tip_single
        给删掉，搞的我很无奈,所以现在有两种方案：1.（默认方案）别管内存占用了，把上面的a.deleteLater()注释掉，每出一个提示占用微量的内存（也有可能没占）
        2.等一个提示消失了再提示下一个（corner_tip_list变得毫无意义）
        seem like if no var point to the value,the value will be released,see '__del__' in 'corner_tip_single' which is comment out,
        however,the corner_tip_single belong to QObject Class,whoes owner is Qt,so python will not release the class.So I tried to
        use deleteLater(),then it will also clear the 'corner_tip_single' which should not be released(because no variable point to it)
        and I have no idea about that,so if you can not solve it either,there are two solutions:1.(defalt)forget the memory occupation,
        comment out 'a.deleteLater()' 2.tip untill last tip disappear (just like 'corner_tip_single')
        '''


    def addtip_q(self,tiper:corner_tip_single):
        if len(self.tiplist)>self.limit_q:
            self.removetip(self.tiplist[0])
        overheight = False
        while self.sumheight + tiper.height() + self.gap > self.parent.height() and len(self.tiplist) != 0:
            overheight = True
            self.removetip(self.tiplist[0])
        if len(self.tiplist) == 0 and overheight:
            tiper.contentchange = True
            tiper.warn('窗口过小，无法展示提示内容')
        self.tiplist.append(tiper)
        tiper.show()
        self.rearrange()
    def addtip_h(self,tiper:corner_tip_single):
        overheight=False
        while self.sumheight+tiper.height()>self.limit_height and len(self.tiplist) != 0:
            overheight=True
            self.removetip(self.tiplist[0])
        if len(self.tiplist) == 0 and overheight:
            tiper.contentchange=True
            tiper.warn('对开发者的提示：高度设置过小，无法展示提示内容')
        self.tiplist.append(tiper)
        tiper.show()
        self.rearrange()

    def addtip_p(self,tiper:corner_tip_single):
        overheight = False
        while self.sumheight + tiper.height() + self.gap > self.parent.height() and len(self.tiplist) != 0:
            overheight = True
            self.removetip(self.tiplist[0])
        if len(self.tiplist) == 0 and overheight:
            tiper.contentchange = True
            tiper.warn('窗口过小，无法展示提示内容')
        self.tiplist.append(tiper)
        tiper.show()
        self.rearrange()

    def tip(self,text:str):
        tiper=corner_tip_single(self.parent,self.b_unc_img,self.b_c_img,False,self.bw,self.bh)
        tiper.wshow.connect(lambda:self.addtip(tiper))
        tiper.wclosed.connect(self.removetip)
        tiper.tip(text)
    def warn(self,text:str):
        tiper=corner_tip_single(self.parent,self.b_unc_img,self.b_c_img,False,self.bw,self.bh)
        tiper.wshow.connect(lambda:self.addtip(tiper))
        tiper.wclosed.connect(self.removetip)
        tiper.warn(text)

    def operate(self,text:str):
        tiper=corner_tip_single(self.parent,self.b_unc_img,self.b_c_img,False,self.bw,self.bh)
        tiper.wshow.connect(lambda:self.addtip(tiper))
        tiper.wclosed.connect(self.removetip)
        tiper.operate(text)

    def rearrange(self):
        self.sumheight=-self.interval
        for x in self.tiplist[::-1]:
            self.sumheight += self.interval
            self.parent.anchorwidget(anchor.rightbottom,x,anchor.rightbottom,0,-self.sumheight)
            self.sumheight += x.height()
        self.parent.adjustcomponentposition()

