from list_hora_extra import *

import leew

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self,obj,obj2, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.obj = obj  # para poder habilitar de nuevo el menu de listado de trabajaodes
        self.obj2 = obj2  # para poder habilitar de nuevo el menu registro de horas extra
        #  print(self.obj)
        # Carga de data
        self.numero_ficha = ""
        self.refresh_tabla()
        self.borrar.setDisabled(1)

        # conexiones

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.tableWidget.clicked.connect(self.cambia_nombre)
        #self.agregar.clicked.connect(self.cmd_agregar)
        self.borrar.clicked.connect(self.borrar_cmd)


    def borrar_cmd(self):
        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted eliminar el registro Número: " + \
                                               self.numero_ficha + "?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                leew.del_gen('worker.db','horas_extras','id_h',f'{self.numero_ficha} AND computado = 0') # este AND computado = 0 es para que no se borre un registro despues de correr nomina con listado abierto
                # self.close()

                QtWidgets.QMessageBox.information(self, "Atención", "Registro borrado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)

        self.refresh_tabla()
        self.borrar.setText('Borrar')
        self.borrar.setDisabled(1)

    def refresh_tabla(self):
        lista_id_he = leew.consulta_lista('worker.db','id_h','horas_extras','computado','"0"')
        n = len(lista_id_he)
        self.tableWidget.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        cont = 0
        for id_h in lista_id_he:
            id_h = str(id_h)
            item = id_h
            self.tableWidget.setItem(cont, 0, QtWidgets.QTableWidgetItem(item))
            id_trab = leew.consulta_gen('worker.db','id','horas_extras','id_h', id_h)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id_trab}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id_trab}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id_trab}"')
            trabajador = f"{id_trab} {nombre} {apellido} {cedula}"
            self.tableWidget.setItem(cont, 1, QtWidgets.QTableWidgetItem(trabajador))
            item = leew.consulta_gen('worker.db','fecha','horas_extras','id_h',id_h)
            self.tableWidget.setItem(cont, 2, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db','hora_i','horas_extras','id_h',id_h)
            self.tableWidget.setItem(cont, 3, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db','hora_f','horas_extras','id_h',id_h)
            self.tableWidget.setItem(cont, 4, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db','horas','horas_extras','id_h',id_h))
            self.tableWidget.setItem(cont, 5, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'total', 'horas_extras', 'id_h', id_h))
            self.tableWidget.setItem(cont, 6, QtWidgets.QTableWidgetItem(item))
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
