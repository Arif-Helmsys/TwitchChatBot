# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt,QObject,pyqtSignal,pyqtSlot,QThread
import webbrowser as wb
import socket
import pickle
import resources
import sys

class ConnecTwitchChatBot(QObject):
    signal = pyqtSignal(str)
    def __init__(self,streamer:str,oauth:str,botname:str) -> None:
        super(ConnecTwitchChatBot,self).__init__()
        self.botname = botname
        self.streamer = streamer.lower()
        self.oauth = oauth
        self.socket = socket.socket()
        self.socket.connect(("irc.chat.twitch.tv",6667))
        
    def connectTwitch(self):
        self.send(self.socket,f"PASS oauth:{self.oauth}"),
        self.send(self.socket,f"NICK {self.botname}"),
        self.send(self.socket,f"JOIN #{self.streamer}"),
        self.send(self.socket,f"CAP REQ :twitch.tv/tags"),
        self.send(self.socket,f"CAP REQ :twitch.tv/commands")
        return self.__run()

    def send(self,socket:socket.socket,msg:str):
        return socket.send(bytes(msg+"\n","utf-8"))

    def recv(self,socket:socket.socket):
        return socket.recv(4096).decode('utf-8')

    def __run(self) -> None:
        if self.recv(self.socket) != '' or self.recv(self.socket) != None:
            while True:
                try:
                    msg = self.recv(self.socket)
                    if msg == "PING :tmi.twitch.tv":
                        self.send(self.socket,"PONG :tmi.twitch.tv")
                    else:
                        parse = self.__messageParse(msg.replace("\n",''))
                        self.signal.emit(f"{parse['name']}: {parse['msg']}")
                except (IndexError,TypeError):
                    pass
                except TimeoutError:
                    print("Zaman aşımı Gerçekleşti! Yeniden dene")
                except (ConnectionAbortedError,ConnectionResetError):
                    print(f"Bağlantıda Sorun algılandı! Yeniden dene")
                    break
    
    def __messageParse(self,msg:str) -> dict[str,str]:
        mod = False
        sub = False
        return_data = {}
        try:
            parse_tag = msg.split(";")
            parse_data = {}
            for i in range(len(parse_tag)):
                for j in range(len(parse_tag[i])):
                    if parse_tag[i][j] == '=':
                        parse_data.update({parse_tag[i][0:j] : parse_tag[i][j+1:len(parse_tag[i])]})

            type_ = parse_data["user-type"].split(f"#{self.streamer} :")
            parse_data["user-type"] = {"MESSAGE":type_[1]}

            if "moderator/1" in parse_data["badges"]:
                mod = True

            if parse_data["subscriber"] == '1':
                sub = True
                           
            if mod:
                return_data.update(
                    { 
                        "name" : f"[MOD]{parse_data['display-name']}",
                        "msg" : f"{parse_data['user-type']['MESSAGE']}",
                        "color" : f"{parse_data['color']}"
                    })
                return return_data

            if sub:
                return_data.update(
                    { "name" : f"[ABONE]{parse_data['display-name']}",
                    "msg" : f"{parse_data['user-type']['MESSAGE']}",
                    "color" : f"{parse_data['color']}"
                    })
                return return_data

            if not sub or not mod:
                return_data.update(
                    { "name" : f"[PLEB]{parse_data['display-name']}",
                      "msg" : f"{parse_data['user-type']['MESSAGE']}",
                      "color" : f"{parse_data['color']}"
                    })
                return return_data
        except KeyError:
            pass

