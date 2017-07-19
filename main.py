from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading,sys,os,time

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
        self.setStyleSheet("border:0px solid grey;background-color:white;font-family:'Ubuntu Light';")

        # self.setAttribute(Qt.WA_TranslucentBackground)
        # effect = QGraphicsDropShadowEffect(self)
        # effect.setBlurRadius(10)
        # effect.setColor(QColor("#bdc3c7"))
        # effect.setOffset(2,2)


        # border = QLabel(self)
        # border.setGeometry(2,2,640-7,550-7)
        # border.setStyleSheet("border-radius:2px;border:0px solid #ddd;border-left:4px solid #2ecc71; background-color:white;border-radius: 0px;")
        # border.setGraphicsEffect(effect)

        close = QPushButton(self)
        close.setGeometry(self.width()-40,0,40,40)
        close.setStyleSheet(".QPushButton{background-color:#ecf0f1;border:0;} .QPushButton:hover{background-color:#d6dadb;}")
        close.setIcon(QIcon(r"Icons\close.png"))
        close.setIconSize(QSize(13,13))
        close.setCursor(Qt.PointingHandCursor)
        close.clicked.connect(self.close)
        
        title = QPushButton(self)
        title.setGeometry(0,0,460,40)
        title.setStyleSheet(".QPushButton{background-color:#ecf0f1;border:0;} .QPushButton:hover{background-color:#ecf0f1;}")
        title.setIcon(QIcon(r"Icons\logo.png"))
        title.setIconSize(QSize(400,29))
        title.clicked.connect(self.close)


        help_icon = QPushButton(self)
        help_icon.setIcon(QIcon(r"Icons\help.png"))
        help_icon.move(4+2,512)
        help_icon.setStyleSheet("background-color:white;border:0;padding:8px;")
        help_icon.setCursor(Qt.PointingHandCursor)
        help_icon.clicked.connect(about.show)

        info = QLabel(self)
        info.setText("Made By Ahmad Taha - Version 1.0 Beta")
        info.move(37+2,520)
        info.setStyleSheet("color:grey;")
        self.show()
                
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