# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resumen_recibos.ui'
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
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.nota = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.nota.setObjectName("nota")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.nota)
        self.periodo = QtWidgets.QComboBox(self.centralwidget)
        self.periodo.setObjectName("periodo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.periodo)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Resumen de recibos"))
        self.label.setText(_translate("MainWindow", "Seleccione periodo:"))
        self.label_3.setText(_translate("MainWindow", "Nota:"))
        self.nota.setToolTip(_translate("MainWindow", "<html><head/><body><p>Agregue una nota al informe.</p></body></html>"))
        self.periodo.setToolTip(_translate("MainWindow", "<html><head/><body><p>En este listado sólo se muestra los segundos periodos de cada mes. La suma resumen de los recibos es un informe mensual. La información de este informe es válida solamente a partir de la de la segunda quincena de abril de 2020. 2Q042020</p></body></html>"))
        self.generar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al presionar este botón se generará el informe.</p></body></html>"))
        self.generar.setText(_translate("MainWindow", "Generar"))
        self.cancelar.setText(_translate("MainWindow", "Cancelar"))
