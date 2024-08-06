from genera_nomina_individual import *

import nomina_quincenal, ordenpago, leew

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self,cmd,cmd2,obj, primer_periodo_abierto, *args,user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.ya_se_puede_cerrar = False

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador
        self.refrescar_tabla_nominas = cmd # para que las fichas sea subwindows mdi
        self.refrescar_imf_primer_per_main = cmd2
        self.obj = obj
        self.primer_periodo_abierto = primer_periodo_abierto

        self.periodo_nomina.setText(self.primer_periodo_abierto)
        self.periodo_nomina.setReadOnly(1)

        ultimo_dia_periodo = leew.consulta_gen('worker.db', 'f_fin', 'periodo', 'idp', f'"{self.primer_periodo_abierto}"')
        #print(ultimo_dia_periodo)
        udp, ump, uap, = ultimo_dia_periodo.split('-')
        self.fecha_fin_pago.setDate(QtCore.QDate(int(uap), int(ump), int(udp)))
        self.fecha_fin_pago.setMaximumDate(QtCore.QDate(int(uap), int(ump), int(udp))) # para que no se paguen dias más allá del fin del periodo
        primer_dia_periodo = leew.consulta_gen('worker.db', 'f_inicio', 'periodo', 'idp',
                                               f'"{self.primer_periodo_abierto}"')
        # print(ultimo_dia_periodo)
        pdp, pmp, pap, = primer_dia_periodo.split('-')
        self.fecha_fin_pago.setMinimumDate(QtCore.QDate(int(pap), int(pmp), int(pdp))) # para que no se puedan pagar dias que esten antes del inicio del periodo
        self.fecha_fin_pago.setToolTip(f"Solo se puede pagar un rango de fechas entre el inicio de este perido: {primer_dia_periodo} y"
                                          f" el final del periodo: {ultimo_dia_periodo}, la fecha de inicio debe ser menor o igual a la final ")

        self.fecha_i_pago.setDate(QtCore.QDate(int(pap), int(pmp), int(pdp)))
        self.fecha_i_pago.setMinimumDate(QtCore.QDate(int(pap), int(pmp), int(pdp)))
        self.fecha_i_pago.setMaximumDate(QtCore.QDate(int(uap), int(ump), int(udp)))
        self.fecha_i_pago.setToolTip(
            f"Solo se puede pagar un rango de fechas entre el inicio de este perido: {primer_dia_periodo} y"
            f" el final del periodo: {ultimo_dia_periodo}, la fecha de inicio debe ser menor o igual a la final ")

        # se sacan a los trabajadores que estan activos pero que ya se les pagó en el periodo
        trabajadores_previamente_pagados = leew.consulta_lista('worker.db', 'ID_TRABAJADOR', 'nomina', 'PERIODO',
                                                               f'"{self.periodo_nomina.text()}"')
        #print(trabajadores_previamente_pagados)
        trab_activos = leew.tambd_nom('worker.db')  # determina el numero de trabajdores activos a incluir en pago
        # abajo saco a los que en el periodo ya se le haya pagado alguna nomina cual sea
        self.trab_activos_sin_nomina = list(set(trab_activos) - set(trabajadores_previamente_pagados))
        for id in self.trab_activos_sin_nomina:
            id = str(id)
            nombre = leew.consulta_gen('worker.db','Nombre', 'info','id',f'"{id}"')
            apellido = leew.consulta_gen('worker.db','Apellido', 'info','id',f'"{id}"')
            self.trab_activo.addItem(f'{id}, {nombre} {apellido}')

        # conexiones
        self.fecha_i_pago.dateChanged.connect(self.disable_guardar)
        self.fecha_fin_pago.dateChanged.connect(self.disable_guardar)


        # conexiones

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.correr.clicked.connect(self.correr_nomina_cmd)
        #self.gen_recibos.clicked.connect(self.generar_recibos_cmd)

    def correr_nomina_cmd(self):

        reply = QtWidgets.QMessageBox.question(self, 'Para continuar',
                                               f'¿Está usted seguro correr la nómina correspondiente al periodo: {self.primer_periodo_abierto}?'
                                               , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if self.imp_recibo.isChecked():
                imprime = 1
            else:
                imprime = 0

            self.id_trab_activo = self.trab_activo.currentText().split(',')[0]

            nomina_quincenal.corrida_de_un_trabajador(self.primer_periodo_abierto,imprime,
                                                      self.pagar_salario_navidad.isChecked(),self.nota.toPlainText(),
                                                      self.id_trab_activo,"Individual",self.fecha_i_pago.text(),
                                                      self.fecha_fin_pago.text())
            self.refrescar_imf_primer_per_main()
            QtWidgets.QMessageBox.information(self,"Aviso", "Nómina procesada satisfactoriamente")
            try:
                self.refrescar_tabla_nominas()
            except:
                pass

            if self.orden_pago.isChecked():
                ordenpago.imprimir(self.primer_periodo_abierto)

            self.ya_se_puede_cerrar = True
            self.close()
            try:
                self.obj.setDisabled(0)
            except:
                pass
        else:
           pass

    def cerrar_cmd(self):
        self.close()

    def verifica_si_hay_trabajadores(self):
        # verificacion de que hay al menos un trabajador activo que no se le ha procesado nómina en el periodo
        if self.trab_activos_sin_nomina == []:
            reply = QtWidgets.QMessageBox.information(self, "Aviso",
                                              "No hay trabajador activo que no se le haya procesado nomina "
                                              f"en el periodo {self.primer_periodo_abierto}. Usted debe correr una nómina quincenal para "
                                              "cerrar este periodo y luego abrir otro, o bien, no hay trabajadores activos en la empresa y debe crear uno nuevo")


            self.ya_se_puede_cerrar = True
            self.cerrar_cmd()

    def disable_guardar(self):
        if self.fecha_i_pago.date() <= self.fecha_fin_pago.date():
            self.correr.setDisabled(0)
            self.fecha_i_pago.setStyleSheet("background: white;")
            self.fecha_fin_pago.setStyleSheet("background: white;")

        else:
            self.correr.setDisabled(1)
            self.fecha_i_pago.setStyleSheet("background: red;")
            self.fecha_fin_pago.setStyleSheet("background: red;")

    def closeEvent(self, QCloseEvent):
        if self.ya_se_puede_cerrar == False:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de salir? Se perderán los datos '
                                                   'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()
                self.parentWidget().close()
                try:
                    self.obj.setDisabled(0)
                except:
                    pass
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()
            try:
                self.obj.setDisabled(0)
            except:
                pass