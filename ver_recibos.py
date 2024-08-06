import imprime
import leew

def ver_recibos(periodo, tipo_nomina='quincenal', nota=''):
    if tipo_nomina == 'quincenal':
        listado_de_recibos = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','PERIODO','"' + periodo + '"')
        DIA_INICIO_PER = leew.consulta_gen('worker.db', 'f_inicio', 'periodo', 'idp', '"' + periodo + '"')
        DIA_FIN_PER = leew.consulta_gen('worker.db', 'f_fin', 'periodo', 'idp', '"' + periodo + '"')
        dias_por_mes = leew.consulta_gen('worker.db', 'dias_mes', 'beneficios', 'status', '"Vigente"')
        for id_trab in listado_de_recibos:
            i = str(id_trab)
            RECIBO_NUMERO = str(leew.consulta_gen('worker.db', 'ID_NOM', 'nomina', 'PERIODO',
                                                  '"' + periodo + '" AND ID_TRABAJADOR = ' + i))
            TIPO_NOMINA = leew.consulta_gen('worker.db','TIPO_NOMINA','nomina','PERIODO','"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            PERIODO = periodo
            SALARIO = leew.consulta_gen('worker.db','SALARIO','nomina','PERIODO','"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            SALARIO_DIARIO = SALARIO / dias_por_mes
            SALARIO_QUINCENA = leew.consulta_gen('worker.db','SALARIO_QUINCENA','nomina','PERIODO','"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            COMISION = leew.consulta_gen('worker.db', 'COMISIONES', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            FRACCION_VAC = leew.consulta_gen('worker.db','FRACCION_VAC','nomina','PERIODO','"' + periodo + '" AND ID_TRABAJADOR = ' + i)

            PAGO_AD_PER_ANT = leew.consulta_gen('worker.db','PAGO_AD_PER_ANT','nomina','PERIODO','"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            PAGO_ADELANTADO = leew.consulta_gen('worker.db', 'PAGO_ADELANTADO', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            PAGO_DE_VAC = leew.consulta_gen('worker.db','PAGO_DE_VAC','nomina','PERIODO','"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            DIAS_DE_VAC_DISFRUTADOS = leew.consulta_gen('worker.db', 'DIAS_DE_VAC_DISFRUTADOS', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            FECHA_INICIO_VAC = leew.consulta_gen('worker.db', 'FECHA_INICIO_VAC', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            FECHA_FIN_VAC = leew.consulta_gen('worker.db', 'FECHA_FIN_VAC', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            AFP_TRAB = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            AFP_VOLUNTARIO = leew.consulta_gen('worker.db', 'APORTE_VOL_TRAB', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            SFS_TRAB = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            ISLR_RETENCION = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            HORAS_EXTRA = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'PERIODO',
                                               '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            DESC_HE = leew.consulta_gen('worker.db', 'DESC_HE', 'nomina', 'PERIODO',
                                            '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            DESC_HE = DESC_HE[1:len(DESC_HE) - 1]

            DESC_HE = [n for n in DESC_HE.split(',')]

            INASIS = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'PERIODO',
                                        '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

            DESC_INA = leew.consulta_gen('worker.db', 'DESC_INA', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            DESC_INA = DESC_INA[1:len(DESC_INA) - 1]

            DESC_INA = [n for n in DESC_INA.split(',')]

            INFOTEP_TRAB = 0 # en quincena no se retiene INFOTEP solo en pago de pat beneficios

            OTRAS_REMUN = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'PERIODO',
                                       '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

            DESC_OTRAS_REMUN = leew.consulta_gen('worker.db', 'DESC_OTRAS_REMUN', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            DESC_OTRAS_REMUN = DESC_OTRAS_REMUN[1:len(DESC_OTRAS_REMUN) - 1]

            DESC_OTRAS_REMUN = [n for n in DESC_OTRAS_REMUN.split(',')]

            SALARIO_DE_NAVIDAD = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            INDEMNIZACION = leew.consulta_gen('worker.db', 'INDEMNIZACIONES', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

            BENEFICIOS = 0 # en nomina quincenal no se paga Bonificaci[on por part en los beneficios

            MONTO_A_PAGAR = leew.consulta_gen('worker.db', 'MONTO_A_PAGAR', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            FECHA = leew.consulta_gen('worker.db', 'FECHA', 'nomina', 'PERIODO',
                                              '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

            PRESTAMOS = leew.consulta_gen('worker.db', 'PRESTAMOS', 'nomina', 'PERIODO',
                                              '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            CUOTAS = leew.consulta_gen('worker.db', 'CUOTAS', 'nomina', 'PERIODO',
                                              '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            TOTAL_DEPOSITAR = leew.consulta_gen('worker.db', 'TOTAL_DEPOSITAR', 'nomina', 'PERIODO',
                                              '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            FECHA_I_PAGO = leew.consulta_gen('worker.db', 'FECHA_INICIO_PAGO', 'nomina', 'PERIODO',
                                             '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            if FECHA_I_PAGO == None:
                FECHA_I_PAGO = 'N/A'
            FECHA_FIN_PAGO = leew.consulta_gen('worker.db', 'FECHA_FIN_PAGO', 'nomina', 'PERIODO',
                                               '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
            if FECHA_FIN_PAGO == None:
                FECHA_FIN_PAGO = 'N/A'

            imprime.imprimir(RECIBO_NUMERO,TIPO_NOMINA,i,PERIODO, DIA_INICIO_PER, DIA_FIN_PER,SALARIO, SALARIO_DIARIO,SALARIO_QUINCENA, COMISION, PAGO_AD_PER_ANT,PAGO_ADELANTADO,PAGO_DE_VAC,
                 DIAS_DE_VAC_DISFRUTADOS, FRACCION_VAC,FECHA_INICIO_VAC,FECHA_FIN_VAC,AFP_TRAB, AFP_VOLUNTARIO,SFS_TRAB,ISLR_RETENCION,HORAS_EXTRA,
                    DESC_HE,INASIS,DESC_INA,INFOTEP_TRAB,OTRAS_REMUN,DESC_OTRAS_REMUN,SALARIO_DE_NAVIDAD,INDEMNIZACION,BENEFICIOS,MONTO_A_PAGAR,FECHA,
                             PRESTAMOS, CUOTAS, TOTAL_DEPOSITAR, FECHA_I_PAGO, FECHA_FIN_PAGO)
    if tipo_nomina == 'beneficios':
        listado_de_recibos = leew.consulta_lista('worker.db', 'idt', 'nomina_beneficios', 'idp_fiscal', '"' + periodo + '"')
        DIA_INICIO_PER = leew.consulta_gen('worker.db', 'fecha_i', 'periodo_fiscal', 'idp', '"' + periodo + '"')
        DIA_FIN_PER = leew.consulta_gen('worker.db', 'fecha_f', 'periodo_fiscal', 'idp', '"' + periodo + '"')
        for id_trab in listado_de_recibos:
            i = str(id_trab)
            RECIBO_NUMERO = str(leew.consulta_gen('worker.db', 'idn', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i))
            TIPO_NOMINA = 'PARTICIPACIÓN EN LOS BENEFICIOS'
            PERIODO = periodo

            SALARIO = leew.consulta_gen('worker.db', 'salario_mensual', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i)
            SALARIO = float(SALARIO.replace('RD$','').replace(',',''))
            SALARIO_DIARIO = leew.consulta_gen('worker.db', 'salario_diario', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i)

            SALARIO_DIARIO = float(SALARIO_DIARIO.replace('RD$','').replace(',',''))
            SALARIO_QUINCENA = 0
            COMISION = 0
            INDEMNIZACION = 0
            FRACCION_VAC = 0.0

            PAGO_AD_PER_ANT = 0.0
            PAGO_ADELANTADO = 0.0
            PAGO_DE_VAC = 0.0
            DIAS_DE_VAC_DISFRUTADOS = 0
            FECHA_INICIO_VAC = 'N/A'
            FECHA_FIN_VAC = 'N/A'
            AFP_TRAB = 0.0
            AFP_VOLUNTARIO = 0.0
            SFS_TRAB = 0.0
            ISLR_RETENCION = leew.consulta_gen('worker.db', 'ret_islr', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i)
            ISLR_RETENCION = float(ISLR_RETENCION.replace('RD$','').replace(',',''))
            HORAS_EXTRA = 0.0
            DESC_HE = ''
            INASIS = 0.0
            DESC_INA = ''
            INFOTEP_TRAB = leew.consulta_gen('worker.db', 'ret_infotep', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i)
            INFOTEP_TRAB = float(INFOTEP_TRAB.replace('RD$','').replace(',',''))
            OTRAS_REMUN = 0.0
            DESC_OTRAS_REMUN = ''
            SALARIO_DE_NAVIDAD = 0.0

            BENEFICIOS = leew.consulta_gen('worker.db', 'monto_ajustado', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i)
            BENEFICIOS = float(BENEFICIOS.replace('RD$','').replace(',',''))

            MONTO_A_PAGAR = BENEFICIOS - INFOTEP_TRAB - ISLR_RETENCION
            FECHA = leew.consulta_gen('worker.db', 'fecha_doc', 'nomina_beneficios', 'idp_fiscal',
                                        '"' + periodo + '" AND idt = ' + i)

            PRESTAMOS = 0
            CUOTAS = 0
            TOTAL_DEPOSITAR = MONTO_A_PAGAR
            FECHA_I_PAGO = leew.consulta_gen('worker.db', 'fecha_i', 'periodo_fiscal', 'idp',
                                        '"' + periodo + '"')
            if FECHA_I_PAGO == None:
                FECHA_I_PAGO = 'N/A'
            FECHA_FIN_PAGO = leew.consulta_gen('worker.db', 'fecha_f', 'periodo_fiscal', 'idp',
                                        '"' + periodo + '"')
            if FECHA_FIN_PAGO == None:
                FECHA_FIN_PAGO = 'N/A'

            imprime.imprimir(RECIBO_NUMERO,TIPO_NOMINA, i, PERIODO, DIA_INICIO_PER, DIA_FIN_PER, SALARIO, SALARIO_DIARIO,
                             SALARIO_QUINCENA, COMISION, PAGO_AD_PER_ANT, PAGO_ADELANTADO, PAGO_DE_VAC,
                             DIAS_DE_VAC_DISFRUTADOS, FRACCION_VAC, FECHA_INICIO_VAC, FECHA_FIN_VAC, AFP_TRAB,
                             AFP_VOLUNTARIO, SFS_TRAB, ISLR_RETENCION, HORAS_EXTRA, DESC_HE, INASIS, DESC_INA,
                             INFOTEP_TRAB, OTRAS_REMUN, DESC_OTRAS_REMUN, SALARIO_DE_NAVIDAD, INDEMNIZACION,
                             BENEFICIOS, MONTO_A_PAGAR, FECHA, PRESTAMOS, CUOTAS, TOTAL_DEPOSITAR, FECHA_I_PAGO,
                             FECHA_FIN_PAGO)


def ver_recibo(id_trab, periodo,tipo_nomina='quincenal'):
    if tipo_nomina == 'quincenal':
        DIA_INICIO_PER = leew.consulta_gen('worker.db', 'f_inicio', 'periodo', 'idp', '"' + periodo + '"')
        DIA_FIN_PER = leew.consulta_gen('worker.db', 'f_fin', 'periodo', 'idp', '"' + periodo + '"')
        dias_por_mes = leew.consulta_gen('worker.db', 'dias_mes', 'beneficios', 'status', '"Vigente"')
        '''esto imprime un recibo solamente'''
        i = str(id_trab)
        RECIBO_NUMERO = str(leew.consulta_gen('worker.db', 'ID_NOM', 'nomina', 'PERIODO',
                                              '"' + periodo + '" AND ID_TRABAJADOR = ' + i))
        TIPO_NOMINA = leew.consulta_gen('worker.db', 'TIPO_NOMINA', 'nomina', 'PERIODO',
                                        '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        PERIODO = periodo
        SALARIO = leew.consulta_gen('worker.db', 'SALARIO', 'nomina', 'PERIODO',
                                    '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        SALARIO_DIARIO = SALARIO / dias_por_mes
        SALARIO_QUINCENA = leew.consulta_gen('worker.db', 'SALARIO_QUINCENA', 'nomina', 'PERIODO',
                                             '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        COMISION = leew.consulta_gen('worker.db', 'COMISIONES', 'nomina', 'PERIODO',
                                     '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        FRACCION_VAC = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

        PAGO_AD_PER_ANT = leew.consulta_gen('worker.db', 'PAGO_AD_PER_ANT', 'nomina', 'PERIODO',
                                            '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        PAGO_ADELANTADO = leew.consulta_gen('worker.db', 'PAGO_ADELANTADO', 'nomina', 'PERIODO',
                                            '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        PAGO_DE_VAC = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'PERIODO',
                                        '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        DIAS_DE_VAC_DISFRUTADOS = leew.consulta_gen('worker.db', 'DIAS_DE_VAC_DISFRUTADOS', 'nomina', 'PERIODO',
                                                    '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        FECHA_INICIO_VAC = leew.consulta_gen('worker.db', 'FECHA_INICIO_VAC', 'nomina', 'PERIODO',
                                             '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        FECHA_FIN_VAC = leew.consulta_gen('worker.db', 'FECHA_FIN_VAC', 'nomina', 'PERIODO',
                                          '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        AFP_TRAB = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'PERIODO',
                                     '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        AFP_VOLUNTARIO = leew.consulta_gen('worker.db', 'APORTE_VOL_TRAB', 'nomina', 'PERIODO',
                                                '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        SFS_TRAB = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'PERIODO',
                                     '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        ISLR_RETENCION = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'PERIODO',
                                           '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        HORAS_EXTRA = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'PERIODO',
                                        '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        DESC_HE = leew.consulta_gen('worker.db', 'DESC_HE', 'nomina', 'PERIODO',
                                    '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        DESC_HE = DESC_HE[1:len(DESC_HE) - 1]

        DESC_HE = [n for n in DESC_HE.split(',')]

        INASIS = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'PERIODO',
                                   '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

        DESC_INA = leew.consulta_gen('worker.db', 'DESC_INA', 'nomina', 'PERIODO',
                                     '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        DESC_INA = DESC_INA[1:len(DESC_INA) - 1]

        DESC_INA = [n for n in DESC_INA.split(',')]

        INFOTEP_TRAB = 0  # en quincena no se retiene INFOTEP solo en pago de pat beneficios

        OTRAS_REMUN = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'PERIODO',
                                        '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

        DESC_OTRAS_REMUN = leew.consulta_gen('worker.db', 'DESC_OTRAS_REMUN', 'nomina', 'PERIODO',
                                             '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        DESC_OTRAS_REMUN = DESC_OTRAS_REMUN[1:len(DESC_OTRAS_REMUN) - 1]

        DESC_OTRAS_REMUN = [n for n in DESC_OTRAS_REMUN.split(',')]

        SALARIO_DE_NAVIDAD = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'PERIODO',
                                               '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        INDEMNIZACION = leew.consulta_gen('worker.db', 'INDEMNIZACIONES', 'nomina', 'PERIODO',
                                          '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        BENEFICIOS = 0 # en esta nomina no se pagan beneficios
        MONTO_A_PAGAR = leew.consulta_gen('worker.db', 'MONTO_A_PAGAR', 'nomina', 'PERIODO',
                                          '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        FECHA = leew.consulta_gen('worker.db', 'FECHA', 'nomina', 'PERIODO',
                                  '"' + periodo + '" AND ID_TRABAJADOR = ' + i)

        PRESTAMOS = leew.consulta_gen('worker.db', 'PRESTAMOS', 'nomina', 'PERIODO',
                                      '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        CUOTAS = leew.consulta_gen('worker.db', 'CUOTAS', 'nomina', 'PERIODO',
                                   '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        TOTAL_DEPOSITAR = leew.consulta_gen('worker.db', 'TOTAL_DEPOSITAR', 'nomina', 'PERIODO',
                                            '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        FECHA_I_PAGO = leew.consulta_gen('worker.db', 'FECHA_INICIO_PAGO', 'nomina', 'PERIODO',
                                         '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        if FECHA_I_PAGO == None:
            FECHA_I_PAGO = 'N/A'
        FECHA_FIN_PAGO = leew.consulta_gen('worker.db', 'FECHA_FIN_PAGO', 'nomina', 'PERIODO',
                                           '"' + periodo + '" AND ID_TRABAJADOR = ' + i)
        if FECHA_FIN_PAGO == None:
            FECHA_FIN_PAGO = 'N/A'

        imprime.imprimir(RECIBO_NUMERO,TIPO_NOMINA,i,PERIODO, DIA_INICIO_PER, DIA_FIN_PER,SALARIO, SALARIO_DIARIO,SALARIO_QUINCENA, COMISION, PAGO_AD_PER_ANT,PAGO_ADELANTADO,PAGO_DE_VAC,
                 DIAS_DE_VAC_DISFRUTADOS, FRACCION_VAC,FECHA_INICIO_VAC,FECHA_FIN_VAC,AFP_TRAB, AFP_VOLUNTARIO,SFS_TRAB,ISLR_RETENCION,HORAS_EXTRA,
                    DESC_HE,INASIS,DESC_INA,INFOTEP_TRAB,OTRAS_REMUN,DESC_OTRAS_REMUN,SALARIO_DE_NAVIDAD,INDEMNIZACION,BENEFICIOS,MONTO_A_PAGAR,FECHA,
                             PRESTAMOS, CUOTAS, TOTAL_DEPOSITAR, FECHA_I_PAGO, FECHA_FIN_PAGO)

    if tipo_nomina == 'beneficios':
        # todo cundo desde la ficha de trbajador se imprima el recibo de part en lo beneficios
        pass

    if tipo_nomina == 'egreso':
        i = str(id_trab)
        PERIODO = periodo
        FECHA_DE_INGRES0 = leew.consulta_gen('worker.db', 'Fecha_ingreso', 'info', 'id', f'"{str(i)}"')
        FECHA_DE_SALIDA = leew.consulta_gen('worker.db', 'Fecha_egreso', 'info', 'id', f'"{str(i)}"')
        TIEMPO_LABORANDO = leew.consulta_gen('worker.db', 'tiempo_lab', 'liquidacion', 'id_trab', f'"{str(i)}"')
        SALARIO_PROM_MES = leew.consulta_gen('worker.db', 'sal_prom_mes', 'liquidacion', 'id_trab', f'"{str(i)}"')
        SALARIO_DIARIO = leew.consulta_gen('worker.db', 'sal_prom_dia', 'liquidacion', 'id_trab', f'"{str(i)}"')
        ULTIMO_SALARIO = leew.consulta_gen('worker.db', 'salario_actual', 'liquidacion', 'id_trab', f'"{str(i)}"')
        AFP_TRAB = leew.consulta_gen('worker.db', 'afp_trab', 'liquidacion', 'id_trab', f'"{str(i)}"')
        SFS_TRAB = leew.consulta_gen('worker.db', 'sfs_trab', 'liquidacion', 'id_trab', f'"{str(i)}"')
        ISLR_RETENCION = leew.consulta_gen('worker.db', 'islr_ret', 'liquidacion', 'id_trab', f'"{str(i)}"')
        PRESTAMOS_PENDIENTES = leew.consulta_gen('worker.db', 'prestamos_pendientes', 'liquidacion', 'id_trab', f'"{str(i)}"')
        PREAVISO = leew.consulta_gen('worker.db', 'monto_pre_aviso', 'liquidacion', 'id_trab', f'"{str(i)}"')
        CESANTIA = leew.consulta_gen('worker.db', 'cesantia_monto', 'liquidacion', 'id_trab', f'"{str(i)}"')
        VACACIONES = leew.consulta_gen('worker.db', 'vac_monto', 'liquidacion', 'id_trab', f'"{str(i)}"')
        SALARIO_NAVIDAD = leew.consulta_gen('worker.db', 'sal_nav_monto', 'liquidacion', 'id_trab', f'"{str(i)}"')
        MONTO_ADICIONAL = leew.consulta_gen('worker.db', 'bono_monto', 'liquidacion', 'id_trab', f'"{str(i)}"')
        MONTO_A_PAGAR = leew.consulta_gen('worker.db', 'total_liq', 'liquidacion', 'id_trab', f'"{str(i)}"')
        imprime.imprimir_liquidacion(i, PERIODO, FECHA_DE_INGRES0, FECHA_DE_SALIDA, TIEMPO_LABORANDO, SALARIO_PROM_MES,
                                     SALARIO_DIARIO, ULTIMO_SALARIO, AFP_TRAB, SFS_TRAB, ISLR_RETENCION,
                                     PRESTAMOS_PENDIENTES, PREAVISO,
                                     CESANTIA, VACACIONES, SALARIO_NAVIDAD, MONTO_ADICIONAL, MONTO_A_PAGAR)
