import webbrowser, leew, os

def imprimir(RECIBO_NUMERO,TIPO_NOMINA,i,PERIODO, DIA_INICIO_PER, DIA_FIN_PER ,SALARIO, SALARIO_DIARIO,SALARIO_QUINCENA_NETO, COMISION,PAGO_AD_PER_ANT,PAGO_ADELANTADO,PAGO_DE_VAC,
             DIAS_DE_VAC_DISFRUTADOS, FRACCION_VAC,FECHA_INICIO_VAC,FECHA_FIN_VAC,AFP_TRAB,AFP_VOLUNTARIO,SFS_TRAB,ISLR_RETENCION,HORAS_EXTRA,
                DESC_HE,INASIS,DESC_INA, INFOTEP_TRAB,OTRAS_REMUN,DESC_OTRAS_REMUN,SALARIO_DE_NAVIDAD, INDEMNIZACION,BENEFICIOS,MONTO_A_PAGAR,FECHA,
             PRESTAMOS, CUOTAS, TOTAL_DEPOSITAR, FECHA_I_PAGO, FECHA_F_PAGO):
    #OBTENER VALORES
    # nombre de la sociedad
    NOMBRE_SOCIEDAD = leew.consulta_gen('worker.db','nombre_sociedad','info_sociedad','estatus','"Vigente"')
    if NOMBRE_SOCIEDAD == None:
        NOMBRE_SOCIEDAD = ''

    # RNC
    RNC = leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'estatus', '"Vigente"')
    if RNC == None:
        RNC = ''

    # LOGO RUTA
    LOGO_RUTA = leew.consulta_gen('worker.db', 'ruta_logo', 'info_sociedad', 'estatus', '"Vigente"')
    if LOGO_RUTA == None:#esto captura un Null de la base de datos
        LOGO_RUTA = ''
    else:
        LOGO_RUTA = LOGO_RUTA.replace('impresiones/', '')

    #print(LOGO_RUTA)

    # nombre trab
    nombre_trab = leew.consulta_gen('worker.db','Nombre','info','id',str(i))
    nombre_trab = nombre_trab + ' ' + leew.consulta_gen('worker.db','Apellido','info','id',str(i))

    # cedula
    cedula = leew.consulta_gen('worker.db','Identificacion', 'info', 'id',str(i))


    # total pagos
    total_pagos = SALARIO_QUINCENA_NETO + FRACCION_VAC + PAGO_DE_VAC + HORAS_EXTRA +\
                  SALARIO_DE_NAVIDAD + OTRAS_REMUN + BENEFICIOS + INDEMNIZACION + COMISION

    # total descuentos
    total_descuentos = AFP_TRAB + SFS_TRAB + ISLR_RETENCION + INASIS + INFOTEP_TRAB + AFP_VOLUNTARIO

    if len(DESC_INA) > 0:
        DESC_INA2 = ''
        for n in DESC_INA:
            DESC_INA2 = DESC_INA2 + '<br>' + n
    else:
        DESC_INA2 = 'No aplica'

    if len(DESC_HE) > 0:
        DESC_HE2 = ''
        for n in DESC_HE:
            DESC_HE2 = DESC_HE2 + '<br>' + n
    else:
        DESC_HE2 = 'No aplica'

    if len(DESC_OTRAS_REMUN) > 0:
        DESC_OTRAS_REMUN2 = ''
        for n in DESC_OTRAS_REMUN:
            DESC_OTRAS_REMUN2 = DESC_OTRAS_REMUN2 + '<br>' + n
    else:
        DESC_OTRAS_REMUN2 = 'No aplica'

    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\nomina' + RECIBO_NUMERO + '.html', 'w',encoding='utf-8')

    mensaje = '''

<html>
<head>
<title>RECIBO ''' + RECIBO_NUMERO +''' </title>
</head>
	<body>
		
		<!--un comentaario-->
		<table>
			<tr>
			<td><img src= "''' + LOGO_RUTA + '''" alt="" height="150" />
			</td>
			<td>
				<p align="center"><b>''' + NOMBRE_SOCIEDAD + '''</b></p>
				<p align="center">RNC: ''' + RNC + '''</p>
				<p align="center">RECIBO DE PAGO DE SALARIO PERIODO: ''' + PERIODO + '''
				<p align="center">NOMINA CORRESPONDIENTE AL PERIODO DEL ''' + DIA_INICIO_PER + ''' AL ''' + DIA_FIN_PER + '''</p>
			</td>
			</tr>
		</table>
		
		<hr />
		<p>FECHA: ''' + FECHA + '''. CON FECHAS EFECTIVAS: DEL: ''' + FECHA_I_PAGO + ''' AL ''' + FECHA_F_PAGO + '''.</p>
		<p>RECIBO N: ''' + RECIBO_NUMERO + '''	TIPO DE NOMINA: ''' + TIPO_NOMINA + '''</p>
		<p>NOMBRE DEL TRABAJADOR: ''' + nombre_trab + '''	/ CEDULA:''' + cedula + '''	/ SALARIO MENSUAL: ''' + str("{:,.2f}".format(SALARIO)) + '''	/ SALARIO DIARIO: ''' + str("{:,.2f}".format(SALARIO_DIARIO)) + '''</p>
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
						   <td><p align="right">''' + str("{:,.2f}".format(SALARIO_QUINCENA_NETO)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- COMISIÓN</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(COMISION)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- OTRAS REMUNERACIONES</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(OTRAS_REMUN)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- VACACIONES art 177 1ero</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(FRACCION_VAC)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>5.- VACACIONES art 177 2do</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(PAGO_DE_VAC)) + '''</P>
						   </td>
					   </tr>
					   
					   <tr>
						   <td><p>6.- HORAS EXTRAS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(HORAS_EXTRA)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>7.- SALARIO DE NAVIDAD</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(SALARIO_DE_NAVIDAD)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>8.- INDEMNIZACIONES LABORALES</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(INDEMNIZACION)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>9.- PARTICIPACIÓN EN LOS BENEFICIOS</p>
						   </td>
						   <td><p align="right"><ins>''' + str("{:,.2f}".format(BENEFICIOS)) + '''</ins></P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL PAGOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_pagos)) + '''</b></P>
						   </td>
					   </tr>
				   </table>
				</td>
				<td>
				<table>
					   <tr>
						   <td><p>1.- AFP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(AFP_TRAB)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- SFS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(SFS_TRAB)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- RETENCION ISLR</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(ISLR_RETENCION)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- INASISTENCIAS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(INASIS)) + '''</P>
						   </td>
					   </tr>
					   
					   <tr>
						   <td><p>5.- INFOTEP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(INFOTEP_TRAB)) +'''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>6.- APORTE VOLUNTARIO AFP</p>
						   </td>
						   <td><p align="right"><ins>''' + str("{:,.2f}".format(AFP_VOLUNTARIO)) +'''</ins></P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL DESCUENTOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_descuentos)) + '''</b></P>
						   </td>
					   </tr>
				</td>
		   </tr>
		</table>
		</table>
	<hr/>
	<p><strong>TOTAL NÓMINA (DOP): ''' + str("{:,.2f}".format(MONTO_A_PAGAR)) + '''</strong></p>
	<p><strong>VARIACION POSITIVA (DOP): ''' + str("{:,.2f}".format(PRESTAMOS)) + '''</strong></p>
	<p><strong>VARIACION NEGATIVA (DOP): ''' + str("{:,.2f}".format(CUOTAS)) + '''</strong></p>
	<p><strong>TOTAL A DEPOSITAR (DOP): ''' + str("{:,.2f}".format(TOTAL_DEPOSITAR)) + '''</strong></p>
	<hr/>
	<hr/>
	<p><strong>DETALLE DE VACACIONES: FECHA DE INICIO: ''' + FECHA_INICIO_VAC + ''', FECHA DE FINALIZACIÓN: ''' + FECHA_FIN_VAC + ''', DIAS DISFRUTADOS: ''' + str(DIAS_DE_VAC_DISFRUTADOS) + '''</strong></p>
	<hr/>
	<ul>
		<li><p><b>DETALLE HORAS EXTRAS: ''' + DESC_HE2 + '''</b></p></li>
		<li><p><b>DETALLE INASISTENCIAS: ''' + DESC_INA2 + '''</b></p></li>
		<li><p><b>DETALLE OTRAS REMUNERACIONES: ''' + DESC_OTRAS_REMUN2 + '''</b></p></li>
	</ul>
	<hr/>
	<p>NOMBRE DEL TRABAJADOR: ______________________</p>
	<p>CEDULA DEL TRABAJADOR: ______________________</p>
	<p></p>
	<p></p>
	<p>FIRMA:_______________________</p>
	<body>
	
</html>
    '''
    #print(mensaje)
    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\nomina' + RECIBO_NUMERO + '.html')


