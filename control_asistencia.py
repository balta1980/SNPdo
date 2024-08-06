# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control_asistencia.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(262, 158)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.ano_select = QtWidgets.QDateEdit(self.centralwidget)
        self.ano_select.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.ano_select.setObjectName("ano_select")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ano_select)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.mes_select = QtWidgets.QDateEdit(self.centralwidget)
        self.mes_select.setObjectName("mes_select")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.mes_select)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.nota = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.nota.setObjectName("nota")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.nota)
        self.verticalLayout.addLayout(self.formLayout)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(33, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.generar = QtWidgets.QPushButton(self.frame)
        self.generar.setObjectName("generar")
        self.horizontalLayout.addWidget(self.generar)
        spacerItem1 = QtWidgets.QSpacerItem(33, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancelar = QtWidgets.QPushButton(self.frame)
        self.cancelar.setObjectName("cancelar")
        self.horizontalLayout.addWidget(self.cancelar)
        spacerItem2 = QtWidgets.QSpacerItem(33, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Formato de asistencia"))
        self.label.setText(_translate("MainWindow", "Seleccione año:"))
        self.ano_select.setDisplayFormat(_translate("MainWindow", "yyyy"))
        self.label_2.setText(_translate("MainWindow", "Seleccione mes:"))
        self.mes_select.setDisplayFormat(_translate("MainWindow", "MM"))
        self.label_3.setText(_translate("MainWindow", "Nota:"))
        self.generar.setText(_translate("MainWindow", "Generar"))
        self.cancelar.setText(_translate("MainWindow", "Cancelar"))
