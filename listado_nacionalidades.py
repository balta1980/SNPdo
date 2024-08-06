# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listado_nacionalidades.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_listadodenacionalidades(object):
    def setupUi(self, listadodenacionalidades):
        listadodenacionalidades.setObjectName("listadodenacionalidades")
        listadodenacionalidades.setWindowModality(QtCore.Qt.WindowModal)
        listadodenacionalidades.resize(428, 352)
        self.centralwidget = QtWidgets.QWidget(listadodenacionalidades)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.verticalLayout.addWidget(self.tableWidget)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addLayout(self.gridLayout)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.importar = QtWidgets.QPushButton(self.frame)
        self.importar.setObjectName("importar")
        self.horizontalLayout.addWidget(self.importar)
        spacerItem1 = QtWidgets.QSpacerItem(29, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.guardar = QtWidgets.QPushButton(self.frame)
        self.guardar.setObjectName("guardar")
        self.horizontalLayout.addWidget(self.guardar)
        spacerItem2 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cancelar = QtWidgets.QPushButton(self.frame)
        self.cancelar.setObjectName("cancelar")
        self.horizontalLayout.addWidget(self.cancelar)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.frame)
        listadodenacionalidades.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(listadodenacionalidades)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 428, 18))
        self.menubar.setObjectName("menubar")
        listadodenacionalidades.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(listadodenacionalidades)
        self.statusbar.setObjectName("statusbar")
        listadodenacionalidades.setStatusBar(self.statusbar)

        self.retranslateUi(listadodenacionalidades)
        QtCore.QMetaObject.connectSlotsByName(listadodenacionalidades)

    def retranslateUi(self, listadodenacionalidades):
        _translate = QtCore.QCoreApplication.translate
        listadodenacionalidades.setWindowTitle(_translate("listadodenacionalidades", "Listado de nacionalidades"))
        self.tableWidget.setToolTip(_translate("listadodenacionalidades", "<html><head/><body><p>El listado de nacionalidades se encuentra disponible en la página de la TSS a través del sistema SUIRPLUS. Es obligatorio colocar la nacionalidad correspondiente a cada trabajador en su ficha de datos.</p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("listadodenacionalidades", "ID_Nacionalidad"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("listadodenacionalidades", "Nacionalidades"))
        self.importar.setToolTip(_translate("listadodenacionalidades", "<html><head/><body><p>Presione éste botón para importar un archivo de MS Excel 2020 .xlsx con el listado de nacionalidades. El archivo debe ser contener dos columnas, la primera con el ID y la segunda con la nacionalidad. Se recomienda descargar el archivo del sistema SUIRPLUS y luego guardar como archivo de Ms Exel 2020 .xlsx.</p></body></html>"))
        self.importar.setText(_translate("listadodenacionalidades", "Importar"))
        self.guardar.setToolTip(_translate("listadodenacionalidades", "<html><head/><body><p>Guarda todas las modificaciones en la base de datos.</p></body></html>"))
        self.guardar.setText(_translate("listadodenacionalidades", "Guardar"))
        self.cancelar.setToolTip(_translate("listadodenacionalidades", "<html><head/><body><p>Al presionar este botón se cierra la ventana sin cambiar nada.</p></body></html>"))
        self.cancelar.setText(_translate("listadodenacionalidades", "Cerrar"))
