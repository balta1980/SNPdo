import leew
import provisiones
import threading
import imprime
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class NominaProc():

    def __init__(self,periodo,imp_recibo,pagar_sal_nav,nota, trabajador_activo, tipo_de_nomina='Quincenal', fecha_i_pago = '',fecha_fin_pago = ''):

        self.imprimir_recibos = imp_recibo # debe ser 0 ó 1
        self.pagar_salario_navidad = pagar_sal_nav # pueder ser True o False
        self.periodo = periodo
        self.DIA_INICIO_PER = leew.consulta_gen('worker.db', 'f_inicio', 'periodo', 'idp', '"' + periodo + '"')
        self.DIA_FIN_PER = leew.consulta_gen('worker.db', 'f_fin', 'periodo', 'idp', '"' + periodo + '"')
        self.nota = nota
        self.i = trabajador_activo # lo pongo aquí para pasarlo a la funcion calculo_por_trab
        self.TIPO_NOMINA = tipo_de_nomina
        self.FECHA_INICIO_PAGO = '' # podría usarse en un futuro para pagar rangos de fechas entre self.FECHA_INICIO_PAGO Y self.FECHA_FIN_PAGO
        self.FECHA_INICIO_PAGO = fecha_i_pago # esto se usa para pagar una nomina individual entre esta fecha y el final del periodo
        self.FECHA_FIN_PAGO = fecha_fin_pago # esto se usa para pagar una nomina individual entre la fecha inicial del periodo y esta fecha
        self.pagar_fraccion_por_cambio_fecha_inicio_fin_periodo = 0
        self.INDICE_VAC = '0'  # lo pongo aquí para asegurar que esta variable siempre exista, luego será sobre escrita
        self.nomina()

    def nomina(self):

        #VARIABLES GLOBALES PARA EL CALCULO DE LAS PARTIDAS DE LA NOMINA

        self.afp_tr, = leew.consulta_legal('afp_trab')
        self.afp_emp, = leew.consulta_legal('afp_emp')
        self.tope_sal_afp = leew.consulta_gen('worker.db', 'tope_sal_afp', 'legales','status', '"Vigente"')
        self.sfs_tr, = leew.consulta_legal('sfs_trab')
        self.sfs_emp, = leew.consulta_legal('sfs_emp')
        self.tope_sal_sfs = leew.consulta_gen('worker.db', 'tope_sal_sfs', 'legales','status', '"Vigente"')
        self.srl, = leew.consulta_legal('srl')
        self.tope_sal_srl = leew.consulta_gen('worker.db', 'tope_sal_srl', 'legales','status', '"Vigente"')
        self.infotep, = leew.consulta_legal('infotep')
        self.sal_min_trib, = leew.consulta_salmin('salario') # salario minimo tributario
        self.factor_riesgo = leew.consulta_gen('worker.db', 'srl', 'legales','status', '"Vigente"') * 100 # factor de riesgo laboral de la tss, lo multiplico por 100 porque en la BD está en 0.012 por ejemplo y más abajo se divide entre 100 otra vez
        self.fecha = date.today() # La fecha del día que se corre la nomina
        self.ano,self.mes,self.dia, = [n for n in str(self.fecha).split('-')]
        self.FECHA = str(self.dia) + '-' + str(self.mes) + '-' + str(self.ano)
        self.diasxmes, = leew.consulta_benef('dias_mes') #mayormente usado en las proviciones
        self.lista_dia_no_lab = leew.lista_dia_no_lab() #mayormente usado en el pago de horas extraordinarias
        self.valor_trab_hora_descanso, = leew.consulta_benef('valor_trab_desc')
        self.valor_he, = leew.consulta_benef('valor_h_extra1')
        self.valor_he_n, = leew.consulta_benef('valor_h_noct')

        hni_h, = leew.consulta_benef('h_i_noct_hora')
        hni_min, = leew.consulta_benef('h_i_noct_min')
        self.hni = hni_h + hni_min / 60

        hnf_h, = leew.consulta_benef('h_f_noct_hora')
        hnf_min, = leew.consulta_benef('h_f_noct_min')
        self.hnf = hnf_h + hnf_min / 60

        self.indice_per_actual = leew.consulta_gen('worker.db', 'indice', 'periodo', 'idp', '"' +self.periodo + '"')
        self.indice_per_anterior = int(self.indice_per_actual) - 1 #usado para descontar el pago adelantado de vac de un periodo anterior
        #print(self.indice_per_anterior)
        self.idp_per_anterior = leew.consulta_gen('worker.db', 'idp', 'periodo', 'indice',
                                                  str(self.indice_per_anterior))
        if self.idp_per_anterior == None:
            self.idp_per_anterior = "None"
        #print(self.idp_per_anterior)

        self.fecha_inicio_periodo = leew.consulta_gen('worker.db','f_inicio','periodo','idp', '"' + self.periodo + '"')  # primer dia del periodo
        if self.FECHA_INICIO_PAGO == '' or self.FECHA_INICIO_PAGO == self.fecha_inicio_periodo:
            self.FECHA_INICIO_PAGO = self.fecha_inicio_periodo
        else:
            self.fecha_inicio_periodo = self.FECHA_INICIO_PAGO
            self.pagar_fraccion_por_cambio_fecha_inicio_fin_periodo = 1

        self.dia_i_p, self.mes_i_p, self.ano_i_p, = [int(n) for n in str(self.fecha_inicio_periodo).split('-')]
        self.fecha_inicio_periodo = date(self.ano_i_p,self.mes_i_p,self.dia_i_p) # esta fecha la uso para ver si el trab trabajo completo

        self.fecha_fin_periodo = leew.consulta_gen('worker.db', 'f_fin', 'periodo', 'idp',
                                                   '"' + self.periodo + '"')  # ultimo dia del periodo
        if self.FECHA_FIN_PAGO == '' or self.FECHA_FIN_PAGO == self.fecha_fin_periodo: # asi es siempre, a menos que se haya corrido una nomina individual con una fecha anterior al final del periodo
            self.FECHA_FIN_PAGO = self.fecha_fin_periodo # se deja que self.fecha_fin_periodo sea tal cual como se busco en la BD
        else:
            self.fecha_fin_periodo = self.FECHA_FIN_PAGO # aqui significa que hay un valor tipo "dd-mm-aaaa" y no un ''
            self.pagar_fraccion_por_cambio_fecha_inicio_fin_periodo = 1 # mas abajo se pagara solo los dias entre el inicio del periodo y la fecha cambiada arriba

        self.dia_f_p, self.mes_f_p, self.ano_f_p, = [int(n) for n in str(self.fecha_fin_periodo).split('-')]
        self.fecha_fin_periodo = date(self.ano_f_p, self.mes_f_p,
                                         self.dia_f_p)  # esta fecha la uso para ver si el trab trabajo completo

        self.dias_habiles_en_periodo = leew.difrencia_fechas_habiles(self.fecha_fin_periodo, self.fecha_inicio_periodo)

        # DETERMINACIÓN DE SI HAY VACACIONES EN EL PERIODO DE NÓMINA

        self.indices_vac = set() # para que en cada corrida no se repita
        self.trabajadores_con_Vacaciones = dict() # {id_t,[id_v,dias_v,fecha_i_vac, fecha_f_vac]}
        listado_indice_vacaciones_abiertas = leew.consulta_lista('worker.db','indice','vacaciones','status','"ABIERTO"')
        #print(listado_indice_vacaciones_abiertas)
        for indice_vac_abierta in listado_indice_vacaciones_abiertas:
            #print(indice_vac_abierta)
            id_v = indice_vac_abierta
            listado_traba_en_vac_del_indice = leew.consulta_gen('worker.db','trabajadores','vacaciones','indice',f'"{indice_vac_abierta}"')
            #print(listado_traba_en_vac_del_indice.split("', "))_
            for n in listado_traba_en_vac_del_indice.split("', "):
                id_t = n.split(',')[0].replace("'", "")
                dias_v = leew.consulta_gen('worker.db','dias','vacaciones','indice',f'"{indice_vac_abierta}"')
                lista = leew.consulta_gen('worker.db','lista_dias','vacaciones','indice',f'"{indice_vac_abierta}"')
                lista = lista.replace('[', '')
                lista = lista.replace(']', '')
                lista = lista.replace("'", "")
                fecha_i_vac = lista.split(',')[0]
                fecha_f_vac = lista.split(',')[len(lista.split(',')) - 1]
                fecha_f_vac = fecha_f_vac.replace(' ','')
                dia_vac, mes_vac, ano_vac, = [int(n) for n in fecha_i_vac.split('-')]
                primer_dia_vac = date(ano_vac, mes_vac, dia_vac)
                # print(dia_vac, mes_vac, ano_vac)

                if self.fecha_inicio_periodo <= primer_dia_vac <= self.fecha_fin_periodo:

                    self.trabajadores_con_Vacaciones.update({id_t: [id_v, dias_v, fecha_i_vac, fecha_f_vac]})
                    self.indices_vac.add(indice_vac_abierta)
        #print(self.trabajadores_con_Vacaciones)


        # FIN

        # CICLO DE CALCULO POR TRABAJADOR ACTIVO
        self.calculo_por_trab()

    def calculo_por_trab(self):

        i = self.i
        #print(i)
        # Determinacion fecha ingreso del trabajador
        fechai, = leew.consultaP('worker.db', 'Fecha_ingreso', 'info', str(i))
        dia, mes, ano = [int(v) for v in fechai.split("-")]
        fechai = date(ano, mes, dia)
        # print(fechai)

        self.ID_TRABAJADOR = i

        self.PERIODO = self.periodo

        self.SALARIO, = leew.consultaPS('worker.db', 'salario','salario', str(i))
        #print(self.SALARIO)

        #DETERMINACION DE CAMBIO DE SALARIO RESPECTO AL PERIODO ANTERIOR
        periodo_anterior = leew.consulta_gen('worker.db', 'idp', 'periodo', 'indice', f'"{self.indice_per_anterior}"')
        if self.SALARIO != leew.consulta_gen('worker.db','SALARIO', 'nomina','PERIODO',
                                             f'"{periodo_anterior}" AND ID_TRABAJADOR = "{i}"') and fechai < self.fecha_inicio_periodo:
            ENTRADA_NOVEDAD = f'NULL, "{i}", "AD", "{self.FECHA}", NULL, "{self.PERIODO[2:]}"'
            leew.introduce_gen('worker.db', 'novedades', ENTRADA_NOVEDAD) # crea una novedad en la tabla novedades para la tss

        # DEFINICIÓN DE SALARIO DE QUINCENA

        if fechai <= self.fecha_inicio_periodo: # por si trabajó un periodo incompleto

            self.SALARIO_QUINCENA = self.SALARIO / 2
        else:
            # quincena trabajada incompleta por ser trabajador nuevo y registrar novedad de ingreso
            self.SALARIO_QUINCENA = leew.difrencia_fechas_habiles(self.fecha_fin_periodo, fechai) * self.SALARIO / self.diasxmes
            # abajo vuelvo a buscar la fecha de ingreso porque fechai fue manipulada
            fecha_ingreso = leew.consulta_gen('worker.db', 'Fecha_ingreso', 'info', 'id', f'"{i}"')
            ENTRADA_NOVEDAD = f'NULL, "{i}", "IN", "{fecha_ingreso}", NULL, "{self.PERIODO[2:]}"'
            leew.introduce_gen('worker.db', 'novedades',
                               ENTRADA_NOVEDAD)  # crea una novedad en la tabla novedades para la tss


        # PARA PAGAR FRACCION DE SALARIO SI EL TRABAJADOR SE LE CORRIO UNA NOMINA INDIVIDUAL A EL SOLO CON UNA FECHA FINAL DE TRABAJO INFEROR A LA FECHA FINAL DEL PERIODO
        if self.pagar_fraccion_por_cambio_fecha_inicio_fin_periodo == 1:
            dias_trabajados_x_pagar = leew.difrencia_fechas_habiles(self.fecha_fin_periodo,
                                                                    self.fecha_inicio_periodo)
            self.SALARIO_QUINCENA = dias_trabajados_x_pagar * self.SALARIO / self.diasxmes

        # PARA PAGAR FRACCION DE SALARIO SI EL TRABAJADOR VIENE DE UNA VACACION QUE TERMINA EN UN DIA ENTRE EL DIA DE INICIO Y FIN DEL PERIODO QUE SE ESTA PAGANDO

        # self.PAGO_AD_PER_ANT es el ultimo día de vacaciones que vienn de un periodo anterior, necesario para poder calcular los días trabajados en el mes
        self.PAGO_AD_PER_ANT = leew.consulta_gen('worker.db','PAGO_ADELANTADO','nomina','PERIODO','"' +
                                             self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(self.ID_TRABAJADOR))
        if self.PAGO_AD_PER_ANT == None: # condicion extrema cuando un trabajador es nuevo para el periodo
            self.PAGO_AD_PER_ANT = 'N/A'
        else:
            if self.PAGO_AD_PER_ANT != 'N/A':
                self.FECHA_INICIO_PAGO = self.PAGO_AD_PER_ANT
                udvpa_dia, udvpa_mes,udvpa_anio, = [int(i) for i in self.PAGO_AD_PER_ANT.split('-')]
                ult_dia_vac_per_ant = date(udvpa_anio,udvpa_mes,udvpa_dia)
                dias_trabajados_x_pagar = leew.difrencia_fechas_habiles(self.fecha_fin_periodo, ult_dia_vac_per_ant + relativedelta(days=1)) # relative delta para sacar dias hábiles desde el dia siguiente al fin de vacaciones
                self.SALARIO_QUINCENA = dias_trabajados_x_pagar * self.SALARIO / self.diasxmes



        # INICIO--------------CALCULO PAGO VACACIONES---------------------------------------------------------------

        # self.PAGO_ADELANTADO en esta variable a partir del 31082022 almacena como una cadena el último día de vacaciones para que en
        # el periodo siguiente se pueda determinar desde las vacaciones hasta el fin del periodo cuantos días se deben pagar
        if str(i) in self.trabajadores_con_Vacaciones: #trabajador en vacacion en el perido
            self.INDICE_VAC = str(self.trabajadores_con_Vacaciones[str(i)][0]) # {id_t,[id_v,dias_v,fecha_i_vac, fecha_f_vac]}
            fecha_i_vac = self.trabajadores_con_Vacaciones[str(i)][2]  # {id_t,[id_v,dias_v,fecha_i_vac, fecha_f_vac]}
            dia_vac, mes_vac, ano_vac, = [int(n) for n in fecha_i_vac.split('-')]
            primer_dia_vac = date(ano_vac, mes_vac, dia_vac)
            ult_dia_vac = self.trabajadores_con_Vacaciones[str(i)][3]  # {id_t,[id_v,dias_v,fecha_i_vac, fecha_f_vac]}
            udv_dia, udv_mes, udv_ano, = [int(n) for n in ult_dia_vac.split(
                '-')]  # usadado para hacer lo de arriba en un if de mas abajo
            ultimo_dia_vac = date(udv_ano, udv_mes, udv_dia)
            self.cant_dias_vac = int(self.trabajadores_con_Vacaciones[str(i)][1])  # {id_t,[id_v,dias_v,fecha_i_vac, fecha_f_vac]}
            if ultimo_dia_vac <= self.fecha_fin_periodo: #determinando que el ultimo dia de vacaciones esté en el periodo
                dias_trabajados = self.dias_habiles_en_periodo - leew.difrencia_fechas_habiles(ultimo_dia_vac, primer_dia_vac) # dias que trabajo en ese periodo
                if self.cant_dias_vac == 7: #determinando si las vacaciones fueron fraccionadas a 7 dias
                    if date(ano,mes,dia) + relativedelta(years=5) < primer_dia_vac:#determinando si el trabajador tiene 5 anos trabajando para el dia de sus vacaciones
                        self.PAGO_DE_VAC = 2 * self.SALARIO / self.diasxmes
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                    else:
                        self.PAGO_DE_VAC = 0
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                else:
                    if date(ano,mes,dia) + relativedelta(years=5) < primer_dia_vac:
                        self.PAGO_DE_VAC = 4 * self.SALARIO / self.diasxmes
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                    else:
                        self.PAGO_DE_VAC = 0
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                self.PAGO_ADELANTADO = 'N/A'
            else: # cuando el ultimo día de vacaciones no cae en el mismo periodo
                dias_trabajados = self.dias_habiles_en_periodo - leew.difrencia_fechas_habiles(self.fecha_fin_periodo, primer_dia_vac)
                if self.cant_dias_vac == 7: #determinando si las vacaciones fueron fraccionadas a 7 dias
                    if date(ano,mes,dia) + relativedelta(years=5) < primer_dia_vac:#determinando si el trabajador tiene 5 anos trabajando para el dia de sus vacaciones

                        self.PAGO_DE_VAC = 2 * self.SALARIO / self.diasxmes
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')

                    else:

                        self.PAGO_DE_VAC = 0
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                else:
                    if date(ano,mes,dia) + relativedelta(years=5) < primer_dia_vac:

                        self.PAGO_DE_VAC = 4 * self.SALARIO / self.diasxmes
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                    else:
                        self.PAGO_DE_VAC = 0
                        self.DIAS_DE_VAC_DISFRUTADOS = self.cant_dias_vac
                        self.FRACCION_VAC = self.SALARIO / self.diasxmes * self.cant_dias_vac
                        self.FECHA_INICIO_VAC = primer_dia_vac.strftime('%d-%m-%Y')
                        self.FECHA_FIN_VAC = ultimo_dia_vac.strftime('%d-%m-%Y')
                self.PAGO_ADELANTADO = ultimo_dia_vac.strftime('%d-%m-%Y')
            self.SALARIO_QUINCENA = dias_trabajados * self.SALARIO / self.diasxmes
            # registro de novedad
            ENTRADA_NOVEDAD = f'NULL, "{i}", "VC", "{self.FECHA_INICIO_VAC}", "{self.FECHA_FIN_VAC}", "{self.PERIODO}"'
            leew.introduce_gen('worker.db', 'novedades',
                               ENTRADA_NOVEDAD)  # crea una novedad en la tabla novedades para la tss
        else:
            self.PAGO_ADELANTADO = 'N/A'
            self.PAGO_DE_VAC = 0 #ESTE ES EL PAGO QUE SE LE HACE A LOS TRABAJADORES CON MAS DE 5 ANOS
            self.DIAS_DE_VAC_DISFRUTADOS = 0 #VALE CERO EN ESTE CASO
            self.FRACCION_VAC = 0
            self.FECHA_INICIO_VAC = 'N/A'
            self.FECHA_FIN_VAC = 'N/A'

        self.SALARIO_QUINCENA_NETO = self.SALARIO_QUINCENA # cuando no hay vacaciones es el salrio de la quincena
        # FIN-----------------CALCULO PAGO VACACIONES---------------------------------------------------------------

        '''vvvvvvvvvvv INICIO VARIACIONES vvvvvvvvvv'''

        # Listas de fechas y salarios utilizadas para el calculo de horas extras y deducciones de faltas
        lista_fechas = leew.consulta_lista('worker.db', 'fecha', 'salario', 'id', str(i))
        lista_salarios = leew.consulta_lista('worker.db', 'salario', 'salario', 'id', str(i))

        # HORAS EXTRAORDINARIAS
        # aqui se calcula el valor de la hora extra

        self.lista_id_horas_extra = leew.consulta_lista('worker.db', 'id_h', 'horas_extras', 'id',
                                                   '' + str(i) + ' AND computado= 0')

        self.HORAS_EXTRA = 0
        self.DESC_HE = []

        for n in self.lista_id_horas_extra:  # comparo fechas de las horas extra con las listas de fechas y salarios.
            horas_extra = leew.consulta_gen('worker.db','total', 'horas_extras','id_h', f'"{n}"')

            self.HORAS_EXTRA = self.HORAS_EXTRA + horas_extra
            detalle_bd = leew.consulta_gen('worker.db','desc_he', 'horas_extras','id_h', f'"{n}"')
            detalle = f'id:{n} {detalle_bd}'
            self.DESC_HE.append(detalle)
        # print(self.HORAS_EXTRA)
        # print(self.DESC_HE)

        # DESCUENTO INASISTENCIAS
        # aqui se calcula el valor de la inasistencia, se toma en cuenta solo las faltas injustificadas.

        self.lista_id_inasis = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id',
                                              '' + str(i) + ' AND computado= 0 AND tipo= "Injustificada"')
        # estas inasistencias justificadas se cerraran al final junto con las injustificadas
        self.lista_id_inasis_justificadas = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id',
                                              '' + str(i) + ' AND computado= 0 AND tipo= "Justificada"')

        self.INASIS = 0
        self.DESC_INA = []

        for n in self.lista_id_inasis:

            valor_inasis = leew.consulta_gen('worker.db','monto', 'inasis','id_i', f'"{n}"')

            self.INASIS = self.INASIS + valor_inasis

            detalle_bd = leew.consulta_gen('worker.db','desc_ina', 'inasis','id_i', f'"{n}"')
            detalle = f'id:{n} {detalle_bd}'
            self.DESC_INA.append(detalle)

        # DETERMINACION DE OTRAS REMUNERACIONES $$$$$$ SALARIALES y NO salariales TODAS JUNTAS $$$$$$
        # estas otras remuneraciones pueden ser bonos, dietas, pagos especiales etc
        self.lista_id_or = leew.consulta_lista('worker.db', 'idor', 'otras_remun', 'id',
                                              '' + str(i) + ' AND computado= 0')

        self.OTRAS_REMUN = 0
        self.DESC_OTRAS_REMUN = []

        for idor in self.lista_id_or:

            detalle_bd = leew.consulta_gen('worker.db','desc_otra_rem','otras_remun','idor',str(idor))
            otra_remun = leew.consulta_gen('worker.db','monto','otras_remun','idor',str(idor))

            self.OTRAS_REMUN = self.OTRAS_REMUN + otra_remun

            self.DESC_OTRAS_REMUN.append(detalle_bd)

        # DETERMINACION DE OTRAS REMUNERACIONES OJO NO SALARIALES
        # se saca para poder restar de las otras remun en el calculo de sal nav, prestaciones, bono
        self.lista_id_or_no_sal = leew.consulta_lista('worker.db', 'idor', 'otras_remun', 'id',
                                               '' + str(i) + ' AND computado= 0 AND salarial=0')

        self.OTRAS_REMUN_NO_SALARIAL = 0

        for idor in self.lista_id_or_no_sal:
            otra_remun_NO_SAL = leew.consulta_gen('worker.db', 'monto', 'otras_remun', 'idor', str(idor))

            self.OTRAS_REMUN_NO_SALARIAL = self.OTRAS_REMUN_NO_SALARIAL + otra_remun_NO_SAL


        # COMISIONES
        self.lista_id_comisiones = leew.consulta_lista('worker.db', 'id_c', 'comisiones', 'id',
                                          '' + str(i) + ' AND computado= 0')
        self.COMISIONES = 0
        self.DESC_COMISIONES = []

        for com in self.lista_id_comisiones:  # comparo fechas de las inasistencias con las listas de fechas y salarios.

            comision = leew.consulta_gen('worker.db', 'monto', 'comisiones', 'id_c', str(com))
            detalle_bd = leew.consulta_gen('worker.db', 'desc_com', 'comisiones', 'id_c', str(com))

            self.COMISIONES = self.COMISIONES + comision

            self.DESC_COMISIONES.append(detalle_bd)

        # REMUNERACION OTROS EMPLEADORES
        # esto no se le paga al trabajador solo se usa para la base del islr
        self.lista_id_rem_otros_emp = leew.consulta_lista('worker.db', 'id_roe', 'remun_otro_empleador', 'id',
                                                  '' + str(i) + ' AND computado= 0')
        self.REM_OTROS_EMPLEADORES = 0
        self.DESC_REM_OTROS_EMPLEADORES = []

        for rem_oe in self.lista_id_rem_otros_emp:  # comparo fechas de las inasistencias con las listas de fechas y salarios.

            monto_rem_oe = leew.consulta_gen('worker.db', 'monto', 'remun_otro_empleador', 'id_roe', str(rem_oe))
            detalle_bd = leew.consulta_gen('worker.db', 'desc_remun_otro_emp', 'remun_otro_empleador', 'id_roe', str(rem_oe))

            self.REM_OTROS_EMPLEADORES = self.COMISIONES + monto_rem_oe

            self.DESC_REM_OTROS_EMPLEADORES.append(detalle_bd)

        # INDEMNIZACIONES
        self.lista_id_indem = leew.consulta_lista('worker.db', 'id_indem', 'indemnizaciones', 'id',
                                                     '' + str(i) + ' AND computado= 0')
        self.INDEMNIZACIONES = 0
        self.DESC_INDEMNIZACIONES = []

        for id_indem in self.lista_id_indem:  # comparo fechas de las inasistencias con las listas de fechas y salarios.

            monto_indem = leew.consulta_gen('worker.db', 'monto', 'indemnizaciones', 'id_indem', str(id_indem))
            detalle_bd = leew.consulta_gen('worker.db', 'desc_indem', 'indemnizaciones', 'id_indem',
                                           str(id_indem))

            self.INDEMNIZACIONES = self.COMISIONES + monto_indem

            self.DESC_INDEMNIZACIONES.append(detalle_bd)

        '''^^^^^^^^^^FIN VARIACIONES^^^^^^^^^^'''

        '''vvvvvvvvvINICIO DEDUCCIONES LEGALES vvvvvvvvvv'''
        # Res. No 72-03 el salario para la seguridad social es el salario ordinario, vacaciones, comisiones no van horas extra, bono anual/utilidades ni regalia pascual
        self.SALARIO_PARA_SEG_SOCIAL = self.SALARIO_QUINCENA_NETO + self.FRACCION_VAC + self.PAGO_DE_VAC - \
                                        self.INASIS + self.COMISIONES

        if int(self.indice_per_anterior) > 0:

            self.salario_para_seg_social_per_anterior = leew.consulta_gen('worker.db', 'SAL_PAR_SEG_SOCIAL', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.salario_para_seg_social_per_anterior is None:
                self.salario_para_seg_social_per_anterior = 0
        else:
            self.salario_para_seg_social_per_anterior = 0

        # calculo AFP trabajador

        if int(self.indice_per_anterior) > 0:

            self.descuento_afp_per_anterior = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.descuento_afp_per_anterior is None:
                self.descuento_afp_per_anterior = 0
        else:
            self.descuento_afp_per_anterior = 0

        if self.periodo[0] == '1':
            if self.SALARIO_PARA_SEG_SOCIAL < self.tope_sal_afp * self.sal_min_trib:
                self.AFP_TRAB = self.SALARIO_PARA_SEG_SOCIAL * self.afp_tr
            else:
                self.AFP_TRAB = self.tope_sal_afp * self.sal_min_trib * self.afp_tr
        else:
            if self.SALARIO_PARA_SEG_SOCIAL + self.salario_para_seg_social_per_anterior < self.tope_sal_afp * self.sal_min_trib:
                self.AFP_TRAB = self.SALARIO_PARA_SEG_SOCIAL * self.afp_tr
            else:
                self.AFP_TRAB = self.tope_sal_afp * self.sal_min_trib * self.afp_tr - self.descuento_afp_per_anterior


        # Calculo AFP empresa

        if int(self.indice_per_anterior) > 0:

            self.descuento_afp_emp_per_anterior = leew.consulta_gen('worker.db', 'AFP_EMP', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.descuento_afp_emp_per_anterior is None:
                self.descuento_afp_emp_per_anterior = 0
        else:
            self.descuento_afp_emp_per_anterior = 0

        if self.periodo[0] == '1':
            if self.SALARIO_PARA_SEG_SOCIAL < self.tope_sal_afp * self.sal_min_trib:
                self.AFP_EMP = self.SALARIO_PARA_SEG_SOCIAL * self.afp_emp
            else:
                self.AFP_EMP = self.tope_sal_afp * self.sal_min_trib * self.afp_emp
        else:
            if self.SALARIO_PARA_SEG_SOCIAL + self.salario_para_seg_social_per_anterior < self.tope_sal_afp * self.sal_min_trib:
                self.AFP_EMP = self.SALARIO_PARA_SEG_SOCIAL * self.afp_emp
            else:
                self.AFP_EMP = self.tope_sal_afp * self.sal_min_trib * self.afp_emp - self.descuento_afp_emp_per_anterior

        # Aportes voluntarios AFP
        self.APORTE_VOL_TRAB = leew.consulta_gen('worker.db','aporte_vol_trab', 'info', 'id', str(self.ID_TRABAJADOR))
        self.APORTE_VOL_EMP = leew.consulta_gen('worker.db','aporte_vol_emp', 'info', 'id', str(self.ID_TRABAJADOR))

        # Calculo SFS Trabajador
        if int(self.indice_per_anterior) > 0:

            self.descuento_sfs_per_anterior = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.descuento_sfs_per_anterior is None:
                self.descuento_sfs_per_anterior = 0
        else:
            self.descuento_sfs_per_anterior = 0

        if self.periodo[0] == '1':
            if self.SALARIO_PARA_SEG_SOCIAL < self.tope_sal_sfs * self.sal_min_trib:
                self.SFS_TRAB = self.SALARIO_PARA_SEG_SOCIAL * self.sfs_tr
            else:
                self.SFS_TRAB = self.tope_sal_sfs * self.sal_min_trib * self.sfs_tr
        else:
            if self.SALARIO_PARA_SEG_SOCIAL + self.salario_para_seg_social_per_anterior < self.tope_sal_sfs * self.sal_min_trib:
                self.SFS_TRAB = self.SALARIO_PARA_SEG_SOCIAL * self.sfs_tr
            else:
                self.SFS_TRAB = self.tope_sal_sfs * self.sal_min_trib * self.sfs_tr - self.descuento_sfs_per_anterior

        # Calculo SFS Empresa

        if int(self.indice_per_anterior) > 0:

            self.descuento_sfs_emp_per_anterior = leew.consulta_gen('worker.db', 'SFS_EMP', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.descuento_sfs_emp_per_anterior is None:
                self.descuento_sfs_emp_per_anterior = 0
        else:
            self.descuento_sfs_emp_per_anterior = 0

        if self.periodo[0] == '1':
            if self.SALARIO_PARA_SEG_SOCIAL < self.tope_sal_sfs * self.sal_min_trib:
                self.SFS_EMP = self.SALARIO_PARA_SEG_SOCIAL * self.sfs_emp
            else:
                self.SFS_EMP = self.tope_sal_sfs * self.sal_min_trib * self.sfs_emp
        else:
            if self.SALARIO_PARA_SEG_SOCIAL + self.salario_para_seg_social_per_anterior < self.tope_sal_sfs * self.sal_min_trib:
                self.SFS_EMP = self.SALARIO_PARA_SEG_SOCIAL * self.sfs_emp
            else:
                self.SFS_EMP = self.tope_sal_sfs * self.sal_min_trib * self.sfs_emp - self.descuento_sfs_emp_per_anterior

        # Calculo SRL Seguro Riesgo laboral

        if int(self.indice_per_anterior) > 0:

            self.descuento_srl_per_anterior = leew.consulta_gen('worker.db', 'SRL', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.descuento_srl_per_anterior is None:
                self.descuento_srl_per_anterior = 0
        else:
            self.descuento_srl_per_anterior = 0

        if self.periodo[0] == '1':
            if self.SALARIO_PARA_SEG_SOCIAL < self.tope_sal_srl * self.sal_min_trib:
                self.SRL = self.SALARIO_PARA_SEG_SOCIAL * self.factor_riesgo / 100
            else:
                self.SRL = self.tope_sal_srl * self.sal_min_trib * self.factor_riesgo / 100
        else:
            if self.SALARIO_PARA_SEG_SOCIAL + self.salario_para_seg_social_per_anterior < self.tope_sal_srl * self.sal_min_trib:
                self.SRL = self.SALARIO_PARA_SEG_SOCIAL * self.factor_riesgo / 100
            else:
                self.SRL = self.tope_sal_srl * self.sal_min_trib * self.factor_riesgo / 100 -  self.descuento_srl_per_anterior

        # sin retenciones AFP, SFS, Riesgo laboral (CASO ESPECIAL)
        self.ret_tss = leew.consulta_gen('worker.db', 'ret_tss', 'info', 'id', str(self.ID_TRABAJADOR))
        if self.ret_tss == 0:  # esto es para trabajadores que no están en la TSS
            self.AFP_TRAB = 0
            self.AFP_EMP = 0
            self.SFS_TRAB = 0
            self.SFS_EMP = 0
            self.SRL = 0

        '''a) El uno por ciento (1%) que sobre el monto total de las planillas de sueldos o 
                        salarios fijos que paguen mensualmente las empresas y entidades privadas de los 
                        sectores económicos del País, así como, las entidades privadas, públicas, mixtas, 
                        autónomas o descentralizadas que realicen actividades con fines lucrativos. 
                        b) El medio por ciento (½%) a cargo de los trabajadores de las mismas empresas y 
                        entidades, deducible de las utilidades y bonificaciones, que será retenido por los 
                        empleadores e ingresado conjuntamente con la cuota empresarial una vez al año. '''
        self.SALARIO_INFOTEP = self.SALARIO_PARA_SEG_SOCIAL

        # Calculo pago INFOTEP
        self.INFOTEP = self.SALARIO_INFOTEP * self.infotep

        self.ret_infotep = leew.consulta_gen('worker.db', 'ret_infotep', 'info', 'id', str(self.ID_TRABAJADOR))
        if self.ret_infotep == 0: # para no pagar infotep por trabajador
            self.INFOTEP = 0

        # SALARIO DE NAVIDAD

        self.SALARIO_DE_NAVIDAD = 0
        parte_grabable_sal_nav = 0
        # print(self.periodo.get()[0:4])
        if self.pagar_salario_navidad == True:  # se comprueba que es la quincena donde se paga el salario de navidad
            # print(len(leew.ultimos_24_per()))
            ultimas_22_quincenas = leew.ultimos_22_per()
            #print(ultimas_22_quincenas)
            for quincena in ultimas_22_quincenas:
                salario_en_quincena = leew.consulta_gen('worker.db', 'SALARIO_QUINCENA', 'nomina', 'periodo',
                                                        '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))
                inasistencias = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'periodo',
                                                        '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))
                otras_rem = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'periodo',
                                                         '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))
                otras_rem_no_sal = leew.consulta_gen('worker.db', 'OTRAS_REMUN_NO_SALARIALES', 'nomina', 'periodo',
                                              '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))
                comisiones = leew.consulta_gen('worker.db', 'COMISIONES', 'nomina', 'periodo',
                                              '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))
                frac_vac = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'periodo',
                                                         '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))
                pago_vac = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'periodo',
                                                         '"' + quincena + '" AND ID_TRABAJADOR = ' + str(i))

                if salario_en_quincena is None:
                    salario_en_quincena = 0
                if inasistencias == None:
                    inasistencias = 0
                if otras_rem is None:
                    otras_rem = 0
                if otras_rem_no_sal is None:
                    otras_rem_no_sal = 0
                if comisiones is None:
                    comisiones = 0
                if frac_vac is None:
                    frac_vac = 0
                if pago_vac is None:
                    pago_vac = 0
                self.SALARIO_DE_NAVIDAD = self.SALARIO_DE_NAVIDAD + salario_en_quincena + otras_rem + frac_vac + \
                                          pago_vac + comisiones - otras_rem_no_sal - inasistencias
            self.SALARIO_DE_NAVIDAD = (self.SALARIO_DE_NAVIDAD + self.SALARIO_QUINCENA * 2 + self.OTRAS_REMUN +
                                       self.PAGO_DE_VAC + self.FRACCION_VAC + self.COMISIONES -
                                       self.OTRAS_REMUN_NO_SALARIAL - self.INASIS) / 12  # aquí sumé el salario de la quincena y las otras remuneraciones/comisiones vigente porque esta quincena no está en la bd
            # print(self.SALARIO_DE_NAVIDAD)

        if self.SALARIO_DE_NAVIDAD > 5 * self.sal_min_trib:
            parte_grabable_sal_nav = self.SALARIO_DE_NAVIDAD - ( 5 * self.sal_min_trib)
        self.calc_sal_navidad = leew.consulta_gen('worker.db', 'calc_sal_navidad', 'info', 'id',
                                                  str(self.ID_TRABAJADOR))

        if self.calc_sal_navidad == 0:  # para evitar pagar sal nav a trabajador
            self.SALARIO_DE_NAVIDAD = 0

        # CALCULO RETENCION ISLR solo una retencion mensual en el pago de fin de mes, segunda quincena

        if int(self.indice_per_anterior) > 0:

            self.base_islr_per_anterior = leew.consulta_gen('worker.db', 'ISLR_BASE', 'nomina', 'PERIODO', '"' +
                                                                self.idp_per_anterior + '" AND ID_TRABAJADOR= ' + str(
                self.ID_TRABAJADOR))
            if self.base_islr_per_anterior is None:
                self.base_islr_per_anterior = 0
        else:
            self.base_islr_per_anterior = 0

        # Calculo base islr

        self.ISLR_BASE = self.SALARIO_QUINCENA_NETO - self.INASIS + self.FRACCION_VAC + self.PAGO_DE_VAC + \
                         self.OTRAS_REMUN + self.HORAS_EXTRA + parte_grabable_sal_nav - self.AFP_TRAB - self.SFS_TRAB + \
                         self.COMISIONES + self.REM_OTROS_EMPLEADORES


        self.salario_base_mes = 0 # esto lo pongo asi para poder imprimir enla primera quincena de cada mes
        if self.periodo[0] == '2': # solo se retiene ISLR mensualmente en el segundo periodo
            if leew.consulta_gen('worker.db', 'monto_ajustado', 'nomina_beneficios', 'idt',
                                 f'"{self.ID_TRABAJADOR}" AND MMAAAA = {self.periodo[2:7]}') != None:
                bonificacion_part_beneficios = leew.consulta_gen('worker.db', 'monto_ajustado', 'nomina_beneficios', 'idt',
                                 f'"{self.ID_TRABAJADOR}" AND MMAAAA = {self.periodo[2:7]}')
                ret_isr_part_beneficios = leew.consulta_gen('worker.db', 'ret_isrl', 'nomina_beneficios',
                                                                 'idt',
                                                                 f'"{self.ID_TRABAJADOR}" AND MMAAAA = {self.periodo[2:7]}')
            else:
                bonificacion_part_beneficios = 0
                ret_isr_part_beneficios = 0

            self.salario_base_mes = self.ISLR_BASE + self.base_islr_per_anterior + bonificacion_part_beneficios
            self.ISLR_RETENCION = leew.calculo_retencion_islr(self.salario_base_mes) - ret_isr_part_beneficios
        else:
            self.ISLR_RETENCION = 0
        #print('salario base:', self.salario_base_mes, 'retencion:',self.ISLR_RETENCION )

        self.ret_isr = leew.consulta_gen('worker.db', 'ret_isr', 'info', 'id', str(self.ID_TRABAJADOR))
        if self.ret_isr == 0: # para no retener ISR a trabajador
            self.ISLR_RETENCION = 0

        self.RET_PENSION_ALIMENTICIA = leew.consulta_gen('worker.db','retencion_pension', 'info', 'id',
                                                         str(self.ID_TRABAJADOR))
        self.SALDO_A_FAVOR = leew.consulta_gen('worker.db','saldo_a_favor', 'info', 'id', str(self.ID_TRABAJADOR))
        self.RNC_AGENTE_RET = leew.consulta_gen('worker.db','rnc_agente', 'info', 'id', str(self.ID_TRABAJADOR))

        self.OTRAS_REMUN_TODAS = self.FRACCION_VAC + self.PAGO_DE_VAC + \
                         self.OTRAS_REMUN + self.HORAS_EXTRA + parte_grabable_sal_nav
        self.SALARIO_ISR = self.SALARIO_QUINCENA_NETO - self.INASIS + self.COMISIONES
        self.ING_EXCENTOS_ISR = self.SALARIO_DE_NAVIDAD + self.RET_PENSION_ALIMENTICIA + self.INDEMNIZACIONES

        '''^^^^^^^^^^^^^FIN DEDUCCIONES LEGALES ^^^^^^^^^^^^^'''

        '''vvvvvvvvvvvvv INICIO PROVICIONES vvvvvvvvvvvvvvvvvv'''
        # NO SE USAN LAS PROVICIONES EN EL PROGRAMA ACTUALMENTE
        #Provision cesantia
        self.CESANTIA_PREV = self.SALARIO_QUINCENA * provisiones.cesantia(fechai,self.fecha)[1] / self.diasxmes

        # Provision PRE AVISO
        self.PREAVISO_PREV = self.SALARIO_QUINCENA * provisiones.pre_aviso(fechai,self.fecha)[1] / self.diasxmes

        # Provision SALARIO NAVIDAD
        self.SAL_NAV_PREV = self.SALARIO_QUINCENA / 12

        # PROVISION UTILIDADES O PART EN LOS BENEFICIOS
        self.UTILIDADES_PREV = self.SALARIO_QUINCENA * provisiones.part_beneficios(fechai,self.fecha)[1] / self.diasxmes

        # Provisión VACACIONES
        self.VACACIONES_PREV = self.SALARIO_QUINCENA * provisiones.vacaciones(fechai, self.fecha)[1] / self.diasxmes
        '''^^^^^^^^^^^^^FIN PROVICIONES ^^^^^^^^^^^^^'''

        # MONTO A PAGAR A TRABAJADOR
        self.MONTO_A_PAGAR = self.SALARIO_QUINCENA_NETO + self.FRACCION_VAC + self.PAGO_DE_VAC - self.AFP_TRAB - \
                             self.SFS_TRAB - self.ISLR_RETENCION + self.HORAS_EXTRA - self.INASIS + \
                             self.SALARIO_DE_NAVIDAD + self.OTRAS_REMUN + self.INDEMNIZACIONES + self.COMISIONES - \
                             self.APORTE_VOL_TRAB
        #print(self.MONTO_A_PAGAR)

        '''vvvvvvvvvvvv INICIO  MANEJO DE PRÉSTAMOS INICIO vvvvvvvvvvvvvvvvv '''

        # determinar si hay uno o varios creditos que se deba abonar, si hay varios prestamos por abonar se suman
        # igual pasa si hay varias cuotas de varios prestamos se descuenta la suma y se indica lo que se desconto en la quincena

        self.TOTAL_PRESTAMOS = 0
        self.DES_PRESTAMOS = []

        lista_prestamos_por_abonar_por_trab = leew.consulta_lista('worker.db','idp', 'prestamos', 'idt', f'"{i}" AND estatus = "ABIERTO" ')
        total = 0
        for idp in lista_prestamos_por_abonar_por_trab:
            monto = leew.consulta_gen('worker.db', 'monto', 'prestamos', 'idp', f'"{idp}"')
            fecha = leew.consulta_gen('worker.db', 'fecha', 'prestamos', 'idp', f'"{idp}"')
            linea = f'Número prestamo: {idp}, monto (DOP): {monto}, de fecha: {fecha}'
            total = total + monto
            self.TOTAL_PRESTAMOS = total
            self.DES_PRESTAMOS.append(linea)
            leew.update_linea_gen('worker.db','prestamos', 'estatus',"PENDIENTE",'idt',i) # para que apenas abone se coloque como pendiente el prestamo

        #print(self.TOTAL_PRESTAMOS)
        #print(self.DES_PRESTAMOS)

        self.TOTAL_CUOTAS = 0
        self.DES_CUOTAS = []

        # op1 es id trabajador en la tabla de prestamos_detalles
        lista_cuotas_por_abonar_por_trab = leew.consulta_lista('worker.db', 'idc', 'prestamos_detalles', 'op1',
                                                                  f'"{i}" AND estatus = "pendiente" AND periodo = "{self.PERIODO}"')

        for idc in lista_cuotas_por_abonar_por_trab:
            # op2 es el monto de la cuota en la tabla
            cuota = float(leew.consulta_gen('worker.db', 'op2', 'prestamos_detalles', 'idc', f'"{idc}"')) #en la BD es un campo de texto
            periodo = leew.consulta_gen('worker.db', 'periodo', 'prestamos_detalles', 'idc', f'"{idc}"')
            self.TOTAL_CUOTAS = self.TOTAL_CUOTAS + cuota
            linea = f'IDC={idc}, Cuota={cuota},Periodo= {periodo}'
            self.DES_CUOTAS.append(linea)
            #cambio el estatus de la cuota pagada
            leew.update_linea_gen('worker.db', 'prestamos_detalles', 'estatus', "pagada", 'idc', idc)
            # Se verifica si el prestamo dedeb ser cerrado dependiendo
            idp_relativoa_cuota_idp = leew.consulta_gen('worker.db', 'idp', 'prestamos_detalles', 'idc', f'"{idc}"')
            cant_cuotas_prestamo = len(leew.consulta_lista('worker.db', 'idc', 'prestamos_detalles', 'idp', f'"{idp_relativoa_cuota_idp}"'))
            cant_cuotas_prestamo_pagadas = len(leew.consulta_lista('worker.db', 'idc', 'prestamos_detalles', 'idp', f'"{idp_relativoa_cuota_idp}" AND estatus = "pagada"'))
            if cant_cuotas_prestamo_pagadas == cant_cuotas_prestamo: # un prestamo con todas las cuotas pagadas
                leew.update_linea_gen('worker.db', 'prestamos', 'estatus', 'PAGADO', 'idp', f'{idp_relativoa_cuota_idp}')

        #print(self.TOTAL_CUOTAS)
        #print(self.DES_CUOTAS)

        self.TOTAL_A_DEPOSITAR = self.MONTO_A_PAGAR + self.TOTAL_PRESTAMOS - self.TOTAL_CUOTAS

        '''^^^^^^^^^^^^ FIN  MANEJO DE PRÉSTAMOS FIN ^^^^^^^^^^^^^^^^^ '''

        self.ENTRADA_NOMINA = 'NULL,'+' "'+self.TIPO_NOMINA+'","'+str(i)+'","'+self.PERIODO+'","'+ self.PERIODO[2:8] +'","'+str(self.SALARIO)+'","'+ \
            str(self.SALARIO_QUINCENA_NETO)+'","'+str(self.SALARIO_PARA_SEG_SOCIAL)+'","'+str(self.PAGO_AD_PER_ANT)+'","'+str(self.PAGO_ADELANTADO)+'","'+str(self.PAGO_DE_VAC)+'","'+\
            str(self.FRACCION_VAC) +'","'+ str(self.DIAS_DE_VAC_DISFRUTADOS)+'","'+self.FECHA_INICIO_VAC+'","'+self.FECHA_FIN_VAC + '","' + self.INDICE_VAC +'","'+\
            str(self.AFP_TRAB) + '","' + str(self.AFP_EMP) + '","' + str(self.APORTE_VOL_TRAB) + '","'+ str(self.APORTE_VOL_EMP) + '","' + str(self.SFS_TRAB) + '","' + str(self.SFS_EMP) + '","'\
        + str(self.SRL) + '","' + str(self.INFOTEP) +'","'+ str(self.SALARIO_INFOTEP) + '","' + str(self.ISLR_BASE) +'","' + str(self.ISLR_RETENCION) + \
            '","' + str(self.CESANTIA_PREV) + '","' + str(self.PREAVISO_PREV) + '","' + str(self.SAL_NAV_PREV) + '","' + \
            str(self.UTILIDADES_PREV) + '","' + str(self.VACACIONES_PREV) + '","' + str(self.HORAS_EXTRA) + '","' + \
            str(self.DESC_HE) + '","' + str(self.INASIS) + '","' + str(self.DESC_INA)+ '","' + str(self.OTRAS_REMUN)+\
                              '","' + str(self.DESC_OTRAS_REMUN) + '","' + str(self.OTRAS_REMUN_NO_SALARIAL) + '","' + str(self.COMISIONES) + '","' + str(self.DESC_COMISIONES) + '","' + \
             str(self.REM_OTROS_EMPLEADORES) + '","' + str(self.DESC_REM_OTROS_EMPLEADORES)+ '","' + str(self.INDEMNIZACIONES) +\
            '","' + str(self.DESC_INDEMNIZACIONES) + '","' + str(self.SALARIO_DE_NAVIDAD) +\
            '","' + str(self.MONTO_A_PAGAR) + '","' + self.nota + '","' + str(self.FECHA) + \
                              f'", "{self.TOTAL_PRESTAMOS}", "{self.DES_PRESTAMOS}", "{self.TOTAL_CUOTAS}", ' \
                              f'"{self.DES_CUOTAS}", "{self.TOTAL_A_DEPOSITAR}", "{self.FECHA_INICIO_PAGO}", ' \
                              f'"{self.FECHA_FIN_PAGO}" ,"{self.RET_PENSION_ALIMENTICIA}", "{self.SALDO_A_FAVOR}", ' \
                              f'"{self.RNC_AGENTE_RET}", "{self.OTRAS_REMUN_TODAS}", "{self.SALARIO_ISR}", "{self.ING_EXCENTOS_ISR}"'
        #print(self.ENTRADA_NOMINA)
        leew.introduce_nomina(self.ENTRADA_NOMINA)
        id_nomina = leew.consulta_gen('worker.db', 'max(ID_NOM)','nomina','ID_NOM>', '0') # notese el max para obtener ulimo reg y ID_NOM>=0 para usar la funcion leew.consulta tal como esta
        # actualizacion horas extra comptutado = 1 y id de nomina
        for idhe in self.lista_id_horas_extra:
            leew.update_gen('worker.db', 'horas_extras', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND id_h={idhe}')
        # actualizacion insistencias comptutado = 1 y id de nomina
        for idina in self.lista_id_inasis:
            leew.update_gen('worker.db', 'inasis', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND id_i={idina}')
        for idina_justificada in self.lista_id_inasis_justificadas:
            leew.update_gen('worker.db', 'inasis', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND id_i={idina_justificada}')

        # actualizacion comisiones comptutado = 1 y id de nomina
        for idc in self.lista_id_comisiones:
            leew.update_gen('worker.db', 'comisiones', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND id_c={idc}')
        # actualizacion otras rem comptutado = 1 y id de nomina
        for idor in self.lista_id_or:
            leew.update_gen('worker.db', 'otras_remun', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND idor={idor}')
        # actualizacion rem otros empleadores comptutado = 1 y id de nomina
        for idroe in self.lista_id_rem_otros_emp:
            leew.update_gen('worker.db', 'remun_otro_empleador', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND id_roe={idroe}')
        # actualizacion indemnizaciones comptutado = 1 y id de nomina
        for idindem in self.lista_id_indem:
            leew.update_gen('worker.db', 'indemnizaciones', 'computado',
                            f'1, id_nom={id_nomina} WHERE id={self.ID_TRABAJADOR} AND id_indem={idindem}')

        # IMPRIMIR RECIBO

        if self.imprimir_recibos == 1: # si el ceckbutton es activado se imprimen los recibos
            recibo_numero = str(leew.consulta_gen('worker.db', 'ID_NOM', 'nomina', 'ID_TRABAJADOR',
                                                  str(i) + ' AND PERIODO = "' + self.PERIODO + '"'))
            imprime.imprimir(recibo_numero, self.TIPO_NOMINA, i, self.PERIODO,self.DIA_INICIO_PER, self.DIA_FIN_PER, self.SALARIO, self.SALARIO / self.diasxmes, self.SALARIO_QUINCENA_NETO, self.COMISIONES,
                             self.PAGO_AD_PER_ANT,self.PAGO_ADELANTADO,self.PAGO_DE_VAC, self.DIAS_DE_VAC_DISFRUTADOS, self.FRACCION_VAC,
                             self.FECHA_INICIO_VAC, self.FECHA_FIN_VAC,self.AFP_TRAB, self.APORTE_VOL_TRAB, self.SFS_TRAB, self.ISLR_RETENCION,
                             self.HORAS_EXTRA,self.DESC_HE, self.INASIS, self.DESC_INA,0, self.OTRAS_REMUN, self.DESC_OTRAS_REMUN,self.SALARIO_DE_NAVIDAD, self.INDEMNIZACIONES,0,
                             self.MONTO_A_PAGAR, self.FECHA, self.TOTAL_PRESTAMOS, self.TOTAL_CUOTAS,
                             self.TOTAL_A_DEPOSITAR, self.FECHA_INICIO_PAGO, self.FECHA_FIN_PAGO)


indices_vac = set()


def funcion_para_hilos(periodo, imp_recibo, pagar_sal_nav, nota, trabajador_activo, tipo_de_nomina='Quincenal',fecha_i_pago = '', fecha_fin_pago = ''):
    corrida_trabajador = NominaProc(periodo, imp_recibo, pagar_sal_nav, nota, trabajador_activo,tipo_de_nomina, fecha_i_pago, fecha_fin_pago)

    # estos valores se sobre escriben en cada hilo o trabajador, pero no importa porque las vacaciones
    # son iguales para todos los trabajadores, entonces al final el ultimo hilo dirá lo mismo que los otros

    global indices_vac # son los indices de vacaciones que deben ser cerrados en la funcion corrida
    indices_vac = corrida_trabajador.indices_vac

def corrida(periodo,imp_recibo, pagar_sal_nav,nota):
    leew.backup_bd('nomina_quincenal')
    # se sacan a los trabajadores que estan activos pero que ya se les pagó en el periodo
    trabajadores_previamente_pagados = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','PERIODO',f'"{periodo}"')
    #print(trabajadores_previamente_pagados)
    trab_activos = leew.tambd_nom('worker.db')  # determina el numero de trabajdores activos a incluir en pago
    # abajo saco a los que en el periodo ya se le haya pagado alguna nomina cual sea
    trab_activos_sin_nomina = list(set(trab_activos) - set(trabajadores_previamente_pagados))

    if trab_activos_sin_nomina != []: # solo se ejecuta el bucle for de hilos cuando la lista tiene al menos un trabajor
        for id_trab_activos in trab_activos_sin_nomina:  # se itera para ir procesando cada trabajador
            hilo = threading.Thread(target=funcion_para_hilos, args=(periodo,imp_recibo, pagar_sal_nav,nota,id_trab_activos,))
            hilo.start()
            #print(hilo.getName())

        hilo.join() # si no hago esto el hilo principal se adelanta y me actualiza las bd de abajo

    # ACTUALIZACIÓN DE LAS BASES DE DATOS

    leew.update_periodo(periodo)  # para cerrar periodo procesado
    # PARA CREAR PERIDODO FISCAL
    fecha_cierre_fiscal_empresa = leew.consulta_gen('worker.db', 'opcional2', 'info_sociedad', 'estatus', '"Vigente"')
    #print(periodo[0:4], ' == ', fecha_cierre_fiscal_empresa)
    if periodo[0:4] == fecha_cierre_fiscal_empresa:# dependiendo de la empresa 2Q12, 2Q03, 2Q06, 2Q09
        leew.crea_periodo_fiscal(periodo) # funcion que crea el periodo fiscal
    #print(indices_vac)
    if indices_vac != set():
        #print("Indices vac: ", indices_vac)
        for indice_de_vac in indices_vac:
            leew.update_vac(str(indice_de_vac))  # para cerrar el status del periodo vacacional tratado en la nomina
    # PARA CERRAR LAS VACACIONES INDIVIDUALES QUE ESTEN ABIERTAS TODAVIA A FIN DE PERIODO
    indices_vacaciones_abiertas = leew.consulta_lista_distintc('worker.db', 'id_vac', 'vac_por_cerrar', 'status', '"Abierto"') # select distinc porque puede estar repetido port varios trabajadores
    for indv in indices_vacaciones_abiertas:
        leew.update_linea_gen('worker.db', 'vacaciones', 'status', 'CERRADO', 'indice', indv)
        leew.update_linea_gen('worker.db', 'vac_por_cerrar', 'status', 'Cerrado', 'id_vac', indv)


def corrida_de_un_trabajador(periodo, imp_recibo, pagar_sal_nav, nota, id_trabajador_activo, tipo_nomina,fecha_i_pago, fecha_fin_pago):

    # funcion para procesar nómina individual, necesario para poder liquidar a alguien
    leew.backup_bd('nomina_individual')
    funcion_para_hilos(periodo,imp_recibo,pagar_sal_nav, nota,id_trabajador_activo,tipo_nomina,fecha_i_pago, fecha_fin_pago)
    # actualizar bases de datos
    # no se cierra el periodo vacacional para que quede abierto para la nomina quincenal
    # no se cierra el periodo para que se pueda correr la nomina quincenal
    #print(indices_vac)
    for indice_de_vac in indices_vac: # tuve que usar este for porque los sets no tienen indices y no puedo hacer indices_vac[0]
        leew.introduce_gen('worker.db', 'vac_por_cerrar', f'NULL, {indice_de_vac}, "Abierto"')
