# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'islr.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_islr(object):
    def setupUi(self, islr):
        islr.setObjectName("islr")
        islr.setWindowModality(QtCore.Qt.WindowModal)
        islr.resize(348, 298)
        self.centralwidget = QtWidgets.QWidget(islr)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tasa3 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.tasa3.setMaximum(99.99)
        self.tasa3.setObjectName("tasa3")
        self.gridLayout.addWidget(self.tasa3, 3, 2, 1, 1)
        self.tasa2 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.tasa2.setMaximum(99.99)
        self.tasa2.setObjectName("tasa2")
        self.gridLayout.addWidget(self.tasa2, 3, 1, 1, 1)
        self.rango1 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.rango1.setMaximum(999999999999.99)
        self.rango1.setObjectName("rango1")
        self.gridLayout.addWidget(self.rango1, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.tasa1 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.tasa1.setMaximum(99.99)
        self.tasa1.setObjectName("tasa1")
        self.gridLayout.addWidget(self.tasa1, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.rango2 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.rango2.setMaximum(999999999999.99)
        self.rango2.setObjectName("rango2")
        self.gridLayout.addWidget(self.rango2, 1, 1, 1, 1)
        self.rango3 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.rango3.setMaximum(999999999999.99)
        self.rango3.setObjectName("rango3")
        self.gridLayout.addWidget(self.rango3, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.valor1 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.valor1.setMaximum(999999999999.99)
        self.valor1.setObjectName("valor1")
        self.gridLayout.addWidget(self.valor1, 5, 0, 1, 1)
        self.valor2 = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.valor2.setMaximum(999999999999.99)
        self.valor2.setObjectName("valor2")
        self.gridLayout.addWidget(self.valor2, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.nota = QtWidgets.QTextEdit(self.groupBox)
        self.nota.setObjectName("nota")
        self.verticalLayout.addWidget(self.nota)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(63, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.actualizar = QtWidgets.QPushButton(self.frame)
        self.actualizar.setObjectName("actualizar")
        self.horizontalLayout.addWidget(self.actualizar)
        spacerItem1 = QtWidgets.QSpacerItem(62, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancelar = QtWidgets.QPushButton(self.frame)
        self.cancelar.setObjectName("cancelar")
        self.horizontalLayout.addWidget(self.cancelar)
        spacerItem2 = QtWidgets.QSpacerItem(63, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addWidget(self.frame)
        islr.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(islr)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 348, 18))
        self.menubar.setObjectName("menubar")
        islr.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(islr)
        self.statusbar.setObjectName("statusbar")
        islr.setStatusBar(self.statusbar)

        self.retranslateUi(islr)
        QtCore.QMetaObject.connectSlotsByName(islr)
        islr.setTabOrder(self.rango1, self.rango2)
        islr.setTabOrder(self.rango2, self.rango3)
        islr.setTabOrder(self.rango3, self.tasa1)
        islr.setTabOrder(self.tasa1, self.tasa2)
        islr.setTabOrder(self.tasa2, self.tasa3)
        islr.setTabOrder(self.tasa3, self.valor1)
        islr.setTabOrder(self.valor1, self.valor2)
        islr.setTabOrder(self.valor2, self.nota)
        islr.setTabOrder(self.nota, self.actualizar)
        islr.setTabOrder(self.actualizar, self.cancelar)

    def retranslateUi(self, islr):
        _translate = QtCore.QCoreApplication.translate
        islr.setWindowTitle(_translate("islr", "Tabla retención impuesto sobre la renta"))
        self.groupBox.setToolTip(_translate("islr", "<html><head/><body><p>Tabla de impuesto sobre la renta, se debe actualizar anualmente para poder procesar correctamente las nóminas quincenales. Esta información se usa para poder hacer retenciones de ISLR a los trabajadores cuando así se amerite.</p></body></html>"))
        self.groupBox.setTitle(_translate("islr", "Tabla de retención de ISLR:"))
        self.tasa3.setSuffix(_translate("islr", "%"))
        self.tasa2.setSuffix(_translate("islr", "%"))
        self.rango1.setSuffix(_translate("islr", "DOP"))
        self.label_3.setText(_translate("islr", "Rango 3"))
        self.label_6.setText(_translate("islr", "Tasa 3"))
        self.label_2.setText(_translate("islr", "Rango 2"))
        self.tasa1.setSuffix(_translate("islr", "%"))
        self.label_4.setText(_translate("islr", "Tasa 1"))
        self.label_5.setText(_translate("islr", "Tasa 2"))
        self.rango2.setSuffix(_translate("islr", "DOP"))
        self.rango3.setSuffix(_translate("islr", "DOP"))
        self.label.setText(_translate("islr", "Rango 1"))
        self.label_8.setText(_translate("islr", "Valor 2"))
        self.label_7.setText(_translate("islr", "Valor 1"))
        self.valor1.setSuffix(_translate("islr", "DOP"))
        self.valor2.setSuffix(_translate("islr", "DOP"))
        self.label_9.setText(_translate("islr", "Nota:"))
        self.nota.setToolTip(_translate("islr", "<html><head/><body><p>Agregar información del ISLR</p></body></html>"))
        self.actualizar.setToolTip(_translate("islr", "<html><head/><body><p>Al presionar este botón se alctualiza la información suministrada en l abase de datos.</p></body></html>"))
        self.actualizar.setText(_translate("islr", "Actualizar"))
        self.cancelar.setToolTip(_translate("islr", "<html><head/><body><p>Cierra la ventana y se pierden las modicifaciones.</p></body></html>"))
        self.cancelar.setText(_translate("islr", "Cancelar"))
