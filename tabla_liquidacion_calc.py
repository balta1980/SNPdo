from tabla_liquidacion import *

import leew, ver_recibos, egreso_calc, ordenpago


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self,obj,obj2, *args, user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador

        self.obj = obj # para que las fichas sea subwindows mdi
        self.obj2 = obj2 # para poder habilitar de nuevo el menu de listado de trabajaodes
        #print(self.obj)
        # Carga de data

        self.refresh_tabla()

        # conexiones

        self.cerrar.clicked.connect(self.cerrar_cmd)

        self.tableWidget.clicked.connect(self.cambia_nombre)
        self.gen_recibos.setDisabled(1)
        self.gen_orden_pagos.setDisabled(1)

        self.correr_nomina.clicked.connect(self.correr_nomina_cmd)
        self.gen_recibos.clicked.connect(self.generar_recibos_cmd)
        self.gen_orden_pagos.clicked.connect(self.generar_orden_de_pago_cmd)


        self.correr_nomina.setFocus() # para obtener el foco
        self.correr_nomina.setDefault(1) # para que se preseleccione y poder dar enter

    def correr_nomina_cmd(self):

        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:

            self.obj.addSubWindow(egreso_calc.MainWindow(self.refresh_tabla, self)).show()

    def generar_recibos_cmd(self):
        id_trab = leew.consulta_gen('worker.db', 'id_trab', 'liquidacion', 'id_liq', f'{self.nomina}')
        periodo = leew.consulta_gen('worker.db', 'periodo_salida', 'liquidacion', 'id_liq', f'{self.nomina}')
        ver_recibos.ver_recibo(id_trab, periodo, tipo_nomina='egreso')

    def generar_orden_de_pago_cmd(self):
        periodo = leew.consulta_gen('worker.db', 'periodo_salida', 'liquidacion', 'id_liq', f'{self.nomina}')
        id_trab = leew.consulta_gen('worker.db', 'id_trab', 'liquidacion', 'id_liq', f'{self.nomina}')
        ordenpago.imprimir(periodo,id_trab=id_trab, tipo_nomina='egreso')

    def refresh_tabla(self):

        # Llenando las filas
        lista_liquidaciones = leew.consulta_lista('worker.db','id_liq','liquidacion','id_liq >', '0')
        #print(lista_liquidaciones)
        self.tableWidget.setRowCount(len(lista_liquidaciones))
        lista_liquidaciones.reverse() # esto para que la ultima liquidacion salga de primero

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        ind = 0
        for liquidacion in lista_liquidaciones:
            self.tableWidget.setItem(ind, 0, QtWidgets.QTableWidgetItem(str(liquidacion)))
            item = leew.consulta_gen('worker.db','fecha_egreso','liquidacion','id_liq',f'"{liquidacion}"')
            self.tableWidget.setItem(ind, 1, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen_sum('worker.db','id_trab', 'liquidacion', 'id_liq', f'"{liquidacion}"')
            self.tableWidget.setItem(ind, 2, QtWidgets.QTableWidgetItem(str(item)))
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{item}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{item}"')
            nombreyapellido = f'{nombre} {apellido}'
            self.tableWidget.setItem(ind, 3, QtWidgets.QTableWidgetItem(nombreyapellido))
            item = leew.consulta_gen('worker.db','total_liq','liquidacion','id_liq',f'"{liquidacion}"')
            self.tableWidget.setItem(ind, 4, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(round(item,2)))))
            item = leew.consulta_gen('worker.db', 'nota', 'liquidacion', 'id_liq', f'"{liquidacion}"')
            self.tableWidget.setItem(ind, 5, QtWidgets.QTableWidgetItem(item))
            ind = ind + 1

    def cambia_nombre(self):

        self.gen_recibos.setDisabled(0)
        self.gen_orden_pagos.setDisabled(0)

        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.nomina = self.tableWidget.item(currentQTableWidgetItem.row(), 0).text()
            self.gen_recibos.setText("Recibos: \n" + self.nomina)

            self.gen_orden_pagos.setText("Orden de pago: \n" + self.nomina)

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def closeEvent(self, QCloseEvent):
        # esta funcion es para que el boton cerrar y la X de la ventana reactiven el menu de listado de trabajadores
        self.close()
        self.parentWidget().close()
        self.obj2.setDisabled(False)