import leew, datetime, webbrowser, os, num_a_letra
def imprime(idp):
    # DATOS DE LA SOCIEDAD
    EMPRESA = leew.consulta_gen('worker.db', 'nombre_sociedad', 'info_sociedad', 'estatus', '"Vigente"')
    RNC = leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'estatus', '"Vigente"')
    # DATOS PERSONALES
    id_trabajador = str(leew.consulta_gen('worker.db', 'idt', 'prestamos', 'idp', f'"{idp}"'))
    FECHA = datetime.date.today().strftime("%d-%m-%Y")

    nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', id_trabajador)
    nombre2 = leew.consulta_gen('worker.db', 'nombre2', 'info', 'id', id_trabajador)
    apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', id_trabajador)
    apellido2 = leew.consulta_gen('worker.db', 'apellido2', 'info', 'id', id_trabajador)

    NOMBRE_TRABAJADOR = f'{nombre} {nombre2} {apellido} {apellido2}'

    TIPO_DOC = leew.consulta_gen('worker.db','Tipo_doc','info','id',f'"{id_trabajador}"')
    if TIPO_DOC == "C":
        TIPO_DOC = "cédula"
    if TIPO_DOC == "P":
        TIPO_DOC = "pasaporte"
    if TIPO_DOC == "N":
        TIPO_DOC = "NSS"

    NUMERO_DOC = leew.consulta_gen('worker.db','Identificacion','info','id',f'"{id_trabajador}"')
    NACIONALIDAD = leew.consulta_gen('worker.db','Nacionalidad','info','id',f'"{id_trabajador}"')

    # DATOS DEL CRÉDITO
    MONTO_ADELANTO = leew.consulta_gen('worker.db', 'monto', 'prestamos', 'idp', f'"{idp}"')
    MONTO_LETRAS = num_a_letra.numero_to_letras(MONTO_ADELANTO)
    MONTO_CUOTA = leew.consulta_gen('worker.db', 'monto_cuotas', 'prestamos', 'idp', f'"{idp}"')
    MONTO_CUOTA_EN_LETRAS = num_a_letra.numero_to_letras(MONTO_CUOTA)

    listado_quincenas = leew.consulta_lista('worker.db', 'periodo', 'prestamos_detalles', 'idp', f'"{idp}"')
    primer_quince_pago = listado_quincenas[0]
    QUINCENA_EN_LETRAS = num_a_letra.quincena_to_letras(primer_quince_pago)

    LINEAS_TABLA = ""

    for l in listado_quincenas:
        linea = f"""<tr>
        <td>{num_a_letra.quincena_to_letras(l)}</td>
        <td>{MONTO_CUOTA}</td>
        </tr>"""
        LINEAS_TABLA =LINEAS_TABLA + linea


    # creando el archivo

    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\contrato_adelanto' + NOMBRE_TRABAJADOR + '.html', 'w',encoding='utf-8')
    #f = open('cartas_trabajo/carta.html', 'w')

    mensaje = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Adelanto de salario</title>
</head>
<body>
<p style="text-align:justify;">
    Yo, {NOMBRE_TRABAJADOR}, de nacionalidad {NACIONALIDAD} y de este domicilio portador del documento: {TIPO_DOC}
    número {NUMERO_DOC} hago constar que he recibido de la empresa {EMPRESA} RNC{RNC}, como yo había solicitado,
    un adelanto de salario por un monto igual {MONTO_ADELANTO} DOP ({MONTO_LETRAS}). Por lo tanto, Yo autorizo a
    {EMPRESA} a descontar de mi quincena un monto de {MONTO_CUOTA} DOP ({MONTO_CUOTA_EN_LETRAS}) a partir de la
    {QUINCENA_EN_LETRAS} tal como se muestra en la siguiente tabla:
</p>
<table border="2">
   <tr>
      <td><strong>QUINCENA</strong></td>
      <td><strong>MONTO CUOTA (DOP)</strong></td>
   </tr>
    {LINEAS_TABLA}
</table>
<p style="text-align:justify;">
    También autorizo a que si por cualquier razón termina mi relación de trabajo con la empresa {EMPRESA} antes de
    haberme descontado estas cuotas, la empresa me descuente de mis derechos adquiridos; como vacaciones o salario de
    navidad o de mi derecho de cesantía, si fuera el caso, el balance total restante de este adelanto.<br>
<br>
<P>En Santo Domingo el {FECHA}</P>
    <br>

Fecha:___________________________<br>
Nombre trab:_________________________<br>
Cédula:__________________________<br>
<br>
<br>

Firma:___________________________<br>
Huella pulgares: <br>



</p>
<svg width="450" height="150">
   <rect width="100" height="120"
     x="220" y="20" fill="white" stroke="black" />
    <rect width="100" height="120"
     x="20" y="20" fill="white" stroke="black" />
</svg>
</body>
</html>
'''

    #print(mensaje)
    f.write(mensaje)
    f.close()
    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\contrato_adelanto' + NOMBRE_TRABAJADOR + '.html')