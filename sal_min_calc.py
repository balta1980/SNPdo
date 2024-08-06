from sal_min import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_sal_min):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Carga de data
        try: # esta serie de manejo de excepciones la hice para evitar problemas cuando no hay datos
            fecha_bd, = leew.consulta_salmin('fecha')
        except:
            fecha_bd = "01-01-2000"
        #print(fecha_bd)
        dia, mes, ano, = [int(n) for n in fecha_bd.split("-")]
        self.dateEdit.setDate(QtCore.QDate(ano,mes,dia))
        try:
            salario_bd, = leew.consulta_salmin('salario')
        except:
            salario_bd = "00.00"
        #print(salario)
        self.doubleSpinBox.setValue(float(salario_bd))
        try:
            nota_bd, = leew.consulta_salmin('nota')
        except:
            nota_bd = ""
        self.textEdit.setText(nota_bd)

        # variable de control para close
        self.cerrar = 0

        # conexiones
        self.dateEdit.dateChanged.connect(self.activa_guardar)
        self.doubleSpinBox.valueChanged.connect(self.activa_guardar)
        self.textEdit.textChanged.connect(self.activa_guardar)
        self.cancelar.clicked.connect(self.close)
        self.guardar.clicked.connect(self.cargar_data)

        # inactiva guardar
        self.guardar.setDisabled(1)

        #self.show() no se usa en mdi

    def activa_guardar(self):
        self.guardar.setDisabled(0)

    def cargar_data(self):
        reply = QtWidgets.QMessageBox.warning(self, "Advertencia!", "¿Está usted seguro de la modificación?", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.update_salmin()
                self.entrada = 'NULL,"' + self.dateEdit.text() + '","' + self.doubleSpinBox.text() + '","' + 'Vigente' + '","' + \
                               self.textEdit.toPlainText() + '"'
                #print(self.entrada)
                QtWidgets.QMessageBox.information(self, "Atención", "Salario modificado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                leew.introduce_salmin(self.entrada)
                self.cerrar = 1
                self.close()
                self.parentWidget().close()


            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)
        else:
            pass

    def closeEvent(self, QCloseEvent):

        if self.cerrar == 0:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia', '¿Está usted seguro de salir? Se perderán los datos '
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
