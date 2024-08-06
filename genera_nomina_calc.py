from genera_nomina import *

import nomina_quincenal, ordenpago, enviar_recibos_nomina_por_correo

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self,cmd,cmd2,obj, primer_periodo_abierto, *args,user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)
        self.arg = args[0]
        #print(args)
        self.ya_se_puede_cerrar = False

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador
        self.refrescar_tabla_nominas = cmd # para refrescar tabla de nomina
        self.refrescar_imf_primer_per_main = cmd2
        self.obj = obj
        self.primer_periodo_abierto = primer_periodo_abierto

        self.periodo_nomina.setText(self.primer_periodo_abierto)
        self.periodo_nomina.setReadOnly(1)

        self.habilitador_correo()

        # conexiones

        self.checkBox.clicked.connect(self.habilitador_correo)

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.correr.clicked.connect(self.correr_nomina_cmd)
        #self.gen_recibos.clicked.connect(self.generar_recibos_cmd)

    def correr_nomina_cmd(self):

        reply = QtWidgets.QMessageBox.question(self, 'Para continuar',
                                               f'¿Está usted seguro correr la nómina correspondiente al periodo: {self.primer_periodo_abierto}?'
                                               , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if self.checkBox.isChecked():
                imprime = 1
            else:
                imprime = 0

            nomina_quincenal.corrida(self.primer_periodo_abierto,imprime, self.pagar_salario_navidad.isChecked(),self.nota.toPlainText())
            self.arg.actualiza_info() # comando que viene de main para actualizar las vacaciones abiertas mostradas
            #print(self.pagar_salario_navidad.isChecked())

            self.refrescar_imf_primer_per_main()

            if self.orden_pago.isChecked():
                ordenpago.imprimir(self.primer_periodo_abierto)
            if self.correo.isChecked():
                enviar_recibos_nomina_por_correo.enviar(self.primer_periodo_abierto)


            QtWidgets.QMessageBox.information(self,"Aviso", "Nómina procesada satisfactoriamente")
            try:
                self.refrescar_tabla_nominas()
            except:
                pass


            self.ya_se_puede_cerrar = True
            self.close()
            try:
                self.obj.setDisabled(0)
            except:
                pass
        else:
           pass

    def habilitador_correo(self):
        if not self.checkBox.isChecked():
            self.correo.setChecked(0)
            self.correo.setDisabled(1)
        else:
            self.correo.setDisabled(0)

    def cerrar_cmd(self):
        self.close()

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