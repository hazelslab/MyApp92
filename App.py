# pyuic5 app.ui -o UI.py
import sys

from PyQt5.QtCore import QEvent, Qt, QSize, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, \
    QVBoxLayout

import Helper
from Database import Database
from UI import Ui_MainWindow


class CustomWidgets:

    @staticmethod
    def copyButtonProperties(newButtonObjectName: str, newButton: QPushButton, copyButton: QPushButton):
        horizontalLayout = QHBoxLayout(newButton)
        iconLabel = QLabel(copyButton)
        iconLabel.setMaximumSize(QSize(30, 30))
        iconLabel.setMinimumSize(QSize(20, 20))
        iconLabel.setLineWidth(1)
        iconLabel.setText("")
        iconLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,0%); margin-left: 10px")
        iconLabel.setPixmap(copyButton.icon().pixmap(20, 20, QIcon.Active, QIcon.On))
        iconLabel.setScaledContents(False)
        iconLabel.setWordWrap(False)
        iconLabel.setObjectName('homeicon')
        horizontalLayout.addWidget(iconLabel, 0)
        textLabel = QLabel(copyButton.text())
        textLabel.setFont(copyButton.font())
        textLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,0%); padding-right: 10px;")
        textLabel.setAlignment(Qt.AlignCenter)
        horizontalLayout.addWidget(textLabel, 1)
        newButton.setText("")
        newButton.setIconSize(QSize(0, 0))
        newButton.setLayout(horizontalLayout)

        newButton.setSizePolicy(copyButton.sizePolicy())
        newButton.setMinimumSize(copyButton.minimumSize())
        newButton.setMaximumSize(copyButton.maximumSize())
        newButton.setSizeIncrement(copyButton.sizeIncrement())
        newButton.setBaseSize(copyButton.baseSize())
        newButton.setFont(copyButton.font())
        newButton.setMouseTracking(copyButton.hasMouseTracking())
        newButton.setLayoutDirection(copyButton.layoutDirection())
        newButton.setCheckable(copyButton.isCheckable())
        newButton.setAutoDefault(copyButton.autoDefault())
        newButton.setDefault(copyButton.isDefault())
        newButton.setFlat(copyButton.isFlat())
        newButton.setObjectName(newButtonObjectName)
        copyButton.parentWidget().layout().replaceWidget(copyButton, newButton)

        copyButton.deleteLater()


class CustomMenuButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        self.setStyleSheet(F"""
        QPushButton{{
            /*outline*/
            outline: 0;
            /*outline-end*/
            /*border*/
            border: none;
            border-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
            /*border-end*/
            /*background-color*/
            background-color:rgba(50, 50, 50, 255);
            /*background-color-end*/
            /*color*/
            color: rgb(255, 255, 255);
            /*color-end*/
            /*padding*/
            padding: 10px;
            /*padding-end*/
            /*margin*/
            margin: 0px;
            /*margin-end*/
            /*margin-right*/
            margin-right: 0px;
            /*margin-right-end*/
        }}
        """)

        self.colorVal = QColor(50, 50, 50)
        self.colorAnim = QPropertyAnimation(self, b'color')
        self.colorAnim.setDuration(100)
        self.colorAnim.setStartValue(QColor(50, 50, 50))
        self.colorAnim.setEndValue(QColor(40, 40, 40))

        self.marginRightVal = 0
        self.marginRightAnim = QPropertyAnimation(self, b'marginRight')
        self.marginRightAnim.setDuration(100)
        self.marginRightAnim.setStartValue(0)
        self.marginRightAnim.setEndValue(20)

        self.borderRadiusVal = 0
        self.borderRadiusAnim = QPropertyAnimation(self, b'borderRadius')
        self.borderRadiusAnim.setDuration(100)
        self.borderRadiusAnim.setStartValue(0)
        self.borderRadiusAnim.setEndValue(20)

        self.animGroup = QParallelAnimationGroup(self)
        self.animGroup.addAnimation(self.colorAnim)
        self.animGroup.addAnimation(self.marginRightAnim)
        self.animGroup.addAnimation(self.borderRadiusAnim)

    @pyqtProperty(QColor)
    def color(self):
        return self.colorVal

    @color.setter
    def color(self, val):
        self.colorVal = val
        current = self.styleSheet()
        start = current.index('/*background-color*/')
        end = current.index('/*background-color-end*/')
        _all = current[start:end]
        new = current.replace(_all,
                              f"/*background-color*/background-color:rgba({val.red()},{val.green()},{val.blue()},{val.alpha()});")
        self.setStyleSheet(new)

    @pyqtProperty(float)
    def marginRight(self):
        return self.marginRightVal

    @marginRight.setter
    def marginRight(self, val):
        self.marginRightVal = val
        current = self.styleSheet()
        start = current.index('/*margin-right*/')
        end = current.index('/*margin-right-end*/')
        _all = current[start:end]
        new = current.replace(_all, f"/*margin-right*/margin-right:{val}px;")
        self.setStyleSheet(new)

    @pyqtProperty(float)
    def borderRadius(self):
        return self.marginRightVal

    @borderRadius.setter
    def borderRadius(self, val):
        self.borderRadiusVal = val
        current = self.styleSheet()
        start = current.index('/*border*/')
        end = current.index('/*border-end*/')
        _all = current[start:end]
        new = current.replace(_all,
                              f"/*border*/border: none;border-radius: 0px;border-top-right-radius: {val}px;border-bottom-right-radius: {val}px;")
        self.setStyleSheet(new)

    def enterEvent(self, event):
        self.animGroup.setDirection(self.animGroup.Forward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self.animGroup.setDirection(self.animGroup.Backward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event) -> None:
        self.animGroup.setDirection(self.animGroup.Backward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.mousePressEvent(self, event)


class FirstCustomMenuButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        self.setStyleSheet(F"""
        QPushButton{{
            /*outline*/
            outline: 0;
            /*outline-end*/
            /*border*/
            border: none;
            border-radius: 0px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 0px;
            /*border-end*/
            /*background-color*/
            background-color:rgba(50, 50, 50, 255);
            /*background-color-end*/
            /*color*/
            color: rgb(255, 255, 255);
            /*color-end*/
            /*padding*/
            padding: 10px;
            /*padding-end*/
            /*margin*/
            margin: 0px;
            /*margin-end*/
            /*margin-right*/
            margin-right: 0px;
            /*margin-right-end*/
        }}
        """)

        self.colorVal = QColor(50, 50, 50)
        self.colorAnim = QPropertyAnimation(self, b'color')
        self.colorAnim.setDuration(100)
        self.colorAnim.setStartValue(QColor(50, 50, 50))
        self.colorAnim.setEndValue(QColor(40, 40, 40))

        self.marginRightVal = 0
        self.marginRightAnim = QPropertyAnimation(self, b'marginRight')
        self.marginRightAnim.setDuration(100)
        self.marginRightAnim.setStartValue(0)
        self.marginRightAnim.setEndValue(20)

        self.borderRadiusVal = 0
        self.borderRadiusAnim = QPropertyAnimation(self, b'borderRadius')
        self.borderRadiusAnim.setDuration(100)
        self.borderRadiusAnim.setStartValue(0)
        self.borderRadiusAnim.setEndValue(20)

        self.animGroup = QParallelAnimationGroup(self)
        self.animGroup.addAnimation(self.colorAnim)
        self.animGroup.addAnimation(self.marginRightAnim)
        self.animGroup.addAnimation(self.borderRadiusAnim)

    @pyqtProperty(QColor)
    def color(self):
        return self.colorVal

    @color.setter
    def color(self, val):
        self.colorVal = val
        current = self.styleSheet()
        start = current.index('/*background-color*/')
        end = current.index('/*background-color-end*/')
        _all = current[start:end]
        new = current.replace(_all,
                              f"/*background-color*/background-color:rgba({val.red()},{val.green()},{val.blue()},{val.alpha()});")
        self.setStyleSheet(new)

    @pyqtProperty(float)
    def marginRight(self):
        return self.marginRightVal

    @marginRight.setter
    def marginRight(self, val):
        self.marginRightVal = val
        current = self.styleSheet()
        start = current.index('/*margin-right*/')
        end = current.index('/*margin-right-end*/')
        _all = current[start:end]
        new = current.replace(_all, f"/*margin-right*/margin-right:{val}px;")
        self.setStyleSheet(new)

    @pyqtProperty(float)
    def borderRadius(self):
        return self.marginRightVal

    @borderRadius.setter
    def borderRadius(self, val):
        self.borderRadiusVal = val
        current = self.styleSheet()
        start = current.index('/*border*/')
        end = current.index('/*border-end*/')
        _all = current[start:end]
        new = current.replace(_all,
                              F"""/*border*/
                                    border: none;
                                    border-radius: 0px;
                                    border-top-left-radius: 20px;
                                    border-top-right-radius: 20px;
                                    border-bottom-right-radius: {val}px;
                                    """)
        self.setStyleSheet(new)

    def enterEvent(self, event):
        self.animGroup.setDirection(self.animGroup.Forward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self.animGroup.setDirection(self.animGroup.Backward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event) -> None:
        self.animGroup.setDirection(self.animGroup.Backward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.mousePressEvent(self, event)


class LastCustomMenuButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        self.setStyleSheet(F"""
        QPushButton{{
            /*outline*/
            outline: 0;
            /*outline-end*/
            /*border*/
            border: none;
            border-radius: 0px;
            border-top-left-radius: 0px;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 0px;
            /*border-end*/
            /*background-color*/
            background-color:rgba(50, 50, 50, 255);
            /*background-color-end*/
            /*color*/
            color: rgb(255, 255, 255);
            /*color-end*/
            /*padding*/
            padding: 10px;
            /*padding-end*/
            /*margin*/
            margin: 0px;
            /*margin-end*/
            /*margin-right*/
            margin-right: 0px;
            /*margin-right-end*/
        }}
        """)

        self.colorVal = QColor(50, 50, 50)
        self.colorAnim = QPropertyAnimation(self, b'color')
        self.colorAnim.setDuration(100)
        self.colorAnim.setStartValue(QColor(50, 50, 50))
        self.colorAnim.setEndValue(QColor(40, 40, 40))

        self.marginRightVal = 0
        self.marginRightAnim = QPropertyAnimation(self, b'marginRight')
        self.marginRightAnim.setDuration(100)
        self.marginRightAnim.setStartValue(0)
        self.marginRightAnim.setEndValue(20)

        self.borderRadiusVal = 0
        self.borderRadiusAnim = QPropertyAnimation(self, b'borderRadius')
        self.borderRadiusAnim.setDuration(100)
        self.borderRadiusAnim.setStartValue(0)
        self.borderRadiusAnim.setEndValue(20)

        self.animGroup = QParallelAnimationGroup(self)
        self.animGroup.addAnimation(self.colorAnim)
        self.animGroup.addAnimation(self.marginRightAnim)
        self.animGroup.addAnimation(self.borderRadiusAnim)

    @pyqtProperty(QColor)
    def color(self):
        return self.colorVal

    @color.setter
    def color(self, val):
        self.colorVal = val
        current = self.styleSheet()
        start = current.index('/*background-color*/')
        end = current.index('/*background-color-end*/')
        _all = current[start:end]
        new = current.replace(_all,
                              f"/*background-color*/background-color:rgba({val.red()},{val.green()},{val.blue()},{val.alpha()});")
        self.setStyleSheet(new)

    @pyqtProperty(float)
    def marginRight(self):
        return self.marginRightVal

    @marginRight.setter
    def marginRight(self, val):
        self.marginRightVal = val
        current = self.styleSheet()
        start = current.index('/*margin-right*/')
        end = current.index('/*margin-right-end*/')
        _all = current[start:end]
        new = current.replace(_all, f"/*margin-right*/margin-right:{val}px;")
        self.setStyleSheet(new)

    @pyqtProperty(float)
    def borderRadius(self):
        return self.marginRightVal

    @borderRadius.setter
    def borderRadius(self, val):
        self.borderRadiusVal = val
        current = self.styleSheet()
        start = current.index('/*border*/')
        end = current.index('/*border-end*/')
        _all = current[start:end]
        new = current.replace(_all,
                              F"""/*border*/
                                    border: none;
                                    border-radius: 0px;
                                    border-top-left-radius: 0px;
                                    border-top-right-radius: 20px;
                                    border-bottom-right-radius: {val}px;
                                    """)
        self.setStyleSheet(new)

    def enterEvent(self, event):
        self.animGroup.setDirection(self.animGroup.Forward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self.animGroup.setDirection(self.animGroup.Backward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event) -> None:
        self.animGroup.setDirection(self.animGroup.Backward)
        if self.animGroup.state() == self.animGroup.State.Stopped:
            self.animGroup.start()
        QPushButton.mousePressEvent(self, event)


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)

        self.database = Database(
            'mongodb+srv://myappuser:mXksi132@cluster0.xxtjtei.mongodb.net/?retryWrites=true&w=majority',
            'myappdatabase')

        self.home_pushButton = FirstCustomMenuButton(self.temp_home_pushButton.parentWidget())
        CustomWidgets.copyButtonProperties('home_pushButton', self.home_pushButton,
                                           self.temp_home_pushButton)

        self.stats_pushButton = CustomMenuButton(self.temp_stats_pushButton.parentWidget())
        CustomWidgets.copyButtonProperties('stats_pushButton', self.stats_pushButton,
                                           self.temp_stats_pushButton)

        self.schedule_pushButton = CustomMenuButton(self.temp_schedule_pushButton.parentWidget())
        CustomWidgets.copyButtonProperties('schedule_pushButton', self.schedule_pushButton,
                                           self.temp_schedule_pushButton)

        self.menuSignOut_pushButton = LastCustomMenuButton(self.temp_menuSignOut_pushButton.parentWidget())
        CustomWidgets.copyButtonProperties('menuSignOut_pushButton', self.menuSignOut_pushButton,
                                           self.temp_menuSignOut_pushButton)

        self.openSignUpPage_pushButton.clicked.connect(lambda: self.switchSignInUpPanel(1))
        self.openSignInPage_pushButton.clicked.connect(lambda: self.switchSignInUpPanel(0))

        self.signIn_pushButton.clicked.connect(self.login)

    def switchSignInUpPanel(self, index: int):
        self.signInUp_stackedWidget.setCurrentIndex(index)

    def login(self):
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        result = self.database.query_one('users', {'username': username})
        if len(result) > 0:
            result_hashed_password = result[0].get('password')
            if Helper.Passwords.verify_password(password, result_hashed_password):
                print('Login succeeded!')
                self.openMainPanel()
            else:
                print('Wrong password!')
        else:
            print(f'No user with username: {username}')

    def openMainPanel(self):
        self.stackedWidget.setCurrentIndex(1)


def main():
    app = QApplication(sys.argv)
    appui = App()
    appui.show()
    app.exec()


if __name__ == '__main__':
    main()
