# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repos\ModOrganizer-Plugins\src\plugin\pluginfinder\ui\pluginfinder_list.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_listTabWidget(object):
    def setupUi(self, listTabWidget):
        listTabWidget.setObjectName("listTabWidget")
        listTabWidget.resize(688, 684)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(listTabWidget.sizePolicy().hasHeightForWidth())
        listTabWidget.setSizePolicy(sizePolicy)
        listTabWidget.setMinimumSize(QtCore.QSize(0, 680))
        self.verticalLayout = QtWidgets.QVBoxLayout(listTabWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(listTabWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchLabel = QtWidgets.QLabel(self.widget)
        self.searchLabel.setObjectName("searchLabel")
        self.horizontalLayout.addWidget(self.searchLabel)
        self.searchText = QtWidgets.QLineEdit(self.widget)
        self.searchText.setObjectName("searchText")
        self.horizontalLayout.addWidget(self.searchText)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(listTabWidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.installedCheck = QtWidgets.QCheckBox(self.widget_2)
        self.installedCheck.setObjectName("installedCheck")
        self.horizontalLayout_2.addWidget(self.installedCheck)
        self.updateCheck = QtWidgets.QCheckBox(self.widget_2)
        self.updateCheck.setObjectName("updateCheck")
        self.horizontalLayout_2.addWidget(self.updateCheck)
        self.supportedCheck = QtWidgets.QCheckBox(self.widget_2)
        self.supportedCheck.setObjectName("supportedCheck")
        self.horizontalLayout_2.addWidget(self.supportedCheck)
        self.workingCheck = QtWidgets.QCheckBox(self.widget_2)
        self.workingCheck.setObjectName("workingCheck")
        self.horizontalLayout_2.addWidget(self.workingCheck)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(listTabWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_3)
        self.scrollArea.setMinimumSize(QtCore.QSize(670, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 651, 583))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pluginListItems = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginListItems.sizePolicy().hasHeightForWidth())
        self.pluginListItems.setSizePolicy(sizePolicy)
        self.pluginListItems.setMinimumSize(QtCore.QSize(0, 0))
        self.pluginListItems.setObjectName("pluginListItems")
        self.pluginListLayout = QtWidgets.QVBoxLayout(self.pluginListItems)
        self.pluginListLayout.setContentsMargins(0, 0, 0, 0)
        self.pluginListLayout.setSpacing(0)
        self.pluginListLayout.setObjectName("pluginListLayout")
        self.verticalLayout_3.addWidget(self.pluginListItems)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(listTabWidget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.refreshButton = QtWidgets.QPushButton(self.widget_4)
        self.refreshButton.setText("")
        self.refreshButton.setFlat(True)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_3.addWidget(self.refreshButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.widget_4)

        self.retranslateUi(listTabWidget)
        QtCore.QMetaObject.connectSlotsByName(listTabWidget)

    def retranslateUi(self, listTabWidget):
        _translate = QtCore.QCoreApplication.translate
        listTabWidget.setWindowTitle(_translate("listTabWidget", "Form"))
        self.searchLabel.setText(_translate("listTabWidget", "Search"))
        self.installedCheck.setText(_translate("listTabWidget", "Installed"))
        self.updateCheck.setText(_translate("listTabWidget", "Update"))
        self.supportedCheck.setText(_translate("listTabWidget", "Supported"))
        self.workingCheck.setText(_translate("listTabWidget", "Working"))