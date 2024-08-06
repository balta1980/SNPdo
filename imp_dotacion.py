import webbrowser, leew, os


def imprimir(id):
    # OBTENER VALORES
    # id de dotacion (id)
    empresa = leew.consulta_gen('worker.db','nombre_sociedad','info_sociedad','estatus','"Vigente"')
    f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\recibos_dotaciones\\dotacion' + id + '.html', 'w')
    nombre = leew.consulta_gen('worker.db','nombre','dotacion','id',id)
    id_trab = leew.consulta_gen('worker.db','id_trab','dotacion','id',id)
    cedula = leew.consulta_gen('worker.db','Identificacion','info','id',str(id_trab))
    cargo = leew.consulta_gen('worker.db','cargo','info','id',str(id_trab))
    camisas = str(leew.consulta_gen('worker.db','cant_camisas','dotacion','id',id))
    pantalones = str(leew.consulta_gen('worker.db','cant_pantalones','dotacion','id',id))
    zapatos = str(leew.consulta_gen('worker.db','zapatos','dotacion','id',id))
    lentes = str(leew.consulta_gen('worker.db','lentes','dotacion','id',id))
    guantes = str(leew.consulta_gen('worker.db','guantes','dotacion','id',id))
    nota = leew.consulta_gen('worker.db','nota','dotacion','id',id)

    mensaje = '''
<!DOCTYPE html>

<head>
    <meta charset=ISO-8859-1>
    <title>Dotacion ''' + id + '''</title>
</head>
<br>
<body>
<div>

    <h2 align="center">Constancia de entrega de Dotación</h2>

<p align="justify">Yo, ''' + nombre + ''', portador de la Cédula de Identidad y Electoral Número ''' + cedula + ''', en mi posición
     de ''' + cargo + ''', por medio de la presente hago constar que me ha sido asignado por la empresa ''' + empresa +''', para uso en mis
    deberes , la siguiente dotación:</p>

    <p>a)	''' + camisas + ''' camisas.</p>
    <p>b)	''' + pantalones + ''' pantalones.</p>
    <p>c)	''' + zapatos + ''' par(es) zapatos.</p>
    <p>d)	''' + lentes + ''' par(es) lentes.</p>
    <p>e)	''' + guantes + ''' par(es) guantes.</p>

<p align="justify">Para la utilización exclusivas de mis funciones y sobre el cual soy la única persona que utilizare ese equipo, el cual
    debo cuidar a fin de evitar deterioros y pérdidas.

Los elementos del uniforme, como mangas y chaqueta, deberán ser mantenidos en las instalaciones de la empresa y solo en caso de tener que lavarlos serán retirados para tal fin y devueltos al día siguiente. En caso de ser sacados de las instalaciones, el empleado se compromete bajo toda responsabilidad a asumir los daños de los equipos.

Al momento de cambiar los uniformes a requerimiento de la empresa, la misma requerira los uniformes anteriores para proporcionar los nuevos.

    Asi mismo me comprometo a pagar la suma del cien por ciento (100%) al momento de la pérdida o daño, como un pago único, como anticipo a salario en caso de daño físico (daños graves) o pérdida para el cuál en su momento me comprometo a firmar un documento al respecto. En caso de negación de firma de ese documento, la firma de este documento será válida para el descuento por anticipo de salario otorgado.</p>


</div>
<br>
Recibido Conforme  (nombre y firma):________________________                       Fecha:___/___/___
<br>
<p>Nota: ''' + nota + '''


</body>
</html>
    '''

    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab(
        f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\recibos_dotaciones\\dotacion' + id + '.html')
