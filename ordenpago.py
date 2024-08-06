import leew
import os
import webbrowser
import datetime


def imprimir(periodo,id_trab=0, tipo_nomina='quincenal', nota=''):

    fecha = datetime.date.today()

    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\ordenes\\orden_' + str(fecha) + '.html', 'w')

    # variables:

    if tipo_nomina == 'quincenal':
        # nota
        nota = leew.consulta_gen('worker.db','NOTA','nomina','PERIODO', '"' + periodo + '"')
        # dia inicio perido
        dia_inicio = leew.consulta_gen('worker.db', 'f_inicio', 'periodo', 'idp', '"' + periodo + '"')

        # dia fin periodo
        dia_fin = leew.consulta_gen('worker.db', 'f_fin', 'periodo', 'idp', '"' + periodo + '"')

    if tipo_nomina == 'beneficios':
        # nota
        nota = leew.consulta_gen('worker.db','nota','nomina_beneficios','idp_fiscal', '"' + periodo + '"')
        # dia inicio perido
        dia_inicio = leew.consulta_gen('worker.db', 'fecha_i', 'periodo_fiscal', 'idp', '"' + periodo + '"')

        # dia fin periodo
        dia_fin = leew.consulta_gen('worker.db', 'fecha_f', 'periodo_fiscal', 'idp', '"' + periodo + '"')

    if tipo_nomina == 'egreso':
        # nota
        nota = leew.consulta_gen('worker.db', 'nota', 'liquidacion', 'periodo_salida', f'"{periodo}" AND id_trab = "{id_trab}"')
        dia_inicio = "N/A"
        dia_fin = "N/A"

    listado_trab = []
    if id_trab == 0: # esto lo hago para poder imprimir una orden especifica por trabajador
        if tipo_nomina == 'quincenal':
            listado_trab = leew.consulta_lista('worker.db','ID_TRABAJADOR','nomina','PERIODO','"' + periodo + '"')
        if tipo_nomina == 'beneficios':
            listado_trab = leew.consulta_lista('worker.db', 'idt', 'nomina_beneficios', 'idp_fiscal', '"' + periodo + '"')


    else:
        listado_trab.append(id_trab)
    # print("listado trab", listado_trab)
    mensaje_lineas = ''
    total = 0
    monto = 0
    for trab in listado_trab:
        nombre = leew.consulta_gen('worker.db','Nombre','info','id',str(trab))
        apellido = leew.consulta_gen('worker.db','Apellido','info','id',str(trab))
        nomb_completo = nombre + ' ' + apellido
        cedula = str(leew.consulta_gen('worker.db','Identificacion','info','id',str(trab)))
        banco = leew.consulta_gen('worker.db','Banco','info','id',str(trab))
        num_cuenta = str(leew.consulta_gen('worker.db','num_c','info','id',str(trab)))
        if tipo_nomina == 'quincenal':
            monto = leew.consulta_gen('worker.db','TOTAL_DEPOSITAR','nomina','ID_TRABAJADOR', str(trab) + ' AND PERIODO=' + '"' + periodo + '"')
        if tipo_nomina == 'beneficios':
            monto = leew.consulta_gen('worker.db','monto_ajustado','nomina_beneficios','idt', str(trab) + ' AND idp_fiscal=' + '"' + periodo + '"')
            monto = monto.replace('RD$', '')
            monto = monto.replace(',', '')
            monto = float(monto)
        if tipo_nomina == 'egreso':
            monto = leew.consulta_gen('worker.db', 'total_liq', 'liquidacion', 'periodo_salida',
                                       f'"{periodo}" AND id_trab = "{trab}"')
            tipo_nomina = 'NOMINA DE FINALIZACIÓN DE CONTRATO'
            # cambio el periodo por el id de la liquidacion
            periodo = str(leew.consulta_gen('worker.db', 'id_liq', 'liquidacion', 'periodo_salida',
                                       f'"{periodo}" AND id_trab = "{trab}"'))

        total = total + monto
        mensaje_lineas = mensaje_lineas + \
            ''' 
            <tr>
        <td><p>''' + str(trab) + '''</p></td><td><p>''' + nomb_completo + '''</p></td><td><p>''' + cedula + '''</p></td><td><p>''' + banco + '''</p></td><td><p>''' + num_cuenta + '''</p></td><td><p align="right">''' + "{:,.2f}".format(monto) + '''</p></td>
    </tr>
            '''
    linea_tabla_total = ''' 
            <tr>
        <td colspan="5"><p align="right">TOTAL NÓMINA</p></td><td><p align="right">''' + "{:,.2f}".format(total) + '''</p></td>
    </tr>
            '''
    mensaje = '''
    <html>
<head>
<p><b>ORDEN DE TRANSFERENCIAS POR CONCEPTO DE NOMINA ''' + tipo_nomina.upper() + ''' </b></p>
<p>NOMINA CORRESPONDIENTE AL PERIODO DEL '''+ dia_inicio + ''' AL ''' + dia_fin +'''</p>
<p>FECHA: ''' + str(fecha) + ''', CODIGO NOMINA: ''' +periodo +'''</p>
</head>
<body>
<table border="1">
    <tr>
        <td><p><b>ID</b></p></td><td><p><b>NOMBRE</b></p></td><td><p><b>CEDULA</b></p></td><td><p><b>BANCO</b></p></td><td><p><b>NUMERO DE CUENTA</b></p></td><td><p><b>MONTO (DOP)</b></p></td>
    </tr>
    ''' + mensaje_lineas + linea_tabla_total +'''
</table>

<hr/>
<p>NOTA: ''' + nota + '''</p>
<hr/>
</body>
</html>
        '''

    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\ordenes\\orden_' + str(fecha) + '.html')
