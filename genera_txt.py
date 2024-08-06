import leew, os

def generar_txt(periodo, novedad = 0, auto_men = 0, auto_retro = 0, recti = 0):
    # esta funcion solo recibe segundos periodos
    # con esta función se hacen los archivos TXT de la TSS
    perido_actual = periodo
    MMAAAA = perido_actual[2:8]
    #print('MMAAA= ',MMAAAA)
    # periodo anterior
    indice_per_actual = leew.consulta_gen('worker.db', 'indice', 'periodo', 'idp', '"' + perido_actual + '"')
    indice_per_anterior = int(indice_per_actual) - 1

    idp_per_anterior = leew.consulta_gen('worker.db', 'idp', 'periodo', 'indice',
                                              str(indice_per_anterior))
    if idp_per_anterior == None:
        idp_per_anterior = ""

    if indice_per_anterior > 0:
        trabajadores_nom_prim_quincena = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','periodo',f'"{idp_per_anterior}"')
    else:
        trabajadores_nom_prim_quincena = []

    trabajadores_nom_seg_quincena = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','periodo',f'"{perido_actual}"')

    list_trab_activos_mes = list(set(trabajadores_nom_prim_quincena + trabajadores_nom_seg_quincena)) # uso set para borrar elementos repetidos
    list_trab_activos_mes.sort()
    #print(list_trab_activos_mes)

    rnc = leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'Estatus', '"Vigente"')
    rnc_fixed = (11 - len(rnc)) * ' ' + rnc

    # creando el archivo txt novedades
    if novedad != 0:
        txt_novedades = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\NV_{rnc}_{periodo[2:]}.txt', 'w')
        encabezado = f'ENV{rnc_fixed}{periodo[2:]}\n'
        txt_novedades.write(encabezado)

    # creando el archivo txt AUTODETERMINACION MENSUAL
    if auto_men != 0:
        txt_autodeterminacion = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\AM_{rnc}_{periodo[2:]}.txt', 'w')
        encabezado = f'EAM{rnc_fixed}{periodo[2:]}\n'
        txt_autodeterminacion.write(encabezado)

    # creando el archivo txt AUTODETERMINACION RETRO
    if auto_retro != 0:
        txt_autodeterminacion_retro = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\AR_{rnc}_{periodo[2:]}.txt', 'w')
        encabezado = f'EAR{rnc_fixed}{periodo[2:]}\n'
        txt_autodeterminacion_retro.write(encabezado)

    # creando el archivo txt RECTIFICATIVA
    if recti != 0:
        txt_rectificativa = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\RT_{rnc}_{periodo[2:]}.txt', 'w')
        encabezado = f'ERT{rnc_fixed}{periodo[2:]}\n'
        txt_rectificativa.write(encabezado)


    listado_trabajadores_con_novedades = leew.consulta_lista_distintc('worker.db', 'idt','novedades','id_n>', f'1 AND periodo IN ("{idp_per_anterior}", "{periodo}")')
    # print(listado_trabajadores_con_novedades)
    linea_txt_novedad = ''
    tipo_de_novedad = ''
    fecha_de_inicio = ''
    fecha_fin = ''

    for id_trabajador in list_trab_activos_mes:
        clave_nomina = leew.consulta_gen('worker.db', 'clave_de_nomina','info','id',str(id_trabajador))
        if id_trabajador in listado_trabajadores_con_novedades: # las consultas sql las ordeno con ORDER BY id_n DESC para que salga la ùltima novedad
            tipo_de_novedad = leew.consulta_gen('worker.db', 'tipo_novedad', 'novedades','idt', f'"{id_trabajador}"AND periodo IN ("{idp_per_anterior}", "{periodo}") ORDER BY id_n DESC')
            fecha_de_inicio = leew.consulta_gen('worker.db', 'fecha_inicio', 'novedades','idt', f'"{id_trabajador}"AND periodo IN ("{idp_per_anterior}", "{periodo}") ORDER BY id_n DESC').replace("-","") # porque es una fecha dd-mm-aaaa
            fecha_fin = leew.consulta_gen('worker.db', 'fecha_fin', 'novedades', 'idt',
                                                f'"{id_trabajador}"AND periodo IN ("{idp_per_anterior}", "{periodo}") ORDER BY id_n DESC')
            if fecha_fin == None:
                fecha_fin = " " * 8
            else:
                fecha_fin = fecha_fin.replace("-","")
        tipo_de_trabajador = leew.consulta_gen('worker.db', 'tipo_de_persona','info','id',str(id_trabajador))
        tipo_documento = leew.consulta_gen('worker.db', 'tipo_doc','info','id',str(id_trabajador))
        num_de_documento = leew.consulta_gen('worker.db', 'Identificacion','info','id',str(id_trabajador))
        num_de_documento = num_de_documento + (25 - len(num_de_documento)) * " " # para rellenar con espacios hasta 25 de longitud
        primer_nombre = leew.consulta_gen('worker.db', 'Nombre','info','id',str(id_trabajador))
        segundo_nombre = leew.consulta_gen('worker.db', 'nombre2','info','id',str(id_trabajador))
        nombres = f'{primer_nombre} {segundo_nombre}'
        nombres = nombres + (50 - len(nombres)) * " "
        primer_apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', str(id_trabajador))
        primer_apellido = primer_apellido + (40 - len(primer_apellido)) * " "
        segundo_apelido = leew.consulta_gen('worker.db', 'apellido2', 'info', 'id', str(id_trabajador))
        segundo_apelido = segundo_apelido + (40 - len(segundo_apelido)) * " "
        sexo = leew.consulta_gen('worker.db', 'Sexo', 'info', 'id', str(id_trabajador))[0] # la primera letra es F o M
        fecha_de_nacimiento = leew.consulta_gen('worker.db', 'Fecha_nacimiento', 'info', 'id', str(id_trabajador)).replace("-", "")
        # vacaciones en liquidacion
        vacaciones_liquidacion = leew.consulta_gen('worker.db', 'vac_monto', 'liquidacion', 'id_trab',
                                                   str(id_trabajador))
        if vacaciones_liquidacion == None:
            vacaciones_liquidacion = 0

        # salario seguridad social
        sal_ss_1q = leew.consulta_gen('worker.db','SAL_PAR_SEG_SOCIAL','nomina','ID_TRABAJADOR',
                                   f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_ss_1q == None:
            sal_ss_1q = 0
        sal_ss_2q = leew.consulta_gen('worker.db', 'SAL_PAR_SEG_SOCIAL', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_ss_2q == None:
            sal_ss_2q = 0
        sal_ss_mes = sal_ss_1q + sal_ss_2q + vacaciones_liquidacion
        Salario_SS = str("{:.2f}".format(sal_ss_mes))
        Salario_SS = (16 - len(Salario_SS)) * "0" + Salario_SS

        #print(sal_ss_1q, sal_ss_2q, sal_ss_mes)
        ''' indice_per_anterior if id_trabajador in trabajadores_nom_seg_quincena'''
        if id_trabajador in trabajadores_nom_seg_quincena:
            # Aporte voluntario
            aporte_ordinario_voluntario_trab = leew.consulta_gen_sum('worker.db', 'APORTE_VOL_TRAB', 'nomina', 'ID_TRABAJADOR',
                                               f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')

            aporte_ordinario_voluntario_emp = leew.consulta_gen_sum('worker.db', 'APORTE_VOL_EMP', 'nomina',
                                                                     'ID_TRABAJADOR',
                                                                     f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')

            aporte_ordinario_voluntario = aporte_ordinario_voluntario_trab + aporte_ordinario_voluntario_emp
            # la funcion estandar zfill se usa para rellenar con ceros a la izquierda
            aporte_ordinario_voluntario = str("{:.2f}".format(aporte_ordinario_voluntario)).zfill(16)
            #print(aporte_ordinario_voluntario)
        else:
            # Aporte voluntario
            aporte_ordinario_voluntario_trab = leew.consulta_gen_sum('worker.db', 'APORTE_VOL_TRAB', 'nomina',
                                                                     'ID_TRABAJADOR',
                                                                     f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')

            aporte_ordinario_voluntario_emp = leew.consulta_gen_sum('worker.db', 'APORTE_VOL_EMP', 'nomina',
                                                                    'ID_TRABAJADOR',
                                                                    f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')

            aporte_ordinario_voluntario = aporte_ordinario_voluntario_trab + aporte_ordinario_voluntario_emp
            # la funcion estandar zfill se usa para rellenar con ceros a la izquierda
            aporte_ordinario_voluntario = str("{:.2f}".format(aporte_ordinario_voluntario)).zfill(16)
            # print(aporte_ordinario_voluntario)

        # salario ISR + las vacaciones de la liquidacion

        sal_isr_1q = leew.consulta_gen('worker.db','SALARIO_ISR','nomina','ID_TRABAJADOR',
                                   f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_isr_1q == None:
            sal_isr_1q = 0
        sal_isr_2q = leew.consulta_gen('worker.db', 'SALARIO_ISR', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_isr_2q == None:
            sal_isr_2q = 0
        Salario_ISR = sal_isr_1q + sal_isr_2q
        Salario_ISR = str("{:.2f}".format(Salario_ISR))
        Salario_ISR = (16 - len(Salario_ISR)) * "0" + Salario_ISR
                #print(sal_isr_1q, sal_isr_2q, sal_isr_mes)

        # Otras remuneraciones del trabajador en el mes aplicables solo al ISR
        otras_remuneraciones = leew.consulta_gen_sum('worker.db', 'OTRAS_REMUN_TODAS', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        otras_remuneraciones = str("{:.2f}".format(otras_remuneraciones + vacaciones_liquidacion))
        otras_remuneraciones = otras_remuneraciones.zfill(16)
        #print(otras_remuneraciones)

        # Rnc de agente de otro retencion
        # el agente de retencion es la propia empresa que reporta el ingreso del trabajador proveniente de otro empleador
        # por lo tanto el campo rnc_agente_ret en la BD que se guarda en nomina_quincenal.py que guardaba el rnc del otro empleo
        # no se usa actualmente
        RNC_agente_de_ret = rnc_fixed

        # remuneracion de otros empleadores
        rem_otros_empleadores = str("{:.2f}".format(leew.consulta_gen_sum('worker.db', 'REM_OTROS_EMPLEADORES',
                            'nomina', 'ID_TRABAJADOR',f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"'))).zfill(16)

        #print(rem_otros_empleadores)
        # sal navidad regalia pascual

        sal_nav_1q = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_nav_1q == None:
            sal_nav_1q = 0
        sal_nav_2q = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_nav_2q == None:
            sal_nav_2q = 0

        sal_nav_en_liq = leew.consulta_gen('worker.db', 'sal_nav_monto', 'liquidacion', 'id_trab',
                                                   str(id_trabajador))
        if sal_nav_en_liq == None:
            sal_nav_en_liq = 0
        sal_nav_mes = sal_nav_1q + sal_nav_2q + sal_nav_en_liq

        if sal_nav_mes != 0:
            sal_navidad01 = sal_nav_mes
            sal_navidad01 = str("{:.2f}".format(sal_navidad01))
            sal_navidad01 = "01" + (16 - len(sal_navidad01)) * "0" + sal_navidad01
        else:
            sal_navidad01 = ''
        # ingreso excentos

        cesantia = leew.consulta_gen('worker.db','cesantia_monto','liquidacion','id_trab',str(id_trabajador))
        if cesantia == None:
            cesantia = 0

        pre_aviso = leew.consulta_gen('worker.db', 'monto_pre_aviso', 'liquidacion', 'id_trab', str(id_trabajador))
        if pre_aviso == None:
            pre_aviso = 0

        indemnizaciones = leew.consulta_gen_sum('worker.db', 'INDEMNIZACIONES','nomina', 'ID_TRABAJADOR',
                                                f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')

        if cesantia + pre_aviso + indemnizaciones != 0:
            pre_aviso_cesantia_viatico_indem02 = cesantia + pre_aviso + indemnizaciones
            pre_aviso_cesantia_viatico_indem02 = str("{:.2f}".format(pre_aviso_cesantia_viatico_indem02))
            pre_aviso_cesantia_viatico_indem02 = "02" + (16 - len(pre_aviso_cesantia_viatico_indem02)) * "0" + pre_aviso_cesantia_viatico_indem02
        else:
            pre_aviso_cesantia_viatico_indem02 = ''

        pension_alimenticia =leew.consulta_gen_sum('worker.db', 'RET_PENSION_ALIM', 'nomina', 'ID_TRABAJADOR',
                                  f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if pension_alimenticia != 0:
            pension_alimenticia03 = "03" + str("{:.2f}".format(leew.consulta_gen_sum('worker.db', 'RET_PENSION_ALIM', 'nomina', 'ID_TRABAJADOR',
                                  f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"'))).zfill(16)
        else:
            pension_alimenticia03 = ''

        ingresos_exentos_ISR = cesantia + pre_aviso + pension_alimenticia + sal_nav_mes + indemnizaciones
        ingresos_exentos_ISR = str("{:.2f}".format(ingresos_exentos_ISR))
        ingresos_exentos_ISR = (16 - len(ingresos_exentos_ISR)) * "0" + ingresos_exentos_ISR
        ingresos_exentos_ISR = '0000000000000.00' # obligatoriamente asi dice el manual de archivo
        #print('ingex',ingresos_exentos_ISR)

        if id_trabajador in trabajadores_nom_seg_quincena:
            # saldo a favor del periodo
            saldo_a_favor_del_per = str("{:.2f}".format(leew.consulta_gen('worker.db', 'SALDO_A_FAVOR', 'nomina', 'ID_TRABAJADOR',
                                              f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"'))).zfill(16)
        else:
            # saldo a favor del periodo
            saldo_a_favor_del_per = str(
                "{:.2f}".format(leew.consulta_gen('worker.db', 'SALDO_A_FAVOR', 'nomina', 'ID_TRABAJADOR',
                                                  f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"'))).zfill(16)

        # salario INFOTEP

        sal_infotep_1q = leew.consulta_gen('worker.db', 'INFOTEP_BASE', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_infotep_1q == None:
            sal_infotep_1q = 0
        sal_infotep_2q = leew.consulta_gen('worker.db', 'INFOTEP_BASE', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_infotep_2q == None:
            sal_infotep_2q = 0
        sal_cotizable_infotep = sal_infotep_1q + sal_infotep_2q + vacaciones_liquidacion
        sal_cotizable_infotep = str("{:.2f}".format(sal_cotizable_infotep))
        sal_cotizable_infotep = (16 - len(sal_cotizable_infotep)) * "0" + sal_cotizable_infotep
        # print(sal_cotizable_infotep)

        # tipo de ingreso

        tipo_de_ingreso = leew.consulta_gen('worker.db', 'tipo_de_ingreso','info','id',str(id_trabajador))

        inasistentes_periodo_ant = leew.consulta_lista('worker.db', 'id', 'inasis', 'periodo', f'"{idp_per_anterior}"')
        inasistentes_periodo_actual = leew.consulta_lista('worker.db', 'id', 'inasis', 'periodo',
                                                          f'"{perido_actual}"')

        inasistentes_del_mes = inasistentes_periodo_ant + inasistentes_periodo_actual # sumo las listas porque no importan los id repetidos
        #print(inasistentes_del_mes)
        if id_trabajador in inasistentes_del_mes:
            tipo_de_ingreso = '0004' # sobre escribo el valor por defecto que tiene el trabajador en la ficha porque tuvo una falta en el mes


        # TXT NOVEDADES INICIO vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
        if novedad != 0:
            if id_trabajador in listado_trabajadores_con_novedades:
                linea_txt_novedad = f'D{clave_nomina}{tipo_de_novedad}{fecha_de_inicio}{fecha_fin}{tipo_documento}' \
                                    f'{num_de_documento}{nombres}{primer_apellido}{segundo_apelido}{sexo}' \
                                    f'{fecha_de_nacimiento}{Salario_SS}{aporte_ordinario_voluntario}{Salario_ISR}' \
                                    f'{otras_remuneraciones}{RNC_agente_de_ret}{rem_otros_empleadores}{ingresos_exentos_ISR}' \
                                    f'{saldo_a_favor_del_per}{sal_cotizable_infotep}{tipo_de_ingreso}{sal_navidad01}' \
                                    f'{pre_aviso_cesantia_viatico_indem02}{pension_alimenticia03}\n'
                txt_novedades.write(linea_txt_novedad)
        # TXT NOVEDADES FIN ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

        # TXT AUTODETERMINACION MENSUAL INICIOvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
        if auto_men != 0:
            linea_txt_auto_men = f'D{clave_nomina}{tipo_documento}' \
                                f'{num_de_documento}{nombres}{primer_apellido}{segundo_apelido}{sexo}' \
                                f'{fecha_de_nacimiento}{Salario_SS}{aporte_ordinario_voluntario}{Salario_ISR}' \
                                f'{otras_remuneraciones}{RNC_agente_de_ret}{rem_otros_empleadores}{ingresos_exentos_ISR}' \
                                f'{saldo_a_favor_del_per}{sal_cotizable_infotep}{tipo_de_ingreso}{sal_navidad01}' \
                                f'{pre_aviso_cesantia_viatico_indem02}{pension_alimenticia03}\n'
            txt_autodeterminacion.write(linea_txt_auto_men)

        # TXT AUTODETERMINACION MENSUALFIN ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

        # TXT AUTODETERMINACION MENSUA RETRO INICIOvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
        if auto_retro != 0:
            linea_txt_auto_retro = f'D{clave_nomina}{tipo_documento}' \
                                f'{num_de_documento}{nombres}{primer_apellido}{segundo_apelido}{sexo}' \
                                f'{fecha_de_nacimiento}{Salario_SS}{aporte_ordinario_voluntario}{Salario_ISR}' \
                                f'{otras_remuneraciones}{RNC_agente_de_ret}{rem_otros_empleadores}{ingresos_exentos_ISR}' \
                                f'{saldo_a_favor_del_per}{sal_cotizable_infotep}{tipo_de_ingreso}{sal_navidad01}' \
                                f'{pre_aviso_cesantia_viatico_indem02}{pension_alimenticia03}\n'
            txt_autodeterminacion_retro.write(linea_txt_auto_retro)

        # TXT AUTODETERMINACION MENSUALFIN ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

        # TXT RECTIFICATIVA INICIOvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
        if recti != 0:
            linea_txt_recti = f'D{tipo_de_trabajador}{tipo_documento}' \
                                f'{num_de_documento}{nombres}{primer_apellido}{segundo_apelido}{sexo}' \
                                f'{fecha_de_nacimiento}{Salario_ISR}' \
                                f'{otras_remuneraciones}{RNC_agente_de_ret}{rem_otros_empleadores}{ingresos_exentos_ISR}' \
                                f'{saldo_a_favor_del_per}{sal_navidad01}' \
                                f'{pre_aviso_cesantia_viatico_indem02}{pension_alimenticia03}\n'
            txt_rectificativa.write(linea_txt_recti)
        # TXT RECTIFICATIVA FIN ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

    if novedad != 0:
        lineas_txt_nov = str(len(listado_trabajadores_con_novedades) + 2) # la suma del 2 es 1 por el encabezado y 1 por el sumario mismo
        lineas_txt_nov = (6 - len(lineas_txt_nov)) * '0' + str(lineas_txt_nov)
        sumario = f'S{lineas_txt_nov}'
        txt_novedades.write(sumario)
        txt_novedades.close()
        os.startfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\NV_{rnc}_{periodo[2:]}.txt')

    lineas_archivos = str(len(list_trab_activos_mes) + 2) # la suma del 2 es 1 por el encabezado y 1 por el sumario mismo
    lineas_txt = (6 - len(lineas_archivos)) * '0' + str(lineas_archivos)
    if auto_men != 0:
        sumario = f'S{lineas_txt}'
        txt_autodeterminacion.write(sumario)
        txt_autodeterminacion.close()
        os.startfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\AM_{rnc}_{periodo[2:]}.txt')

    if auto_retro != 0:
        sumario = f'S{lineas_txt}'
        txt_autodeterminacion_retro.write(sumario)
        txt_autodeterminacion_retro.close()
        os.startfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\AR_{rnc}_{periodo[2:]}.txt')

    if recti != 0:
        sumario = f'S{lineas_txt}'
        txt_rectificativa.write(sumario)
        txt_rectificativa.close()
        os.startfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\RT_{rnc}_{periodo[2:]}.txt')

