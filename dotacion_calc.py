from dotacion import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.carga_data()

        self.ya_se_puede_cerrar = False

        self.cancelar.clicked.connect(self.close_cmd)

        self.fecha = QtCore.QDate.currentDate().toString("dd-MM-yyyy")

        self.crear.clicked.connect(self.add_dotacion)

        self.crear.setDisabled(1)

        self.cant_pant.valueChanged.connect(self.activa)
        self.cant_guantes.valueChanged.connect(self.activa)
        self.cant_lentes.valueChanged.connect(self.activa)
        self.cant_zapatos.valueChanged.connect(self.activa)
        self.cant_camisa.valueChanged.connect(self.activa)
        self.nota_dota.textChanged.connect(self.activa)

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

    def add_dotacion(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar","Desea usted agregar la dotación al trabajador?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:

                self.id = self.trabajador.currentText().split(' ')[0]  # con esta linea saco el id de una cadena de texto
                self.nombre = leew.consulta_gen('worker.db','Nombre','info','id',self.id)
                self.apellido = leew.consulta_gen('worker.db','Apellido','info','id',self.id)

                self.nombre_y_apellido = f"{self.nombre} {self.apellido}"

                self.entrada = f'NULL, "{self.id}","{self.nombre_y_apellido}","{self.cant_camisa.text()}","{self.cant_pant.text()}","{self.cant_zapatos.text()}",' \
                               f'"{self.cant_lentes.text()}","{self.cant_guantes.text()}","{self.fecha}",' \
                               f'"{self.nota_dota.text()}"'
                #print(self.entrada)
                leew.introduce_gen('worker.db','dotacion',self.entrada)

                QtWidgets.QMessageBox.information(self, "Atención", "Dotación agregada satisfactoriamente. Si desea imprimir"
                                                                    " o borrar este registro por favor acceda a la ficha del trabajador"
                                                                    " y seleccione la pestaña de dotaciones",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def activa(self):

        if self.nota_dota.text() != '':
            if self.cant_camisa.text() != '0' or self.cant_zapatos.text() != '0' or self.cant_lentes.text() != '0' or \
                    self.cant_guantes.text() != '0' or self.cant_pant.text() != '0':
                self.crear.setDisabled(0)
            else:
                self.crear.setDisabled(1)
        else:
            self.crear.setDisabled(1)

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