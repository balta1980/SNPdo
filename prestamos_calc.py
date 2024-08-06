from prestamos import *

import leew, registro_prestamo_calc, imprime_prestamo


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, obj, obj2, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.obj = obj  # para que la ventana de agregar inasistencia sea subwindows mdi
        self.obj2 = obj2  # para poder habilitar de nuevo el menu de listado de inasistencias
        # print(self.obj)
        # Carga de data
        self.id_prestamo = ""
        self.refresh_tabla_prestamo()
        self.borrar.setDisabled(1)
        self.imprimir.setDisabled(1)

        # conexiones

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.tabla_prestamos.clicked.connect(self.cambia_nombre)
        self.tabla_prestamos.clicked.connect(self.refresh_tabla_detalles_prestamo)
        self.agregar.clicked.connect(self.cmd_agregar)
        self.borrar.clicked.connect(self.borrar_cmd)
        self.imprimir.clicked.connect(self.imprimir_cmd)

    def cmd_agregar(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:

            self.obj.addSubWindow(registro_prestamo_calc.MainWindow(self.refresh_tabla_prestamo, self)).show()

    def borrar_cmd(self):

        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted eliminar el préstamo Número: " + \
                                               self.id_prestamo + "?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                leew.del_gen('worker.db','prestamos','idp', f'"{self.id_prestamo}"')
                leew.del_gen('worker.db', 'prestamos_detalles', 'idp', f'"{self.id_prestamo}"')
                self.tabla_detalles.setRowCount(0)# para que cada vez que borre un prestamo se impie la tabla
                self.imprimir.setText(f"Imprimir:")#para volver a poner el boton como iba
                self.imprimir.setDisabled(1)
                QtWidgets.QMessageBox.information(self, "Atención", "Registro borrado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)

        self.refresh_tabla_prestamo()
        self.borrar.setText('Borrar: ') # esto para que el boton se vuelva a desbilitar
        self.borrar.setDisabled(1)

    def imprimir_cmd(self):
        imprime_prestamo.imprime(self.id_prestamo)

    def refresh_tabla_prestamo(self):
        lista_id_prestamos = leew.consulta_lista('worker.db', 'idp', 'prestamos', 'idp>', '"1"')
        n = len(lista_id_prestamos)
        self.tabla_prestamos.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tabla_prestamos.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

        cont = 0
        for id_prestamo in lista_id_prestamos:
            id_prestamo = str(id_prestamo)
            item = id_prestamo
            self.tabla_prestamos.setItem(cont, 0, QtWidgets.QTableWidgetItem(item))
            id_trab = leew.consulta_gen('worker.db', 'idt', 'prestamos', 'idp', id_prestamo)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id_trab}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id_trab}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id_trab}"')
            trabajador = f"{id_trab} {nombre} {apellido} {cedula}"
            self.tabla_prestamos.setItem(cont, 1, QtWidgets.QTableWidgetItem(trabajador))
            item = leew.consulta_gen('worker.db', 'fecha', 'prestamos', 'idp', id_prestamo)
            self.tabla_prestamos.setItem(cont, 2, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'monto', 'prestamos', 'idp', id_prestamo))
            self.tabla_prestamos.setItem(cont, 3, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'cuotas', 'prestamos', 'idp', id_prestamo))
            self.tabla_prestamos.setItem(cont, 4, QtWidgets.QTableWidgetItem(item))
            monto_cuota = leew.consulta_gen('worker.db', 'monto_cuotas', 'prestamos', 'idp', id_prestamo)
            self.tabla_prestamos.setItem(cont, 5, QtWidgets.QTableWidgetItem(str(monto_cuota)))
            item = leew.consulta_gen('worker.db', 'estatus', 'prestamos', 'idp', id_prestamo)
            self.tabla_prestamos.setItem(cont, 6, QtWidgets.QTableWidgetItem(item))
            cat_cuotas_pend = len(leew.consulta_lista('worker.db','idc','prestamos_detalles','idp',f'"{id_prestamo}" and estatus = "pendiente"'))
            self.tabla_prestamos.setItem(cont, 7, QtWidgets.QTableWidgetItem(str(cat_cuotas_pend)))
            monto_pendiente = round(cat_cuotas_pend * monto_cuota, 2)# redondeo a 2 decimales
            self.tabla_prestamos.setItem(cont, 8, QtWidgets.QTableWidgetItem(str(monto_pendiente)))
            item = str(leew.consulta_gen('worker.db', 'nota', 'prestamos', 'idp', id_prestamo))
            self.tabla_prestamos.setItem(cont, 9, QtWidgets.QTableWidgetItem(item))
            cont = cont + 1

    def refresh_tabla_detalles_prestamo(self):
        idp = 0# esto para quitar el mensaje de alerta de pycharm de que idp se podí usar sin estar declarada
        for currentQTableWidgetItem in self.tabla_prestamos.selectedItems():
            idp = self.tabla_prestamos.item(currentQTableWidgetItem.row(), 0).text()

        lista_idc = leew.consulta_lista('worker.db', 'idc', 'prestamos_detalles', 'idp', f'"{idp}"')
        n = len(lista_idc)
        self.tabla_detalles.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tabla_detalles.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)


        cont = 0
        for id_prestamo in lista_idc:
            id_prestamo = str(id_prestamo)
            item = id_prestamo
            self.tabla_detalles.setItem(cont, 0, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'periodo', 'prestamos_detalles', 'idc', f'"{id_prestamo}"')
            self.tabla_detalles.setItem(cont, 1, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'estatus', 'prestamos_detalles', 'idc', f'"{id_prestamo}"'))
            self.tabla_detalles.setItem(cont, 2, QtWidgets.QTableWidgetItem(item))

            cont = cont + 1

    def cambia_nombre(self):
        #cambio nombres convenientemente para los botones borrar e imprimir

        for currentQTableWidgetItem in self.tabla_prestamos.selectedItems():
            #estatus = self.tabla_prestamos.item(currentQTableWidgetItem.row(), 6).text()
            self.id_prestamo = self.tabla_prestamos.item(currentQTableWidgetItem.row(), 0).text()
            self.imprimir.setText(f"Imprimir: {self.id_prestamo}")
            self.imprimir.setDisabled(0)
            estatus = leew.consulta_gen('worker.db', 'estatus', 'prestamos', 'idp', f'"{self.id_prestamo}"')
            if estatus == "ABIERTO":
                self.borrar.setText("Borrar: " + self.id_prestamo)
                self.borrar.setDisabled(0)
            else:
                self.borrar.setDisabled(1)
                self.borrar.setText("Borrar: ")

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def closeEvent(self, QCloseEvent):
        # esta funcion es para que el boton cerrar y la X de la ventana reactiven el menu de listado de trabajadores
        self.close()
        self.parentWidget().close()
        self.obj2.setDisabled(False)