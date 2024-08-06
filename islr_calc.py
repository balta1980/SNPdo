from islr import *
import leew

class MainWindow(QtWidgets.QMainWindow, Ui_islr):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Carga de data
        if leew.tambd_par2("worker.db", "islr") == 0:
            pass # esto para evitar problemas con tablas vacias
        else:
            # se cargan los valores que estan en la tabla
            rango1, = leew.consulta_islr('rango1')
            self.rango1.setValue(rango1)
            rango2, = leew.consulta_islr('rango2')
            self.rango2.setValue(rango2)
            rango3, = leew.consulta_islr('rango3')
            self.rango3.setValue(rango3)
            tasa1, = leew.consulta_islr('tasa1')
            self.tasa1.setValue(tasa1)
            tasa2, = leew.consulta_islr('tasa2')
            self.tasa2.setValue(tasa2)
            tasa3, = leew.consulta_islr('tasa3')
            self.tasa3.setValue(tasa3)
            valor1, = leew.consulta_islr('valor1')
            self.valor1.setValue(valor1)
            valor2, = leew.consulta_islr('valor2')
            self.valor2.setValue(valor2)
            nota, = leew.consulta_islr('nota')
            self.nota.setText(nota)
            last_fecha = leew.consulta_gen('worker.db', 'fecha', 'islr', 'status', '"Vigente"')
            self.statusbar.addWidget(QtWidgets.QLabel(f'  Última vez modificado el: {last_fecha}'))
        self.dia = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, hh:mm:ss AP")

        # variable de control para close
        self.cerrar = 0

        # conexiones

        self.cancelar.clicked.connect(self.close)
        self.rango1.valueChanged.connect(self.activa_actualizar)
        self.rango2.valueChanged.connect(self.activa_actualizar)
        self.rango3.valueChanged.connect(self.activa_actualizar)
        self.tasa1.valueChanged.connect(self.activa_actualizar)
        self.tasa2.valueChanged.connect(self.activa_actualizar)
        self.tasa3.valueChanged.connect(self.activa_actualizar)
        self.valor1.valueChanged.connect(self.activa_actualizar)
        self.valor2.valueChanged.connect(self.activa_actualizar)
        self.nota.textChanged.connect(self.activa_actualizar)
        self.actualizar.clicked.connect(self.cargar_data)

        # inactiva guardar

        self.actualizar.setDisabled(1)

        #self.show() no se usa en mdi

    def activa_actualizar(self):
        self.actualizar.setDisabled(0)

    def cargar_data(self):
        reply = QtWidgets.QMessageBox.warning(self, "Advertencia!", "¿Está usted seguro de la modificación?",
                                              QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.update_islr()
                self.entrada = 'NULL,"' + str(self.rango1.value()) + '","' + str(self.rango2.value()) + '","' + str(self.rango3.value()) + '","' + \
                               str(self.tasa1.value()) + '","' + str(self.tasa2.value()) + '","' + str(self.tasa3.value()) + '","' + \
                               str(self.valor1.value()) + '","' + str(self.valor2.value()) + '","' + self.nota.toPlainText() \
                               + '","' + self.dia + '","Vigente"'
                #print(self.entrada)
                leew.introduce_par('islr', self.entrada)
                QtWidgets.QMessageBox.information(self, "Atención", "Tabla modificada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
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
