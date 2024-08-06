from salario_nuevo import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.carga_data()

        self.ya_se_puede_cerrar = False

        self.cancelar.clicked.connect(self.close_cmd)

        self.fecha.setDate(QtCore.QDate.currentDate())

        self.agregar.clicked.connect(self.add_salario)

        self.agregar.setDisabled(1)

        self.trabajador.currentTextChanged.connect(self.refresca_salario_actual)

        self.nota.textChanged.connect(self.activa)

        self.fecha.dateChanged.connect(self.activa)

        self.salario.valueChanged.connect(self.activa)


    def carga_data(self):
        # llenado de filas combobox
        idies = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        # print(idies)
        for id in idies:
            id = str(id)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id}"')
            trabajador = f"{id} {nombre} {apellido} {cedula}"
            self.trabajador.addItem(trabajador)
        self.refresca_salario_actual()

    def refresca_salario_actual(self):
        self.salario_actual.setText(str(leew.consulta_gen('worker.db', 'salario', 'salario',
                                                      'status', f'"Vigente" AND id = "{self.trabajador.currentText().split(" ")[0]}" '))) # agarro solo el id

    def add_salario(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar","Desea usted agregar el nuevo salario al trabajador?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:

                self.id = self.trabajador.currentText().split(' ')[0]  # con esta linea saco el id de una cadena de texto
                leew.actualiza_salario(self.id)
                self.entrada = f'"{self.id}","{self.fecha.date().toString("dd-MM-yyyy")}",' \
                               f'"{self.salario.text()}","Vigente",NULL,' \
                               f'"{self.nota.toPlainText()}"'
                #print(datos)
                leew.introduce_gen('worker.db','salario',self.entrada)

                QtWidgets.QMessageBox.information(self, "Atención", "Salario agregado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def activa(self):

        if self.salario.text() != '0.00' and self.nota.toPlainText() != '':
            self.agregar.setDisabled(0)
        else:
            self.agregar.setDisabled(1)

    def close_cmd(self):
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