class LoginWindow(QMainWindow):
    def __init__(self) -> None:
        super(LoginWindow,self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("ChatB0T")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(361, 576)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 361, 576))
        self.widget.setMinimumSize(QtCore.QSize(361, 576))
        self.widget.setMaximumSize(QtCore.QSize(361, 576))
        self.widget.setStyleSheet("QWidget{\n"
"    border: 2px solid rgb(255,0,255);\n"
"    background-color: rgb(53, 54, 58);\n"
"    border-top-left-radius :35px;\n"
"    border-bottom-right-radius : 35px\n"
"}")
        self.widget.setObjectName("widget")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 361, 41))
        self.frame.setStyleSheet("QFrame{\n"
"    border: 2px solid rgb(138,43,226);\n"
"    background-color: rgb(47,54,79);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.installEventFilter(self)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(303, 4, 51, 31))
        self.pushButton_2.clicked.connect(lambda: self.close())
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    border-top-left-radius :25px;\n"
"    border-bottom-right-radius : 25px;\n"
"    background-color: rgb(138,43,226);\n"
"    color: rgb(255,0,255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(255,43,255);\n"
"    color: rgb(138,43,226);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(47,54,79);\n"
"    color: rgb(255,43,255);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(48, 10, 81, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border: rgb(47,54,79);\n"
"color: rgb(255, 0, 255);")
        self.label_2.setObjectName("label_2")
        self.iconLabel = QtWidgets.QLabel(self.frame)
        self.iconLabel.setGeometry(QtCore.QRect(16, 11, 24, 24))
        self.iconLabel.setStyleSheet("border:rgb(47,79,79);")
        self.iconLabel.setText("")
        self.iconLabel.setPixmap(QtGui.QPixmap(":/icons/twitch_icon.ico"))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setObjectName("iconLabel")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(19, 10, 20, 20))
        self.label_4.setStyleSheet("border: rgb(53, 54, 58);")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/prfx/twitch_icon.ico"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(120, 76, 122, 121))
        self.label.setStyleSheet("border: 0px solid rgb(53, 54, 58);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/twitch_icon.ico"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setGeometry(QtCore.QRect(90, 305, 191, 41))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit{\n"
"    border-top-left-radius :20px;\n"
"    border-bottom-right-radius : 20px;\n"
"    color: rgb(138,43,226);\n"
"}\n"
"QLineEdit:hover{\n"
"    border: 2px solid rgb(138,43,226);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(138,43,226);\n"
"}\n"
"    /*border-top-left-radius :20px;*/\n"
"    /*border-bottom-right-radius : 20px;*/\n"
"")
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(137, 511, 91, 41))
        self.pushButton.clicked.connect(lambda: self.openChatScreen())
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton{\n"
"    background-color: rgb(138,43,226);\n"
"    color: rgb(255,0,255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(255,43,255);\n"
"    color: rgb(138,43,226);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(47,54,79);\n"
"    color: rgb(255,43,255);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(317, 530, 34, 34))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("QPushButton:hover{\n"
"    background-color: rgb(255,43,255);\n"
"    color: rgb(138,43,226);\n"
"}\n"
"QPushButton{\n"
"border-radius: 15px;\n"
"border: rgb(53, 54, 58);\n"
"}\n"
"")
        self.pushButton_3.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/prfx/github.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QtCore.QSize(44, 46))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: wb.open_new("https://github.com/Arif-Helmsys"))
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 370, 191, 41))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("QLineEdit{\n"
"    border-top-left-radius :20px;\n"
"    border-bottom-right-radius : 20px;\n"
"    color: rgb(138,43,226);\n"
"}\n"
"QLineEdit:hover{\n"
"    border: 2px solid rgb(138,43,226);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(138,43,226);\n"
"}\n"
"    /*border-top-left-radius :20px;*/\n"
"    /*border-bottom-right-radius : 20px;*/\n"
"")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 240, 191, 41))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("QLineEdit{\n"
"    border-top-left-radius :20px;\n"
"    border-bottom-right-radius : 20px;\n"
"    color: rgb(138,43,226);\n"
"}\n"
"QLineEdit:hover{\n"
"    border: 2px solid rgb(138,43,226);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(138,43,226);\n"
"}\n"
"    /*border-top-left-radius :20px;*/\n"
"    /*border-bottom-right-radius : 20px;*/\n"
"")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(130, 70, 131, 131))
        self.label_3.setStyleSheet("border: rgb(53, 54, 58);")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/prfx/twitch_icon.ico"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "X"))
        self.label_2.setText(_translate("MainWindow", "Login"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Token"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "B0T Name"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Channel Name"))


    def eventFilter(self, source, event) -> bool:
        if source == self.frame:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                        self.offset = event.pos()
                elif event.type() == QtCore.QEvent.MouseMove and self.offset is not None:
                        self.move(self.pos() - self.offset + event.pos())
                        return True
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                        self.offset = None
        return super().eventFilter(source, event)
    
    def openChatScreen(self):
        if self.lineEdit_3.text() and self.lineEdit.text() and len(self.lineEdit.text()) == 30 and self.lineEdit_2.text():
            self.close()
            cw = ChatWindow(streamer=self.lineEdit_3.text(),
                            oauth=self.lineEdit.text(),
                            bot=self.lineEdit_2.text())
            cw.show()

#### --*-- CHAT EKRANI --*-- ###

