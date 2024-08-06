from inasis import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,obj, obj2, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.fecha_doc.setDate(QtCore.QDate.currentDate())
        self.borrar.setDisabled(True)
        self.id_visible.setDisabled(True)

        self.aviso = QtWidgets.QLabel("") # para poner un aviso si el trabajador faltó ya en el mes
        self.statusbar.addWidget(self.aviso)

        self.hubo_modificacion = 0  # para avisar al usuario que va a perder la informació ingresada

        # listado de id de horas extra
        self.listados_id_ina = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id_i >', '"0"')
        # print(self.listados_id_hora_e)

        # para ordenar y posicionar información
        self.posicion = len(self.listados_id_ina)

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

        self.define_fecha()
        self.fija_horas()
        self.cargar_data()
        self.calcula_ina()

        self.agregar.setDisabled(1)

        self.ya_se_puede_cerrar = False

        self.tipoina.setCurrentIndex(1) #para que salga INJUSTIFICADA por defecto

        self.fechai.dateTimeChanged.connect(self.calcula_ina)
        self.fechaf.dateTimeChanged.connect(self.calcula_ina)
        self.fechai.dateChanged.connect(self.fija_horas)
        self.fechaf.dateChanged.connect(self.fija_horas)
        self.fechai.dateChanged.connect(self.determina_falta_previa_en_el_mes)

        self.trabajador.currentTextChanged.connect(self.define_fecha)
        self.trabajador.currentTextChanged.connect(self.cargar_data)
        self.trabajador.currentTextChanged.connect(self.calcula_ina)

        self.nota.textChanged.connect(self.set_enable_agregar)
        self.inasis.textChanged.connect(self.set_enable_agregar)
        self.cancelar.clicked.connect(self.close)
        self.agregar.clicked.connect(self.guardar_cmd)
        self.borrar.clicked.connect(self.borrar_cmd)
        self.borrar.setDisabled(True)

    def probador_de_instancia_para_toolbar(self):
        # comparo si el nombre subventana activa es igual al nombre de esta ventana ("Registro de inasistencia")
        if self.main_instancia.mdiArea.currentSubWindow().windowTitle() == self.windowTitle():
            return True

    def manejador_toolbar_nav_izquierda(self):
        if self.probador_de_instancia_para_toolbar():
            if len(self.listados_id_ina) > 0:  # verifica que la bd no está vacia
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.hubo_modificacion = 0
                        if self.posicion == 0:
                            self.posicion = len(self.listados_id_ina) - 1
                        else:
                            self.posicion = self.posicion - 1
                        self.muestra_historial(self.listados_id_ina[self.posicion])
                else:
                    if self.posicion == 0:
                        self.posicion = len(self.listados_id_ina) - 1
                    else:
                        self.posicion = self.posicion - 1
                    self.muestra_historial(self.listados_id_ina[self.posicion])

    def manejador_toolbar_nav_derecha(self):
        if self.probador_de_instancia_para_toolbar():
            if len(self.listados_id_ina) > 0:  # verifica que la bd no está vacia
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        if self.posicion >= len(self.listados_id_ina) - 1:
                            self.posicion = 0
                        else:
                            self.posicion = self.posicion + 1

                        self.muestra_historial(self.listados_id_ina[self.posicion])
                else:
                    if self.posicion >= len(self.listados_id_ina) - 1:
                        self.posicion = 0
                    else:
                        self.posicion = self.posicion + 1

                    self.muestra_historial(self.listados_id_ina[self.posicion])

    def manejador_toolbar_nav_izq_fin(self):
        if self.probador_de_instancia_para_toolbar():
            if len(self.listados_id_ina) > 0:  # verifica que la bd no está vacia
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.posicion = 0
                        self.muestra_historial(self.listados_id_ina[0])
                else:
                    self.posicion = 0
                    self.muestra_historial(self.listados_id_ina[0])

    def manejador_toolbar_nav_derecha_fin(self):
        if self.probador_de_instancia_para_toolbar():
            if len(self.listados_id_ina) > 0:  # verifica que la bd no está vacia
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.posicion = len(self.listados_id_ina) - 1
                        self.muestra_historial(self.listados_id_ina[self.posicion])
                else:
                    self.posicion = len(self.listados_id_ina) - 1
                    self.muestra_historial(self.listados_id_ina[self.posicion])

    def manejador_boton_nuevo(self):
        if self.probador_de_instancia_para_toolbar():
            if self.hubo_modificacion == 1:
                if self.advertencia_de_perdida_de_datos() == 1:
                    self.recarga_en_blanco_nuevo_doc()
            else:
                self.recarga_en_blanco_nuevo_doc()

    def muestra_historial(self, id_ina):
        # carga la pantalla con la info de la BD al usar los botenes de flechas
        # print(id_hora_extra)
        try:  # uso este captyrador de error para que no cargue la data
            # print(self.trabajador.isSignalConnected(self.carga_data))
            self.fechai.dateTimeChanged.disconnect(self.calcula_ina)
            self.fechaf.dateTimeChanged.disconnect(self.calcula_ina)
            self.fechai.dateChanged.disconnect(self.fija_horas)
            self.fechaf.dateChanged.disconnect(self.fija_horas)
            self.trabajador.currentTextChanged.disconnect(self.define_fecha)
            self.trabajador.currentTextChanged.disconnect(self.cargar_data)
            self.trabajador.currentTextChanged.disconnect(self.calcula_ina)
            self.nota.textChanged.disconnect(self.set_enable_agregar)
            self.inasis.textChanged.disconnect(self.set_enable_agregar)
            #self.cancelar.clicked.connect(self.close)
            self.agregar.clicked.disconnect(self.guardar_cmd)

        except:
            pass
        self.agregar.setDisabled(True)
        self.id_visible.setText(f'{id_ina}')

        # fecha de computo
        data = leew.consulta_gen('worker.db', 'fecha_doc', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.fecha_doc.setDate(QtCore.QDate(1900, 1, 1))
        else:
            self.fecha_doc.setDate(
                QtCore.QDate(int(data.split('-')[2]), int(data.split('-')[1]), int(data.split('-')[0])))
        self.fecha_doc.setDisabled(True)

        # nombre trabajador
        data = leew.consulta_gen('worker.db', 'nombre_trab', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            data = 'N/D'
        self.trabajador.setCurrentText(data)
        self.trabajador.setDisabled(True)

        # salario mensual
        data = leew.consulta_gen('worker.db', 'sal_mensual', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            data = 'N/D'
        # print(type(data))
        self.sal_mensual.setText(str(data))
        self.sal_mensual.setDisabled(True)

        # salario diario
        data = leew.consulta_gen('worker.db', 'sal_hora', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            data = 'N/D'
        # print(type(data))
        self.sal_hora.setText(str(data))
        self.sal_hora.setDisabled(True)

        # tipo inasis
        data = leew.consulta_gen('worker.db', 'tipo', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            data = 'N/D'
        # print(type(data))
        self.tipoina.setCurrentText(data)
        self.tipoina.setDisabled(True)

        #fecha inicio
        data = leew.consulta_gen('worker.db', 'fecha_i', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.fechai.setDate(QtCore.QDate(1900, 1, 1))
        else:
            self.fechai.setDate(
                QtCore.QDate(int(data.split('-')[2]), int(data.split('-')[1]), int(data.split('-')[0])))
        self.fechai.setDisabled(True)

        #hora inicio

        data = leew.consulta_gen('worker.db', 'hora_i', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.fechai.setTime(QtCore.QTime(0, 0, 0))
        else:
            self.fechai.setTime(
                QtCore.QTime(int(data.split(':')[0]), int(data.split(':')[1])))
        self.fechai.setDisabled(True)

        # fecha fin
        data = leew.consulta_gen('worker.db', 'fecha_f', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.fechaf.setDate(QtCore.QDate(1900, 1, 1))
        else:
            self.fechaf.setDate(
                QtCore.QDate(int(data.split('-')[2]), int(data.split('-')[1]), int(data.split('-')[0])))
        self.fechaf.setDisabled(True)

        # hora fin

        data = leew.consulta_gen('worker.db', 'hora_f', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.fechaf.setTime(QtCore.QTime(0, 0, 0))
        else:
            self.fechaf.setTime(
                QtCore.QTime(int(data.split(':')[0]), int(data.split(':')[1])))
        self.fechaf.setDisabled(True)

        # nota
        data = leew.consulta_gen('worker.db', 'nota', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.nota.setText("N/D")
        else:
            self.nota.setText(data)
        self.nota.setDisabled(True)

        # dias falta
        data = leew.consulta_gen('worker.db', 'dias', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.inasis.setText("N/D")
        else:
            self.inasis.setText(str(data))
        self.inasis.setDisabled(True)

        # horas falta
        data = leew.consulta_gen('worker.db', 'horas', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.horas_inasis.setText("N/D")
        else:
            self.horas_inasis.setText(str(data))
        self.horas_inasis.setDisabled(True)

        # monto
        data = leew.consulta_gen('worker.db', 'monto', 'inasis', 'id_i', f'{id_ina}')
        if data == None:
            self.tota_inasis.setText("N/D")
        else:
            self.tota_inasis.setText(str(data))
        self.tota_inasis.setDisabled(True)

        # para habilitar el borrado de la ina
        status_ina = leew.consulta_gen('worker.db', 'computado', 'inasis', 'id_i', f'{id_ina}')
        if status_ina == 0:

            self.borrar.setDisabled(False)
        else:
            self.borrar.setDisabled(True)

        # aviso
        self.aviso.setText("")

    def recarga_en_blanco_nuevo_doc(self, *args, **kwargs):
        self.setupUi(self)
        self.fecha_doc.setDate(QtCore.QDate.currentDate())
        self.borrar.setDisabled(True)
        self.id_visible.setDisabled(True)

        self.aviso = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.aviso)

        self.hubo_modificacion = 0  # para avisar al usuario que va a perder la informació ingresada

        # listado de id de horas extra
        self.listados_id_ina = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id_i >', '"0"')
        # print(self.listados_id_hora_e)

        # para ordenar y posicionar información
        self.posicion = len(self.listados_id_ina)
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

        self.define_fecha()
        self.fija_horas()
        self.cargar_data()
        self.calcula_ina()

        self.agregar.setDisabled(1)

        self.ya_se_puede_cerrar = False

        self.tipoina.setCurrentIndex(1)  # para que salga INJUSTIFICADA por defecto

        self.fechai.dateTimeChanged.connect(self.calcula_ina)
        self.fechaf.dateTimeChanged.connect(self.calcula_ina)
        self.fechai.dateChanged.connect(self.fija_horas)
        self.fechaf.dateChanged.connect(self.fija_horas)
        self.fechai.dateChanged.connect(self.determina_falta_previa_en_el_mes)

        self.trabajador.currentTextChanged.connect(self.define_fecha)
        self.trabajador.currentTextChanged.connect(self.cargar_data)
        self.trabajador.currentTextChanged.connect(self.calcula_ina)

        self.nota.textChanged.connect(self.set_enable_agregar)
        self.inasis.textChanged.connect(self.set_enable_agregar)
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
        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted borrar la inasistencia al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            leew.del_gen('worker.db', 'inasis', 'id_i', f'{self.id_visible.text()} AND computado = 0')
            self.recarga_en_blanco_nuevo_doc()
            # para ordenar y posicionar información
            self.listados_id_ina = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id_i >', '"0"')
            self.posicion = len(self.listados_id_ina)

    def cargar_data(self):
        #poner carga de salarios
        self.id = self.trabajador.currentText().split(' ')[0]  # con esta linea saco el id de una cadena de texto
        self.salario = leew.consulta_gen('worker.db', 'salario', 'salario', 'id', f'"{self.id}" AND status = "Vigente"')
        self.sal_mensual.setText(str("{:,.2f}".format(self.salario)))
        self.dias_por_mes = leew.consulta_gen('worker.db', 'dias_mes', 'beneficios', 'status', f'"Vigente"')
        self.horas_dia = leew.consulta_gen('worker.db', 'horas_dia', 'beneficios', 'status', f'"Vigente"')
        self.sal_hora.setText(str("{:,.2f}".format(self.salario / self.dias_por_mes / self.horas_dia)))
        self.determina_falta_previa_en_el_mes()

    def calcula_ina(self):

        # calcula la diferencia de horas extras

        dif_hora = self.fechaf.time().hour() - self.fechai.time().hour()
        dif_min = self.fechaf.time().minute() - self.fechai.time().minute()
        dif_dia = self.fechai.date().daysTo(self.fechaf.date()) # funcion fecha-inicial.daysTo(fecha-final)
        #print(dif_dia)
        #print(dif_hora)
        #print(dif_min)
        
        if self.fechai.dateTime() > self.fechaf.dateTime(): # la hora de salida no puede ser menor a la de llegada
            self.inasis.setText('Fechas/Horas inválidas')
            self.horas_inasis.setText('Fechas/Horas inválidas')
            self.tota_inasis.setText('Fechas/Horas inválidas')
        else:
            # esto para restar la hora del medio día
            if (self.fechai.time().hour() >= 12 and self.fechaf.time().hour() >= 12) or \
                    (self.fechai.time().hour() <= 12 and self.fechaf.time().hour() <= 12) :
                self.inasis.setText(str(round(dif_dia + dif_hora / 8 + dif_min / 60 / 8,4)))
                self.horas_inasis.setText(str(round(dif_dia * 8 + dif_hora + dif_min / 60,4)))
            else:
                self.inasis.setText(str(round(dif_dia + dif_hora / 8 + dif_min / 60 / 8 - 1 / 8, 4)))
                self.horas_inasis.setText(str(round(dif_dia * 8 + dif_hora + dif_min / 60 - 1, 4)))

            self.tota_inasis.setText(str("{:,.2f}".format(self.salario / self.dias_por_mes / self.horas_dia
                                                          * float(self.horas_inasis.text()))))

    def define_fecha(self):
        # hace que la minima fecha seleccionable sea la fecha de ingreso del trabajador
        self.id = self.trabajador.currentText().split(' ')[0] # con esta linea saco el id de una cadena de texto
        fecha_ingreso = leew.consulta_gen('worker.db','Fecha_ingreso','info', 'id', f'"{self.id}"')
        #print(fecha_ingreso)
        dia, mes, ano = fecha_ingreso.split('-')
        self.fechai.setMinimumDate(QtCore.QDate(int(ano),int(mes),int(dia))) # fijo como dia minimo el ingreso
        self.fechai.setDate(QtCore.QDate.currentDate()) # fijo el dia actual como fecha
        self.fechaf.setMinimumDate(QtCore.QDate(int(ano), int(mes), int(dia)))  # fijo como dia minimo el ingreso
        self.fechaf.setDate(QtCore.QDate.currentDate())  # fijo el dia actual como fecha

    def fija_horas(self):
        # con esta funcion dependiendo del día se fija una hora de salida tal cual el horario de trabajo
        # lunes 1, martes 2, miercoles 3, jueves 4, viernes 5, sabado 6, domingo 7
        self.fechai.setMinimumTime(QtCore.QTime(7, 0, 0))
        self.fechai.setTime(QtCore.QTime(7, 0, 0))
        if self.fechaf.date().dayOfWeek() < 5: # de lunes a jueves
            self.fechaf.setMinimumTime(QtCore.QTime(17, 0, 0))
            self.fechaf.setTime(QtCore.QTime(17, 0, 0))
        else:
            if self.fechaf.date().dayOfWeek() < 6:# viernes
                self.fechaf.setMinimumTime(QtCore.QTime(16, 0, 0))
                self.fechaf.setTime(QtCore.QTime(16, 0, 0))
            else:# sabado y domingo
                self.fechaf.setMaximumTime(QtCore.QTime(12, 0, 0))
                self.fechaf.setTime(QtCore.QTime(12, 0, 0))

    def set_enable_agregar(self):
        if self.inasis.text() != '' and self.inasis.text() != 'Fechas/Horas inválidas' and \
            self.inasis.text() != '0.0' and self.nota.text() != '':
            self.agregar.setDisabled(0)
            self.hubo_modificacion = 1 # para que cuando se vaya a navegar se pregunte si desea perder la data
        else:
            self.agregar.setDisabled(1)

    def guardar_cmd(self):
        # determinacion del periodo, esto es solo informativo realmente

        if self.fechai.date().day() < 16:
            self.periodo = "1Q" + self.fechai.dateTime().toString("MMyyyy")
        else:
            self.periodo = "2Q" + self.fechai.dateTime().toString("MMyyyy")

        #print(self.periodo)
        self.desc_ina = f'Valor descontado(DOP): {self.tota_inasis.text().replace(",","")} días descontados: {self.inasis.text()} del día: ' \
                        f'{self.fechai.dateTime().toString("dd-MM-yyyy")} al día: {self.fechai.dateTime().toString("dd-MM-yyyy")}' \
                        f' hora inicial: {self.fechai.dateTime().toString("hh:mm")} hora final: {self.fechaf.dateTime().toString("hh:mm")}'

        self.entrada = f'"{self.fecha_doc.dateTime().toString("dd-MM-yyyy")}", NULL,"{self.trabajador.currentText()}",' \
                       f'"{self.sal_mensual.text()}","{self.sal_hora.text()}","{self.tipoina.currentText()}", ' \
                       f'"{self.fechai.dateTime().toString("dd-MM-yyyy")}","{self.fechai.dateTime().toString("hh:mm")}",' \
                       f'"{self.fechaf.dateTime().toString("dd-MM-yyyy")}","{self.fechaf.dateTime().toString("hh:mm")}",' \
                       f'"{self.nota.text()}","{self.inasis.text()}","{self.horas_inasis.text()}","{self.tota_inasis.text().replace(",","")}",' \
                       f'"{self.periodo}", "{self.id}", 0,NULL,"{self.desc_ina}", "{self.main_instancia.usuario}"'


        #print(self.entrada)

        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted agregar la variación al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.introduce_gen('worker.db','inasis',self.entrada)
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

    def determina_falta_previa_en_el_mes(self):
        # deternminar mes donde se pretende incluir HE
        mes_actual = self.fechai.date().month()
        anio_actual = self.fechai.date().year()

        # print(mes)
        # saca listado de dias inasistencias anteriores
        lista_ina_anteriores = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id',
                                                  f'"{self.id}"')
        # print(lista_ina_anteriores)
        total_dias = 0
        for id_ina in lista_ina_anteriores:
            # determino la semana sea la misma de la que se va a agregar
            fecha_ina = leew.consulta_gen('worker.db', 'fecha_i', 'inasis', 'id_i', f'"{id_ina}"')
            dia, mes, anio = [int(i) for i in fecha_ina.split('-')]
            mes = QtCore.QDate(anio, mes, dia).month()
            anio = QtCore.QDate(anio, mes, dia).year()
            mes_anio = (mes, anio)
            if (mes_actual, anio_actual) == mes_anio:
                dias = leew.consulta_gen('worker.db', 'dias', 'inasis', 'id_i', f'"{id_ina}"')
                # print(dia, mes, anio)
                total_dias = total_dias + dias

        if total_dias > 0:
            self.aviso.setText(f" HA FALTADO EN EL MES UN EQUIVALENTE EN DÍAS IGUAL A: {total_dias} ")
            self.aviso.setStyleSheet("background:#FA5858 ;border-radius:3;")
        else:
            self.aviso.setText(f"")
            self.aviso.setStyleSheet("background:None ;border-radius:3;")

    def closeEvent(self, QCloseEvent):
        if self.ya_se_puede_cerrar == False:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia', '¿Está usted seguro de salir? Se perderán los datos '
                                                                        'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                         QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()
                self.parentWidget().close()
                self.obj.setDisabled(0)  # vuelvo a habilitar el listado de horas extra
                self.obj2.setDisabled(0)  # el menu o action registro HE lo vuelvo a habilitar
                self.main_instancia.letrero.setText('') # borra el letrero en el toolbar
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()