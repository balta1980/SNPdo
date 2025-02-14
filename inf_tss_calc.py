from inf_tss import *
import leew, imprime_tss, genera_txt

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args,user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.ya_se_puede_cerrar = False
        # abajo se listan los periodos cerrados porque son los que una nomina cerró
        self.list_todos_periodos = leew.consulta_lista('worker.db','idp','periodo','indice >', '0 and status = "CERRADO"')
        self.list_per_fin_de_mes = []
        for per in self.list_todos_periodos: # aqui filtro los periodos 1 que son la primera quincena
            if per[0] == '2':
                self.list_per_fin_de_mes.append(per)

        #print(self.list_per_fin_de_mes[::-1])
        self.periodo.addItems(self.list_per_fin_de_mes[::-1]) # tuve que usar el slice de lista porque reverse no sirvio

        # conexiones

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.generar.clicked.connect(self.generar_cmd)
        #self.gen_recibos.clicked.connect(self.generar_recibos_cmd)

    def generar_cmd(self):

        if self.list_per_fin_de_mes == []:# cuando la BD está vacía
            self.advertencia_no_hay_informacion_para_mostrar()
        else:

            reply = QtWidgets.QMessageBox.question(self, 'Para continuar',
                                                   f'¿Está usted seguro de generar el informe TSS?'
                                                   , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                imprime_tss.imprime(self.periodo.currentText(), self.nota.toPlainText())
                self.ya_se_puede_cerrar = True
                self.generar_txt()
                self.close()

    def advertencia_no_hay_informacion_para_mostrar(self):
        QtWidgets.QMessageBox.warning(self, 'Advertencia','No hay información para mostrar', QtWidgets.QMessageBox.Ok)

    def generar_txt(self):

        if self.novedades_periodo.isChecked():
            genera_txt.generar_txt(self.periodo.currentText(), novedad=1)
        if self.autodeterminacion.isChecked():
            genera_txt.generar_txt(self.periodo.currentText(), auto_men=1)
        if self.autodetermincacion_retro.isChecked():
            genera_txt.generar_txt(self.periodo.currentText(), auto_retro=1)
        if self.rectificativa.isChecked():
            genera_txt.generar_txt(self.periodo.currentText(), recti=1)

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

            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()