def imprimir_liquidacion(i, PERIODO, FECHA_DE_INGRES0, FECHA_DE_SALIDA, TIEMPO_LABORANDO, SALARIO_PROM_MES, SALARIO_DIARIO,
                         ULTIMO_SALARIO, AFP_TRAB, SFS_TRAB, ISLR_RETENCION,PRESTAMOS_PENDIENTES, PREAVISO,CESANTIA, VACACIONES,
                         SALARIO_NAVIDAD, MONTO_ADICIONAL, MONTO_A_PAGAR):
    # OBTENER VALORES
    # nombre de la sociedad
    NOMBRE_SOCIEDAD = leew.consulta_gen('worker.db', 'nombre_sociedad', 'info_sociedad', 'estatus', '"Vigente"')
    if NOMBRE_SOCIEDAD == None:
        NOMBRE_SOCIEDAD = ''

    # RNC
    RNC = leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'estatus', '"Vigente"')
    if RNC == None:
        RNC = ''

    # LOGO RUTA
    LOGO_RUTA = leew.consulta_gen('worker.db', 'ruta_logo', 'info_sociedad', 'estatus', '"Vigente"')
    if LOGO_RUTA == None:  # esto captura un Null de la base de datos
        LOGO_RUTA = ''
    else:
        LOGO_RUTA = LOGO_RUTA.replace('impresiones/', '')

    # print(LOGO_RUTA)
    # recibo numero
    recibo_numero = str(leew.consulta_gen('worker.db', 'id_liq', 'liquidacion', 'id_trab',
                                          f'"{str(i)}" AND periodo_salida = "{PERIODO}"'))

    # nombre trab
    nombre_trab = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', str(i))
    nombre_trab = nombre_trab + ' ' + leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', str(i))

    # cedula
    cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', str(i))

    # total pagos

    SUBTOTAL_A_RECIBIR = PREAVISO + CESANTIA + VACACIONES + SALARIO_NAVIDAD + MONTO_ADICIONAL

    # total descuentos
    total_descuentos = AFP_TRAB + SFS_TRAB + ISLR_RETENCION + PRESTAMOS_PENDIENTES


    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\nomina_liquidacion' + recibo_numero + '.html', 'w', encoding='utf-8')

    mensaje = '''

<html>
<head>
<title>RECIBO ''' + recibo_numero + ''' </title>
</head>
	<body>

		<!--un comentaario-->
		<table>
			<tr>
			<td><img src= "''' + LOGO_RUTA + '''" alt="" height="150" />
			</td>
			<td>
				<p align="center"><b>''' + NOMBRE_SOCIEDAD + '''</b></p>
				<p align="center">RNC: ''' + RNC + '''</p>
				<p align="center">RECIBO DE PAGO DE PRESTACIONES Y DERECHOS ADQUIRIDOS</p>
			</td>
			</tr>
		</table>

		<hr />
		<p>RECIBO N: ''' + recibo_numero + '''</p>
		<p>NOMBRE DEL TRABAJADOR: ''' + nombre_trab + '''	/ CEDULA:''' + cedula + '''	/ SALARIO PROMEDIO MENSUAL: ''' + str(
        "{:,.2f}".format(SALARIO_PROM_MES)) + '''	/ SALARIO DIARIO: ''' + str("{:,.2f}".format(SALARIO_DIARIO)) +\
    '''	/ ÚLTIMO SALARIO: ''' + str("{:,.2f}".format(ULTIMO_SALARIO)) +  '''</p>
		<p>FECHA DE INGRESO: ''' + FECHA_DE_INGRES0 + '''</P>
		<p>FECHA DE SALIDA: ''' + FECHA_DE_SALIDA + '''</P>
		<p>TIEMPO LABORANDO: ''' + TIEMPO_LABORANDO + '''</P>
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
						   <td><p>1.- SALARIO PREAVISO (ART. 76 C.T.)</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(PREAVISO)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- CESANTÍA (ART. 80 C.T.)</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(CESANTIA)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- SALARIO VACACIONES (ART. 177 C.T.)</p>
						   </td>
						   <td><p  align="right">''' + str("{:,.2f}".format(VACACIONES)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- SALARIO NAVIDAD (ART. 219 C.T.)</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(SALARIO_NAVIDAD)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- MONTO ADICIONAL</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(MONTO_ADICIONAL)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>SUBTOTAL A RECIBIR</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(SUBTOTAL_A_RECIBIR)) + '''</b></P>
						   </td>
					   </tr>
				   </table>
				</td>
				<td>
				<table>
					   <tr>
						   <td><p>1.- AFP</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(AFP_TRAB)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>2.- SFS</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(SFS_TRAB)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>3.- RETENCION ISLR</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(ISLR_RETENCION)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p>4.- ADELANTOS PENDIENTES POR DESCONTAR</p>
						   </td>
						   <td><p align="right">''' + str("{:,.2f}".format(PRESTAMOS_PENDIENTES)) + '''</P>
						   </td>
					   </tr>
					   <tr>
						   <td><p><b>TOTAL DESCUENTOS</b></p>
						   </td>
						   <td><p align="right"><b>''' + str("{:,.2f}".format(total_descuentos)) + '''</b></P>
						   </td>
					   </tr>
				</td>
		   </tr>
		</table>
		</table>
	<hr/>
	<p><strong>TOTAL A RECIBIR (DOP): ''' + str("{:,.2f}".format(MONTO_A_PAGAR)) + '''</strong></p>
	
	
	<hr/>
	<hr/>
	
	<hr/>
	<hr/>
	<p>NOMBRE DEL TRABAJADOR: ______________________</p>
	<p>CEDULA DEL TRABAJADOR: ______________________</p>
	<p></p>
	<p></p>
	<p>FIRMA:_______________________</p>
	<body>

</html>
    '''
    # print(mensaje)
    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\nomina_liquidacion' + recibo_numero + '.html')