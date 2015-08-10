# -*- coding: utf-8 -*-

# To-do list
#
# optimize validateCard and setIssuerImg - less cycles
# automatically add spaces at the end of each 4-digit group. modify validator accordingly
#
# possibly in future - remove validateBtn and make resultLabel update on text update in ccText

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import re


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.pixmaps = {
            'American Express': 'american_express.png',
            'Diners Club': 'diners_club.png',
            'Discover': 'discover.png',
            'JCB': 'jcb.png',
            'Dankort': 'Dankort.png',
            'MasterCard': 'Master_Card.png',
            'Maestro': 'Maestro.png',
            'Visa': 'Visa.png'
        }

        self.redPalette = QtGui.QPalette()
        self.redPalette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)

        self.greenPalette = QtGui.QPalette()
        self.greenPalette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.darkGreen)

        self.aboutWindow = AboutWindow()

        self.setup_ui(self)

    def setup_ui(self, MainWindow):

        MainWindow.setFixedSize(560, 225)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)

        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.ccTextLabel = QtWidgets.QLabel(self.centralwidget)

        self.verticalLayout.addWidget(self.ccTextLabel)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.ccImgLabel = QtWidgets.QLabel(self.centralwidget)
        self.ccImgLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.ccImgLabel.setMaximumSize(QtCore.QSize(64, 64))
        self.ccImgLabel.setText("")

        self.horizontalLayout.addWidget(self.ccImgLabel)

        self.ccText = QtWidgets.QLineEdit(self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ccText.sizePolicy().hasHeightForWidth())

        self.ccText.setSizePolicy(sizePolicy)
        self.ccText.setMaximumSize(QtCore.QSize(16777215, 28))

        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp("(?:[0-9]{4}(?:-?| ?)){3}[0-9]{4}$"), self.ccText)
        self.ccText.setValidator(self.validator)

        self.ccText.textChanged.connect(self.set_issuer_img)

        self.horizontalLayout.addWidget(self.ccText)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.resultLabel = QtWidgets.QLabel(self.centralwidget)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.resultLabel.setFont(font)
        self.resultLabel.setText("")
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.verticalLayout.addWidget(self.resultLabel)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.validateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.validateBtn.clicked.connect(self.validate_card)
        self.validateBtn.setAutoDefault(True)
        self.validateBtn.setDefault(True)

        self.verticalLayout.addWidget(self.validateBtn)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 560, 23))

        self.menuFile = QtWidgets.QMenu(self.menubar)

        self.menuAbout = QtWidgets.QMenu(self.menubar)

        MainWindow.setMenuBar(self.menubar)

        self.actionExit = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', MainWindow)
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)

        self.actionAbout = QtWidgets.QAction(QtGui.QIcon('gnome-info.png'), '&About', MainWindow)
        self.actionAbout.triggered.connect(self.aboutWindow.show)

        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.setWindowIcon(QtGui.QIcon('cc_icon.png'))

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Validator"))

        self.ccTextLabel.setText(_translate("MainWindow", "Enter your card number below"))

        self.validateBtn.setText(_translate("MainWindow", "Validate"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))

        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit application"))
        self.actionExit.setShortcut(_translate("MainWindow", "Alt+X"))

        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setStatusTip(_translate("MainWindow", "About application"))

    def validate_card(self):

        issuers = {
            'American Express': '^3[47]\d{13}$',
            'Diners Club': '^(30[0-5]\d|309\d|36\d\d|3[89]\d\d)\d{10}',
            'Discover': '^6(?:011\d\d|5\d{4}|4[4-9]\d{3}|22(?:1(?:2[6-9]|[3-9]\d)|[2-8]\d\d|9(?:[01]\d|2[0-5])))\d{10}$',
            'JCB': '^35(?:2[89]|[3-8]\d)\d{12}$',
            'Dankort': '^5019\d{12}',
            'MasterCard': '^5[1-5]\d{14}$',
            'Maestro': '^(?:5[06789]\d\d|6304|6390|67\d\d)\d{8,15}$',
            'Visa': '^4\d{15}$'
        }

        cc_number = self.ccText.text()

        stripped = re.sub(r"\D", '', cc_number)

        reverse = stripped[::-1]

        total = 0
        i = 1
        valid = None

        for issuer in issuers:

            exp = issuers[issuer]

            if re.match(exp, stripped):

                for char in reverse:

                    digit = int(char)

                    if i % 2 == 0:

                        digit *= 2
                        temp_lst = [int(d) for d in str(digit)]

                        for d in temp_lst:

                            total += d

                    else:

                        total += digit

                    i += 1

                if total % 10 == 0:

                    valid = True
                    self.resultLabel.setText('Card is valid')
                    self.resultLabel.setPalette(self.greenPalette)
                    break

                else:

                    self.resultLabel.setText('Invalid card number')
                    self.resultLabel.setPalette(self.redPalette)
                    break

        if not valid:
            self.resultLabel.setText('Invalid card')
            self.resultLabel.setPalette(self.redPalette)

    def set_issuer_img(self):

        issuers = {
            'American Express': '^3[47]\d\d',
            'Diners Club': '^30[0-5]\d|309\d|36\d\d|3[89]\d\d',
            'Discover': '^6(?:011\d\d|5\d{4}|4[4-9]\d{3}|22(?:1(?:2[6-9]|[3-9]\d)|[2-8]\d\d|9(?:[01]\d|2[0-5])))',
            'JCB': '^35(?:2[89]|[3-8]\d)',
            'Dankort': '^5019',
            'MasterCard': '^5[1-5]\d\d',
            'Maestro': '^(?:5[06789]\d\d|6304|6390|67\d\d)',
            'Visa': '^4\d\d\d'
        }

        current_text = self.ccText.text()

        if len(current_text) < 4:

            self.ccImgLabel.setPixmap(QtGui.QPixmap('blank.png'))
            self.ccImgLabel.setToolTip('')

        else:

            for issuer in issuers:

                exp = issuers[issuer]

                if re.match(exp, current_text):

                    pixmap = QtGui.QPixmap(self.pixmaps[issuer])
                    self.ccImgLabel.setPixmap(pixmap)
                    self.ccImgLabel.setToolTip(issuer)
                    break


class AboutWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.pixmap = QtGui.QPixmap('logo.png')

        self.image_label = QtWidgets.QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.about_label_1 = QtWidgets.QLabel('Credit card validator application')
        self.about_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.about_label_1.setWordWrap(True)

        self.about_label_2 = QtWidgets.QLabel('Created by Dannyo')
        self.about_label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.pressed.connect(self.close)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)

        vbox.addWidget(self.image_label)
        vbox.addWidget(self.about_label_1)
        vbox.addWidget(self.about_label_2)
        vbox.addWidget(self.close_button)

        self.setWindowTitle('About')
        self.setFixedSize(200, 200)
        self.setWindowIcon(QtGui.QIcon('cc_icon.png'))

        self.setLayout(vbox)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
