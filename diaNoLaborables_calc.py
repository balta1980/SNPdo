from diaNoLaborables import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_DiasNoLaborables):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.carga_data()

        self.tableWidget.clicked.connect(self.on_click)

        self.cancelar.clicked.connect(self.close_cmd)

        self.agregar.clicked.connect(self.add_fecha)

        self.agregar.setDisabled(1)

        self.lineEdit.textEdited.connect(self.activa)

        self.dateEdit.dateChanged.connect(self.activa)

        self.borrar.setDisabled(1)

        self.borrar.clicked.connect(self.borrar_comand)

        self.anuncio = QtWidgets.QLabel("") # para poder advertir al usuario de fechas repetidas
        self.statusbar.addWidget(self.anuncio)

        #self.show() no se usa este comando cuando la ventana esta en mdi

    def carga_data(self):
        # llenado de filas
        self.dias_no_lab = leew.consulta_lista('worker.db', 'indice', 'dia_no_laborables', 'indice>','0')
        self.tableWidget.setRowCount(len(self.dias_no_lab))
        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        n = 0
        for i in self.dias_no_lab:
            text = str(i)
            item, = leew.consultaP2('worker.db', 'fecha', 'dia_no_laborables', text)
            self.tableWidget.setItem(n, 0, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'nombre', 'dia_no_laborables', text)
            self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem(item))
            n = n + 1

    def add_fecha(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar","Desea usted agregar la nueva fecha?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            # obtencion fecha
            fecha = self.dateEdit.date().toString("dd-MM-yyyy")

            # obtencion descripcion

            descripcion = self.lineEdit.text()


            try:
                datos = 'NULL,"' + fecha + '","' + descripcion + '"'
                #print(datos)
                leew.introduce_par('dia_no_laborables', datos)
                self.carga_data()
                self.dateEdit.setDate(QtCore.QDate(2000,1,1))
                self.lineEdit.clear()
                #self.close()
                #self.parentWidget().close() # este comando es para cerrar la ventana MDI
                QtWidgets.QMessageBox.information(self, "Atención", "Fecha agregada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def borrar_comand(self):

        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted eliminar la fecha: " + \
                                           currentQTableWidgetItem.text() + " referente a "+ \
                                                   str(self.tableWidget.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column() + 1).text()) + "?"
                                           , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    leew.del_dia_no_lab(currentQTableWidgetItem.text())
                    #self.close()
                    self.carga_data()
                    self.dateEdit.setDate(QtCore.QDate(2000, 1, 1))
                    self.lineEdit.clear()

                    QtWidgets.QMessageBox.information(self, "Atención", "Fecha borrada satisfactoriamente",
                                                      QtWidgets.QMessageBox.Ok)
                except:
                    QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)
            break # esto se pone para que no siga iterando si se selecciona una fila y no una celda

                #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            if currentQTableWidgetItem.column() == 0:
                self.borrar.setDisabled(0)
                #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            else:
                self.borrar.setDisabled(1)

    def activa(self):

        if self.lineEdit.text() != "" and self.dateEdit.text() not in leew.consulta_lista('worker.db', 'fecha', 'dia_no_laborables', 'indice>','0'):
            self.agregar.setDisabled(0)
            self.anuncio.setText("")
        else:
            self.agregar.setDisabled(1)
            self.anuncio.setText("Fecha repetida o no ha colocado descripción")
            self.anuncio.setStyleSheet("background:#FA5858 ;border-radius:3;")

    def close_cmd(self):
        self.close()
        self.parentWidget().close() # este comando es para cerrar la ventana MDI