class ChatWindow(QMainWindow):
    def __init__(self,streamer,oauth,bot) -> None:
        super(ChatWindow,self).__init__()
        self.setWindowTitle("ChatB0T")
        self.thread_ = QThread()
        self.twitch = ConnecTwitchChatBot(streamer,oauth,bot)
        self.twitch.moveToThread(self.thread_)
        self.thread_.started.connect(self.twitch.connectTwitch)
        self.thread_.start()
        self.twitch.signal.connect(self.ekrandaGoster)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(533, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainWidget = QtWidgets.QWidget(self.centralwidget)
        self.mainWidget.setGeometry(QtCore.QRect(10, 10, 521, 591))
        self.mainWidget.setStyleSheet("QWidget{\n"
"    background-color: rgb(53, 54, 58);\n"
"    border-radius: 50px;\n"
"}")
        self.mainWidget.setObjectName("mainWidget")
        self.statusBarFrame = QtWidgets.QFrame(self.mainWidget)
        self.statusBarFrame.setGeometry(QtCore.QRect(0, 0, 521, 41))
        self.statusBarFrame.setStyleSheet("QFrame{\n"
"    border: 2px solid rgb(255,0,255);\n"
"    background-color: rgb(47,54,79);\n"
"    border-radius: 12px;\n"
"}")
        self.statusBarFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.statusBarFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusBarFrame.setObjectName("statusBarFrame")
        self.statusBarFrame.installEventFilter(MainWindow)
        self.iconLabel = QtWidgets.QLabel(self.statusBarFrame)
        self.iconLabel.setGeometry(QtCore.QRect(18, 5, 31, 31))
        self.iconLabel.setStyleSheet("border:rgb(47,79,79);")
        self.iconLabel.setText("")
        self.iconLabel.setPixmap(QtGui.QPixmap(":/icons/twitch_icon.ico"))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setObjectName("iconLabel")
        self.subLabel = QtWidgets.QLabel(self.statusBarFrame)
        self.subLabel.setGeometry(QtCore.QRect(60, 10, 201, 21))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.subLabel.setFont(font)
        self.subLabel.setStyleSheet("border:rgb(47,79,79);\n"
"color: rgb(255,0,255);")
        self.subLabel.setObjectName("subLabel")
        self.closePushButton = QtWidgets.QPushButton(self.statusBarFrame)
        self.closePushButton.setGeometry(QtCore.QRect(454, 7, 61, 28))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.closePushButton.setFont(font)
        self.closePushButton.clicked.connect(lambda: self.close())
        self.closePushButton.setStyleSheet("QPushButton{\n"
"    border-radius: 12px;\n"
"    background-color: rgb(138,43,226);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(255,43,255);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(47,54,79);\n"
"    color: rgb(255,43,255);\n"
"}")
        self.closePushButton.setObjectName("closePushButton")
        self.minimizePushButton = QtWidgets.QPushButton(self.statusBarFrame)
        self.minimizePushButton.setGeometry(QtCore.QRect(388, 7, 61, 28))
        self.minimizePushButton.clicked.connect(self.showMinimized)
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.minimizePushButton.setFont(font)
        self.minimizePushButton.setStyleSheet("QPushButton{\n"
"    border-radius: 12px;\n"
"    background-color: rgb(138,43,226);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(255,43,255);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(47,54,79);\n"
"    color: rgb(255,43,255);\n"
"}")
        self.minimizePushButton.setObjectName("minimizePushButton")
        self.label_7 = QtWidgets.QLabel(self.statusBarFrame)
        self.label_7.setGeometry(QtCore.QRect(15, 5, 31, 31))
        self.label_7.setStyleSheet("border: rgb(53, 54, 58);")
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/prfx/twitch_icon.ico"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.send_message_entry = QtWidgets.QLineEdit(self.mainWidget)
        self.send_message_entry.setGeometry(QtCore.QRect(40, 506, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.send_message_entry.setFont(font)
        self.send_message_entry.setStyleSheet("QLineEdit{\n"
"    border: 2px solid rgb(138,43,226);\n"
"    border-top-left-radius :15px;\n"
"    border-bottom-right-radius : 15px;\n"
"    color: rgb(138,43,226);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(138,43,226);\n"
"")
        self.send_message_entry.setText("")
        self.send_message_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.send_message_entry.setObjectName("send_message_entry")
        self.send_message_entry.setStyleSheet("color: rgb(138,43,226);\n"
                                              "border: 2px solid rgb(255,43,255);\n"
                                              "border-top-right-radius :5px;\n"
                                              "border-bottom-left-radius : 5px;\n")
        self.send_message_button = QtWidgets.QPushButton(self.mainWidget)
        self.send_message_button.setGeometry(QtCore.QRect(270, 506, 231, 61))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.send_message_button.setFont(font)
        self.send_message_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send_message_button.setStyleSheet("QPushButton{\n"
"    background-color: rgb(138,43,226);\n"
"    color: rgb(255,0,255);\n"
"    border-top-left-radius :5px;\n"
"    border-bottom-right-radius : 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(255,43,255);\n"
"    color: rgb(138,43,226);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(47,54,79);\n"
"    color: rgb(255,43,255);\n"
"}")
        self.send_message_button.setObjectName("send_message_button")
        self.formLayout = QtWidgets.QFormLayout()
        self.groupBox = QtWidgets.QGroupBox()
        self.scroll_ = QtWidgets.QScrollArea(self)
        self.scroll_.setWidget(self.groupBox)
        self.scroll_.setWidgetResizable(True)
        self.scroll_.setGeometry(15, 60, 501, 441)
        self.scroll_.setStyleSheet("QScrollBar:vertical {"              
    "    border: 2px solid rgb(53, 54, 58);"
    "    background: white;"
    "    width:10px;    "
    "    margin: 0px 0px 0px 0px;"
    "}"
    "QScrollBar::handle:vertical {"
    "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
    "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));"
    "    min-height: 0px;"
    "}"
    "QScrollBar::add-line:vertical {"
    "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
    "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
    "    height: 0px;"
    "    subcontrol-position: bottom;"
    "    subcontrol-origin: margin;"
    "}"
    "QScrollBar::sub-line:vertical {"
    "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
    "    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
    "    height: 0 px;"
    "    subcontrol-position: top;"
    "    subcontrol-origin: margin;"
    "}")
        self.scroll_.horizontalScrollBar().hide()
        self.layout_ = QtWidgets.QVBoxLayout()
        self.layout_.setSpacing(5)
        self.groupBox.setStyleSheet("background-color: rgb(47,54,79);\n"
                                    "border: 1px solid rgb(255,0,255);\n"
                                    )
        self.groupBox.setFixedWidth(499)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.subLabel.setText(_translate("MainWindow", "Chat Bot for You"))
        self.closePushButton.setText(_translate("MainWindow", "X"))
        self.minimizePushButton.setText(_translate("MainWindow", "_"))
        self.send_message_entry.setPlaceholderText(_translate("MainWindow", "message"))
        self.send_message_entry.returnPressed.connect(self.sendMessage)
        self.send_message_button.setText(_translate("MainWindow", "Send"))
        self.send_message_button.clicked.connect(lambda: self.sendMessage())

    def eventFilter(self, source, event) -> bool:
        if source == self.statusBarFrame:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                        self.offset = event.pos()
                elif event.type() == QtCore.QEvent.MouseMove and self.offset is not None:
                        self.move(self.pos() - self.offset + event.pos())
                        return True
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                        self.offset = None
        return super().eventFilter(source, event)

    def sendMessage(self):
        if self.send_message_entry.text() != ' ' or self.send_message_entry.text():
            self.twitch.send(self.twitch.socket,f"PRIVMSG #{self.twitch.streamer} :{self.send_message_entry.text()}")
            me = QtWidgets.QLabel(f"[B0T]: {self.send_message_entry.text()}")
            me.setFont(QtGui.QFont("Cascadia Code",11))
            me.setStyleSheet("padding-top: 3px;\n"
                              "color: rgb(255,0,255);\n"
                              "border: 2px solid rgb(138,43,226);\n"
                              "padding-bottom: 5px;\n"
                              "padding-top: 5px;\n"
	                          "border-top-right-radius :5px;\n"
	                          "border-bottom-left-radius : 5px;\n")
            self.formLayout.addRow(me)
            self.send_message_entry.clear()

    @pyqtSlot(str)
    def ekrandaGoster(self,msg:str):
        while True:
            self.layout_.addWidget(self.scroll_)
            vbar = self.scroll_.verticalScrollBar()
            vbar.setValue(vbar.maximum())
            lbl = QtWidgets.QLabel(msg,wordWrap=True)
            
            self.formLayout.addRow(lbl)
            self.groupBox.setLayout(self.formLayout)
            lbl.setFont(QtGui.QFont("Cascadia Code",10))
            lbl.setStyleSheet( f"color: rgb(47,54,79);\n"
                               "border: 2px solid rgb(138,43,226);\n"
	                           "background-color: rgb(255, 0, 255);\n"
                               "padding-bottom: 5px;\n"
                               "padding-top: 5px;\n"
                               "border-top-right-radius :10px;\n"
	                           "border-bottom-left-radius : 5px;\n")
            break

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginWindow()
    ui.show()
    sys.exit(app.exec_())