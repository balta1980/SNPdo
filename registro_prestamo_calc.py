from registro_prestamo import *
import leew, imprime_prestamo


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, cmd, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.refrescar_tabla_list_ina = cmd  # este comando viene del listado de horas extras y es para refrescar la tabla
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
        self.period_abono_prestamo = QtCore.QDate.currentDate().toString()
        self.hoy = QtCore.QDate.currentDate()
        #print(self.hoy.addDays(self.hoy.daysInMonth()-self.hoy.day()+1))

        self.listado_periodos_de_pago = []
        self.listado_periodos_de_pago_formato = []

        self.monto.valueChanged.connect(self.calcula_monto_cuota)
        self.cuotas.valueChanged.connect(self.calcula_monto_cuota)
        self.nota.textChanged.connect(self.set_enable_agregar)
        self.cancelar.clicked.connect(self.close)
        self.agregar.clicked.connect(self.guardar_cmd)

    def calcula_monto_cuota(self):
        self.monto_cuotas.setValue(self.monto.value()/self.cuotas.value())

    def determina_listado_periodos_pago_prestamo(self):
        self.listado_periodos_de_pago.append(self.hoy)
        for p in range(self.cuotas.value()):
            self.listado_periodos_de_pago.append(self.proxima_quincena(self.listado_periodos_de_pago[len(self.listado_periodos_de_pago)-1]))
        for p in self.listado_periodos_de_pago:
            if p.day() < 16:
                self.listado_periodos_de_pago_formato.append("1Q" + p.toString("MMyyyy"))
            else:
                self.listado_periodos_de_pago_formato.append("2Q" + p.toString("MMyyyy"))
        #print(self.listado_periodos_de_pago_formato)

    def proxima_quincena(self,fecha):
        if fecha.day() < 16:
            #se convierte en la segunda quincena
            return fecha.addDays(fecha.daysInMonth() - fecha.day())
        else:
            # se convierte en la primera quincena del siguiente mes
            return fecha.addDays(fecha.daysInMonth() - fecha.day() + 1)

    def set_enable_agregar(self):
        if self.nota.toPlainText() != '':
            self.agregar.setDisabled(0)
        else:
            self.agregar.setDisabled(1)

    def guardar_cmd(self):

        self.determina_listado_periodos_pago_prestamo()
        self.id = self.trabajador.currentText().split(' ')[0]  # con esta linea saco el id de una cadena de texto
        self.entrada_prestamo = f'NULL,"{self.id}","{self.monto.text()}","{self.cuotas.text()}", "{self.monto_cuotas.text()}",'\
        f'"{QtCore.QDate.currentDate().toString("dd-MM-yyyy")}","ABIERTO","{self.nota.toPlainText()}",NULL,NULL,NULL '
        #print(self.entrada_prestamo)

        idp = leew.consulta_lista('worker.db','idp', 'prestamos','idp>','0')#para poder poner el id del periodo en la tabla detalles

        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted agregar la variación al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.introduce_gen('worker.db', 'prestamos', self.entrada_prestamo)
                lista_de_idp = leew.consulta_lista('worker.db', 'idp', 'prestamos', 'idp>', '0')
                idp = str(lista_de_idp[len(lista_de_idp) - 1])
                #print(idp)
                #lo de abajo es para eliminar el primer periodo que es cuando se otorga el prestamo
                self.listado_periodos_de_pago_formato = self.listado_periodos_de_pago_formato[1:len(self.listado_periodos_de_pago_formato)]
                for p in self.listado_periodos_de_pago_formato:
                    #op1 = idt = id de trabajador, se me hizo necesario ponerlo
                    #op2 = monto de la cuota, se me hizo necesario
                    fila = f'NULL,"{idp}","{p}","pendiente",{self.id},{self.monto_cuotas.text()},NULL'
                    leew.introduce_gen('worker.db','prestamos_detalles',fila)

                QtWidgets.QMessageBox.information(self, "Atención", "Variación agregada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                if self.imprimir.isChecked():
                    imprime_prestamo.imprime(idp)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)
            try:
                self.refrescar_tabla_list_ina()  # refresco la tabla del listado de horas extra
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
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()