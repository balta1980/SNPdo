from tabla_nomina import *

import leew, ver_recibos, genera_nomina_calc, ordenpago

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self,cmd,obj,obj2, *args, user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)
        #print(args)

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador
        self.actualizar_per_abierto_main = cmd
        self.obj = obj # para que las fichas sea subwindows mdi
        self.obj2 = obj2 # para poder habilitar de nuevo el menu de listado de trabajaodes
        self.args = args
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

        if leew.consultaPer_top('worker.db') == []:
            QtWidgets.QMessageBox.warning(self, "Advertencia",
                                          "No existen periodos abiertos. Por favor cree uno nuevo en el modulo de Definiciones",
                                          QtWidgets.QMessageBox.Ok)

        else:
            self.primer_periodo_abierto = leew.consultaPer_top('worker.db')[0]
            self.correr_nomina.setDisabled(True)
            self.obj.addSubWindow(genera_nomina_calc.MainWindow(self.refresh_tabla, self.actualizar_per_abierto_main,self.correr_nomina,self.primer_periodo_abierto, self.args[0],user=self.user)).show()

    def generar_recibos_cmd(self):

        ver_recibos.ver_recibos(self.nomina)

    def generar_orden_de_pago_cmd(self):
        ordenpago.imprimir(self.nomina)

    def refresh_tabla(self):

        # Llenando las filas
        lista_de_nominas = leew.consulta_lista_distintc('worker.db','PERIODO','nomina','ID_NOM >', '0')
        #print(lista_de_nominas)
        self.tableWidget.setRowCount(len(lista_de_nominas))
        lista_de_nominas.reverse() # esto para que la ultima nomina salga de primero

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        ind = 0
        for nomina in lista_de_nominas:

            item = leew.consulta_gen('worker.db','FECHA','nomina','PERIODO',f'"{nomina}"')
            self.tableWidget.setItem(ind, 0, QtWidgets.QTableWidgetItem(item))

            self.tableWidget.setItem(ind, 1, QtWidgets.QTableWidgetItem(nomina))
            item = leew.consulta_gen_sum('worker.db','MONTO_A_PAGAR', 'nomina', 'PERIODO', f'"{nomina}"')
            self.tableWidget.setItem(ind, 2, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(round(item,2)))))
            self.tableWidget.item(ind,2).setTextAlignment(2999)
            item = leew.consulta_gen('worker.db','NOTA','nomina','PERIODO',f'"{nomina}"')
            self.tableWidget.setItem(ind, 3, QtWidgets.QTableWidgetItem(item))
            ind = ind + 1

    def cambia_nombre(self):

        self.gen_recibos.setDisabled(0)
        self.gen_orden_pagos.setDisabled(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.nomina = self.tableWidget.item(currentQTableWidgetItem.row(), 1).text()
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
        