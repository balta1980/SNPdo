from list_inasis import *

import leew


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, obj, obj2, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.obj = obj  # para poder habilitar de nuevo el menu de listado de inasistencias
        self.obj2 = obj2  # para poder habilitar de nuevo el menu de registro de ina
        # print(self.obj)
        # Carga de data
        self.numero_ficha = ""
        self.refresh_tabla()
        self.borrar.setDisabled(1)

        # conexiones

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.tableWidget.clicked.connect(self.cambia_nombre)
        self.borrar.clicked.connect(self.borrar_cmd)


    def borrar_cmd(self):
        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted eliminar el registro Número: " + \
                                               self.numero_ficha + "?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                leew.del_gen('worker.db', 'inasis', 'id_i', f'{self.numero_ficha} AND computado = 0')
                # self.close()

                QtWidgets.QMessageBox.information(self, "Atención", "Registro borrado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)

        self.refresh_tabla()
        self.borrar.setText('Borrar') # esto para que el boton se vuelva a desbilitar
        self.borrar.setDisabled(1)

    def refresh_tabla(self):
        lista_id_inasis = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'computado', '"0"')
        n = len(lista_id_inasis)
        self.tableWidget.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

        cont = 0
        for id_ina in lista_id_inasis:
            id_ina = str(id_ina)
            item = id_ina
            self.tableWidget.setItem(cont, 0, QtWidgets.QTableWidgetItem(item))
            id_trab = leew.consulta_gen('worker.db', 'id', 'inasis', 'id_i', id_ina)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id_trab}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id_trab}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id_trab}"')
            trabajador = f"{id_trab} {nombre} {apellido} {cedula}"
            self.tableWidget.setItem(cont, 1, QtWidgets.QTableWidgetItem(trabajador))
            item = leew.consulta_gen('worker.db', 'fecha_i', 'inasis', 'id_i', id_ina)
            self.tableWidget.setItem(cont, 2, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'hora_i', 'inasis', 'id_i', id_ina)
            self.tableWidget.setItem(cont, 3, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'fecha_f', 'inasis', 'id_i', id_ina)
            self.tableWidget.setItem(cont, 4, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'hora_f', 'inasis', 'id_i', id_ina)
            self.tableWidget.setItem(cont, 5, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'tipo', 'inasis', 'id_i', id_ina)
            self.tableWidget.setItem(cont, 6, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'dias', 'inasis', 'id_i', id_ina))
            self.tableWidget.setItem(cont, 7, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'monto', 'inasis', 'id_i', id_ina))
            self.tableWidget.setItem(cont, 8, QtWidgets.QTableWidgetItem(item))
            cont = cont + 1

    def cambia_nombre(self):

        self.borrar.setDisabled(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.numero_ficha = self.tableWidget.item(currentQTableWidgetItem.row(), 0).text()
            self.borrar.setText("Borrar: " + self.numero_ficha)

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def closeEvent(self, QCloseEvent):
        # esta funcion es para que el boton cerrar y la X de la ventana reactiven el menu de listado de trabajadores
        self.close()
        self.parentWidget().close()
        self.obj.setDisabled(False)
        self.obj2.setDisabled(False)
