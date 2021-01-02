import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUi
import psycopg2

from PasswordManager import memorizeAccount, loadMemorizedAccount, storedDataExists, removeDataFile
from userAccount import userAccount, connectToDatabase


class LoginPage(QDialog):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi('login.ui', self)
        try:
            conn = connectToDatabase()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Can't contact remote server")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            sys.exit()
        self.dbconn = conn
        self.LogInBtn.clicked.connect(self.logIn)
        self.CreateAccountBtn.clicked.connect(self.createAccount)
        self.loadExistingAccount()

    def logIn(self):
        login = self.Email.text().lower()
        password = self.Password.text().lower()
        account = userAccount(self.dbconn)
        account.LogIn(login, password)
        if not account.isLoginSuccessfull():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText("Invalid Password or Email")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif (self.RemeberMeFlag.isChecked()):
            memorizeAccount(login, password)

    def createAccount(self):
        self.close()
        signUpPage = SignUpPage(self.dbconn)
        signUpPage.exec_()

    def loadExistingAccount(self):
        if storedDataExists():
            try:
                email, password = loadMemorizedAccount()
                self.Email.setText(email)
                self.Password.setText(password)
                print(email, password)
            except:
                removeDataFile()


class SignUpPage(QDialog):
    def __init__(self, dbconn):
        super(SignUpPage, self).__init__()
        loadUi('signUp.ui', self)
        self.dbconn = dbconn
        self.ShowPasswordFlag.stateChanged.connect(
            self.changePasswordVisibility)
        self.SignUpBtn.clicked.connect(self.signUp)

    def changePasswordVisibility(self):
        if self.ShowPasswordFlag.isChecked():
            self.Password.setEchoMode(QLineEdit.Normal)
        else:
            self.Password.setEchoMode(QLineEdit.Password)

    def signUp(self):
        login = self.Email.text().lower()
        password = self.Password.text().lower()
        account = userAccount(self.dbconn)
        try:
            if login is not None and password is not None:
                account.Create(login, password)
                print(login, password)
                if (self.RemeberMeFlag.isChecked()):
                    memorizeAccount(login, password)
        except psycopg2.errors.UniqueViolation:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("This account already exists")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Improper email or password")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wg = LoginPage()
    wg.show()
    sys.exit(app.exec_())
