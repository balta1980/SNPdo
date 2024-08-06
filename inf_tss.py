# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inf_tss.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(288, 277)
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
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.frame_2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.novedades_periodo = QtWidgets.QCheckBox(self.groupBox)
        self.novedades_periodo.setObjectName("novedades_periodo")
        self.verticalLayout_3.addWidget(self.novedades_periodo)
        self.autodeterminacion = QtWidgets.QCheckBox(self.groupBox)
        self.autodeterminacion.setObjectName("autodeterminacion")
        self.verticalLayout_3.addWidget(self.autodeterminacion)
        self.autodetermincacion_retro = QtWidgets.QCheckBox(self.groupBox)
        self.autodetermincacion_retro.setObjectName("autodetermincacion_retro")
        self.verticalLayout_3.addWidget(self.autodetermincacion_retro)
        self.rectificativa = QtWidgets.QCheckBox(self.groupBox)
        self.rectificativa.setObjectName("rectificativa")
        self.verticalLayout_3.addWidget(self.rectificativa)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.frame_2)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Informe TSS"))
        self.label.setText(_translate("MainWindow", "Seleccione periodo:"))
        self.label_3.setText(_translate("MainWindow", "Nota:"))
        self.nota.setToolTip(_translate("MainWindow", "<html><head/><body><p>Agregue una nota al informe.</p></body></html>"))
        self.periodo.setToolTip(_translate("MainWindow", "<html><head/><body><p>En este listado sólo se muestra los segundos periodos de cada mes. El informe de la TSS es un informe mensual. La información de este informe es válida solamente a partir de la de la segunda quincena de abril de 2020. 2Q042020</p></body></html>"))
        self.groupBox.setTitle(_translate("MainWindow", "Generar archivos TXT del periodo:"))
        self.novedades_periodo.setText(_translate("MainWindow", "Novedades del Período"))
        self.autodeterminacion.setText(_translate("MainWindow", "Autodeterminación Mensual"))
        self.autodetermincacion_retro.setText(_translate("MainWindow", "Autodeterminación Retroactiva"))
        self.rectificativa.setText(_translate("MainWindow", "Rectificativa"))
        self.generar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al presionar este botón se generará el informe.</p></body></html>"))
        self.generar.setText(_translate("MainWindow", "Generar"))
        self.cancelar.setText(_translate("MainWindow", "Cancelar"))


