# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repos\ModOrganizer-Plugins\src\plugin\reinstaller\ui\reinstaller_installers.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_reinstallerInstallers(object):
    def setupUi(self, reinstallerInstallers):
        reinstallerInstallers.setObjectName("reinstallerInstallers")
        reinstallerInstallers.resize(541, 336)
        reinstallerInstallers.setMinimumSize(QtCore.QSize(541, 336))
        self.verticalLayout = QtWidgets.QVBoxLayout(reinstallerInstallers)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(reinstallerInstallers)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtName = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtName.sizePolicy().hasHeightForWidth())
        self.txtName.setSizePolicy(sizePolicy)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout.addWidget(self.txtName)
        self.ddlDownloads = QtWidgets.QComboBox(self.widget)
        self.ddlDownloads.setObjectName("ddlDownloads")
        self.horizontalLayout.addWidget(self.ddlDownloads)
        self.btnAdd = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.verticalLayout.addWidget(self.widget)
        self.widget_3 = QtWidgets.QWidget(reinstallerInstallers)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lstInstallers = QtWidgets.QListWidget(self.widget_3)
        self.lstInstallers.setObjectName("lstInstallers")
        self.verticalLayout_2.addWidget(self.lstInstallers)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_2 = QtWidgets.QWidget(reinstallerInstallers)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ddlInstaller = QtWidgets.QComboBox(self.widget_2)
        self.ddlInstaller.setObjectName("ddlInstaller")
        self.horizontalLayout_2.addWidget(self.ddlInstaller)
        self.btnInstall = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnInstall.sizePolicy().hasHeightForWidth())
        self.btnInstall.setSizePolicy(sizePolicy)
        self.btnInstall.setObjectName("btnInstall")
        self.horizontalLayout_2.addWidget(self.btnInstall)
        self.btnDelete = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDelete.sizePolicy().hasHeightForWidth())
        self.btnDelete.setSizePolicy(sizePolicy)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(reinstallerInstallers)
        QtCore.QMetaObject.connectSlotsByName(reinstallerInstallers)

    def retranslateUi(self, reinstallerInstallers):
        _translate = QtCore.QCoreApplication.translate
        reinstallerInstallers.setWindowTitle(_translate("reinstallerInstallers", "Form"))
        self.btnAdd.setText(_translate("reinstallerInstallers", "Add"))
        self.btnInstall.setText(_translate("reinstallerInstallers", "Install"))
        self.btnDelete.setText(_translate("reinstallerInstallers", "Delete"))