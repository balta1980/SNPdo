from vacaciones import *
import leew, trat_fecha
from datetime import timedelta, datetime, date


class MainWindow(QtWidgets.QMainWindow, Ui_vacaciones):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #llenado de filas
        self. carga_tabla()

        self.dias_de_vac_periodo = []
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.agregar.clicked.connect(self.agregar_command)
        self.cerrar.clicked.connect(self.cerrar_cmd)
        self.checkBox.clicked.connect(self.activar_all)
        # self.comboBox.currentTextChanged.connect(self.calcula_dias_per)
        # self.comboBox.currentTextChanged.connect(self.carga_listado_trabajadores)
        self.dateEdit.dateChanged.connect(self.calcula_dias_per)
        self.siete_dias.clicked.connect(self.calcula_dias_per)
        self.catorce_dias.clicked.connect(self.calcula_dias_per)
        self.otro.clicked.connect(self.calcula_dias_per)
        self.otro_dias.valueChanged.connect(self.calcula_dias_per)
        self.el_dia.clicked.connect(self.calcula_dias_per)
        self.medio_dia.clicked.connect(self.calcula_dias_per)
        self.no_contar.clicked.connect(self.calcula_dias_per)
        self.dateEdit.dateChanged.connect(self.carga_listado_trabajadores)
        self.siete_dias.clicked.connect(self.carga_listado_trabajadores)
        self.catorce_dias.clicked.connect(self.carga_listado_trabajadores)
        self.otro.clicked.connect(self.carga_listado_trabajadores)
        self.otro_dias.valueChanged.connect(self.carga_listado_trabajadores)
        self.medio_dia.clicked.connect(self.carga_listado_trabajadores)
        self.el_dia.clicked.connect(self.carga_listado_trabajadores)
        self.no_contar.clicked.connect(self.carga_listado_trabajadores)
        self.tableWidget.clicked.connect(self.on_click)
        self.siete_dias.clicked.connect(self.activa_otros)
        self.catorce_dias.clicked.connect(self.activa_otros)
        self.otro.clicked.connect(self.activa_otros)
        self.tableWidget.grabKeyboard()
        self.agregar.setDisabled(1)
        self.cancelar.clicked.connect(self.cancelar_cmd)
        self.inactivar_all()
        self.siete_dias.setChecked(1)
        self.el_dia.setChecked(1)
        self.activa_otros()
        #self.show() no se usa cuando uso are MDI

    def carga_tabla(self):
        lista = leew.consulta_lista('worker.db', 'indice', 'vacaciones', 'indice>', '0')

        self.tableWidget.setRowCount(len(lista))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

        n = 0
        for i in lista:
            text = str(i)
            item = str(leew.consultaP2('worker.db', 'indice', 'vacaciones', text)[0])
            self.tableWidget.setItem(n, 0, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'fecha_inicio', 'vacaciones', text)
            self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'lista_dias', 'vacaciones', text)
            self.tableWidget.setItem(n, 2, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'dias', 'vacaciones', text)
            self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'status', 'vacaciones', text)
            self.tableWidget.setItem(n, 4, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'nota', 'vacaciones', text)
            self.tableWidget.setItem(n, 5, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP2('worker.db', 'trabajadores', 'vacaciones', text)
            self.tableWidget.setItem(n, 6, QtWidgets.QTableWidgetItem(item))
            n = n + 1


    def agregar_command(self):
        trabajadores_con_vacaciones = []
        filas = self.trabajadores.count()
        for fila in range(filas):
            if self.trabajadores.item(fila).checkState() == 2:
                trabajadores_con_vacaciones.append(self.trabajadores.item(fila).text())
        trabajadores_con_vacaciones = str(trabajadores_con_vacaciones).replace('[', '').replace(']', '')

        print(trabajadores_con_vacaciones)
        reply = 0
        reply0 = 0

        if trabajadores_con_vacaciones == '':

            advrt0 = "No hay trabajadores seleccionados"
            reply0 = QtWidgets.QMessageBox.warning(self, "Advertencia!", advrt0, QtWidgets.QMessageBox.Ok)
        else:
            advrt = "Antes de agregar un nuevo preriodo vacacional para un año determinado, usted primero debe haber " \
                    "cargado los días no laborables del año en cuestion. Desea Continuar?"
            reply = QtWidgets.QMessageBox.warning(self,"Advertencia!",advrt,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            info = 'NULL,"' + self.dateEdit.date().toString("dd-MM-yyyy") + '","' + str(self.dias_vac()) + '","' + \
                   str(self.dias_de_vac_periodo) + '","ABIERTO","' + self.nota.text() + '","' + str(trabajadores_con_vacaciones) + '"'

            #print(info)
            try:
                leew.introduce_par('vacaciones', info)
                QtWidgets.QMessageBox.information(self, "Atención", "Periodo de vacaciones agregado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)

            self.cerrar_cmd()

    def lista(self,ano,mes,dia,dias_vac):

        lista_dia_no_lab = leew.lista_dia_no_lab()
        #print(lista_dia_no_lab)

        fecha_inicio = date(ano,mes,dia)

        dias_vacaciones = dias_vac

        lista_dias_vac = []

        #self.lista_dias_vac.append(str(fecha_inicio.day) + '-' + str(fecha_inicio.month) + '-' + str(fecha_inicio.year))

        ano, mes, dia, = [str(i) for i in str(fecha_inicio).split('-')] # para que la fecha se formato dd-mm-aaaa

        lista_dias_vac.append(dia + '-' + mes + '-' + ano) # se agrega el primer dia de vac con formato dd-mm-aaaa

        fecha = fecha_inicio

        delta = 1
        while delta < dias_vacaciones:
            #print(delta)
            fecha = fecha + timedelta(days=1)
            #print(fecha)
            ano, mes, dia, = [str(i) for i in str(fecha).split('-')]

            # 0-Lunes, 1-Martes, 2-Miércoles, 3-Jueves, 4-Viernes , 5-Sábado y 6-Domingo
            if dia + '-' + mes + '-' + ano in lista_dia_no_lab or datetime.weekday(datetime(int(ano), int(mes), int(dia), 0, 0, 0)) == 6:
                pass
            else:
                if datetime.weekday(datetime(int(ano), int(mes), int(dia), 0, 0, 0)) == 5:
                    if self.tratar_sabado() == "no contar sab":
                        pass
                    if self.tratar_sabado() == "sabado completo":
                        lista_dias_vac.append(dia + '-' + mes + '-' + ano)
                        delta = delta + 1
                    if self.tratar_sabado() == "medio sabado":
                        lista_dias_vac.append(dia + '-' + mes + '-' + ano)
                        delta = delta + 0.5

                else:
                    lista_dias_vac.append(dia + '-' + mes + '-' + ano)
                    delta = delta + 1


        return str(lista_dias_vac)

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def inactivar_all(self):
        self.frame_6.setDisabled(1)
        self.frame_3.setDisabled(1)
        self.frame_2.setDisabled(1)
        # self.cancelar.setDisabled(1)
        # self.agregar.setDisabled(1)
        # self.comboBox.setDisabled(1)
        # self.dateEdit.setDisabled(1)
        # self.textBrowser.setDisabled(1)
        # self.textEdit.setDisabled(1)
        # self.trabajadores.setDisabled(1)

    def activar_all(self):
        if self.checkBox.isChecked():
            self.tableWidget.releaseKeyboard()
            self.frame_6.setDisabled(0)
            self.frame_3.setDisabled(0)
            self.frame_2.setDisabled(0)
            # self.cancelar.setDisabled(0)
            #self.agregar.setDisabled(0)
            # self.comboBox.setDisabled(0)
            # self.dateEdit.setDisabled(0)
            # self.textBrowser.setDisabled(0)
            # self.textEdit.setDisabled(0)
            # self.trabajadores.setDisabled(0)
            self.cerrar.setDisabled(1)
            self.checkBox.setDisabled(1)

    def dias_vac(self):
        # funcion que retorna la cantidad de días que la empresa quiere dar
        if self.siete_dias.isChecked():
            return 7
        if self.catorce_dias.isChecked():
            return 14
        if self.otro.isChecked():
            return self.otro_dias.value()

    def tratar_sabado(self):
        if self.el_dia.isChecked():
            return "sabado completo"
        if self.medio_dia.isChecked():
            return "medio sabado"
        if self.no_contar.isChecked():
            return "no contar sab"

    def activa_otros(self):
        if self.otro.isChecked():
            self.otro_dias.setDisabled(0)
        else:
            self.otro_dias.setDisabled(1)

    def calcula_dias_per(self):
        if self.dateEdit.date().toString("dd-MM-yyyy") not in leew.lista_dia_no_lab()\
            and self.dateEdit.date().dayOfWeek() != 7: # 7 es el domingo
            dias_vac = self.dias_vac()
            dia = self.dateEdit.date().day()
            mes = self.dateEdit.date().month()
            ano = self.dateEdit.date().year()
            self.dias_de_vac_periodo = self.lista(ano,mes,dia,dias_vac)
            #print(self.dias_de_vac_periodo)
            self.textBrowser.setText(str(self.dias_de_vac_periodo))
            self.agregar.setDisabled(0)
        else:
            QtWidgets.QMessageBox.warning(self, "Error en fecha de inicio de vacaciones",
                                          "La fecha de inicio de vacaciones NO puede ser un domingo o un día feriado. Verifique e intente de nuevo",
                                          QtWidgets.QMessageBox.Ok)
            #self.checkBox.click()  # quita tilde a al checkbox
            self.agregar.setDisabled(1)

    def carga_listado_trabajadores(self):

        self.trabajadores.clear()# para limpiarla cada vez que se modifique con esta funcion

        listado_de_listas_trabajadores_vacaciones_abiertas = leew.consulta_lista('worker.db','trabajadores','vacaciones', 'status','"ABIERTO"')
        #print(listado_de_listas_trabajadores_vacaciones_abiertas)
        trabajadores_con_vac_abiertas = set() #un set o conjunto para poner a los trabajaores con vacaciones abiertas
        if listado_de_listas_trabajadores_vacaciones_abiertas != []:#solo si hay vacaciones abiertas
            for listado in listado_de_listas_trabajadores_vacaciones_abiertas:
                #print(listado)
                listado = listado.split("',")

                for trabajador in listado:
                    #print(trabajador.split(",")[0].replace("'", ""))
                    trabajadores_con_vac_abiertas.add(trabajador.split(",")[0].replace("'", "").replace(" ",""))# para limpiar los i de los trabajadores sorry :(
        #print(trabajadores_con_vac_abiertas)
        list_id_trab_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')


        fila = 0
        for id in list_id_trab_activos:
            if str(id) not in trabajadores_con_vac_abiertas:# que el trabajador no tenga ya programada una vacacion
                nombre = leew.consulta_gen('worker.db','Nombre','info','id',f'"{id}"')
                nombre2 = leew.consulta_gen('worker.db','nombre2','info','id',f'"{id}"')
                apellido = leew.consulta_gen('worker.db','Apellido','info','id',f'"{id}"')
                apellido2 = leew.consulta_gen('worker.db', 'apellido2', 'info', 'id', f'"{id}"')
                doc = leew.consulta_gen('worker.db','Identificacion','info','id',f'"{id}"')
                self.trabajadores.addItem(f"{id}, {nombre}, {nombre2}, {apellido}, {apellido2}, {doc}")

                #lo de abajo es para poner letra en rojo de trab con menos de un anio de servicio
                fecha_ingreso = leew.consulta_gen('worker.db', 'fecha_ingreso', 'info', 'id',f'"{id}"')
                dia, mes, anio = [int(v) for v in fecha_ingreso.split("-")]
                fecha_ing_datetype = date(anio, mes, dia)
                #esta funcion de abajo usa clases date de python
                tiempo_servicio = trat_fecha.calcular_ano_f(fecha_ing_datetype, date(self.dateEdit.date().year(),
                                                                                     self.dateEdit.date().month(),
                                                                                     self.dateEdit.date().day()))
                if tiempo_servicio < 1:
                    self.trabajadores.item(fila).setBackground(QtGui.QColor('red'))
                    self.trabajadores.item(fila).setToolTip(f"Fecha de ingreso del trabajador: {fecha_ingreso}, todavía "
                                                            f"no cumple un año de trabajo en la empresa.")
                fila = fila + 1

        # de aqui para abajo hace que a los trabajadores les salga el tilde
        cant_filas = self.trabajadores.count()

        for item in range(cant_filas): # para hacer que sea tildable cada trabajador
            self.trabajadores.item(item).setCheckState(2) # 2 es tildado 1 semitildado 0 no tildado

    def cancelar_cmd(self):
        reply = QtWidgets.QMessageBox.question(self, "Desea cancelar?", "Se perderá la información suministrada. Continuar?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()
            self.parentWidget().close()

    def eliminar_cmd(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems(): # con este iterador puedo usar las celdas selecionadas
            reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted eliminar el perido con ID: " + \
                                           currentQTableWidgetItem.text() + " y fecha de inicio: "+ \
                                                   str(self.tableWidget.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column() + 1).text()) + "?"
                                           , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    #print(currentQTableWidgetItem.text())
                    leew.del_vac(currentQTableWidgetItem.text())
                    QtWidgets.QMessageBox.information(self, "Atención", "Fecha borrada satisfactoriamente",
                                                      QtWidgets.QMessageBox.Ok)
                    self.carga_tabla()
                except:
                    QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)
            break # esto se pone para que no siga iterando si se selecciona una fila y no una celda

    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            if currentQTableWidgetItem.column() == 0:
                status, = leew.consultaP2('worker.db', 'status', 'vacaciones', currentQTableWidgetItem.text())
                if status == 'ABIERTO':
                    self.eliminar_cmd()
                    #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

