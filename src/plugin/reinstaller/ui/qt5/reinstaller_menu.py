# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repos\ModOrganizer-Plugins\src\plugin\reinstaller\ui\reinstaller_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_reinstallerMenu(object):
    def setupUi(self, reinstallerMenu):
        reinstallerMenu.setObjectName("reinstallerMenu")
        reinstallerMenu.resize(530, 228)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(reinstallerMenu)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.contentSplitter = QtWidgets.QSplitter(reinstallerMenu)
        self.contentSplitter.setOrientation(QtCore.Qt.Vertical)
        self.contentSplitter.setObjectName("contentSplitter")
        self.tabList = QtWidgets.QTabWidget(self.contentSplitter)
        self.tabList.setObjectName("tabList")
        self.installersTab = QtWidgets.QWidget()
        self.installersTab.setObjectName("installersTab")
        self.tabList.addTab(self.installersTab, "")
        self.updateTab = QtWidgets.QWidget()
        self.updateTab.setObjectName("updateTab")
        self.tabList.addTab(self.updateTab, "")
        self.helpTab = QtWidgets.QWidget()
        self.helpTab.setObjectName("helpTab")
        self.tabList.addTab(self.helpTab, "")
        self.verticalLayout_2.addWidget(self.contentSplitter)

        self.retranslateUi(reinstallerMenu)
        self.tabList.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(reinstallerMenu)

    def retranslateUi(self, reinstallerMenu):
        _translate = QtCore.QCoreApplication.translate
        reinstallerMenu.setWindowTitle(_translate("reinstallerMenu", "Form"))
        self.tabList.setTabText(self.tabList.indexOf(self.installersTab), _translate("reinstallerMenu", "Installers"))
        self.tabList.setTabText(self.tabList.indexOf(self.updateTab), _translate("reinstallerMenu", "Update"))
        self.tabList.setTabText(self.tabList.indexOf(self.helpTab), _translate("reinstallerMenu", "Help"))
