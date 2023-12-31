# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mywiget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1000, 600))
        Form.setMaximumSize(QtCore.QSize(1000, 600))
        self.cv_label = QtWidgets.QLabel(Form)
        self.cv_label.setGeometry(QtCore.QRect(10, 10, 781, 581))
        self.cv_label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.cv_label.setStyleSheet("border: 1px solid black;")
        self.cv_label.setLineWidth(6)
        self.cv_label.setMidLineWidth(0)
        self.cv_label.setObjectName("cv_label")
        self.msg_browser = QtWidgets.QTextBrowser(Form)
        self.msg_browser.setGeometry(QtCore.QRect(800, 10, 191, 331))
        self.msg_browser.setObjectName("msg_browser")
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.setGeometry(QtCore.QRect(800, 400, 191, 41))
        self.save_btn.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.save_btn.setObjectName("save_btn")
        self.begin_btn = QtWidgets.QPushButton(Form)
        self.begin_btn.setGeometry(QtCore.QRect(800, 450, 191, 41))
        self.begin_btn.setObjectName("begin_btn")
        self.pause_btn = QtWidgets.QPushButton(Form)
        self.pause_btn.setGeometry(QtCore.QRect(800, 500, 191, 41))
        self.pause_btn.setObjectName("pause_btn")
        self.exit_btn = QtWidgets.QPushButton(Form)
        self.exit_btn.setGeometry(QtCore.QRect(800, 550, 191, 41))
        self.exit_btn.setObjectName("exit_btn")
        self.select_box = QtWidgets.QComboBox(Form)
        self.select_box.setGeometry(QtCore.QRect(800, 350, 191, 41))
        self.select_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.select_box.setObjectName("select_box")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Demo"))
        self.cv_label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">摄像头</span></p></body></html>"))
        self.save_btn.setText(_translate("Form", "图片保存路径"))
        self.begin_btn.setText(_translate("Form", "开始"))
        self.pause_btn.setText(_translate("Form", "暂停"))
        self.exit_btn.setText(_translate("Form", "退出"))
