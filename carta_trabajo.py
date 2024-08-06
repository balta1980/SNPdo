# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'carta_trabajo.ui'
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
        self.trabajador = QtWidgets.QComboBox(self.centralwidget)
        self.trabajador.setObjectName("trabajador")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.trabajador)
        self.dirigido = QtWidgets.QLineEdit(self.centralwidget)
        self.dirigido.setObjectName("dirigido")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dirigido)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.firmante = QtWidgets.QLineEdit(self.centralwidget)
        self.firmante.setObjectName("firmante")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.firmante)
        self.cargo_firmante = QtWidgets.QLineEdit(self.centralwidget)
        self.cargo_firmante.setObjectName("cargo_firmante")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cargo_firmante)
        self.telf_firmante = QtWidgets.QLineEdit(self.centralwidget)
        self.telf_firmante.setObjectName("telf_firmante")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.telf_firmante)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Generador de carta de trabajo"))
        self.label.setText(_translate("MainWindow", "Trabajador:"))
        self.label_3.setText(_translate("MainWindow", "Dirigido a:"))
        self.trabajador.setToolTip(_translate("MainWindow", "<html><head/><body><p>Seleccione el trabajador(a) al que desea otorgar la carta de trabajo</p></body></html>"))
        self.dirigido.setToolTip(_translate("MainWindow", "<html><head/><body><p>Coloque el nombre de la entidad al que va dirigido la carta de trabajo. Campo obligatorio.</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Firmante:"))
        self.label_4.setText(_translate("MainWindow", "Cargo firmante:"))
        self.label_5.setText(_translate("MainWindow", "Teléfono:"))
        self.firmante.setToolTip(_translate("MainWindow", "<html><head/><body><p>Nombre de la persona que firma la carta de trabajo. Campo obligatorio.</p></body></html>"))
        self.cargo_firmante.setToolTip(_translate("MainWindow", "<html><head/><body><p>Cargo de la persona que firma la carta de trabajo. Campo obligatorio.</p></body></html>"))
        self.telf_firmante.setToolTip(_translate("MainWindow", "<html><head/><body><p>Teléfono de la persona que firma la carta de trabajo. Campo obligatorio.</p></body></html>"))
        self.generar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al presionar este botón se generará la carta. Sólo se activa cuando se llena el campo &quot;dirigido a&quot;.</p></body></html>"))
        self.generar.setText(_translate("MainWindow", "Generar"))
        self.cancelar.setText(_translate("MainWindow", "Cancelar"))
