from PySide6.QtWidgets import QApplication,QWidget,QPushButton,QTextEdit,QProgressBar
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
try:
    from PIL import Image
except ImportError:
    import Image
import os
import pytesseract 
import numpy as np
import fitz
#from PySide6.QtGui import QClipboard
pytesseract.pytesseract.tesseract_cmd ='./Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config ='--tessdata-dir "./Tesseract-OCR/tessdata"'


prefix=['PDF转换_','删空格_','图像识别_','删换行_','删换页_','合并文件_']
def goutputtxt(text):
    #文件加—_1，数字后缀
    i=0
    p=f'Output/{text}.txt'
    if os.path.exists('Output')==False:
        os.mkdir('Output')
    while os.path.isfile(p):
        i += 1
        p=f'Output/{text}_{i}.txt'
    return p

def removea(text):
    for pre in prefix:
        if pre in text:
            return text.replace(pre,'')
    return text
def ptof(a,p):
    return goutputtxt('%s_%s..'% (a,removea(p.split('/')[-1].split('.')[0][0:10])))


class Window:
    def __init__(self):
        self.win = QWidget()
        self.win.setFixedSize(300, 485)
#        self.win.move(700, 210)
        self.win.setWindowTitle("PDF_OCR程序")
        self.win.setWindowIcon(QIcon('./Tesseract-OCR/OCRproj/OCR.ico'))
        self.pt=os.path.abspath('.')


        self.textEdit = QTextEdit(self.win)
        self.textEdit.move(7,0)
        self.textEdit.resize(286, 200)
        
        self.textEdit.setPlaceholderText(
'''            PDF、TXT文件拖入此处
                 直接拖进来！！！
                 图片也不是不可以
           不要在这里乱敲东西！！！
     都可以批量操作，都可以批量操作>:(
       图像、PDF、TXT批量处理请分开
        非常不建议批量转换PDF文档！！！
      及时把输出文件取走，以免乱成一团
软件可以挪位置，但要整个OCR文件夹一起挪
                  按对应的按钮！！！
                 bilibili::Ordneri''')
