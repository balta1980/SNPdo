import leew, numpy, webbrowser, os
def imprime(periodo, nota):
    # esta funcion solo recibe segundos periodos
    # con esta función se imprime detalle de pago tss, isr e infotep
    perido_actual = periodo
    MMAAAA = periodo[2:8]
    #print(MMAAAA)

    # periodo anterior
    indice_per_actual = leew.consulta_gen('worker.db', 'indice', 'periodo', 'idp', '"' + perido_actual + '"')
    indice_per_anterior = int(
        indice_per_actual) - 1  # usado para descontar el pago adelantado de vac de un periodo anterior

    idp_per_anterior = leew.consulta_gen('worker.db', 'idp', 'periodo', 'indice',
                                              str(indice_per_anterior))

    if indice_per_anterior > 0:
        trabajadores_nom_prim_quincena = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','periodo',f'"{idp_per_anterior}"')
    else:
        trabajadores_nom_prim_quincena = []

    trabajadores_nom_seg_quincena = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','periodo',f'"{perido_actual}"')

    list_trab_activos_mes = list(set(trabajadores_nom_prim_quincena + trabajadores_nom_seg_quincena)) # uso set para borrar elementos repetidos
    list_trab_activos_mes = numpy.sort(list_trab_activos_mes) # forma fácil de ordenar la lista
    #print(list_trab_activos_mes)

    periodos_juntos = f'{idp_per_anterior}_{perido_actual}'

    # creando el archivo

    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\informe_tss/informe' + periodos_juntos + '.html', 'w',encoding='utf-8')

    total_lineas_tabla_tss = ''
    total_linea_tabla_tss_detalle = ''
    total_a_pagar_tss = 0
    total_linea_tabla_detalle_tss_isr = ''
    total_a_pagar_isr = 0
    total_linea_tabla_infotep = ''
    total_a_pagar_infotep = 0

    for id_trabajador in list_trab_activos_mes:
        nombre_trab = leew.consulta_gen('worker.db', 'Nombre','info','id',str(id_trabajador))
        apellido_trab = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', str(id_trabajador))
        nom_completo = f'{nombre_trab} {apellido_trab}'
        cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', str(id_trabajador))

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
        #print(sal_ss_1q, sal_ss_2q, sal_ss_mes)

        # salario ISR
        sal_isr_1q = leew.consulta_gen('worker.db','SALARIO_ISR','nomina','ID_TRABAJADOR',
                                   f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_isr_1q == None:
            sal_isr_1q = 0
        sal_isr_2q = leew.consulta_gen('worker.db', 'SALARIO_ISR', 'nomina', 'ID_TRABAJADOR',
                                           f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_isr_2q == None:
            sal_isr_2q = 0
        sal_isr_mes = sal_isr_1q + sal_isr_2q
        #print(sal_isr_1q, sal_isr_2q, sal_isr_mes)

        # salario INFOTEP

        sal_infotep_1q = leew.consulta_gen('worker.db', 'INFOTEP_BASE', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_infotep_1q == None:
            sal_infotep_1q = 0
        sal_infotep_2q = leew.consulta_gen('worker.db', 'INFOTEP_BASE', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_infotep_2q == None:
            sal_infotep_2q = 0
        sal_infotep_mes = sal_infotep_1q + sal_infotep_2q + vacaciones_liquidacion
        #print(sal_infotep_1q, sal_infotep_2q, sal_infotep_mes)

        # otras remuneraciones
        sal_or_mes = leew.consulta_gen_sum('worker.db', 'OTRAS_REMUN_TODAS', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if not sal_or_mes:
            sal_or_mes = 0
        sal_or_mes = sal_or_mes + vacaciones_liquidacion

        # ingresos excentos

        monto_preaviso = leew.consulta_gen('worker.db', 'monto_pre_aviso', 'liquidacion', 'id_trab', str(id_trabajador))
        if monto_preaviso == None:
            monto_preaviso = 0
        cesantia_monto = leew.consulta_gen('worker.db', 'cesantia_monto', 'liquidacion', 'id_trab', str(id_trabajador))
        if cesantia_monto == None:
            cesantia_monto = 0
        sal_navidad_monto = leew.consulta_gen('worker.db', 'sal_nav_monto', 'liquidacion', 'id_trab', str(id_trabajador))
        if sal_navidad_monto == None:
            sal_navidad_monto = 0
        monto_adicional = leew.consulta_gen('worker.db', 'bono_monto', 'liquidacion', 'id_trab', str(id_trabajador))
        if monto_adicional == None:
            monto_adicional = 0
        de_la_liquidacion = monto_preaviso + cesantia_monto + sal_navidad_monto + monto_adicional

        sal_ie_1q = leew.consulta_gen('worker.db', 'ING_EXCENTOS_ISR', 'nomina', 'ID_TRABAJADOR',
                                      f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if sal_ie_1q == None:
            sal_ie_1q = 0
        sal_ie_2q = leew.consulta_gen('worker.db', 'ING_EXCENTOS_ISR', 'nomina', 'ID_TRABAJADOR',
                                      f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if sal_ie_2q == None:
            sal_ie_2q = 0
        sal_ie_mes = sal_ie_1q + sal_ie_2q + de_la_liquidacion
        #print(sal_ie_1q, sal_ie_2q, sal_ie_mes)

        # Remuneraciones Otros Agentes
        roa = leew.consulta_gen_sum('worker.db', 'REM_OTROS_EMPLEADORES', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')

        # solo utiliza el RNC y el saldo a favor registrado de la segunda quincena o en su defecto si el trabajador
        # solo trabajo la primera quincena
        if id_trabajador in trabajadores_nom_seg_quincena:
            # RNC. Agente Unico de Retención.
            rnc = leew.consulta_gen('worker.db', 'RNC_AGENTE_RET', 'nomina', 'ID_TRABAJADOR',
                                          f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
            # Saldo a favor
            saldo_a_favor = leew.consulta_gen('worker.db', 'SALDO_A_FAVOR', 'nomina', 'ID_TRABAJADOR',
                                          f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        else: # no trabajó durante la segunda quincena del mes pero sí en la primera
            # RNC. Agente Unico de Retención.
            rnc = leew.consulta_gen('worker.db', 'RNC_AGENTE_RET', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
            # Saldo a favor
            saldo_a_favor = leew.consulta_gen('worker.db', 'SALDO_A_FAVOR', 'nomina', 'ID_TRABAJADOR',
                                              f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        # aportes voluntarios AFP
        aporte_empresa = leew.consulta_gen_sum('worker.db', 'APORTE_VOL_EMP', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        aporte_trab = leew.consulta_gen_sum('worker.db', 'APORTE_VOL_TRAB', 'nomina', 'ID_TRABAJADOR',
                                       f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        aporte_ord_vol_mes = aporte_empresa + aporte_trab

        linea_tabla_tss = f'''<tr>
       <td>{periodos_juntos}</td>
       <td> {str(id_trabajador)} </td>
      <td> {nom_completo} </td>
      <td> {cedula} </td>
      <td>{"{:,.2f}".format(sal_ss_mes)}</td>
      <td>{"{:,.2f}".format(sal_isr_mes)}</td>
      <td>{"{:,.2f}".format(sal_infotep_mes)}</td>
      <td>{"{:,.2f}".format(sal_or_mes)}</td>
      <td>{"{:,.2f}".format(sal_ie_mes)}</td>
      <td>{"{:,.2f}".format(roa)}</td>
      <td>{rnc}</td>
      <td>{"{:,.2f}".format(saldo_a_favor)}</td>
      <td>{"{:,.2f}".format(aporte_ord_vol_mes)}</td>
      </tr>'''
        total_lineas_tabla_tss = total_lineas_tabla_tss + linea_tabla_tss

        # ----------------------------------------------------------------------------------------------------------#

        nss = leew.consulta_gen('worker.db', 'num_seguro', 'info', 'id', str(id_trabajador))

        # sfs retencion (trabajador)
        rsfs_1q = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_TRABAJADOR',
                                      f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if rsfs_1q == None:
            rsfs_1q = 0
        rsfs_2q = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_TRABAJADOR',
                                      f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if rsfs_2q == None:
            rsfs_2q = 0

        rsfs_en_liq = leew.consulta_gen('worker.db', 'sfs_trab', 'liquidacion', 'id_trab', str(id_trabajador))
        if rsfs_en_liq == None:
            rsfs_en_liq = 0

        rsfs_mes = rsfs_1q + rsfs_2q + rsfs_en_liq
        #print(rsfs_1q, rsfs_2q, rsfs_mes)

        # sfs contribucion (empresa)
        csfs_1q = leew.consulta_gen('worker.db', 'SFS_EMP', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if csfs_1q == None:
            csfs_1q = 0
        csfs_2q = leew.consulta_gen('worker.db', 'SFS_EMP', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if csfs_2q == None:
            csfs_2q = 0
        csfs_en_liq = leew.consulta_gen('worker.db', 'sfs_emp', 'liquidacion', 'id_trab', str(id_trabajador))
        if csfs_en_liq == None:
            csfs_en_liq = 0

        csfs_mes = csfs_1q + csfs_2q + csfs_en_liq

        # afp retencion (trabajador)
        rafp_1q = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if rafp_1q == None:
            rafp_1q = 0
        rafp_2q = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if rafp_2q == None:
            rafp_2q = 0

        rafp_en_liq = leew.consulta_gen('worker.db', 'afp_trab', 'liquidacion', 'id_trab', str(id_trabajador))
        if rafp_en_liq == None:
            rafp_en_liq = 0

        rafp_mes = rafp_1q + rafp_2q + rafp_en_liq

        # afp contribucion (empresa)
        cafp_1q = leew.consulta_gen('worker.db', 'AFP_EMP', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if cafp_1q == None:
            cafp_1q = 0
        cafp_2q = leew.consulta_gen('worker.db', 'AFP_EMP', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if cafp_2q == None:
            cafp_2q = 0

        cafp_en_liq = leew.consulta_gen('worker.db', 'afp_emp', 'liquidacion', 'id_trab', str(id_trabajador))
        if cafp_en_liq == None:
            cafp_en_liq = 0
        cafp_mes = cafp_1q + cafp_2q + cafp_en_liq

        # SRL contribucion (empresa)
        srl_1q = leew.consulta_gen('worker.db', 'SRL', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if srl_1q == None:
            srl_1q = 0
        srl_2q = leew.consulta_gen('worker.db', 'SRL', 'nomina', 'ID_TRABAJADOR',
                                    f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if srl_2q == None:
            srl_2q = 0

        srl_en_liq = leew.consulta_gen('worker.db', 'srl_emp', 'liquidacion', 'id_trab', str(id_trabajador))
        if srl_en_liq == None:
            srl_en_liq = 0
        srl_mes = srl_1q + srl_2q + srl_en_liq

        total_tss = rsfs_mes + csfs_mes + rafp_mes + cafp_mes + srl_mes + aporte_ord_vol_mes


        linea_tabla_tss_detalle =f'''<tr>
       <td>{cedula}</td>
       <td> {nss} </td>
      <td> {nom_completo} </td>
      <td> {"{:,.2f}".format(sal_ss_mes)} </td>
      <td>{"{:,.2f}".format(sal_ss_mes)}</td>
       <td>{"{:,.2f}".format(rsfs_mes)}</td>
       <td>{"{:,.2f}".format(csfs_mes)}</td>
       <td>{"{:,.2f}".format(rafp_mes)}</td>
       <td>{"{:,.2f}".format(cafp_mes)}</td>
       <td>{"{:,.2f}".format(srl_mes)}</td>
       <td>{"{:,.2f}".format(aporte_ord_vol_mes)}</td> <!--aporte voluntario -->
       <td>0.00</td> <!--percapita adicional -->
       <td>0.00</td> <!--intereses y recargos -->
       <td>0.00</td> <!--creditos -->
       <td>{"{:,.2f}".format(total_tss)}</td>

   </tr>'''
        total_linea_tabla_tss_detalle = total_linea_tabla_tss_detalle + linea_tabla_tss_detalle
        total_a_pagar_tss = total_a_pagar_tss + total_tss
        #----------------------------------------------------------------------------------------#

        # total paga TP
        tp = sal_isr_mes + sal_or_mes + sal_ie_mes + roa

        # retencion seguridad social RSS

        rss = rsfs_mes + rafp_mes

        # total sujeto a retencion

        tsr = tp - rss - sal_ie_mes

        # retencio ISR
        ret_isr_nomina = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'ID_TRABAJADOR',
                                  f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if ret_isr_nomina is None:
            ret_isr_nomina = 0

        ret_isr_egreso = leew.consulta_gen('worker.db', 'islr_ret', 'liquidacion', 'id_trab',
                                  f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if ret_isr_egreso is None:
            ret_isr_egreso = 0

        ret_isr_bonificacion = leew.consulta_gen('worker.db', 'ret_islr', 'nomina_beneficios', 'idt',
                                  f'"{str(id_trabajador)}" and MMAAAA = "{MMAAAA}"')
        if ret_isr_bonificacion is None:
            ret_isr_bonificacion = 0

        total_ret_isr = ret_isr_nomina + ret_isr_egreso + ret_isr_bonificacion


        linea_tabla_detalle_tss_isr =f'''<tr>
       <td>{cedula}</td>
       <td>{nom_completo}</td>
      <td> {"{:,.2f}".format(sal_isr_mes)} </td>
      <td> {"{:,.2f}".format(sal_or_mes)} </td>
      <td>{"{:,.2f}".format(sal_ie_mes)}</td>
       <td>{"{:,.2f}".format(roa)}</td><!--R.O.A. -->
       <td>{"{:,.2f}".format(tp)}</td>
       <td>{"{:,.2f}".format(rss)}</td>
       <td>{"{:,.2f}".format(tsr)}</td>
       <td>0.00</td> <!--SFP -->
        <td>{"{:,.2f}".format(total_ret_isr)}</td>
   </tr>'''

        total_linea_tabla_detalle_tss_isr = total_linea_tabla_detalle_tss_isr + linea_tabla_detalle_tss_isr
        total_a_pagar_isr = total_a_pagar_isr + total_ret_isr
        # ----------------------------------------------------------------------------------------#

        # Pago por infotep

        pago_info_1q = leew.consulta_gen('worker.db', 'INFOTEP', 'nomina', 'ID_TRABAJADOR',
                                  f'"{str(id_trabajador)}" and PERIODO = "{idp_per_anterior}"')
        if pago_info_1q is None:
            pago_info_1q = 0

        pago_info_2q = leew.consulta_gen('worker.db', 'INFOTEP', 'nomina', 'ID_TRABAJADOR',
                                         f'"{str(id_trabajador)}" and PERIODO = "{perido_actual}"')
        if pago_info_2q is None:
            pago_info_2q = 0
        pago_info_en_liq = leew.consulta_gen('worker.db', 'infotep_emp', 'liquidacion', 'id_trab', str(id_trabajador))
        if pago_info_en_liq == None:
            pago_info_en_liq = 0

        pago_info_mes = pago_info_1q + pago_info_2q + pago_info_en_liq

        linea_tabla_infotep = f'''<tr>
       <td>{cedula}</td>
       <td>{nss} </td>
      <td> {nom_completo}</td>
      <td> {"{:,.2f}".format(sal_infotep_mes)}</td>
      <td>{"{:,.2f}".format(pago_info_mes)}</td>       
   </tr>'''

        total_linea_tabla_infotep = total_linea_tabla_infotep + linea_tabla_infotep
        total_a_pagar_infotep = total_a_pagar_infotep + pago_info_mes

        # ----------------------------------------------------------------------------------------#
    mensaje = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pago Mensual a la TSS del periodo:</title>
</head>
<body>
<p>Tabla de pago de la TSS {periodos_juntos}</p>
<table border="1">
   <tr>
       <td>Periodo</td>
       <td> Id Trab </td>
       <td> Nombre de Trabajador </td>
       <td> Cédula </td>
       <td><b>Sal. SS</b></td>
       <td><b>Sal. ISR</b></td>
       <td><b>Sal. INF</b></td>
       <td><b>O.R.</b></td>
       <td><b>I.E.</b></td>
       <td><b>R.O.A.</b></td>
       <td><b>R.A.U.R.</b></td>
       <td><b>Saldo a favor</b></td>
       <td><b>Aporte Vol. Ordinario</b></td>
   </tr>{total_lineas_tabla_tss}


</table>
<P>Leyenda:<br>
NSS:    Número de Seguridad Social.<br>
Sal.:   S.S. Salario Cotizable para la Seguridad Social.<br>
Sal.:   ISR Salario Cotizable para el ISR.<br>
Sal.:   INF Salario Cotizable para el INFOTEP<br>
O. R:   Otras Remuneraciones que cotizan para ISR.<br>
S.F:    Saldos a Favor del período.<br>
I.E:    Ingresos Exentos del período.<br>
R.O.A:  Remuneraciones Otros Agentes<br>
R.A.U.R.: RNC. Agente Unico de Retención. </P>
<br>
<p>Tabla de pago de la TSS -DETALLE-</p> <!--tabla DETALLE PAGO TSS -->
<table border="1">
   <tr>
       <td>Cédula</td>
       <td> NSS </td>
      <td> Nombre </td>
      <td> Salario </td>
      <td>Salario Reportado</td>
       <td>R.S.F.S</td>
       <td>C.S.F.S</td>
       <td>R.P</td>
       <td>C.P</td>
       <td>S.R.L</td>
       <td>A.V</td>
       <td>P.C.A</td>
       <td>I.R</td>
       <td>C.R</td>
       <td>Total</td>

   </tr>{total_linea_tabla_tss_detalle}

</table>
<p>Leyenda:<br>
R.S.F.S: Retención Seguro Familiar de Salud.<br>
C.S.F.S: Contribución Seguro Familiar de Salud.<br>
R.P: Retención Pensión.<br>
C.P: Contribución Pensión.<br>
S.R.L: Seguro de Riesgo Laboral.<br>
A.V: Aporte Voluntarios.<br>
P.C.A: Per Cápita Adicional.<br>
I.R: Intereses y Recargos.<br>
C.R: Crédito.<br>
</p>
<p>Tabla de pago de la TSS -ISR-</p> <!-- -->
<table border="2">
   <tr>
       <td>Documento</td>
       <td> Nombre </td>
      <td> Salario </td>
      <td> O.I </td>
      <td>I.E.</td>
       <td>R.O.A</td>
       <td>T.P.</td>
       <td>R.S.S</td>
       <td>T.S.R</td>
       <td>S.F.P</td>
        <td>Retencion ISR</td>
   </tr>{total_linea_tabla_detalle_tss_isr}

</table>
<p>Leyenda<br>
O.I.:	Otros Ingresos<br>
I.E.:	Ingresos Exentos<br>
R.O.A.:	Remuneraciones de Otros Agentes<br>
T.P:	Total Pagado<br>
R.S.S:	Retención Seguridad Social<br>
T.S.R:	Total Sujeto a Retención<br>
S.F.P.:	Saldo a Favor del Periodo<br>
</p>

<p>Tabla de pago de la TSS -INFOTEP-</p> <!--todo arreglar tabla segun excel de patty -->
<table border="2">
   <tr>
       <td>Cedula</td>
       <td>NSS </td>
      <td> Nombre </td>
      <td> Salario </td>
      <td>INFOTEP</td>
   </tr>{total_linea_tabla_infotep}
</table>
<p>
RESUMEN: <br>
TOTAL A PAGAR TSS = {"{:,.2f}".format(total_a_pagar_tss)}<br>
TOTAL A PAGAR ISR VIA IR3 = {"{:,.2f}".format(total_a_pagar_isr)}<br>
TOTAL A PAGAR INFOTEP = {"{:,.2f}".format(total_a_pagar_infotep)}<br>

</p>
<br>
<p>Nota:{nota}</p>
</body>
</html>
'''

    f.write(mensaje)
    f.close()
    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\informe_tss/informe' + periodos_juntos + '.html')
