from horas_extra import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,obj, obj2, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.id_h_visible.setDisabled(True)
        self.borrar.clicked.connect(self.borrar_cmd)
        self.borrar.setDisabled(True)
        self.fecha_doc.setDate(QtCore.QDate.currentDate())

        self.hubo_modificacion = 0 # para avisar al usuario que va a perder la informació ingresada

        # listado de id de horas extra
        self.listados_id_hora_e  = leew.consulta_lista('worker.db', 'id_h', 'horas_extras', 'id_h >', '"0"')
        #print(self.listados_id_hora_e)

        # para ordenar y posicionar información
        self.posicion = len(self.listados_id_hora_e)

        # para controlar desde menu de afuera
        self.main_instancia = args[0]
        self.main_instancia.flecha_izq.triggered.connect(self.manejador_toolbar_nav_izquierda)
        self.main_instancia.flecha_der.triggered.connect(self.manejador_toolbar_nav_derecha)
        self.main_instancia.flecha_izq_fin.triggered.connect(self.manejador_toolbar_nav_izq_fin)
        self.main_instancia.flecha_der_fin.triggered.connect(self.manejador_toolbar_nav_derecha_fin)

        self.obj = obj  # para poder habilitar el menu listado HE
        self.obj2 = obj2  # para poder habilitar el menu registro HE
        self.main_instancia.nuevo_doc.triggered.connect(self.manejador_boton_nuevo)

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

        self.hora_extra.setText('0')
        self.hora_extra_doble.setText('0')
        self.hora_extra_noct.setText('0')

        self.aviso = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.aviso)

        self.carga_porcentajes()

        self.carga_data()

        self.calcula_hora()
        self.agregar.setDisabled(1)

        self.ya_se_puede_cerrar = False

        self.trabajador.currentTextChanged.connect(self.carga_data)
        self.hora_i.timeChanged.connect(self.calcula_hora)
        self.hora_f.timeChanged.connect(self.calcula_hora)
        self.hora_i.timeChanged.connect(self.suma_gran_total)
        self.hora_f.timeChanged.connect(self.suma_gran_total)
        self.trabajador.currentTextChanged.connect(self.define_fecha)
        self.nota.textChanged.connect(self.set_enable_agregar)
        self.gran_total.valueChanged.connect(self.set_enable_agregar)
        self.trabajo_en_descanso.clicked.connect(self.verificador_trabajo_en_descanso)
        self.fecha.dateChanged.connect(self.determina_tope_24h_semanal)
        self.fecha.dateChanged.connect(self.determina_tope_80h_trimestral)
        self.cancelar.clicked.connect(self.close)
        self.agregar.clicked.connect(self.guardar_cmd)

    def probador_de_instancia_para_toolbar(self):
        # comparo si el nombre subventana activa es igual al nombre de esta ventana ("Registro de inasistencia")
        if self.main_instancia.mdiArea.currentSubWindow().windowTitle() == self.windowTitle():
            return True

    def manejador_toolbar_nav_izquierda(self):
        if len(self.listados_id_hora_e) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.hubo_modificacion = 0
                        if self.posicion == 0:
                            self.posicion = len(self.listados_id_hora_e) - 1
                        else:
                            self.posicion = self.posicion - 1
                        self.muestra_historial(self.listados_id_hora_e[self.posicion])
                else:
                    if self.posicion == 0:
                        self.posicion = len(self.listados_id_hora_e) - 1
                    else:
                        self.posicion = self.posicion - 1
                    self.muestra_historial(self.listados_id_hora_e[self.posicion])

    def manejador_toolbar_nav_derecha(self):
        if len(self.listados_id_hora_e) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        if self.posicion >= len(self.listados_id_hora_e) - 1:
                            self.posicion = 0
                        else:
                            self.posicion = self.posicion + 1

                        self.muestra_historial(self.listados_id_hora_e[self.posicion])
                else:
                    if self.posicion >= len(self.listados_id_hora_e) - 1:
                        self.posicion = 0
                    else:
                        self.posicion = self.posicion + 1

                    self.muestra_historial(self.listados_id_hora_e[self.posicion])

    def manejador_toolbar_nav_izq_fin(self):
        if len(self.listados_id_hora_e) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.posicion = 0
                        self.muestra_historial(self.listados_id_hora_e[0])
                else:
                    self.posicion = 0
                    self.muestra_historial(self.listados_id_hora_e[0])

    def manejador_toolbar_nav_derecha_fin(self):
        if len(self.listados_id_hora_e) > 0:  # verifica que la bd no está vacia
            if self.probador_de_instancia_para_toolbar():
                if self.hubo_modificacion == 1:
                    if self.advertencia_de_perdida_de_datos() == 1:
                        self.posicion = len(self.listados_id_hora_e) - 1
                        self.muestra_historial(self.listados_id_hora_e[self.posicion])
                else:
                    self.posicion = len(self.listados_id_hora_e) - 1
                    self.muestra_historial(self.listados_id_hora_e[self.posicion])

    def manejador_boton_nuevo(self):
        if self.probador_de_instancia_para_toolbar():
            if self.hubo_modificacion == 1:
                if self.advertencia_de_perdida_de_datos() == 1:
                    self.recarga_en_blanco_nuevo_doc()
            else:
                self.recarga_en_blanco_nuevo_doc()

    def muestra_historial(self, id_hora_extra):
        # carga la pantalla con la info de la BD al usar los botenes de flechas
        #print(id_hora_extra)
        try: # uso este captyrador de error para que no cargue la data
            #print(self.trabajador.isSignalConnected(self.carga_data))
            self.trabajador.currentTextChanged.disconnect(self.carga_data)
            self.hora_i.timeChanged.disconnect(self.calcula_hora)
            self.hora_f.timeChanged.disconnect(self.calcula_hora)
            self.hora_i.timeChanged.disconnect(self.suma_gran_total)
            self.hora_f.timeChanged.disconnect(self.suma_gran_total)
            self.trabajador.currentTextChanged.disconnect(self.define_fecha)
            self.nota.textChanged.disconnect(self.set_enable_agregar)
            self.gran_total.valueChanged.disconnect(self.set_enable_agregar)
            self.trabajo_en_descanso.clicked.disconnect(self.verificador_trabajo_en_descanso)
            self.fecha.dateChanged.disconnect(self.determina_tope_24h_semanal)
            self.fecha.dateChanged.disconnect(self.determina_tope_80h_trimestral)
            #self.cancelar.clicked.disconnect(self.close)
            self.agregar.clicked.disconnect(self.guardar_cmd)

        except:
            pass

        self.agregar.setDisabled(True)

        self.id_h_visible.setText(f'{id_hora_extra}')

        # fecha de computo
        data = leew.consulta_gen('worker.db', 'fecha_doc', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.fecha_doc.setDate(QtCore.QDate(1900,1,1))
        else:
            self.fecha_doc.setDate(QtCore.QDate(int(data.split('-')[2]), int(data.split('-')[1]), int(data.split('-')[0])))
        self.fecha_doc.setDisabled(True)

        # nombre trabajador
        data = leew.consulta_gen('worker.db', 'trab_nombre','horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            data = 'N/D'
        self.trabajador.setCurrentText(data)
        self.trabajador.setDisabled(True)

        # salario mensual
        data = leew.consulta_gen('worker.db', 'sal_mensual', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            data = 'N/D'
        #print(type(data))
        self.salario_mensual.setText(str(data))
        self.salario_mensual.setDisabled(True)

        # salario diario
        data = leew.consulta_gen('worker.db', 'sal_hora', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            data = 'N/D'
        #print(type(data))
        self.salario_hora.setText(str(data))
        self.salario_hora.setDisabled(True)

        # tipo hora extra
        data = leew.consulta_gen('worker.db', 'tipo', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            data = 'N/D'
        # print(type(data))
        self.tipohoraextra.setCurrentText(data)
        self.tipohoraextra.setDisabled(True)

        # fecha de ocurrencia
        data = leew.consulta_gen('worker.db', 'fecha', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.fecha.setDate(QtCore.QDate(1900, 1, 1))
        else:
            self.fecha.setDate(
                QtCore.QDate(int(data.split('-')[2]), int(data.split('-')[1]), int(data.split('-')[0])))
        self.fecha.setDisabled(True)

        # hora inicial
        data = leew.consulta_gen('worker.db', 'hora_i', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.hora_i.setTime(QtCore.QTime(0,0,0))
        else:
            self.hora_i.setTime(
                QtCore.QTime(int(data.split(':')[0]), int(data.split(':')[1])))
        self.hora_i.setDisabled(True)

        # hora final
        data = leew.consulta_gen('worker.db', 'hora_f', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.hora_f.setTime(QtCore.QTime(0, 0, 0))
        else:
            self.hora_f.setTime(
                QtCore.QTime(int(data.split(':')[0]), int(data.split(':')[1])))
        self.hora_f.setDisabled(True)

        # nota
        data = leew.consulta_gen('worker.db', 'nota', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.nota.setText("N/D")
        else:
            self.nota.setText(data)
        self.nota.setDisabled(True)

        # trabajo en sobretiempo
        data = leew.consulta_gen('worker.db', 'dia_desc_trab', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            pass
        else:
            self.trabajo_en_descanso.setChecked(data)
        self.trabajo_en_descanso.setDisabled(True)

        # horas extra
        data = leew.consulta_gen('worker.db', 'horas', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.hora_extra.setText('N/D')
        else:
            self.hora_extra.setText(str(data))
        self.hora_extra.setDisabled(True)

        # horas extra exceso
        data = leew.consulta_gen('worker.db', 'horas_exceso', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.hora_extra_doble.setText('N/D')
        else:
            self.hora_extra_doble.setText(str(data))
        self.hora_extra_doble.setDisabled(True)

        # horas nocturnas
        data = leew.consulta_gen('worker.db', 'horas_he_noct', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.hora_extra_noct.setText('N/D')
        else:
            self.hora_extra_noct.setText(str(data))
        self.hora_extra_noct.setDisabled(True)

        # porcentaje he
        data = leew.consulta_gen('worker.db', 'porc_he', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.porc_hora_extra.setText('N/D')
        else:
            self.porc_hora_extra.setText(str(data))
        self.porc_hora_extra.setDisabled(True)

        # porcentaje he exceso
        data = leew.consulta_gen('worker.db', 'porc_he_exceso', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.porc_hora_extra_exceso.setText('N/D')
        else:
            self.porc_hora_extra_exceso.setText(str(data))
        self.porc_hora_extra_exceso.setDisabled(True)

        # porcentaje he noct
        data = leew.consulta_gen('worker.db', 'porc_he_noct', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.porc_nocturno.setText('N/D')
        else:
            self.porc_nocturno.setText(str(data))
        self.porc_nocturno.setDisabled(True)

        # total he
        data = leew.consulta_gen('worker.db', 'valor_he', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.total_he_normal.setValue(0.00)
        else:
            self.total_he_normal.setValue(data)
        self.total_he_normal.setDisabled(True)

        # total he exceso
        data = leew.consulta_gen('worker.db', 'valor_he_exceso', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.total_he_doble_exceso.setValue(0.00)
        else:
            self.total_he_doble_exceso.setValue(data)
        self.total_he_doble_exceso.setDisabled(True)

        # total he noct
        data = leew.consulta_gen('worker.db', 'valor_he_noct', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.total_he_nocturno.setValue(0.00)
        else:
            self.total_he_nocturno.setValue(data)
        self.total_he_nocturno.setDisabled(True)

        # gran total
        data = leew.consulta_gen('worker.db', 'total', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if data == None:
            self.gran_total.setValue(0.00)
        else:
            self.gran_total.setValue(data)
        self.gran_total.setDisabled(True)

        self.aviso.setText("")

        status_he = leew.consulta_gen('worker.db', 'computado', 'horas_extras', 'id_h', f'{id_hora_extra}')
        if status_he == 0:
            self.borrar.setDisabled(False)
        else:
            self.borrar.setDisabled(True)

    def recarga_en_blanco_nuevo_doc(self, *args, **kwargs):
        # funcion usada para crear nuevo documento refrescando el formulario
        #QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        # para ordenar y posicionar información
        self.posicion = len(self.listados_id_hora_e)
        self.hubo_modificacion = 0
        self.id_h_visible.setDisabled(True)
        self.borrar.clicked.connect(self.borrar_cmd)
        self.borrar.setDisabled(True)
        self.fecha_doc.setDate(QtCore.QDate.currentDate())

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

        self.hora_extra.setText('0')
        self.hora_extra_doble.setText('0')
        self.hora_extra_noct.setText('0')

        self.aviso = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.aviso)

        self.carga_porcentajes()

        self.carga_data()

        self.calcula_hora()
        self.agregar.setDisabled(1)

        #self.ya_se_puede_cerrar = False

        self.trabajador.currentTextChanged.connect(self.carga_data)
        self.hora_i.timeChanged.connect(self.calcula_hora)
        self.hora_f.timeChanged.connect(self.calcula_hora)
        self.hora_i.timeChanged.connect(self.suma_gran_total)
        self.hora_f.timeChanged.connect(self.suma_gran_total)
        self.trabajador.currentTextChanged.connect(self.define_fecha)
        self.nota.textChanged.connect(self.set_enable_agregar)
        self.gran_total.valueChanged.connect(self.set_enable_agregar)
        self.trabajo_en_descanso.clicked.connect(self.verificador_trabajo_en_descanso)
        self.fecha.dateChanged.connect(self.determina_tope_24h_semanal)
        self.fecha.dateChanged.connect(self.determina_tope_80h_trimestral)
        self.cancelar.clicked.connect(self.close)
        self.agregar.clicked.connect(self.guardar_cmd)

    def advertencia_de_perdida_de_datos(self):
        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "¿Desea usted continuar? los datos ingresados se perderán"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return 1
        else:
            return 0

    def borrar_cmd(self):
        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted borrar la hora extra al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            leew.del_gen('worker.db', 'horas_extras', 'id_h', f'{self.id_h_visible.text()} AND computado = 0')
            self.recarga_en_blanco_nuevo_doc()
            # para ordenar y posicionar información
            self.listados_id_hora_e = leew.consulta_lista('worker.db', 'id_h', 'horas_extras', 'id_h >', '"0"')
            self.posicion = len(self.listados_id_hora_e)

    def carga_data(self):
        self.id = self.trabajador.currentText().split(' ')[0]  # con esta linea saco el id de una cadena de texto
        salario = leew.consulta_gen('worker.db', 'salario', 'salario', 'id', f'"{self.id}" AND status = "Vigente"')
        self.salario_mensual.setText(str("{:,.2f}".format(salario)))
        dias_por_mes = leew.consulta_gen('worker.db', 'dias_mes', 'beneficios', 'status', f'"Vigente"')
        horas_dia = leew.consulta_gen('worker.db', 'horas_dia', 'beneficios', 'status', f'"Vigente"')
        self.salario_hora.setText(str("{:,.2f}".format(salario / dias_por_mes / horas_dia)))
        self.hora_i.setTime(QtCore.QTime(0, 0, 0))
        self.hora_f.setTime(QtCore.QTime(0, 0, 0))
        self.hni = leew.consulta_gen('worker.db', 'h_i_noct_hora', 'beneficios', 'status', f'"Vigente"')
        self.min_inicio_h_noct = leew.consulta_gen('worker.db', 'h_i_noct_min', 'beneficios', 'status', f'"Vigente"')
        self.hnf = leew.consulta_gen('worker.db', 'h_f_noct_hora', 'beneficios', 'status', f'"Vigente"')
        self.min_fin_h_noct = leew.consulta_gen('worker.db', 'h_f_noct_min', 'beneficios', 'status', f'"Vigente"')
        self.hni_msec = self.hni * 3600 * 1000 + self.min_inicio_h_noct * 60 * 1000 # en milisegundos
        self.hnf_msec = self.hnf * 3600 * 1000 + self.min_fin_h_noct * 60 * 1000  # en milisegundos

        self.trabajo_en_descanso.setChecked(0)
        self.define_fecha()
        self.determina_tope_24h_semanal()
        self.determina_tope_80h_trimestral()
        self.verificador_trabajo_en_descanso()

    def carga_porcentajes(self):
        self.porc_nocturno.setText(str(leew.consulta_gen('worker.db', 'valor_h_noct', 'beneficios', 'status', '"Vigente"')))
        self.porc_hora_extra.setText(str(leew.consulta_gen('worker.db', 'valor_h_extra1', 'beneficios', 'status', '"Vigente"')))
        self.porc_hora_extra_exceso.setText(str(leew.consulta_gen('worker.db', 'valor_h_extra2', 'beneficios', 'status', '"Vigente"')))

    def verificador_trabajo_en_descanso(self):
        if self.trabajo_en_descanso.isChecked():
            self.porc_hora_extra.setText(str(leew.consulta_gen('worker.db', 'valor_trab_desc', 'beneficios', 'status', '"Vigente"')))
        else:
            self.porc_hora_extra.setText(str(leew.consulta_gen('worker.db', 'valor_h_extra1', 'beneficios', 'status', '"Vigente"')))
        self.calcula_hora()
        self.suma_gran_total()

    def calcula_hora(self):
        # calcula la diferencia de horas extras
        dif_hora = self.hora_f.time().hour() - self.hora_i.time().hour()
        dif_min = self.hora_f.time().minute() - self.hora_i.time().minute()
        #print(dif_hora)
        #print(dif_min)

        if dif_hora < 0 or (dif_hora == 0 and dif_min < 0):
            self.hora_extra.setText('Horas inválidas')
            self.hora_extra_doble.setText('Horas inválidas')
            self.hora_extra_noct.setText('Horas inválidas')
            self.total_he_normal.setValue(0)
            self.total_he_nocturno.setValue(0)
            self.total_he_doble_exceso.setValue(0)
            self.gran_total.setValue(0)
        else:
            self.hora_extra.setText(str(round(dif_hora + dif_min / 60,2)))
            self.determina_tope_24h_semanal() # lo pongo justo ahí para que de ser necesario sobre escriba lo anterior
            self.total_he_normal.setValue(float(self.hora_extra.text().replace(',', '')) *
                                          float(self.salario_hora.text().replace(',', '')) *
                                          (1 + float(self.porc_hora_extra.text()) / 100))
            # hora extra nocturna hen
            hen = 0
            minhe = 0

            hora_i_ms = self.hora_i.time().msecsSinceStartOfDay() # esta funcion retorna los msecs desde las 00 hasta la hora indicada, lo uso para hacer una linea del tiempo
            hora_f_ms = self.hora_f.time().msecsSinceStartOfDay()

            # rango 1, hei y hef antes de la hnf
            if hora_i_ms < self.hnf_msec and hora_f_ms <= self.hnf_msec:
                hen = (hora_f_ms - hora_i_ms) // 3600000 # parte entera
                minhe = (hora_f_ms - hora_i_ms) % 3600000 / 60000 # resto de la division

            # rango 2, hei menor que hnf pero hef mayor que hnf
            elif hora_i_ms < self.hnf_msec and hora_f_ms > self.hnf_msec:
                hen = (self.hnf_msec - hora_i_ms) // 3600000  # parte entera
                minhe = (self.hnf_msec - hora_i_ms) % 3600000 / 60000  # resto de la division

            # rango 3, hei mayor que hnf y hef menor que hni, es decir no hay hora nocturna
            elif hora_i_ms > self.hnf_msec and hora_f_ms < self.hni_msec:
                hen = 0 # parte entera
                minhe = 0  # resto de la division

            # rango 4, hei menor que hni pero hef mayor que hni
            elif hora_i_ms < self.hni_msec and hora_f_ms > self.hni_msec:
                hen = (hora_f_ms - self.hni_msec) // 3600000  # parte entera
                minhe = (hora_f_ms - self.hni_msec) % 3600000 / 60000  # resto de la division

            # rango 5, hei y hef mayor que hni
            elif hora_i_ms >= self.hni_msec and hora_f_ms > self.hni_msec:
                hen = (hora_f_ms - hora_i_ms) // 3600000  # parte entera
                minhe = (hora_f_ms - hora_i_ms) % 3600000 / 60000  # resto de la division

            # rango 6, los dos extremos tomando hora extra desde las 00 hasta el fin de las horas noct y pasando más
            # allá del inicio de las horas nocturnas
            if hora_i_ms < self.hnf_msec and hora_f_ms > self.hni_msec:# tuve que usar if en vez de elif porque nunca iba a llegar a esa condición ya que en se llegaba antes
                hen = ((self.hnf_msec - hora_i_ms) + (hora_f_ms - self.hni_msec)) // 3600000  # parte entera
                minhe = ((self.hnf_msec - hora_i_ms) + (hora_f_ms - self.hni_msec)) % 3600000 / 60000  # resto de la division

            self.hora_extra_noct.setText(str(round(hen + minhe / 60,2)))
            self.total_he_nocturno.setValue(float(self.hora_extra_noct.text()) *
                                          float(self.salario_hora.text().replace(',', '')) *
                                            (1 + float(self.porc_nocturno.text()) / 100))

            # horas en exceso 24 horas semanal

            self.total_he_doble_exceso.setValue(float(self.hora_extra_doble.text()) *
                                                float(self.salario_hora.text().replace(',', '')) *
                                                (1 + float(self.porc_hora_extra_exceso.text()) / 100))

    def suma_gran_total(self):
        self.gran_total.setValue(self.total_he_normal.value() + self.total_he_doble_exceso.value() +
                                 self.total_he_nocturno.value())

    def define_fecha(self):
        # hace que la minima fecha seleccionable sea la fecha de ingreso del trabajador

        fecha_ingreso = leew.consulta_gen('worker.db','Fecha_ingreso','info', 'id', f'"{self.id}"')
        #print(fecha_ingreso)
        dia, mes, ano = fecha_ingreso.split('-')
        self.fecha.setMinimumDate(QtCore.QDate(int(ano),int(mes),int(dia))) # fijo como dia minimo el ingreso
        self.fecha.setDate(QtCore.QDate.currentDate()) # fijo el dia actual como fecha

    def set_enable_agregar(self):
        if self.gran_total.value() > 0.00 and self.nota.text() != "":
            self.agregar.setDisabled(0)
            self.hubo_modificacion = 1
        else:
            self.agregar.setDisabled(1)

    def guardar_cmd(self):
        # determinacion del periodo, esto es solo informativo realmente

        if self.fecha.date().day() < 16:
            self.periodo = "1Q" + self.fecha.dateTime().toString("MMyyyy")
        else:
            self.periodo = "2Q" + self.fecha.dateTime().toString("MMyyyy")

        #print(self.periodo)


        self.descripcion_he = f'Total: {round(self.gran_total.value(), 2)} horas extra: {self.hora_extra.text()} ' \
                              f'horas extras en exceso: {self.hora_extra_doble.text()} horas nocturnas: {self.hora_extra_noct.text()}' \
                              f' fecha: {self.fecha.dateTime().toString("dd-MM-yyyy")} H. inicio: {self.hora_i.time().toString("hh:mm")}' \
                              f' H. Final: {self.hora_f.time().toString("hh:mm")}'

        self.entrada = f'"{self.trabajador.currentText()}", "{self.salario_mensual.text()}", "{self.salario_hora.text()}",' \
                       f'"{self.tipohoraextra.currentText()}", "{self.fecha.dateTime().toString("dd-MM-yyyy")}",' \
                       f'"{self.hora_i.time().toString("hh:mm")}", "{self.hora_f.time().toString("hh:mm")}",' \
                       f'"{self.nota.text()}", "{self.trabajo_en_descanso.checkState()}", "{self.hora_extra.text()}", ' \
                       f'"{self.porc_hora_extra.text()}", "{self.total_he_normal.text()}", "{self.hora_extra_doble.text()}",' \
                       f'"{self.porc_hora_extra_exceso.text()}", "{self.total_he_doble_exceso.text()}",' \
                       f'"{self.hora_extra_noct.text()}", "{self.porc_nocturno.text()}", "{self.total_he_nocturno.text()}",' \
                       f'"{self.gran_total.text()}", NULL, "{self.id}", "{self.periodo}", 0,NULL, "{self.descripcion_he}",' \
                       f'"{self.fecha_doc.dateTime().toString("dd-MM-yyyy")}", "{self.main_instancia.usuario}"'

        #print(self.entrada)

        reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted agregar la variación al trabajador?"
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.introduce_gen('worker.db','horas_extras',self.entrada)
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

    def determina_tope_24h_semanal(self):
        # deternminar semana donde se pretende incluir HE
        semana = self.fecha.date().weekNumber()
        #print(semana)
        # saca listado de horas extras anteriores
        lista_he_anteriores = leew.consulta_lista('worker.db', 'id_h', 'horas_extras', 'id',
                                                  f'"{self.id}"')
        #print(lista_he_anteriores)
        total_horas = 0
        for id_he in lista_he_anteriores:
            # determino la semana sea la misma de la que se va a agregar
            fecha_he = leew.consulta_gen('worker.db', 'fecha', 'horas_extras', 'id_h', f'"{id_he}"')
            dia, mes, anio = [int(i) for i in fecha_he.split('-')]
            if semana == QtCore.QDate(anio,mes,dia).weekNumber():
                horas = leew.consulta_gen('worker.db', 'horas', 'horas_extras', 'id_h', f'"{id_he}"')
                #print(dia, mes, anio)
                total_horas = total_horas + horas

        if total_horas > 24:
            self.hora_extra_doble.setText(self.hora_extra.text())
        else:
            diferencia = round(total_horas - 24, 2)
            if float(self.hora_extra.text()) + diferencia < 0:
                self.hora_extra_doble.setText('0.0')
            else:
                self.hora_extra_doble.setText(str(round(float(self.hora_extra.text()) + diferencia, 2)))
                self.hora_extra.setText(str(abs(diferencia))) # tope de horas extras normales

    def determina_tope_80h_trimestral(self):
        # deternminar mes donde se pretende incluir HE
        mes_actual = self.fecha.date().month()
        anio_actual = self.fecha.date().year()

        #print(mes)
        # saca listado de horas extras anteriores
        lista_he_anteriores = leew.consulta_lista('worker.db', 'id_h', 'horas_extras', 'id',
                                                  f'"{self.id}"')
        # print(lista_he_anteriores)
        total_horas = 0
        for id_he in lista_he_anteriores:
            # determino la semana sea la misma de la que se va a agregar
            fecha_he = leew.consulta_gen('worker.db', 'fecha', 'horas_extras', 'id_h', f'"{id_he}"')
            dia, mes, anio = [int(i) for i in fecha_he.split('-')]
            mes = QtCore.QDate(anio, mes, dia).month()
            anio = QtCore.QDate(anio, mes, dia).year()
            mes_anio = (mes, anio)
            if (mes_actual, anio_actual) == mes_anio or (mes_actual - 1, anio_actual) == mes_anio or \
                    (mes_actual - 2, anio_actual) == mes_anio:
                horas = leew.consulta_gen('worker.db', 'horas', 'horas_extras', 'id_h', f'"{id_he}"')
                # print(dia, mes, anio)
                total_horas = total_horas + horas

        if total_horas > 80:
            self.aviso.setText(f" EL TRABAJADOR TIENE MÁS DE 80 HORAS TRABAJADAS EN UN TRIMESTRE: {total_horas} ")

            self.aviso.setStyleSheet("background:#FA5858 ;border-radius:3;")
        else:
            self.aviso.setText(f" HORAS TRABAJADAS EN EL ÚLTIMO TRIMESTRE: {total_horas} ")
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
                self.main_instancia.letrero.setText('')
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()