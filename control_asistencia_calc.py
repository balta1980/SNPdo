from control_asistencia import *

import formato_asistencia

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args,user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.ya_se_puede_cerrar = False
        self.ano_select.setDate(QtCore.QDate.currentDate())
        self.mes_select.setDate(QtCore.QDate.currentDate())
        # conexiones

        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.generar.clicked.connect(self.generar_cmd)
        #self.gen_recibos.clicked.connect(self.generar_recibos_cmd)

    def generar_cmd(self):

        reply = QtWidgets.QMessageBox.question(self, 'Para continuar',
                                               f'¿Está usted seguro de generar los formatos de asistencia?'
                                               , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            formato_asistencia.imprimir(self.mes_select.text(), self.ano_select.text(),self.nota.toPlainText())
            self.ya_se_puede_cerrar = True
            self.close()

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
