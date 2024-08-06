from tabla_nomina_individual import *

import leew, ver_recibos, genera_nomina_individual_calc, ordenpago

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self,cmd,obj,obj2, *args, user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador
        self.actualizar_per_abierto_main = cmd
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

        if leew.consultaPer_top('worker.db') == []:
            QtWidgets.QMessageBox.warning(self, "Advertencia",
                                          "No existen periodos abiertos. Por favor cree uno nuevo en el modulo de Definiciones",
                                          QtWidgets.QMessageBox.Ok)

        else:
            self.primer_periodo_abierto = leew.consultaPer_top('worker.db')[0]
            self.correr_nomina.setDisabled(True)
            vent = genera_nomina_individual_calc.MainWindow(self.refresh_tabla, self.actualizar_per_abierto_main,
                                                         self.correr_nomina, self.primer_periodo_abierto, self,
                                                         user=self.user)

            self.obj.addSubWindow(vent).show()
            vent.verifica_si_hay_trabajadores() # este comando es para que no se pueda correr una nomina individual si ya todos los trabajadores tienen una nomina en el periodo
            #comando de abajo es viejo, se puede borrar
            #self.obj.addSubWindow(genera_nomina_individual_calc.MainWindow(self.refresh_tabla, self.actualizar_per_abierto_main,self.correr_nomina,self.primer_periodo_abierto, self,user=self.user)).show()

    def generar_recibos_cmd(self):

        ver_recibos.ver_recibo(self.id_trabajador,self.nomina)

    def generar_orden_de_pago_cmd(self):
        ordenpago.imprimir(self.nomina,self.id_trabajador)

    def refresh_tabla(self):

        # Llenando las filas
        lista_de_id_nominas = leew.consulta_lista('worker.db','ID_NOM','nomina','TIPO_NOMINA', '"Individual"')
        #print(lista_de_nominas)
        self.tableWidget.setRowCount(len(lista_de_id_nominas))
        lista_de_id_nominas.reverse() # esto para que la ultima nomina salga de primero

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        ind = 0
        for id_nomina in lista_de_id_nominas:

            item = leew.consulta_gen('worker.db','FECHA','nomina','ID_NOM',f'"{id_nomina}"')
            self.tableWidget.setItem(ind, 0, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'ID_TRABAJADOR', 'nomina', 'ID_NOM', f'"{id_nomina}"')
            nombre = leew.consulta_gen('worker.db','Nombre','info','id',str(item))
            apellido = leew.consulta_gen('worker.db','Apellido','info','id',str(item))
            nombre_apellido = f"{item},{nombre} {apellido}"
            self.tableWidget.setItem(ind, 1, QtWidgets.QTableWidgetItem(nombre_apellido))
            item = leew.consulta_gen('worker.db','PERIODO','nomina','ID_NOM',str(id_nomina))
            self.tableWidget.setItem(ind, 2, QtWidgets.QTableWidgetItem(str(item)))
            self.tableWidget.setItem(ind, 3, QtWidgets.QTableWidgetItem(str(id_nomina)))
            item = leew.consulta_gen('worker.db','MONTO_A_PAGAR','nomina','ID_NOM',f'"{id_nomina}"')
            self.tableWidget.setItem(ind, 4, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(round(item,2)))))
            self.tableWidget.item(ind,4).setTextAlignment(2999)
            item = leew.consulta_gen('worker.db','NOTA','nomina','ID_NOM',f'"{id_nomina}"')
            self.tableWidget.setItem(ind, 5, QtWidgets.QTableWidgetItem(item))
            ind = ind + 1

    def cambia_nombre(self):

        self.gen_recibos.setDisabled(0)
        self.gen_orden_pagos.setDisabled(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.nomina = self.tableWidget.item(currentQTableWidgetItem.row(), 2).text()
            self.id_trabajador = str(self.tableWidget.item(currentQTableWidgetItem.row(), 1).text().split(',')[0])
            self.recibo = self.tableWidget.item(currentQTableWidgetItem.row(), 3).text()
            self.gen_recibos.setText("Recibos: \n" + self.recibo)
            self.gen_orden_pagos.setText("Orden de pago: \n" + self.recibo)

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def closeEvent(self, QCloseEvent):
        # esta funcion es para que el boton cerrar y la X de la ventana reactiven el menu de listado de trabajadores
        self.close()
        self.parentWidget().close()
        self.obj2.setDisabled(False)