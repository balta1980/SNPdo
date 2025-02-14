# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sal_lote.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(376, 297)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.groupBox)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(264, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.fecha = QtWidgets.QDateEdit(self.frame_2)
        self.fecha.setObjectName("fecha")
        self.horizontalLayout_2.addWidget(self.fecha)
        self.verticalLayout.addWidget(self.frame_2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.aumento_porc = QtWidgets.QRadioButton(self.groupBox)
        self.aumento_porc.setObjectName("aumento_porc")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.aumento_porc)
        self.aumento_abs = QtWidgets.QRadioButton(self.groupBox)
        self.aumento_abs.setObjectName("aumento_abs")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.aumento_abs)
        self.val_porcentual = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.val_porcentual.setEnabled(False)
        self.val_porcentual.setMinimum(0.0)
        self.val_porcentual.setMaximum(999.0)
        self.val_porcentual.setObjectName("val_porcentual")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.val_porcentual)
        self.valor_absoluto = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.valor_absoluto.setEnabled(False)
        self.valor_absoluto.setMaximum(99999999.99)
        self.valor_absoluto.setObjectName("valor_absoluto")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.valor_absoluto)
        self.verticalLayout.addLayout(self.formLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.nota = QtWidgets.QLineEdit(self.groupBox)
        self.nota.setObjectName("nota")
        self.verticalLayout.addWidget(self.nota)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.exportar = QtWidgets.QPushButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("iconos/excel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportar.setIcon(icon)
        self.exportar.setObjectName("exportar")
        self.horizontalLayout.addWidget(self.exportar)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.aceptar = QtWidgets.QPushButton(self.frame)
        self.aceptar.setObjectName("aceptar")
        self.horizontalLayout.addWidget(self.aceptar)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.cancelar = QtWidgets.QPushButton(self.frame)
        self.cancelar.setObjectName("cancelar")
        self.horizontalLayout.addWidget(self.cancelar)
        self.verticalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.aumento_porc.clicked['bool'].connect(self.val_porcentual.setEnabled)
        self.aumento_porc.clicked['bool'].connect(self.valor_absoluto.setDisabled)
        self.aumento_abs.clicked['bool'].connect(self.val_porcentual.setDisabled)
        self.aumento_abs.clicked['bool'].connect(self.valor_absoluto.setEnabled)
        self.aumento_abs.clicked['bool'].connect(self.val_porcentual.clear)
        self.aumento_porc.clicked['bool'].connect(self.valor_absoluto.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aumento de salario por lote"))
        self.groupBox.setTitle(_translate("MainWindow", "Aumento Salarial por lote:"))
        self.fecha.setDisplayFormat(_translate("MainWindow", "dd-MM-yyyy"))
        self.aumento_porc.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al seleccionar aumento porcentual todos los trabajadores serán afectados por el mismo factor de aumento.</p></body></html>"))
        self.aumento_porc.setText(_translate("MainWindow", "Aumento porcentual"))
        self.aumento_abs.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al seleccionar aumento absoluto todos los trabajadores recibirán un aumento de una catidad especifica de dinero.</p></body></html>"))
        self.aumento_abs.setText(_translate("MainWindow", "Aumento absoluto"))
        self.tableWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p>Listado de trabajadores activos suceptibles de aumento. No se toman en cuenta trabajadores suspendidos por alguna razón.</p></body></html>"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nombre de trabajador"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Salario Actual"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Nuevo salario"))
        self.label.setText(_translate("MainWindow", "Nota:"))
        self.nota.setToolTip(_translate("MainWindow", "<html><head/><body><p>Coloque una nota relativa al aumento por lote. Es obligatorio para poder realizar el aumento por lote.</p></body></html>"))
        self.exportar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Exporta el listado de trabajadores activos con sus respectivos salarios a una hoja de MS Excel.</p></body></html>"))
        self.exportar.setText(_translate("MainWindow", "Exportar"))
        self.aceptar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al presionar se procesará el aumento por lote</p></body></html>"))
        self.aceptar.setText(_translate("MainWindow", "Aceptar"))
        self.cancelar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Al presionar se cerrará la ventana.</p></body></html>"))
        self.cancelar.setText(_translate("MainWindow", "Cancelar"))