#        self.textEdit.setAlignment (Qt.AlignCenter)



        self.button = QPushButton("PDF文字识别", self.win)
        self.button.resize(140,43)
        self.button.move(7, 203)
        self.button.clicked.connect(self.pdfs)

        self.button4 = QPushButton("图像识别", self.win)
        self.button4.resize(140,43)
        self.button4.move(153, 203)
        self.button4.clicked.connect(self.imgocr)

        self.btconv2 = QPushButton('TXT删空格',self.win)
        self.btconv2.resize(140,43)
        self.btconv2.move(7, 252)
        self.btconv2.clicked.connect(self.removespaces)

        self.btconv3 = QPushButton('TXT删回车',self.win)
        self.btconv3.resize(140,43)
        self.btconv3.move(153, 252)
        self.btconv3.clicked.connect(self.removeenter)

        
        self.btconv5 = QPushButton('TXT删换页',self.win)
        self.btconv5.resize(140,43)
        self.btconv5.move(7, 298)
        self.btconv5.clicked.connect(self.removepages)

        self.btconv6 = QPushButton('TXT文档合并',self.win)
        self.btconv6.resize(140,43)
        self.btconv6.move(153, 298)
        self.btconv6.clicked.connect(self.comp)

        
        self.textEdit3 = QTextEdit(self.win)
        self.textEdit3.move(7,344)
        self.textEdit3.resize(286, 100)
        self.textEdit3.setReadOnly(True)

        self.progress = QProgressBar(self.win)
        self.progress.resize(286,35)
        self.progress.setTextVisible(False)
        self.progress.move(7,447)
        self.progress.setRange(0,1)

        self.tip('这里是程序进程框')
        self.tip('海内存知己，天涯若比邻')
        try:
            self.langs='+'.join(pytesseract.get_languages())
            self.tip(f'检测到已安装的语言:\n{self.langs}')
        except pytesseract.pytesseract.TesseractNotFoundError:
            self.warn('寄!tesseract-ocr找不到了，程序不能乱挪位置哦')
        except UnicodeDecodeError:
            self.warn('估计是因为放在D盘目录下的原因，不介意的话，放C盘吧')
        except Exception:
            self.warn('我程序遇到了问题，估计是用不了了:(')
            self.warn('长风破浪会有时，直挂云帆济沧海')
        else:
            self.tip('程序正常运行（应该吧，大概）')
        
    def pdfocr(self,text):
        
        try:
            pdf = fitz.open(text)
            tlal=pdf.page_count
            self.progress.setRange(0,tlal)
            fname=ptof('PDF转换',text)
            fout=open(fname,'a',encoding='utf-8')
            for pg in range(0, tlal):
                self.act(f'开始转换：{pg+1}/{tlal}')
                page = pdf[pg]
                pm = page.get_pixmap(alpha=False)
                img=np.frombuffer( pm.samples , np.uint8)
                img=img.reshape(pm.height,pm.width,3)
                text=pytesseract.image_to_string(Image.fromarray(img),self.langs)
                fout.write(text)
                self.progress.setValue(pg+1)
                
            self.tip('文件转化完成:')
        except pytesseract.pytesseract.TesseractNotFoundError:
            self.warn('没有安装tesseract-ocr')
        except Exception:
            self.warn('未知错误')
            
    def pdfs(self):
        fin=self.textEdit.toPlainText().replace("file:///","").split('\n')
        self.textEdit.clear()
        if '' in fin:
            fin.remove('')
        for f in fin:
            self.tip('正在转换:\n%s'%f.split('/')[-1])
            self.pdfocr(f)
        os.startfile('Output')

    def imgocr(self):
        fin=self.textEdit.toPlainText().replace("file:///","").split('\n')
        self.textEdit.clear()
        if '' in fin:
            fin.remove('')
        self.progress.setRange(0,len(fin))
        sc=0
        for f in range(0,len(fin)):
            foutn=ptof('图像识别',fin[f])
            with open(foutn,'a',encoding='utf-8') as fout:
                try:
                    text=pytesseract.image_to_string(Image.open(fin[f]),self.langs)
                    fout.write(text)
                    self.progress.setValue(f+1)
                    self.tip(f'转换完成：{self.pt}\{foutn}')
                    sc+=1
                except pytesseract.pytesseract.TesseractNotFoundError:
                    self.warn('没有安装tesseract-ocr')
                except pytesseract.pytesseract.TesseractError:
                    self.warn('没有安装中文语言包')
                except Exception:
                    self.warn('未知错误')
            self.tip('进度：%d/%d'%(f+1,len(fin)))
        self.tip('已成功完成%d/%d张图片转换'%(sc,len(fin)))
        os.startfile('Output')
        

    def removespaces(self):
        fs=self.textEdit.toPlainText().replace("file:///","").split('\n')
        self.textEdit.clear()
        if '' in fs:
            fs.remove('')
        self.progress.setRange(0,len(fs))
        for f in range(0,len(fs)):
            fout=open(ptof('删空格',fs[f]),'w',encoding='utf-8')
            fin=open(fs[f],'r',encoding='utf-8')
            fout.write(fin.read().replace(' ',''))
            fin.close()
            fout.close()
            self.progress.setValue(f+1)
        self.tip('已删除所有文件空格')
        os.startfile('Output')

    def removeenter(self):
        fs=self.textEdit.toPlainText().replace("file:///","").split('\n')
        self.textEdit.clear()
        if '' in fs:
            fs.remove('')
        self.progress.setRange(0,len(fs))
        for f in range(0,len(fs)):
            fout=open(ptof('删换行',fs[f]),'w',encoding='utf-8')
            fin=open(fs[f],'r',encoding='utf-8')
            fout.write(fin.read().replace('\n',''))
            fin.close()
            fout.close()
            self.progress.setValue(f+1)
        self.tip('已删除所有文件换行')
        os.startfile('Output')

    def removepages(self):
        fs=self.textEdit.toPlainText().replace("file:///","").split('\n')
        self.textEdit.clear()
        if '' in fs:
            fs.remove('')
        self.progress.setRange(0,len(fs))
        for f in range(0,len(fs)):
            fout=open(ptof('删换页',fs[f]),'w',encoding='utf-8')
            fin=open(fs[f],'r',encoding='utf-8')
            fout.write(fin.read().replace('\f',''))
            fin.close()
            fout.close()
            self.progress.setValue(f+1)
        self.tip('已删除所有文件换页')
        os.startfile('Output')

    def comp(self):
        fs=self.textEdit.toPlainText().replace("file:///","").split('\n')
        self.textEdit.clear()
        if '' in fs:
            fs.remove('')
        self.progress.setRange(0,len(fs))
        fout=open(goutputtxt('合并文件'),'a',encoding='utf-8')
        for f in range(0,len(fs)):
            fl=open(fs[f],'r',encoding='utf-8')
            fout.write(fl.read())
            self.progress.setValue(f+1)
            fl.close()
        fout.close()
        self.tip('已完成合并')
        os.startfile('Output')


    def tip(self,text):
        self.textEdit3.setTextColor(Qt.blue)
        self.textEdit3.append(text)

    def warn(self,text):
        self.textEdit3.setTextColor(Qt.red)
        self.textEdit3.append(text)

    def act(self,text):
        self.textEdit3.setTextColor(Qt.gray)
        self.textEdit3.append(text)
                
            

if __name__ == '__main__':
    app = QApplication([])
    w = Window()
    w.win.show()
    app.exec()
