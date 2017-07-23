from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading,sys,os,time,random,pyperclip
import qtawesome as qta
from faker import Factory

scrollbar_STYLE = "QScrollBar:vertical {border: 0px solid #66b1e4;background:#d9e9f4;}QScrollBar::handle:vertical {background: #3498db;min-height: 80px;}QScrollBar::handle:vertical::pressed {background-color: #45a0de;}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: #d9e9f4;}"
fake = Factory.create()
colors="#34495e,#b9c9d8;#3bd37b,#dbf7e7;#e67e22,#fae5d2;#3498db,#dbedf9;#9b59b6,#ede1f2;#95a5a6,#eaedee;#f39c12,#fceacd;#e74c3c,#fadcd9;#795548,#efe7e4".split(";")

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        
        
        directory = r"Data\\"
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("ERROR DIRECTORY 'DATA' WAS NOT FOUND: FIXED")

            # TODO Prompt showing files missing, software may not work properly

        QtGui.QFontDatabase.addApplicationFont('Data\\Fonts\\Ubuntu-Light.ttf')


        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())
        pos1 = self.x()
        pos2 = self.y()
        thread = threading.Thread(target=self.animate)
        thread.start()
        self.setGeometry(100,100,500,550)
        position_animator(self,pos1,900,pos1,pos2,duration=600)
        self.setWindowOpacity(0.0)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        font = QFont("Times",25)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)
        self.setWindowIcon(QIcon(r"Icons\\mainIcon.png"))
        self.setWindowTitle("Text Saver")
        self.setStyleSheet("border:0px solid grey;background-color:#ecf0f1;font-family:'Ubuntu Light';")

        # self.setAttribute(Qt.WA_TranslucentBackground)
        # effect = QGraphicsDropShadowEffect(self)
        # effect.setBlurRadius(10)
        # effect.setColor(QColor("#bdc3c7"))
        # effect.setOffset(2,2)


        # border = QLabel(self)
        # border.setGeometry(0,0,self.width(),self.height())
        # border.setStyleSheet("border-radius:2px;border:0px solid #ddd;border-left:4px solid #2ecc71; background-color:white;border-radius: 0px;")
        # border.setGraphicsEffect(effect)

        self.mdi = QMdiArea(self)
        self.mdi.setGeometry(5,60,self.width()-10,self.height()-100)
        self.mdi.setBackground(QtGui.QColor("#ecf0f1"))
        self.mdi.setAttribute(Qt.WA_TranslucentBackground)

        self.mdiSub = QMdiSubWindow(self.mdi)
        self.mdiSub.setWindowFlags(Qt.FramelessWindowHint)
        self.mdiSub.setGeometry(0,0,self.mdi.width()-20,self.mdi.height())
        self.mdiSub.setStyleSheet("background-color:#ecf0f1;")
        
        scroller_sub = QMdiSubWindow(self.mdi)
        scroller_sub.setGeometry(self.mdiSub.width(),0,20,self.mdi.height())
        scroller_sub.setWindowFlags(Qt.FramelessWindowHint)

        self.scroller = QScrollBar(scroller_sub)
        self.scroller.setGeometry(0,0,20,self.mdi.height())
        self.scroller.setStyleSheet(scrollbar_STYLE)
        self.scroller.valueChanged.connect(self.scroll)

        close = QPushButton(self)
        close.setGeometry(self.width()-40,0,40,40)
        close.setStyleSheet(".QPushButton{background-color:#ecf0f1;border:0;border-bottom:2px solid #34495e;} .QPushButton:hover{background-color:#d6dadb;}")
        close.setIcon(QIcon(r"Icons\close.png"))
        close.setIconSize(QSize(13,13))
        close.setCursor(Qt.PointingHandCursor)
        close.clicked.connect(self.close)
        
        title = QPushButton(self)
        title.setGeometry(0,0,460,40)
        title.setStyleSheet(".QPushButton{background-color:#ecf0f1;border:0;border-bottom:2px solid #34495e;} .QPushButton:hover{background-color:#ecf0f1;}")
        title.setIcon(QIcon(r"Icons\logo.png"))
        title.setIconSize(QSize(400,29))


        help_icon = QPushButton(self)
        help_icon.setIcon(QIcon(r"Icons\help.png"))
        help_icon.move(4+2,512)
        help_icon.setStyleSheet("background-color:white;border:0;padding:8px;")
        help_icon.setCursor(Qt.PointingHandCursor)
        help_icon.clicked.connect(lambda: self.createNewItem())
        # help_icon.clicked.connect(about.show)

        self.pos = 0
        self.items = []
        self.copiedBtnVisible = False


        copied_text = pyperclip.paste()
        if copied_text != "" and copied_text != None and copied_text != " ":
            self.createNewItem(text=copied_text,box_type = "copied")

        CThread2 = self.Clipboard_Thread()
        self.connect(CThread2, CThread2.signal, lambda: self.createNewItem(box_type="copied"))
        CThread2.start()

        # print("COPIED:"+copied_text+">")

        info = QLabel(self)
        info.setText("Made By Ahmad Taha - Version 1.0 Beta")
        info.move(37+2,520)
        info.setStyleSheet("color:grey;")
        self.show()
    class Clipboard_Thread(QtCore.QThread):
        def __init__(self):
            QtCore.QThread.__init__(self, parent=None)
            self.signal = QtCore.SIGNAL("signal")
        def run(self):
            old_text = pyperclip.paste()
            while True:
                text = pyperclip.paste()
                if text != old_text:
                    self.emit(self.signal)
                old_text = text
                time.sleep(1)
                
    def createNewItem(self,text = None,box_type = "text"):
        if text == None:
            if box_type == "copied":
                text = pyperclip.paste()
            else:
                text = fake.text() + fake.text()
        if box_type == "copied" and self.copiedBtnVisible == True:
            self.copiedBtn.main_text.setText(text)
            return
        if text in self.items:
            # TODO : notify already listed item
            return
        self.mdiSub.close()
        back,border = self.getRandomColor()
        if box_type == "copied":
            back,border = "#19B5FE","white"
        self.items.append(text)



        btn = QPushButton(self.mdiSub)
        btn.setGeometry(10,self.pos,self.mdiSub.width()-40,100)
        btn.setStyleSheet(".QPushButton{background-color:" + back + ";border:0px solid "+border+";color:"+border+";font-size:14px;text-align:left;padding-left:7px;}")
        btn.setObjectName(text)


        scrol_Style = "QScrollBar:vertical {border: 0;background:"+back+";}QScrollBar::handle:vertical {background: "+border+";}QScrollBar::handle:vertical::pressed {background-color:"+border+";}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background:"+back+";}"
        btn.main_text = QTextEdit(self.mdiSub)
        btn.main_text.setGeometry(14,self.pos+4,btn.width()-50,100-8)
        if box_type == "copied":
            btn.main_text.setGeometry(14,self.pos+4+20,btn.width()-50,80-8)
        btn.main_text.setStyleSheet(".QTextEdit{background-color:" + back + ";border:0px solid "+border+";color:"+border+";font-size:14px;text-align:left;}" + scrol_Style)
        btn.main_text.setText(text)
        btn.main_text.setReadOnly(True)

        
        deleteIcon = qta.icon('fa.scissors',color=border)
        btn.delete = QPushButton(deleteIcon,"",parent = self.mdiSub)
        btn.delete.setGeometry(self.mdi.width()-88,self.pos+10,30,30)
        if box_type == "copied":
            btn.delete.setGeometry(self.mdi.width()-88,self.pos+25,30,30)
        btn.delete.setStyleSheet(".QPushButton{background-color:"+back+";} .QPushButton:hover{border: 1px solid " + border+";}")
        btn.delete.setCursor(Qt.PointingHandCursor)
        btn.delete.setToolTip("Delete")
        btn.delete.clicked.connect(self.deleteItem)
        btn.delete.objectText = text
        
        if box_type == "copied":
            addIcon = qta.icon('fa.plus',color=border)
            btn.add = QPushButton(addIcon,"",parent = self.mdiSub)
            btn.add.setGeometry(self.mdi.width()-88,self.pos+65,30,30)
            btn.add.setStyleSheet(".QPushButton{background-color:"+back+";} .QPushButton:hover{border: 1px solid " + border+";}")
            btn.add.setCursor(Qt.PointingHandCursor)
            btn.add.setToolTip("Delete")
            btn.add.clicked.connect(lambda: self.createNewItem(text = btn.main_text.toPlainText()))

            btn.head = QPushButton(self.mdiSub)
            btn.head.setGeometry(10,self.pos,btn.width(),20)
            btn.head.setStyleSheet("background-color:#22A7F0;color:white;text-align:left;padding-left:10px;")
            btn.head.setText("Copied Text")

            btn.main_text.setObjectName("copied")

            self.copiedBtnVisible = True

            self.copiedBtn = btn

        position_animator(btn,-500,btn.y(),10,btn.y(),duration=600)
        position_animator(btn.main_text,-500,btn.main_text.y(),14,btn.main_text.y(),duration=700)
        position_animator(btn.delete,-500,btn.delete.y(),self.mdi.width()-88,btn.delete.y(),duration=500)
        if box_type == "copied":
            position_animator(btn.add,-500,btn.add.y(),self.mdi.width()-88,btn.add.y(),duration=500)
            position_animator(btn.head,-500,btn.head.y(),10,btn.head.y(),duration=600)

        if len(self.items) <= 3:
            self.scroller.move(20,0)
        else:
            self.scroller.move(0,0)
            self.scroller.setValue(self.scroller.maximum()-300)

        self.pos +=120
        self.mdiSub.resize(self.mdiSub.width(),self.pos)
        self.scroller.setMaximum(self.pos)
        self.mdiSub.show()
    def deleteItem(self):
        btn  = self.findChild(QPushButton,self.sender().objectText)
        
        self.items.remove(btn.objectName())

        position_animator(btn,btn.x(),btn.y(),-500,btn.y(),duration=800)
        position_animator(btn.main_text,btn.main_text.x(),btn.main_text.y(),-500,btn.main_text.y(),duration=1000)
        position_animator(btn.delete,btn.delete.x(),btn.delete.y(),-500,btn.delete.y(),duration=700)

        if "copied" in btn.main_text.objectName():
            self.copiedBtnVisible = False
            position_animator(btn.add,btn.add.x(),btn.add.y(),-500,btn.add.y(),duration=500)
            position_animator(btn.head,btn.head.x(),btn.head.y(),-500,btn.head.y(),duration=600)
    
        self.pos = 0

        for i in self.items:
            btn  = self.findChild(QPushButton,i)
            if "copied" in btn.main_text.objectName():
                self.pos += 120
                continue
            position_animator(btn,btn.x(),btn.y(),10,self.pos)
            position_animator(btn.main_text,btn.main_text.x(),btn.main_text.y(),14,self.pos+4)
            position_animator(btn.delete,btn.delete.x(),btn.delete.y(),self.mdi.width()-88,self.pos+20)

            self.pos +=120

        self.mdiSub.resize(self.mdiSub.width(),self.pos+120)
        self.scroller.setMaximum(self.pos)
    def scroll(self):
        value = self.scroller.value()
        self.mdiSub.move(self.mdiSub.x(),-(value))
    def getRandomColor(self):
        color = random.choice(colors)
        color = color.split(",")
        return color[1],color[0]
    def animate(self):
        opcty = 0.0
        for i in range(11):
            time.sleep(0.06)
            self.setWindowOpacity(opcty)
            opcty+=0.1
    def validate_file(self,location,def_content = ""):
        try:
            filee = open(location,"r")
            filee.close()
            return "File Validation Successfull"
        except:
            try:
                filee = open(location,"w")
                if def_content != "":
                    filee.write(def_content)
                filee.close()
                return "File Not Found : FIXED"
            except Exception as e:
                return "File Not Found : FAILED TO FIX"
def position_animator(obj = None,from_x = 0,from_y = 0,to_x = 0,to_y = 0,duration=500):
    animation = QPropertyAnimation(obj,"geometry",obj)
    animation.setStartValue(QRect(from_x,from_y,obj.width(),obj.height()))
    animation.setEndValue(QRect(to_x,to_y,obj.width(),obj.height()))
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuart)
    animation.start()
def fader(obj = None,From = 0.0,to = 1.0,duration = 400):
    animation = QPropertyAnimation(obj,"opacity",obj)
    animation.setStartValue(From)
    animation.setEndValue(to)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuad)
    animation.start()
class Help(QWidget):
    def __init__(self,parent = None):
        super(Help,self).__init__(parent)
        self.setWindowTitle("About Text Saver")
        self.setWindowIcon(QIcon(r"Icons\\2.png"))
        self.setStyleSheet("Background-color:white;")

        btn = QPushButton(self)
        btn.setIcon(QIcon(r"Icons\about.png"))
        btn.setIconSize(QSize(400,400))
        btn.move(0,0)
        btn.setStyleSheet("background-color:None;border:0;")

        self.resize(390,400)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    about = Help()
    wndw = MainWindow()
    # wndw.show()
    sys.exit(app.exec_())