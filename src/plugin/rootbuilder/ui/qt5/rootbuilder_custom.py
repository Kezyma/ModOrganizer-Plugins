# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repos\ModOrganizer-Plugins\src\plugin\rootbuilder\ui\rootbuilder_custom.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_customTabWidget(object):
    def setupUi(self, customTabWidget):
        customTabWidget.setObjectName("customTabWidget")
        customTabWidget.resize(580, 300)
        customTabWidget.setMinimumSize(QtCore.QSize(580, 300))
        self.horizontalLayout = QtWidgets.QHBoxLayout(customTabWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.copyModeWidget = QtWidgets.QWidget(customTabWidget)
        self.copyModeWidget.setObjectName("copyModeWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.copyModeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.copyModeTitle = QtWidgets.QLabel(self.copyModeWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.copyModeTitle.setFont(font)
        self.copyModeTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.copyModeTitle.setObjectName("copyModeTitle")
        self.verticalLayout.addWidget(self.copyModeTitle)
        self.copyModeDesc = QtWidgets.QLabel(self.copyModeWidget)
        self.copyModeDesc.setWordWrap(True)
        self.copyModeDesc.setObjectName("copyModeDesc")
        self.verticalLayout.addWidget(self.copyModeDesc)
        self.copyModePriorityWidget = QtWidgets.QWidget(self.copyModeWidget)
        self.copyModePriorityWidget.setObjectName("copyModePriorityWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.copyModePriorityWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.copyModePriorityLabel = QtWidgets.QLabel(self.copyModePriorityWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.copyModePriorityLabel.setFont(font)
        self.copyModePriorityLabel.setObjectName("copyModePriorityLabel")
        self.horizontalLayout_2.addWidget(self.copyModePriorityLabel)
        self.copyModePrioritySpin = QtWidgets.QSpinBox(self.copyModePriorityWidget)
        self.copyModePrioritySpin.setMaximumSize(QtCore.QSize(32, 16777215))
        self.copyModePrioritySpin.setWrapping(False)
        self.copyModePrioritySpin.setMinimum(1)
        self.copyModePrioritySpin.setMaximum(3)
        self.copyModePrioritySpin.setObjectName("copyModePrioritySpin")
        self.horizontalLayout_2.addWidget(self.copyModePrioritySpin)
        self.verticalLayout.addWidget(self.copyModePriorityWidget)
        self.copyModeTable = QtWidgets.QTableWidget(self.copyModeWidget)
        self.copyModeTable.setShowGrid(True)
        self.copyModeTable.setGridStyle(QtCore.Qt.SolidLine)
        self.copyModeTable.setCornerButtonEnabled(True)
        self.copyModeTable.setRowCount(10)
        self.copyModeTable.setColumnCount(1)
        self.copyModeTable.setObjectName("copyModeTable")
        self.copyModeTable.horizontalHeader().setVisible(False)
        self.copyModeTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.copyModeTable)
        self.horizontalLayout.addWidget(self.copyModeWidget)
        self.linkModeWidget = QtWidgets.QWidget(customTabWidget)
        self.linkModeWidget.setObjectName("linkModeWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.linkModeWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.linkModeTitle = QtWidgets.QLabel(self.linkModeWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.linkModeTitle.setFont(font)
        self.linkModeTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.linkModeTitle.setObjectName("linkModeTitle")
        self.verticalLayout_2.addWidget(self.linkModeTitle)
        self.linkModeDesc = QtWidgets.QLabel(self.linkModeWidget)
        self.linkModeDesc.setWordWrap(True)
        self.linkModeDesc.setObjectName("linkModeDesc")
        self.verticalLayout_2.addWidget(self.linkModeDesc)
        self.linkModePriorityWidget = QtWidgets.QWidget(self.linkModeWidget)
        self.linkModePriorityWidget.setObjectName("linkModePriorityWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.linkModePriorityWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.linkModePriorityLabel = QtWidgets.QLabel(self.linkModePriorityWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.linkModePriorityLabel.setFont(font)
        self.linkModePriorityLabel.setObjectName("linkModePriorityLabel")
        self.horizontalLayout_3.addWidget(self.linkModePriorityLabel)
        self.linkModePrioritySpin = QtWidgets.QSpinBox(self.linkModePriorityWidget)
        self.linkModePrioritySpin.setMaximumSize(QtCore.QSize(32, 16777215))
        self.linkModePrioritySpin.setWrapping(False)
        self.linkModePrioritySpin.setMinimum(1)
        self.linkModePrioritySpin.setMaximum(3)
        self.linkModePrioritySpin.setProperty("value", 2)
        self.linkModePrioritySpin.setObjectName("linkModePrioritySpin")
        self.horizontalLayout_3.addWidget(self.linkModePrioritySpin)
        self.verticalLayout_2.addWidget(self.linkModePriorityWidget)
        self.linkModeTable = QtWidgets.QTableWidget(self.linkModeWidget)
        self.linkModeTable.setShowGrid(True)
        self.linkModeTable.setGridStyle(QtCore.Qt.SolidLine)
        self.linkModeTable.setCornerButtonEnabled(True)
        self.linkModeTable.setRowCount(10)
        self.linkModeTable.setColumnCount(1)
        self.linkModeTable.setObjectName("linkModeTable")
        self.linkModeTable.horizontalHeader().setVisible(False)
        self.linkModeTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.linkModeTable)
        self.horizontalLayout.addWidget(self.linkModeWidget)
        self.usvfsModeWidget = QtWidgets.QWidget(customTabWidget)
        self.usvfsModeWidget.setObjectName("usvfsModeWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.usvfsModeWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.usvfsModeTitle = QtWidgets.QLabel(self.usvfsModeWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.usvfsModeTitle.setFont(font)
        self.usvfsModeTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.usvfsModeTitle.setObjectName("usvfsModeTitle")
        self.verticalLayout_3.addWidget(self.usvfsModeTitle)
        self.usvfsModeDesc = QtWidgets.QLabel(self.usvfsModeWidget)
        self.usvfsModeDesc.setWordWrap(True)
        self.usvfsModeDesc.setObjectName("usvfsModeDesc")
        self.verticalLayout_3.addWidget(self.usvfsModeDesc)
        self.usvfsModePriorityWidget = QtWidgets.QWidget(self.usvfsModeWidget)
        self.usvfsModePriorityWidget.setObjectName("usvfsModePriorityWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.usvfsModePriorityWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.usvfsModePriorityLabel = QtWidgets.QLabel(self.usvfsModePriorityWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.usvfsModePriorityLabel.setFont(font)
        self.usvfsModePriorityLabel.setObjectName("usvfsModePriorityLabel")
        self.horizontalLayout_4.addWidget(self.usvfsModePriorityLabel)
        self.usvfsModePrioritySpin = QtWidgets.QSpinBox(self.usvfsModePriorityWidget)
        self.usvfsModePrioritySpin.setMaximumSize(QtCore.QSize(32, 16777215))
        self.usvfsModePrioritySpin.setWrapping(False)
        self.usvfsModePrioritySpin.setMinimum(1)
        self.usvfsModePrioritySpin.setMaximum(3)
        self.usvfsModePrioritySpin.setProperty("value", 3)
        self.usvfsModePrioritySpin.setObjectName("usvfsModePrioritySpin")
        self.horizontalLayout_4.addWidget(self.usvfsModePrioritySpin)
        self.verticalLayout_3.addWidget(self.usvfsModePriorityWidget)
        self.usvfsModeTable = QtWidgets.QTableWidget(self.usvfsModeWidget)
        self.usvfsModeTable.setShowGrid(True)
        self.usvfsModeTable.setGridStyle(QtCore.Qt.SolidLine)
        self.usvfsModeTable.setCornerButtonEnabled(True)
        self.usvfsModeTable.setRowCount(10)
        self.usvfsModeTable.setColumnCount(1)
        self.usvfsModeTable.setObjectName("usvfsModeTable")
        self.usvfsModeTable.horizontalHeader().setVisible(False)
        self.usvfsModeTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.usvfsModeTable)
        self.horizontalLayout.addWidget(self.usvfsModeWidget)

        self.retranslateUi(customTabWidget)
        QtCore.QMetaObject.connectSlotsByName(customTabWidget)

    def retranslateUi(self, customTabWidget):
        _translate = QtCore.QCoreApplication.translate
        customTabWidget.setWindowTitle(_translate("customTabWidget", "Form"))
        self.copyModeTitle.setText(_translate("customTabWidget", "Copy"))
        self.copyModeDesc.setText(_translate("customTabWidget", "Files matching the specified rules will be copied to the game folder during a build. During a clear, the source files will be updated with any changes and the copied files are deleted. Supports glob wildcards, and regex expressions when using the prefix r:"))
        self.copyModePriorityLabel.setText(_translate("customTabWidget", "Priority"))
        self.linkModeTitle.setText(_translate("customTabWidget", "Link"))
        self.linkModeDesc.setText(_translate("customTabWidget", "Files matching the specified rules will have links created in the game folder during build. During a clear, the source files will be updated with any changes and the links are removed. Supports glob wildcards, and regex expressions when using the prefix r:"))
        self.linkModePriorityLabel.setText(_translate("customTabWidget", "Priority"))
        self.usvfsModeTitle.setText(_translate("customTabWidget", "USVFS"))
        self.usvfsModeDesc.setText(_translate("customTabWidget", "Files matching the specified rules will be mapped to the game folder using Mod Organizer\'s VFS. This is not compatible with all mods and does not support manual build, sync or clear. Supports glob wildcards, and regex expressions when using the prefix r:"))
        self.usvfsModePriorityLabel.setText(_translate("customTabWidget", "Priority"))
