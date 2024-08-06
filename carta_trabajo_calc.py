from carta_trabajo import *
import leew, imprime_carta_trabajo

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args,user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.ya_se_puede_cerrar = False
        # abajo se listan los periodos cerrados porque son los que una nomina cerró
        self.list_todos_trabajadores = leew.consulta_lista('worker.db','id','info','id>','0 and Estatus = "Activo"')
        self.list_todos_trabajadores_con_datos = []
        for id_trabajador in self.list_todos_trabajadores:
            id_trabajador = str(id_trabajador)
            nombre = leew.consulta_gen('worker.db','Nombre','info','id',id_trabajador)
            nombre2 = leew.consulta_gen('worker.db','nombre2','info','id',id_trabajador)
            apellido = leew.consulta_gen('worker.db','Apellido','info','id',id_trabajador)
            apellido2 = leew.consulta_gen('worker.db','apellido2','info','id',id_trabajador)
            identificacion = leew.consulta_gen('worker.db','Identificacion','info','id',id_trabajador)
            trabajador = f'{id_trabajador} {nombre} {nombre2} {apellido} {apellido2} {str(identificacion)}'
            self.list_todos_trabajadores_con_datos.append(trabajador)

        #print(self.list_per_fin_de_mes[::-1])
        self.trabajador.addItems(self.list_todos_trabajadores_con_datos) # tuve que usar el slice de lista porque reverse no sirvio

        self.generar.setDisabled(1)

        # conexiones
        self.dirigido.textChanged.connect(self.activar_boton_generar)
        self.firmante.textChanged.connect(self.activar_boton_generar)
        self.cargo_firmante.textChanged.connect(self.activar_boton_generar)
        self.telf_firmante.textChanged.connect(self.activar_boton_generar)
        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.generar.clicked.connect(self.generar_cmd)
        #self.gen_recibos.clicked.connect(self.generar_recibos_cmd)

    def generar_cmd(self):
        #para tomar el id del trabajador seleccionado en el combo box
        id_trab = self.trabajador.currentText().split(' ')[0]
        #print(id_trab)
        reply = QtWidgets.QMessageBox.question(self, 'Para continuar',
                                               f'¿Está usted seguro de generar la carta de trabajo?'
                                               , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            imprime_carta_trabajo.imprime(id_trab,self.dirigido.text(),self.firmante.text(),
                                          self.cargo_firmante.text(),self.telf_firmante.text())
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

    def activar_boton_generar(self):
        if self.dirigido.text() == "" or self.firmante.text() == "" or \
                self.cargo_firmante.text() == "" or self.telf_firmante.text() == "":
            self.generar.setDisabled(1)
        else:
            self.generar.setDisabled(0)

