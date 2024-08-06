import leew, datetime, webbrowser, os
def imprime(id_trabajador, DIRIGIDO, FIRMANTE, CARGO_FIRMANTE, TELF_FIRMANTE):

    FECHA = datetime.date.today().strftime("%d-%m-%Y")

    nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', id_trabajador)
    nombre2 = leew.consulta_gen('worker.db', 'nombre2', 'info', 'id', id_trabajador)
    apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', id_trabajador)
    apellido2 = leew.consulta_gen('worker.db', 'apellido2', 'info', 'id', id_trabajador)

    NOMBRE_TRABAJADOR = f'{nombre} {nombre2} {apellido} {apellido2}'

    TIPO_DOC = leew.consulta_gen('worker.db','Tipo_doc','info','id',f'"{id_trabajador}"')
    if TIPO_DOC == 'C':
        TIPO_DOC = 'cédula'
    elif TIPO_DOC == 'P':
        TIPO_DOC = 'pasaporte'
    else:
        TIPO_DOC = 'NSS'
    NUM_CEDULA = leew.consulta_gen('worker.db','Identificacion','info','id',f'"{id_trabajador}"')
    CARGO = leew.consulta_gen('worker.db','cargo','info','id',f'"{id_trabajador}"')
    FECHA_INICIO = leew.consulta_gen('worker.db','fecha_ingreso','info','id',f'"{id_trabajador}"')
    SALARIO = leew.consulta_gen('worker.db','salario','salario','status',f'"Vigente" and id ={id_trabajador}')
    LOGO = leew.consulta_gen('worker.db', 'ruta_logo', 'info_sociedad', 'estatus', '"Vigente"')
    LOGO = LOGO.replace('impresiones/', '')
    LOGO_PIE = leew.consulta_gen('worker.db', 'opcional1', 'info_sociedad', 'estatus', '"Vigente"')
    LOGO_PIE = LOGO_PIE.replace('impresiones/', '')
    # creando el archivo

    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\carta_trabajo' + NOMBRE_TRABAJADOR + '.html', 'w',encoding='utf-8')
    #f = open('cartas_trabajo/carta.html', 'w')

    mensaje = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Carta de trabajo</title>
    <img src="{LOGO}" alt="" height="130" />
</head>
<body>
<p align="right"> Santo Domingo, {FECHA}.</p><br>
<p align="center"><big>CONSTANCIA DE TRABAJO</big></p>
<p><strong>Señores:{DIRIGIDO}<br>
Asunto: Constancia de Trabajo
</strong></p>

<p align="justify">
    Se hace constar que el(la) Sr(a) {NOMBRE_TRABAJADOR}  titular del documento: {TIPO_DOC}, número {NUM_CEDULA}, quien ocupa la
    posición de {CARGO}; presta sus servicios a esta Empresa desde el {FECHA_INICIO} devengando un salario mensual
    básico de {SALARIO} DOP.


Se expide la presente constancia a petición de la parte interesada, en Santo Domingo, al {FECHA}.
<br>
<br>
Se despide atentamente
<br>
Por Filtertech, S.R.L
<br>
<br>
<br></p>
<p align="center">
____________________<br>
{FIRMANTE}<br>
{CARGO_FIRMANTE}<br>
{TELF_FIRMANTE}</p>


</body>
<img src="{LOGO_PIE}" alt="" height="150" />
</html>
'''

    #print(mensaje)
    f.write(mensaje)
    f.close()
    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\carta_trabajo' + NOMBRE_TRABAJADOR + '.html')