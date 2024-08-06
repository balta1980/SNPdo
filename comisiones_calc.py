from comisiones import *
import leew

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, obj, obj2, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.fecha_doc.setDate(QtCore.QDate.currentDate())
        self.borrar.setDisabled(True)
        self.id_visible.setDisabled(True)

        self.hubo_modificacion = 0  # para avisar al usuario que va a perder la informació ingresada

        # listado de id de horas extra
        self.listados_id_com = leew.consulta_lista('worker.db', 'id_c', 'comisiones', 'id_c >', '"0"')
        # print(self.listados_id_hora_e)

        # para ordenar y posicionar información
        self.posicion = len(self.listados_id_com)

        # para controlar desde menu de afuera
        self.main_instancia = args[0]
        self.main_instancia.flecha_izq.triggered.connect(self.manejador_toolbar_nav_izquierda)
        self.main_instancia.flecha_der.triggered.connect(self.manejador_toolbar_nav_derecha)
        self.main_instancia.flecha_izq_fin.triggered.connect(self.manejador_toolbar_nav_izq_fin)
        self.main_instancia.flecha_der_fin.triggered.connect(self.manejador_toolbar_nav_derecha_fin)
        self.main_instancia.nuevo_doc.triggered.connect(self.manejador_boton_nuevo)

        self.obj = obj  # para poder habilitar el menu listado ina
        self.obj2 = obj2  # para poder habilitar el menu registro ina


        # listado de trabajadores

        idies = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        # print(idies)
        for id in idies:
            id = str(id)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id}"')
            trabajador = f"{id} {nombre} {apellido} {cedula}"
            self.trabajador.addItem(trabajador)

        self.agregar.setDisabled(1)

        self.ya_se_puede_cerrar = False


        self.monto.valueChanged.connect(self.set_enable_agregar)
        self.nota.textChanged.connect(self.set_enable_agregar)
        self.cancelar.clicked.connect(self.close)
        self.agregar.clicked.connect(self.guardar_cmd)
        self.borrar.clicked.connect(self.borrar_cmd)

    def probador_de_instancia_para_toolbar(self):
        # comparo si el nombre subventana activa es igual al nombre de esta ventana ("Registro de inasistencia")
        if self.main_instancia.mdiArea.currentSubWindow().windowTitle() == self.windowTitle():
            return True

    def manejador_toolbar_nav_izquierda(self):
        if self.probador_de_instancia_para_toolbar():
            if len(self.listados_id_com) > 0: # verifica que la bd no está vacia
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.hubo_modificacion = 0
                        if self.posicion == 0:
                            self.posicion = len(self.listados_id_com) - 1
                        else:
                            self.posicion = self.posicion - 1
                        self.muestra_historial(self.listados_id_com[self.posicion])
                else:
                    if self.posicion == 0:
                        self.posicion = len(self.listados_id_com) - 1
                    else:
                        self.posicion = self.posicion - 1

                    self.muestra_historial(self.listados_id_com[self.posicion])

    def manejador_toolbar_nav_derecha(self):
        if len(self.listados_id_com) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        if self.posicion >= len(self.listados_id_com) - 1:
                            self.posicion = 0
                        else:
                            self.posicion = self.posicion + 1

                        self.muestra_historial(self.listados_id_com[self.posicion])
                else:
                    if self.posicion >= len(self.listados_id_com) - 1:
                        self.posicion = 0
                    else:
                        self.posicion = self.posicion + 1

                    self.muestra_historial(self.listados_id_com[self.posicion])

    def manejador_toolbar_nav_izq_fin(self):
        if len(self.listados_id_com) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.posicion = 0
                        self.muestra_historial(self.listados_id_com[0])
                else:
                    self.posicion = 0
                    self.muestra_historial(self.listados_id_com[0])

    def manejador_toolbar_nav_derecha_fin(self):
        if len(self.listados_id_com) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.posicion = len(self.listados_id_com) - 1
                        self.muestra_historial(self.listados_id_com[self.posicion])
                else:
                    self.posicion = len(self.listados_id_com) - 1
                    self.muestra_historial(self.listados_id_com[self.posicion])

    def manejador_boton_nuevo(self):
        if self.probador_de_instancia_para_toolbar():
            if self.hubo_modificacion == 1:
                if self.advertencia_de_perdida_de_datos() == 1:
                    self.recarga_en_blanco_nuevo_doc()

            else:
                self.recarga_en_blanco_nuevo_doc()


    def muestra_historial(self, id_com):
        # carga la pantalla con la info de la BD al usar los botenes de flechas
        # print(id_hora_extra)
        try:  # uso este captyrador de error para que no cargue la data
            # print(self.trabajador.isSignalConnected(self.carga_data))
            self.monto.valueChanged.disconnect(self.set_enable_agregar)
            self.nota.textChanged.disconnect(self.set_enable_agregar)

            #self.cancelar.clicked.connect(self.close)
            self.agregar.clicked.disconnect(self.guardar_cmd)

        except:
            pass
        self.agregar.setDisabled(True)
        self.id_visible.setText(f'{id_com}')

        # fecha de computo
        data = leew.consulta_gen('worker.db', 'fecha_doc', 'comisiones', 'id_c', f'{id_com}')
        if data == None:
            self.fecha_doc.setDate(QtCore.QDate(1900, 1, 1))
        else:
            self.fecha_doc.setDate(
                QtCore.QDate(int(data.split('-')[2]), int(data.split('-')[1]), int(data.split('-')[0])))
        self.fecha_doc.setDisabled(True)

        # nombre trabajador
        data = leew.consulta_gen('worker.db', 'nombre_trab', 'comisiones', 'id_c', f'{id_com}')
        if data == None:
            data = 'N/D'
        self.trabajador.setCurrentText(data)
        self.trabajador.setDisabled(True)

        # nota
        data = leew.consulta_gen('worker.db', 'nota', 'comisiones', 'id_c', f'{id_com}')
        if data == None:
            self.nota.setPlainText("N/D")
        else:
            self.nota.setPlainText(data)
        self.nota.setDisabled(True)

        # monto
        data = leew.consulta_gen('worker.db', 'monto', 'comisiones', 'id_c', f'{id_com}')
        if data == None:
            self.monto.setValue(0)
        else:
            self.monto.setValue(data)
        self.monto.setDisabled(True)

        # para habilitar el borrado de la ina
        status_ina = leew.consulta_gen('worker.db', 'computado', 'comisiones', 'id_c', f'{id_com}')
        if status_ina == 0:

            self.borrar.setDisabled(False)
        else:
            self.borrar.setDisabled(True)

    def recarga_en_blanco_nuevo_doc(self, *args, **kwargs):
        self.setupUi(self)
        self.fecha_doc.setDate(QtCore.QDate.currentDate())
        self.borrar.setDisabled(True)
        self.id_visible.setDisabled(True)

        self.hubo_modificacion = 0  # para avisar al usuario que va a perder la informació ingresada

        # listado de id de horas extra
        self.listados_id_com = leew.consulta_lista('worker.db', 'id_c', 'comisiones', 'id_c >', '"0"')
        # print(self.listados_id_hora_e)

        # para ordenar y posicionar información
        self.posicion = len(self.listados_id_com)
        # listado de trabajadores

        idies = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        # print(idies)
        for id in idies:
            id = str(id)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id}"')
            trabajador = f"{id} {nombre} {apellido} {cedula}"
            self.trabajador.addItem(trabajador)


        self.agregar.setDisabled(1)

        self.ya_se_puede_cerrar = False

        self.monto.valueChanged.connect(self.set_enable_agregar)
        self.nota.textChanged.connect(self.set_enable_agregar)
        self.cancelar.clicked.connect(self.close)
        self.agregar.clicked.connect(self.guardar_cmd)
        self.borrar.clicked.connect(self.borrar_cmd)

    def advertencia_de_perdida_de_datos(self):
        reply = QtWidgets.QMessageBox.question(self, "Para continuar",
                                               "¿Desea usted continuar? los datos ingresados se perderán"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return 1
        else:
            return 0

    def borrar_cmd(self):
        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted borrar la variación al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            leew.del_gen('worker.db', 'comisiones', 'id_c', f'{self.id_visible.text()} AND computado = 0')
            self.recarga_en_blanco_nuevo_doc()
            # para ordenar y posicionar información
            self.listados_id_com = leew.consulta_lista('worker.db', 'id_c', 'comisiones', 'id_c >', '"0"')
            self.posicion = len(self.listados_id_com)

    def set_enable_agregar(self):
        if self.nota.toPlainText() != '' and self.monto.value() > 0:
            self.agregar.setDisabled(0)
            self.hubo_modificacion = 1
        else:
            self.agregar.setDisabled(1)

    def guardar_cmd(self):
        # determinacion del periodo, esto es solo informativo realmente

        if QtCore.QDate.currentDate().day() < 16:
            self.periodo = "1Q" + QtCore.QDate.currentDate().toString("MMyyyy")
        else:
            self.periodo = "2Q" + QtCore.QDate.currentDate().toString("MMyyyy")

        self.id = self.trabajador.currentText().split(' ')[0]  # con esta linea saco el id de una cadena de texto

        # print(self.periodo)
        self.desc_com = "n/d" # no implementado o usado porque las comisiones son auto explicatorias

        self.entrada = f'NULL,"{QtCore.QDate.currentDate().toString("dd-MM-yyyy")}","{self.id}",' \
                       f'"{self.trabajador.currentText()}","{self.nota.toPlainText()}",' \
                       f'"{self.monto.text()}", 0,NULL,"{self.main_instancia.usuario}","{self.periodo}","{self.desc_com}"'

        # print(self.entrada)

        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted agregar la variación al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.introduce_gen('worker.db', 'comisiones', self.entrada)
                QtWidgets.QMessageBox.information(self, "Atención", "Variación agregada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)
            try:
                self.obj.setDisabled(0)  # vuelvo a habilitar el listado de horas extra
                self.obj2.setDisabled(0)  # el menu o action registro HE lo vuelvo a habilitar
                self.main_instancia.letrero.setText('')  # borra el letrero en el toolbar
            except:
                pass

    def closeEvent(self, QCloseEvent):
        if self.ya_se_puede_cerrar == False:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de salir? Se perderán los datos '
                                                   'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()
                self.parentWidget().close()
                self.obj.setDisabled(0)  # vuelvo a habilitar el listado de horas extra
                self.obj2.setDisabled(0)  # el menu o action registro HE lo vuelvo a habilitar
                self.main_instancia.letrero.setText('')  # borra el letrero en el toolbar
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()