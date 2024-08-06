import leew, numpy, webbrowser, os, datetime


def imprime(periodo, nota):
    # esta funcion solo recibe segundos periodos
    # con esta función se imprime un resumen de la suma de los recibos de cada trabajador en un mes. Se suman ambas quincenas
    perido_actual = periodo

    # periodo anterior
    indice_per_actual = leew.consulta_gen('worker.db', 'indice', 'periodo', 'idp', '"' + perido_actual + '"')
    indice_per_anterior = int(
        indice_per_actual) - 1
    MMAAAA = perido_actual[2:8]
    #print(MMAAAA)

    idp_per_anterior = leew.consulta_gen('worker.db', 'idp', 'periodo', 'indice',
                                              str(indice_per_anterior))

    if indice_per_anterior > 0: # por si acaso no hay registros en la BD
        trabajadores_nom_prim_quincena = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','periodo',f'"{idp_per_anterior}"')
    else:
        trabajadores_nom_prim_quincena = []

    trabajadores_nom_seg_quincena = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','periodo',f'"{perido_actual}"')

    list_trab_activos_mes = list(set(trabajadores_nom_prim_quincena + trabajadores_nom_seg_quincena)) # uso set para borrar elementos repetidos
    list_trab_activos_mes = numpy.sort(list_trab_activos_mes) # forma fácil de ordenar la lista
    #print("listado de trabajadores activos",list_trab_activos_mes)

    # discrimino por tipo de nomina: planta o daministracion
    list_trab_activos_mes_produccion = []
    list_trab_activos_mes_administrativo = []
    for id_trabajador in list_trab_activos_mes:
        if leew.consulta_gen('worker.db','tipo_de_nomina','info','id',f'"{str(id_trabajador)}"') == "Producción":
            list_trab_activos_mes_produccion.append(id_trabajador)
        else:#en el caso de que sea administrativo
            list_trab_activos_mes_administrativo.append(id_trabajador)

    #print("Produccion",list_trab_activos_mes_produccion)
    #print("Administracion",list_trab_activos_mes_administrativo)
    periodos_juntos = f'{idp_per_anterior}_{perido_actual}'

    # creando el archivo

    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\resumen_recibos\\resumen' + periodos_juntos + '.html', 'w', encoding='utf-8')

    salario_de_produccion = 0 #salario_de_produccion del mes, la suma de ambas quincenas de todos los trabajadores de produccion
    for id_trabajador in list_trab_activos_mes_produccion:
        #salario
        sumando_1q = leew.consulta_gen('worker.db','SALARIO_QUINCENA','nomina','ID_TRABAJADOR',
                                   f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        salario_de_produccion = salario_de_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'SALARIO_QUINCENA', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        salario_de_produccion = salario_de_produccion + sumando_2q
    #print(salario_de_produccion)

    comisiones_de_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        sumando_mes = leew.consulta_gen_sum('worker.db', 'COMISIONES', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if sumando_mes == None:
            sumando_mes = 0
        comisiones_de_produccion = sumando_mes + comisiones_de_produccion

    comisiones_de_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        sumando_mes = leew.consulta_gen_sum('worker.db', 'COMISIONES', 'nomina', 'ID_TRABAJADOR',
                                            f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if sumando_mes == None:
            sumando_mes = 0
        comisiones_de_administracion = sumando_mes + comisiones_de_administracion

    salario_de_administracion = 0  # salario_de_produccion del mes, la suma de ambas quincenas de todos los trabajadores de produccion
    for id_trabajador in list_trab_activos_mes_administrativo:
        # salario
        sumando_1q = leew.consulta_gen('worker.db','SALARIO_QUINCENA','nomina','ID_TRABAJADOR',
                                   f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        salario_de_administracion = salario_de_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'SALARIO_QUINCENA', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        salario_de_administracion = salario_de_administracion + sumando_2q
    #print(salario_de_administracion)

    otras_remuneraciones_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        #otras remuneraciones
        sumando_1q = leew.consulta_gen('worker.db','OTRAS_REMUN','nomina','ID_TRABAJADOR',
                                   f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        otras_remuneraciones_produccion = otras_remuneraciones_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        otras_remuneraciones_produccion = otras_remuneraciones_produccion + sumando_2q
    print(otras_remuneraciones_produccion)

    otras_remuneraciones_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # otras remuneraciones
        sumando_1q = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        otras_remuneraciones_administracion = otras_remuneraciones_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        otras_remuneraciones_administracion = otras_remuneraciones_administracion + sumando_2q
    print(otras_remuneraciones_administracion)

    fraccion_vacaciones_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        fraccion_vacaciones_produccion = fraccion_vacaciones_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        fraccion_vacaciones_produccion = fraccion_vacaciones_produccion + sumando_2q
    print(fraccion_vacaciones_produccion)

    fraccion_vacaciones_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        fraccion_vacaciones_administracion = fraccion_vacaciones_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        fraccion_vacaciones_administracion = fraccion_vacaciones_administracion + sumando_2q
    print(fraccion_vacaciones_administracion)

    pago_adicional_vacaciones_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        pago_adicional_vacaciones_produccion = pago_adicional_vacaciones_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        pago_adicional_vacaciones_produccion = pago_adicional_vacaciones_produccion + sumando_2q
    print(pago_adicional_vacaciones_produccion)

    pago_adicional_vacaciones_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        pago_adicional_vacaciones_administracion = pago_adicional_vacaciones_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        pago_adicional_vacaciones_administracion = pago_adicional_vacaciones_administracion + sumando_2q
    print(pago_adicional_vacaciones_administracion)

    horas_extra_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        horas_extra_produccion = horas_extra_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        horas_extra_produccion = horas_extra_produccion + sumando_2q
    #print(horas_extra_produccion)

    horas_extra_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        horas_extra_administracion = horas_extra_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        horas_extra_administracion = horas_extra_administracion + sumando_2q
    print(horas_extra_administracion)

    salario_de_navidad_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        salario_de_navidad_produccion = salario_de_navidad_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        salario_de_navidad_produccion = salario_de_navidad_produccion + sumando_2q
    print(salario_de_navidad_produccion)

    salario_de_navidad_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        salario_de_navidad_administracion = salario_de_navidad_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        salario_de_navidad_administracion = salario_de_navidad_administracion + sumando_2q
    print(salario_de_navidad_administracion)

    indemnizaciones_de_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        sumando_mes = leew.consulta_gen_sum('worker.db', 'INDEMNIZACIONES', 'nomina', 'ID_TRABAJADOR',
                                            f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if sumando_mes == None:
            sumando_mes = 0
        indemnizaciones_de_produccion = sumando_mes + indemnizaciones_de_produccion

    indemnizaciones_de_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        sumando_mes = leew.consulta_gen_sum('worker.db', 'INDEMNIZACIONES', 'nomina', 'ID_TRABAJADOR',
                                            f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if sumando_mes == None:
            sumando_mes = 0
        indemnizaciones_de_administracion = sumando_mes + indemnizaciones_de_administracion

    part_beneficios_de_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        sumando_mes = leew.consulta_gen_sum('worker.db', 'INDEMNIZACIONES', 'nomina', 'idt',
                                            f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        part_beneficios_de_produccion = sumando_mes + part_beneficios_de_produccion

    part_beneficios_de_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        sumando_mes = leew.consulta_gen_sum('worker.db', 'monto_ajustado', 'nomina_beneficios', 'idt',
                                            f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if sumando_mes == None:
            sumando_mes = 0
        part_beneficios_de_administracion = sumando_mes + part_beneficios_de_administracion


    total_pagos_produccion = salario_de_produccion + comisiones_de_produccion + otras_remuneraciones_produccion +fraccion_vacaciones_produccion +\
                            pago_adicional_vacaciones_produccion + \
                             horas_extra_produccion + salario_de_navidad_produccion + indemnizaciones_de_produccion + part_beneficios_de_produccion

    total_pagos_administracion = salario_de_administracion + comisiones_de_administracion + otras_remuneraciones_administracion +fraccion_vacaciones_administracion +\
                            pago_adicional_vacaciones_administracion + \
                             horas_extra_administracion + salario_de_navidad_administracion + indemnizaciones_de_administracion + part_beneficios_de_administracion

    afp_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        afp_produccion = afp_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        afp_produccion = afp_produccion + sumando_2q
    #print(afp_produccion)

    afp_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        afp_administracion = afp_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        afp_administracion = afp_administracion + sumando_2q
    #print(afp_administracion)

    sfs_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        sfs_produccion = sfs_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        sfs_produccion = sfs_produccion + sumando_2q
    #print(sfs_produccion)

    sfs_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        sfs_administracion = sfs_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        sfs_administracion = sfs_administracion + sumando_2q
    #print(sfs_administracion)

    retencion_islr_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        retencion_islr_produccion = retencion_islr_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        retencion_islr_produccion = retencion_islr_produccion + sumando_2q
    #print(retencion_islr_produccion)

    retencion_islr_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        retencion_islr_administracion = retencion_islr_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        retencion_islr_administracion = retencion_islr_administracion + sumando_2q
    #print(retencion_islr_administracion)

    inasistencias_produccion = 0
    for id_trabajador in list_trab_activos_mes_produccion:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        inasistencias_produccion = inasistencias_produccion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        inasistencias_produccion = inasistencias_produccion + sumando_2q
    #print(inasistencias_produccion)

    inasistencias_administracion = 0
    for id_trabajador in list_trab_activos_mes_administrativo:
        # Fraccion de vacaciones, es la fraccion del salario que es vacacion
        sumando_1q = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sumando_1q == None:
            sumando_1q = 0

        inasistencias_administracion = inasistencias_administracion + sumando_1q
        sumando_2q = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sumando_2q == None:
            sumando_2q = 0
        inasistencias_administracion = inasistencias_administracion + sumando_2q
    #print(inasistencias_administracion)


    otros_descuentos_produccion = 0
    otros_descuentos_administracion = 0

    total_descuentos_produccion = afp_produccion + sfs_produccion + retencion_islr_produccion + \
                                inasistencias_produccion + otros_descuentos_produccion

    total_descuentos_administracion = afp_administracion + sfs_administracion + retencion_islr_administracion + \
                                  inasistencias_administracion + otros_descuentos_administracion

    total_a_pagar_total = total_pagos_produccion + total_pagos_administracion -\
                          total_descuentos_produccion - total_descuentos_administracion


        # ----------------------------------------------------------------------------------------#
    mensaje = f'''
<html>
<head><title>RESUMEN DE RECIBOS DE LOS PERIODOS {periodos_juntos}, EMITIDO EN { datetime.date.today().strftime('%m/%d/%Y, %H:%M:%S') }  </title>
</head>
	<body>

		<!--un comentaario-->
		<hr />
		<p>FECHA: {datetime.date.today().strftime('%d/%m/%Y')}</p>
		<p>RESUMEN DE TRABAJADORES NÓMINA DE PRODUCCIÓN</p>
		<hr />
		<table>
			<tr>
			    <td>
				  <P><INS>DETALLE DE PAGO<INS></P>

				</td>
			   <td>
					<P><INS>DETALLE DE DESCUENTOS<INS>
			   </td>
		   </tr>
		   <tr>
			   <td>
				   <table>
					   <tr>
						   <td><p>1.- SALARIO</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(salario_de_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- COMISIÓN</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(comisiones_de_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- OTRAS REMUNERACIONES</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(otras_remuneraciones_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- VACACIONES art 177 1ero</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(fraccion_vacaciones_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>5.- VACACIONES art 177 2do</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(pago_adicional_vacaciones_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>6.- HORAS EXTRAS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(horas_extra_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>7.- SALARIO DE NAVIDAD</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(salario_de_navidad_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>8.- INDEMNIZACIONES LABORALES</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(indemnizaciones_de_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>9.- PARTICIPACIÓN EN LOS BENEFICIOS</p>
						   </td>
						   <td><p align="right"><ins>''' + str("{:,.2f}".format(part_beneficios_de_produccion)) + '''</ins></P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL PAGOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_pagos_produccion)) + '''</b></P>
						   </td>
					   </tr>
				   </table>
				</td>
				<td>
				<table>
					   <tr>
						   <td><p>1.- AFP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(afp_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- SFS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(sfs_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- RETENCION ISLR</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(retencion_islr_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- INASISTENCIAS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(inasistencias_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>5.- INFOTEP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(inasistencias_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>6.- APORTE VOLUNTARIO AFP</p>
						   </td>
						   <td><p align="right"><ins>''' + str("{:,.2f}".format(otros_descuentos_produccion)) + '''</ins></P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL DESCUENTOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_descuentos_produccion)) + '''</b></P>
						   </td>
					   </tr>
				</td>
		   </tr>
		</table>
		</table>
	<hr/>
	<p>RESUMEN DE TRABAJADORES NÓMINA DE ADMINISTRACION Y VENTAS</p>
		<hr />
		<table>
			<tr>
			    <td>
				  <P><INS>DETALLE DE PAGO<INS></P>

				</td>
			   <td>
					<P><INS>DETALLE DE DESCUENTOS<INS>
			   </td>
		   </tr>
		   <tr>
			   <td>
				   <table>
					   <tr>
						   <td><p>1.- SALARIO</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(salario_de_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- COMISIÓN</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(comisiones_de_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- OTRAS REMUNERACIONES</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(otras_remuneraciones_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- VACACIONES art 177 1ero</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(fraccion_vacaciones_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>5.- VACACIONES art 177 2do</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(pago_adicional_vacaciones_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>6.- HORAS EXTRAS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(horas_extra_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>7.- SALARIO DE NAVIDAD</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(salario_de_navidad_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>8.- INDEMNIZACIONES LABORALES</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(indemnizaciones_de_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>9.- PARTICIPACIÓN EN LOS BENEFICIOS</p>
						   </td>
						   <td><p align="right"><ins>''' + str("{:,.2f}".format(part_beneficios_de_administracion)) + '''</ins></P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL PAGOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_pagos_administracion)) + '''</b></P>
						   </td>
					   </tr>
				   </table>
				</td>
				<td>
				<table>
					   <tr>
						   <td><p>1.- AFP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(afp_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- SFS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(sfs_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- RETENCION ISLR</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(retencion_islr_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- INASISTENCIAS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(inasistencias_administracion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>5.- INFOTEP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(inasistencias_produccion)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>6.- APORTE VOLUNTARIO AFP</p>
						   </td>
						   <td><p align="right"><ins>''' + str("{:,.2f}".format(otros_descuentos_administracion)) + '''</ins></P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL DESCUENTOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_descuentos_administracion)) + '''</b></P>
						   </td>
					   </tr>
				</td>
		   </tr>
		</table>
		</table>
		<hr/>
		<p><b>Total a pagar a la vista DOP ''' + str("{:,.2f}".format(total_a_pagar_total)) + '''</b></p>
	<body>

</html>
    '''

    f.write(mensaje)
    f.close()
    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\resumen_recibos\\resumen' + periodos_juntos + '.html')
