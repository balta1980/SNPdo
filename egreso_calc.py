from egreso import *
import leew, trat_fecha
from datetime import date

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,cmd, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.advertencia()

        self.mensaje = QtWidgets.QLabel("")
        self.statusBar.addWidget(self.mensaje)
        self.mensaje.setStyleSheet('background:#FA5858 ;border-radius:3;')


        self.refrescar_tabla_liquidacion = cmd # para refrescar la tabla de liquidacion

        self.tiempo_trabajado.setReadOnly(True) # para que no se borre

        self.listado_idp_prestamos_pendientes = []

        self.suma_retenciones = 0

        # para el cálculo de las retenciones con base en las vacaciones
        self.porc_afp_trab = leew.consulta_gen('worker.db', 'afp_trab', 'legales', 'status', '"Vigente"')
        self.porc_sfs_trab = leew.consulta_gen('worker.db', 'sfs_trab', 'legales', 'status', '"Vigente"')
        self.porc_afp_emp = leew.consulta_gen('worker.db', 'afp_emp', 'legales', 'status', '"Vigente"')
        self.porc_sfs_emp = leew.consulta_gen('worker.db', 'sfs_emp', 'legales', 'status', '"Vigente"')
        self.porc_infotep = leew.consulta_gen('worker.db', 'infotep', 'legales', 'status', '"Vigente"')
        self.porc_srl = leew.consulta_gen('worker.db', 'srl', 'legales', 'status', '"Vigente"')
        self.tope_sal_afp = leew.consulta_gen('worker.db', 'tope_sal_afp', 'legales', 'status', '"Vigente"')
        self.tope_sal_sfs = leew.consulta_gen('worker.db', 'tope_sal_sfs', 'legales', 'status', '"Vigente"')
        self.tope_sal_srl = leew.consulta_gen('worker.db', 'tope_sal_srl', 'legales', 'status', '"Vigente"')
        self.sal_min_tributable = leew.consulta_gen('worker.db', 'salario', 'salario_min', 'status', '"Vigente"')

        self.carga_data()

        self.refrescar_datos()

        self.ya_se_puede_cerrar = False

        self.datos_trabajador.currentIndexChanged.connect(self.refrescar_datos)
        self.pre_aviso.clicked.connect(self.calc_preaviso)
        self.tipo_cesantia_82.clicked.connect(self.calc_censatia)
        self.cesantia.clicked.connect(self.calc_censatia)
        self.vacaciones.clicked.connect(self.calc_vacaciones)
        self.monto_vacaciones.valueChanged.connect(self.calcular_retenciones)
        self.salario_navidad.clicked.connect(self.calc_salario_navidad)

        self.fecha_egreso.dateChanged.connect(self.tiempo_trabajando_calc)
        self.fecha_egreso.dateChanged.connect(self.refrescar_datos)

        self.monto_preaviso.valueChanged.connect(self.calc_total_a_recibir)
        self.monto_vacaciones.valueChanged.connect(self.calc_total_a_recibir)
        self.monto_cesantia.valueChanged.connect(self.calc_total_a_recibir)
        self.monto_sal_nav.valueChanged.connect(self.calc_total_a_recibir)
        self.monto_bonificacion.valueChanged.connect(self.calc_total_a_recibir)

        self.cancelar.clicked.connect(self.close_cmd)
        self.procesar.clicked.connect(self.add_data)

        self.fecha = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss AP")

        self.nota.textChanged.connect(self.activa)

        self.procesar.setDisabled(1)

    def determinacion_del_periodo_de_salida(self):
        if self.fecha_egreso.date().day() < 16:
            self.periodo_salida = self.fecha_egreso.date().toString('1QMMyyyy')
        else:
            self.periodo_salida = self.fecha_egreso.date().toString('2QMMyyyy')
        self.MMAAAA = self.fecha_egreso.date().toString('MMyyyy')
        #print(self.periodo_salida)

    def refrescar_datos(self):
        self.dias_por_mes = leew.consulta_gen('worker.db','dias_mes','beneficios','status', '"Vigente"')

        self.pre_aviso.setCheckState(0)
        self.cesantia.setCheckState(0)
        self.vacaciones.setCheckState(0)
        self.salario_navidad.setCheckState(0)

        self.monto_bonificacion.setValue(0.0)
        self.nota.setText('')

        #ID del trabajador

        self.idw = self.datos_trabajador.currentText().split(' ')[0]

        # Fecha ingreso
        fecha_ingreso = leew.consulta_gen('worker.db', 'Fecha_ingreso', 'info', 'id', self.idw)
        self.dia, self.mes, self.ano = [int(n) for n in fecha_ingreso.split('-')]
        self.fecha_ingreso.setDate(QtCore.QDate(self.ano, self.mes, self.dia))

        self.fecha_egreso.setMinimumDate(QtCore.QDate(self.ano, self.mes, self.dia))

        self.parte_grabable_sal_nav = 0

        self.tiempo_trabajando_calc()

        meses_con_pagos = leew.consulta_lista_distintc('worker.db','MMAAAA','nomina','ID_TRABAJADOR',f'"{self.idw}"')
        meses_con_pagos.reverse() # invierte la lista
        #print(meses_con_pagos)

        pagos_por_mes = []
        comisiones_por_mes = []
        total_mes = []
        for mes in meses_con_pagos:
            salario_mes = leew.consulta_gen_sum('worker.db', 'SALARIO_QUINCENA', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if salario_mes == None:
                salario_mes = 0

            inasistencias_mes = leew.consulta_gen_sum('worker.db', 'INASIS', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if inasistencias_mes == None:
                inasistencias_mes = 0
            vac_mes = leew.consulta_gen_sum('worker.db', 'FRACCION_VAC', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if vac_mes == None:
                vac_mes = 0
            vac_pago = leew.consulta_gen_sum('worker.db', 'PAGO_DE_VAC', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if vac_pago == None:
                vac_pago = 0
            otras_remun = leew.consulta_gen_sum('worker.db', 'OTRAS_REMUN', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if otras_remun == None:
                otras_remun = 0
            otras_remun_no_sal = leew.consulta_gen_sum('worker.db', 'OTRAS_REMUN_NO_SALARIALES', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if otras_remun_no_sal == None:
                otras_remun_no_sal = 0

            pagos_por_mes.append(salario_mes + vac_mes + vac_pago + otras_remun - otras_remun_no_sal - inasistencias_mes)

            comision_mes = leew.consulta_gen_sum('worker.db', 'COMISIONES', 'nomina', 'MMAAAA',
                                                f'"{mes}" AND ID_TRABAJADOR = "{self.idw}"')
            if comision_mes == None:
                comision_mes = 0
            comisiones_por_mes.append(comision_mes)
            total_mes.append(salario_mes + vac_mes + vac_pago + otras_remun - otras_remun_no_sal - inasistencias_mes +
                             comision_mes)
        #print(pagos_por_mes)

        if len(meses_con_pagos) < 12: # para rellenar con cero los meses que no se ha pagado
            for n in range(12 - len(meses_con_pagos)):
                meses_con_pagos.append("SIN PAGO")
                pagos_por_mes.append("0.0")
                comisiones_por_mes.append("0.0")
                total_mes.append("0.0")
        fila = 0

        for n in range(11,-1, - 1):

            self.tableWidget.setItem(fila, 0, QtWidgets.QTableWidgetItem(meses_con_pagos[n]))
            self.tableWidget.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(pagos_por_mes[n])))
            self.tableWidget.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(comisiones_por_mes[n])))
            self.tableWidget.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(total_mes[n])))
            fila = fila + 1

        # calculo suma

        suma = 0
        celda_con_datos = 0
        if self.tiempo_trab[0] < 1:  # cuando un trabajador entra el ano de su salida
            for fila in range(12):
                try:# este try lo hago para una situacion donde no se saco un trabajador en su momento
                    #print(self.tableWidget.item(fila, 3).text())
                    if float(self.tableWidget.item(fila, 3).text()) != 0.0:
                        celda_con_datos = celda_con_datos + 1
                except:
                    celda_con_datos = 1
        else:
            celda_con_datos = 12

        for fila in range(12):
            try:# este try lo hago para una situacion donde no se saco un trabajador en su momento
                suma = suma + float(self.tableWidget.item(fila,3).text())
            except:
                suma = 0

        try: # este try lo hago para una situacion donde no se saco un trabajador en su momento y la
            # tabla de salarios está vacía con puros 0.00
            promedio = suma / celda_con_datos
        except:
            promedio = suma / 1

        self.suma_salarios.setValue(suma)
        self.promedio_mensual.setValue(promedio)
        self.sal_diario_prom.setValue(promedio/self.dias_por_mes)
        self.determinacion_del_periodo_de_salida()
        self.calc_preaviso()
        self.calc_censatia()
        self.calc_vacaciones()
        self.calc_salario_navidad()
        self.calc_total_a_recibir()
        self.calc_prestamo()

    def calc_preaviso(self):
        # del preaviso

        self.desc_preaviso.setText('')
        self.monto_preaviso.setValue(0.0)

        if self.pre_aviso.isChecked():
            if int(self.tiempo_trab[1]) < 3:
                self.desc_preaviso.setText('Cero días (0)')
            if int(self.tiempo_trab[1]) >= 3 and int(self.tiempo_trab[1]) <= 6:
                self.desc_preaviso.setText('Siete días (7)')
                self.monto_preaviso.setValue(7 * self.sal_diario_prom.value())
            if int(self.tiempo_trab[1]) > 6 and int(self.tiempo_trab[0]) < 1:
                self.desc_preaviso.setText('Catorce días (14)')
                self.monto_preaviso.setValue(14 * self.sal_diario_prom.value())
            if int(self.tiempo_trab[0]) >= 1:
                self.desc_preaviso.setText('Veintiocho días (28)')
                self.monto_preaviso.setValue(28 * self.sal_diario_prom.value())

        self.calc_total_a_recibir() # para modificar el total cada vez que se ejeute esta funcion

    def calc_prestamo(self):
        self.monto_prestamos.setValue(0.00)
        self.desc_prestamos.setText('')
        #verificación de prestamos pendientes
        prestamos_pendientes_del_trabajador = leew.consulta_lista('worker.db','idp','prestamos','estatus',f'"PENDIENTE" AND idt = {self.idw}')
        monto_pendiente = 0
        descripcion = ''
        self.listado_idp_prestamos_pendientes = []
        for idp in prestamos_pendientes_del_trabajador:
            monto_pendiente_idp = leew.consulta_gen_sum('worker.db', 'op2', 'prestamos_detalles', 'idp', f'"{idp}" AND estatus = "pendiente"')
            monto_pendiente = monto_pendiente + monto_pendiente_idp
            descripcion = descripcion + f'Adelanto # {idp}, Monto pendiente = {"{:,.2f}".format(monto_pendiente_idp)}\n '
            self.listado_idp_prestamos_pendientes.append(idp)
        self.monto_prestamos.setValue(monto_pendiente)
        self.desc_prestamos.setText(descripcion)
        self.calc_total_a_recibir()

    def calc_censatia(self):
        # Calculo cesantia

        self.desc_cesantia.setText('')
        self.monto_cesantia.setValue(0.0)

        if self.tipo_cesantia_82.isChecked() == False :
            if self.cesantia.isChecked():
                if int(self.tiempo_trab[1]) < 3:
                    self.desc_cesantia.setText('Cero días (0)')
                if int(self.tiempo_trab[1]) >= 3 and int(self.tiempo_trab[1]) <= 6:
                    self.desc_cesantia.setText('Seis días (6)')
                    self.monto_cesantia.setValue(6 * self.sal_diario_prom.value())
                if int(self.tiempo_trab[1]) > 6 and int(self.tiempo_trab[0]) < 1:
                    self.desc_cesantia.setText('Trece días (13)')
                    self.monto_cesantia.setValue(13 * self.sal_diario_prom.value())
                if int(self.tiempo_trab[0]) >= 1 and int(self.tiempo_trab[0]) <= 5:
                    self.desc_cesantia.setText(f' ({21*self.tiempo_trab[0]}) días')
                    self.monto_cesantia.setValue(21 * self.sal_diario_prom.value() * self.tiempo_trab[0])
                    # a partir de aquí abajo es para pagar la proporcion de dias del ano
                    if int(self.tiempo_trab[1]) < 3:
                        pass
                    if int(self.tiempo_trab[1]) >= 3 and int(self.tiempo_trab[1]) <= 6:
                        self.desc_cesantia.setText(f'({21*self.tiempo_trab[0] + 6}) días')
                        self.monto_cesantia.setValue(self.monto_cesantia.value() + 6 * self.sal_diario_prom.value())
                    if int(self.tiempo_trab[1]) > 6:
                        self.desc_cesantia.setText(f'({21 * self.tiempo_trab[0] + 13}) días')
                        self.monto_cesantia.setValue(self.monto_cesantia.value() + 13 * self.sal_diario_prom.value())
                if int(self.tiempo_trab[0]) > 5:
                    self.desc_cesantia.setText(f' ({23*self.tiempo_trab[0]}) días')
                    self.monto_cesantia.setValue(23 * self.sal_diario_prom.value() * self.tiempo_trab[0])
                    # a partir de aquí abajo es para pagar la proporcion de dias del ano
                    if int(self.tiempo_trab[1]) < 3:
                        pass
                    if int(self.tiempo_trab[1]) >= 3 and int(self.tiempo_trab[1]) <= 6:
                        self.desc_cesantia.setText(f'({23*self.tiempo_trab[0] + 6}) días')
                        self.monto_cesantia.setValue(self.monto_cesantia.value() + 6 * self.sal_diario_prom.value())
                    if int(self.tiempo_trab[1]) > 6:
                        self.desc_cesantia.setText(f'({23 * self.tiempo_trab[0] + 13}) días')
                        self.monto_cesantia.setValue(self.monto_cesantia.value() + 13 * self.sal_diario_prom.value())
        else:
            # montos y dias del articulo 82
            if self.cesantia.isChecked():
                if int(self.tiempo_trab[1]) < 3:
                    self.desc_cesantia.setText('Cero días (0)')
                if int(self.tiempo_trab[1]) >= 3 and int(self.tiempo_trab[1]) <= 6:
                    self.desc_cesantia.setText('Cinco días (5)')
                    self.monto_cesantia.setValue(5 * self.sal_diario_prom.value())
                if int(self.tiempo_trab[1]) > 6 and int(self.tiempo_trab[0]) < 1:
                    self.desc_cesantia.setText('Diez días (10)')
                    self.monto_cesantia.setValue(10 * self.sal_diario_prom.value())
                if int(self.tiempo_trab[0]) >= 1:
                    self.desc_cesantia.setText(f' ({15 * self.tiempo_trab[0]}) días')
                    self.monto_cesantia.setValue(15 * self.sal_diario_prom.value() * self.tiempo_trab[0])
                    # a partir de aquí abajo es para pagar la proporcion de dias del ano
                    if int(self.tiempo_trab[1]) < 3:
                        pass
                    if int(self.tiempo_trab[1]) >= 3 and int(self.tiempo_trab[1]) <= 6:
                        self.desc_cesantia.setText(f'({15 * self.tiempo_trab[0] + 5}) días')
                        self.monto_cesantia.setValue(self.monto_cesantia.value() + 5 * self.sal_diario_prom.value())
                    if int(self.tiempo_trab[1]) > 6:
                        self.desc_cesantia.setText(f'({15 * self.tiempo_trab[0] + 10}) días')
                        self.monto_cesantia.setValue(self.monto_cesantia.value() + 10 * self.sal_diario_prom.value())

        self.calc_total_a_recibir()  # para modificar el total cada vez que se ejeute esta funcion
    def calc_vacaciones(self):
        # cálculo de vacaciones

        self.desc_vac.setText('')
        self.monto_vacaciones.setValue(0.0)
        # el salaraio usado para calculo de las vacaciones es el salario actual segun el reglamento
        try:
            self.salario_actual = leew.consulta_gen('worker.db','salario','salario', 'status',
                                                    f'"Vigente" AND id = "{self.idw}"')
            self.salario_para_vacaciones = self.salario_actual / self.dias_por_mes

        except:
            self.salario_para_vacaciones = 0
            self.salario_actual = 0

        if self.vacaciones.isChecked():

            if int(self.tiempo_trab[1]) < 5:
                self.desc_vac.setText('Cero días (0)')
            if int(self.tiempo_trab[1]) >= 5:
                self.desc_vac.setText('Seis días (6)')
                self.monto_vacaciones.setValue(6 * self.salario_para_vacaciones)
            if int(self.tiempo_trab[1]) >= 6:
                self.desc_vac.setText('Siete días (7)')
                self.monto_vacaciones.setValue(7 * self.salario_para_vacaciones)
            if int(self.tiempo_trab[1]) >= 7:
                self.desc_vac.setText('Ocho días (8)')
                self.monto_vacaciones.setValue(8 * self.salario_para_vacaciones)
            if int(self.tiempo_trab[1]) >= 8:
                self.desc_vac.setText('Nueve días (9)')
                self.monto_vacaciones.setValue(9 * self.salario_para_vacaciones)
            if int(self.tiempo_trab[1]) >= 9:
                self.desc_vac.setText('Diez días (10)')
                self.monto_vacaciones.setValue(10 * self.salario_para_vacaciones)
            if int(self.tiempo_trab[1]) >= 10:
                self.desc_vac.setText('Once días (11)')
                self.monto_vacaciones.setValue(11 * self.salario_para_vacaciones)
            if int(self.tiempo_trab[1]) >= 11:
                self.desc_vac.setText('Doce días (12)')
                self.monto_vacaciones.setValue(12 * self.salario_para_vacaciones)
        else:

            if int(self.tiempo_trab[0]) >=1:
                self.desc_vac.setText('Catorce días (14)')
                self.monto_vacaciones.setValue(14 * self.salario_para_vacaciones)

            if int(self.tiempo_trab[0]) >= 5:
                self.desc_vac.setText('Dieciocho (18)')
                self.monto_vacaciones.setValue(18 * self.salario_para_vacaciones)

        self.calcular_retenciones()
        self.calc_total_a_recibir()  # para modificar el total cada vez que se ejeute esta funcion
    def calcular_retenciones(self):
        # Funcion para calcular retenciones que se originan por el pago de las vacaciones que son base de calculo para
        # la TSS y el ISLR
        # AFP tiene un máximo de base de 20 salarios minimos nacional
        # afp que se pagó con base al periodo de salida del trabajador
        self.ret_afp_trab = 0
        self.ret_sfs_trab = 0
        self.ret_islr = 0
        self.ret_afp_emp = 0
        self.ret_sfs_emp = 0
        self.ret_srl = 0
        self.infotep = 0

        # abajo busco como lista porque es posible que se hagan vaias nominas indiviuales en vaios periodos y asi puedo
        # ver el ultimo pago realmente
        self.trabajador_con_pago_en_periodo_de_salida = leew.consulta_lista('worker.db', 'FECHA_FIN_PAGO', 'nomina', 'PERIODO',
                                                       f'"{self.periodo_salida}" AND ID_TRABAJADOR = "{self.idw}"')

        # print(self.trabajador_con_pago_en_periodo_de_salida)
        if self.trabajador_con_pago_en_periodo_de_salida == []:
            self.trabajador_con_pago_en_periodo_de_salida = None
            self.fecha_ultimo_pago = leew.consulta_lista('worker.db', 'FECHA_FIN_PAGO', 'nomina', 'ID_NOM>',
                                                       f'1 AND ID_TRABAJADOR = "{self.idw}"')
            if self.fecha_ultimo_pago == []:
                self.fecha_ultimo_pago = "NUNCA SE LE HA PAGADO NOMINA"
            else:
                self.fecha_ultimo_pago = self.fecha_ultimo_pago[len(self.fecha_ultimo_pago) - 1]

        else:
            self.trabajador_con_pago_en_periodo_de_salida = self.trabajador_con_pago_en_periodo_de_salida[
                len(self.trabajador_con_pago_en_periodo_de_salida) - 1]

        # print(self.trabajador_con_pago_en_periodo_de_salida)

        if self.trabajador_con_pago_en_periodo_de_salida != None:
            self.mensaje.setText('')
            self.indice_per_actual = leew.consulta_gen('worker.db', 'indice', 'periodo', 'idp',
                                                       '"' + self.periodo_salida + '"')

            self.indice_per_anterior = int(
                self.indice_per_actual) - 1  # usado para descontar el pago adelantado de vac de un periodo anterior
            # print(self.indice_per_anterior)
            self.idp_per_anterior = leew.consulta_gen('worker.db', 'idp', 'periodo', 'indice',
                                                      str(self.indice_per_anterior))

            if int(self.indice_per_anterior) > 0:

                self.sal_seg_social_per_anterior = leew.consulta_gen('worker.db', 'SAL_PAR_SEG_SOCIAL', 'nomina', 'PERIODO', '"' +
                                                                     self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                    self.idw))

                if self.sal_seg_social_per_anterior is None:
                    self.sal_seg_social_per_anterior = 0

            else:
                self.sal_seg_social_per_anterior = 0

            try:
                self.SAL_SEG_SOCIAL_SALIDA = leew.consulta_gen('worker.db', 'SAL_PAR_SEG_SOCIAL', 'nomina', 'PERIODO', '"' +
                                                               self.periodo_salida + '" AND ID_TRABAJADOR= ' + str(
                        self.idw))
            except:
                self.SAL_SEG_SOCIAL_SALIDA = 0

            if self.periodo_salida[0] == '1':
                salarios_seguridad_social = self.SAL_SEG_SOCIAL_SALIDA
            else:
                salarios_seguridad_social = self.SAL_SEG_SOCIAL_SALIDA + self.sal_seg_social_per_anterior

            # calculo AFP trabajador
            if salarios_seguridad_social < self.tope_sal_afp * self.sal_min_tributable:
                if salarios_seguridad_social + self.monto_vacaciones.value() < self.tope_sal_afp * self.sal_min_tributable:
                    self.ret_afp_trab = self.monto_vacaciones.value() * self.porc_afp_trab
                    self.ret_afp_emp = self.monto_vacaciones.value() * self.porc_afp_emp
                else:
                    self.ret_afp_trab = (self.tope_sal_afp * self.sal_min_tributable - salarios_seguridad_social) * self.porc_afp_trab
                    self.ret_afp_emp = (self.tope_sal_afp * self.sal_min_tributable - salarios_seguridad_social) * self.porc_afp_emp
            else:
                self.ret_afp_trab = 0
                self.ret_afp_emp = 0

            # cálculo SFS trabajador
            if salarios_seguridad_social < self.tope_sal_sfs * self.sal_min_tributable:
                if salarios_seguridad_social + self.monto_vacaciones.value() < self.tope_sal_sfs * self.sal_min_tributable:
                    self.ret_sfs_trab = self.monto_vacaciones.value() * self.porc_sfs_trab
                    self.ret_sfs_emp = self.monto_vacaciones.value() * self.porc_sfs_emp
                else:
                    self.ret_sfs_trab = (self.tope_sal_sfs * self.sal_min_tributable - salarios_seguridad_social) * self.porc_sfs_trab
                    self.ret_sfs_emp = (self.tope_sal_sfs * self.sal_min_tributable - salarios_seguridad_social) * self.porc_sfs_emp
            else:
                self.ret_sfs_trab = 0
                self.ret_sfs_emp = 0

            # SRL
            if salarios_seguridad_social < self.tope_sal_srl * self.sal_min_tributable:
                if salarios_seguridad_social + self.monto_vacaciones.value() < self.tope_sal_srl * self.sal_min_tributable:
                    self.ret_srl = self.monto_vacaciones.value() * self.porc_srl
                else:
                    self.ret_srl = (self.tope_sal_srl * self.sal_min_tributable - salarios_seguridad_social) * self.porc_srl
            else:
                self.ret_srl = 0

            # INFOTEP
            self.infotep = self.monto_vacaciones.value() * self.porc_infotep

            # ISLR
            if int(self.indice_per_anterior) > 0:

                self.sal_base_islr_per_anterior = leew.consulta_gen('worker.db', 'ISLR_BASE', 'nomina', 'PERIODO', '"' +
                                                       self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                    self.idw))

                if self.sal_base_islr_per_anterior is None:
                    self.sal_base_islr_per_anterior = 0


            else:
                self.sal_base_islr_per_anterior = 0

            try:
                self.SAL_BASE_ISLR_SALIDA = leew.consulta_gen('worker.db', 'ISLR_BASE', 'nomina', 'PERIODO', '"' +
                                                               self.periodo_salida + '" AND ID_TRABAJADOR= ' + str(
                    self.idw))
                self.RET_ISLR_SALIDA = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'PERIODO', '"' +
                                                               self.periodo_salida + '" AND ID_TRABAJADOR= ' + str(
                    self.idw))
            except:
                self.SAL_BASE_ISLR_SALIDA = 0
                self.RET_ISLR_SALIDA = 0

            if self.periodo_salida[0] == '1':
                salarios_base_islr = self.SAL_BASE_ISLR_SALIDA
                retenciones_islr = 0 # porque el programa no retiene en el primer periodo de nomina
            else:
                salarios_base_islr = self.SAL_BASE_ISLR_SALIDA + self.sal_base_islr_per_anterior
                retenciones_islr = self.RET_ISLR_SALIDA

            self.islr_base_bonificacion = leew.consulta_gen_sum('worker.db', 'monto_ajustado', 'nomina_beneficios',
                                                                'idt', f'"{self.idw}" AND MMAAAA = {self.MMAAAA}')
            if self.islr_base_bonificacion == None:
                self.islr_base_bonificacion = 0

            self.ret_islr_bonificacion = leew.consulta_gen_sum('worker.db', 'ret_islr', 'nomina_beneficios',
                                                                'idt', f'"{self.idw}" AND MMAAAA = {self.MMAAAA}')
            if self.ret_islr_bonificacion ==None:
                self.ret_islr_bonificacion = 0

            # parte grabable del salario de navidad

            if self.monto_sal_nav.value() > 5 * self.sal_min_tributable:
                self.parte_grabable_sal_nav = self.monto_sal_nav.value() - (5 * self.sal_min_tributable)

            self.ret_islr = leew.calculo_retencion_islr(salarios_base_islr + self.islr_base_bonificacion
                                                        + self.monto_vacaciones.value() + self.parte_grabable_sal_nav -\
                                                        self.ret_afp_trab - self.ret_sfs_trab) -\
                            retenciones_islr - self.ret_islr_bonificacion


        else: # esto es para descontar algo al trabajador cuando no se proceso su última nómina antes de sacarlo

            self.mensaje.setText(
                f'Al trabajador no se le ha pagado nada en esta quincena, el ultimo día pagado fue: {self.fecha_ultimo_pago}')
            self.mensaje.setToolTip("No se evidencia algún pago en la quincena donde se está retirando al trabajador,\n"
                                    " esto puede causar una incongruencia en el calculo y generción de los TXT para\n"
                                    " declarar en la TSS")


            self.ret_afp_trab = self.monto_vacaciones.value() * self.porc_afp_trab
            self.ret_afp_emp = self.monto_vacaciones.value() * self.porc_afp_emp
            self.ret_islr = leew.calculo_retencion_islr(self.monto_vacaciones.value())
            self.ret_sfs_trab = self.monto_vacaciones.value() * self.porc_sfs_trab
            self.ret_sfs_emp = self.monto_vacaciones.value() * self.porc_sfs_emp
            self.ret_srl = self.monto_vacaciones.value() * self.porc_srl
            self.infotep = self.monto_vacaciones.value() * self.porc_infotep

        # para que se vea en la pantalla:
        self.retencion_afp.setValue(self.ret_afp_trab)
        self.retencion_sfs.setValue(self.ret_sfs_trab)
        self.retencion_islr.setValue(self.ret_islr)
        self.suma_retenciones = self.ret_afp_trab + self.ret_sfs_trab + self.ret_islr
        self.total_retenciones.setValue(self.suma_retenciones)
        self.total_retenciones_2.setValue(self.suma_retenciones)

    def calc_salario_navidad(self):
        # se calcula el salario de navidad tomando en cuenta que el traba haya entrado o no el mismo a;o que sale
        self.desc_sal_nav.setText('')
        self.monto_sal_nav.setValue(0.0)
        if self.salario_navidad.isChecked():
            if self.fecha_ingreso.date().year() < self.fecha_egreso.date().year(): #cuando un trabajador entra el ano anterior a su salida
                self.desc_sal_nav.setText(f"{self.tiempo_trab_en_ano[1]} meses, {self.tiempo_trab_en_ano[2]} días")
                self.monto_sal_nav.setValue((int(self.tiempo_trab_en_ano[1]) + int(self.tiempo_trab_en_ano[2]) / self.fecha_egreso.date().daysInMonth()) *
                                             self.promedio_mensual.value() / 12 )
            else:# cuando trabajador entre y salga de la empresa el mismo ano
                self.desc_sal_nav.setText(f"{self.tiempo_trab[1]} meses, {self.tiempo_trab[2]} días")
                self.monto_sal_nav.setValue(((int(self.tiempo_trab[1]) + int(self.tiempo_trab[2]) / self.fecha_egreso.date().daysInMonth()) *
                                             self.promedio_mensual.value()) / 12)

        self.calc_total_a_recibir()  # para modificar el total cada vez que se ejeute esta funcion

    def calc_total_a_recibir(self):
        # Calculo a pagar total
        self.subtotal.setValue(self.monto_vacaciones.value() + self.monto_sal_nav.value() +
                                      self.monto_cesantia.value() + self.monto_preaviso.value() +
                                      self.monto_bonificacion.value() - self.monto_prestamos.value())
        self.total_a_recibir.setValue(self.monto_vacaciones.value() + self.monto_sal_nav.value() +
                                      self.monto_cesantia.value() + self.monto_preaviso.value() +
                                      self.monto_bonificacion.value() - self.monto_prestamos.value() -
                                      self.suma_retenciones)
    def tiempo_trabajando_calc(self):
        # tiempo trabajando
        self.tiempo_trab = trat_fecha.calc_dif_fecha(date(self.ano, self.mes, self.dia), date(self.fecha_egreso.date().year(),
                                                                          self.fecha_egreso.date().month(),
                                                                          self.fecha_egreso.date().day()))
        self.tiempo_trabajado.setText(f"{self.tiempo_trab[0]} años, {self.tiempo_trab[1]} meses, {self.tiempo_trab[2]} días")

        self.tiempo_trab_en_ano = trat_fecha.calc_dif_fecha(date(self.fecha_egreso.date().year(), 1, 1), date(self.fecha_egreso.date().year(),
                                                                          self.fecha_egreso.date().month(),
                                                                          self.fecha_egreso.date().day()))

    def carga_data(self):
        # listado de trabajadores
        idies = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        # print(idies)
        for id in idies:
            id = str(id)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id}"')
            trabajador = f"{id} {nombre} {apellido} {cedula}"
            self.datos_trabajador.addItem(trabajador)

        self.fecha_egreso.setDate(QtCore.QDate.currentDate())

    def add_data(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar",f"Desea usted procesar el retiro definitivo del trabajador \n"
                                                                     f" {self.datos_trabajador.currentText()}?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                # columna salario actual que es igual a salario para vaciones

                self.entrada = f'NULL,"{self.idw}","{self.fecha_egreso.text()}","{self.periodo_salida}","{self.MMAAAA}","{self.tiempo_trabajado.text()}", ' \
                               f'"{str(self.tipo_cesantia_82.isChecked())}","{self.suma_salarios.text()}",' \
                               f'"{self.promedio_mensual.text()}","{self.sal_diario_prom.text()}","{self.salario_actual}","{str(self.pre_aviso.isChecked())}",' \
                               f'"{self.monto_preaviso.text()}","{self.desc_preaviso.text()}","{str(self.cesantia.isChecked())}",' \
                               f'"{self.monto_cesantia.text()}","{self.desc_cesantia.text()}","{str(self.vacaciones.isChecked())}",' \
                               f'"{self.monto_vacaciones.text()}","{self.desc_vac.text()}","{str(self.salario_navidad.isChecked())}",' \
                               f'"{self.monto_sal_nav.text()}","{self.desc_sal_nav.text()}","{self.monto_bonificacion.text()}",' \
                               f'"{self.monto_prestamos.text()}","{self.desc_prestamos.text()}",'\
                               f'"{self.total_a_recibir.text()}","{self.nota.text()}","{self.fecha}",' \
                               f'"{self.ret_afp_trab}", "{self.ret_sfs_trab}","{self.ret_islr}","{self.parte_grabable_sal_nav}", "{self.ret_afp_emp}",' \
                               f'"{self.ret_sfs_emp}", "{self.ret_srl}", "{self.infotep}"'
                #print(self.entrada)
                leew.backup_bd('liquidacion')
                leew.introduce_gen('worker.db','liquidacion',self.entrada)
                leew.update_gen('worker.db','info','Estatus',f'"Desincorporado" WHERE id ="{self.idw}"')
                leew.update_gen('worker.db', 'info', 'Fecha_egreso', f'"{self.fecha_egreso.text()}" WHERE id ="{self.idw}"')
                leew.update_gen('worker.db', 'prestamos', 'estatus', f'"PAGADO" WHERE idt = "{self.idw}"')
                for idp in self.listado_idp_prestamos_pendientes:
                    leew.update_gen('worker.db', 'prestamos_detalles', 'estatus', f'"pagada" WHERE idp = "{idp}"')
                # registro de novedad
                #print(type(self.fecha_egreso.date().day()))

                ENTRADA_NOVEDAD = f'NULL, "{self.idw}", "SA", "{self.fecha_egreso.date().toString("dd-MM-yyyy")}", NULL, "{self.periodo_salida}"'
                leew.introduce_gen('worker.db', 'novedades',
                                   ENTRADA_NOVEDAD)  # crea una novedad en la tabla novedades para la tss


                QtWidgets.QMessageBox.information(self, "Atención", "Liquidación procesada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:

                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)
        try:
            self.refrescar_tabla_liquidacion()
        except:
            pass

    def activa(self):
        if self.nota.text() != '':
            self.procesar.setDisabled(0)
        else:
            self.procesar.setDisabled(1)

        if self.nota.isModified():
            self.nota.setStyleSheet("background: #ffbcbd;")

    def advertencia(self):
        # se le advierte al usuario que antes de liquidar a traba se debe
        # estar seguro de que se le pagaron todas sus nominas
        QtWidgets.QMessageBox.warning(self, "Advertencia", "Antes de retirar algún trabajador usted debe primero haber "
                                                        "procesado todas las nóminas relacionadas a dicho trabajador, "
                                                        "bien sea con una corrida de nómina quincenal o una individual",
                                          QtWidgets.QMessageBox.Ok)

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
