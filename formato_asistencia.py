import leew
import os
import webbrowser
import datetime, calendar

def imprimir(mes,ano, nota):
     # para obtener una lista con los dias de vacaciones
    lista_de_lista_de_dias_vac = leew.consulta_lista('worker.db','lista_dias','vacaciones','status', '"' + 'ABIERTO' + '"')
    #print(lista_de_lista_de_dias_vac)
    lista_temp = []
    for lista in lista_de_lista_de_dias_vac:

        lista = lista.replace("[","")
        lista = lista.replace("]", "")
        lista = lista.replace(" ", "")
        lista = lista.replace("'", "")
        lista = [i for i in lista.split(',')]
        lista_temp = lista_temp + lista
    lista_de_dias_de_vac = lista_temp

    # FABRICACION DE FILAS DEL FORMATO DE ASISTENCIA

    largo_del_mes = calendar.monthlen(int(ano),int(mes))
    FILAS_DE_FECHAS = ''
    for dia in range(1,largo_del_mes + 1):

        # tuve que crear dia y mes corregido porque en la base de datos las fechas son 00-00-0000
        if len(str(dia)) < 2:
            dia_corregido = '0' + str(dia)
        else:
            dia_corregido = str(dia)

        if len(mes) < 2:
            mes_corregido = '0' + mes
        else:
            mes_corregido = mes

        FECHA = dia_corregido + '-' + mes_corregido + '-' + ano

        fecha_datetime = datetime.datetime(int(ano), int(mes), dia)
        tupla_diassem = ("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO")
        dia_sem = datetime.datetime.weekday(
            fecha_datetime)  # 0-Lunes, 1-Martes, 2-Miércoles, 3-Jueves, 4-Viernes , 5-Sábado y 6-Domingo
        DIA_DE_SEMANA = tupla_diassem[dia_sem]

        dicc_hora_de_salida = {4: '04:00 PM, Firma:__________________', 5: 'DESCANSO', 6: 'DESCANSO'}
        dicc_hora_de_entrada = {4: '07:00 AM, Firma:__________________', 5: 'DESCANSO', 6: 'DESCANSO'}

        if leew.consulta_gen('worker.db','nombre','dia_no_laborables','fecha','"' + FECHA + '"') is not None:
            OBSERVACION = 'Feriado. ' + leew.consulta_gen('worker.db','nombre','dia_no_laborables','fecha','"' + FECHA + '"')
            HORA_DE_SALIDA = 'FERIADO'
            HORA_DE_ENTRADA = 'FERIADO'
        else:
            OBSERVACION = ''
            HORA_DE_SALIDA = dicc_hora_de_salida.get(dia_sem, '05:00 PM, Firma:__________________')
            HORA_DE_ENTRADA = dicc_hora_de_entrada.get(dia_sem, '07:00 AM, Firma:__________________')

        # para identificar los dias con vacaciones

        if FECHA in lista_de_dias_de_vac:
            HORA_DE_SALIDA = HORA_DE_ENTRADA = 'VACACIONES'

        #print(OBSERVACION)
        #print(FECHA)
        #print(DIA_DE_SEMANA)
        #print(HORA_DE_SALIDA)
        #print(HORA_DE_ENTRADA)
        FILAS_DE_FECHAS = FILAS_DE_FECHAS + \
            ''' 
            <tr>
            <td height="50" align="center">''' + FECHA + '''</td>
            <td align="center">'''+ DIA_DE_SEMANA + '''</td>
            <td align="center">''' + HORA_DE_ENTRADA +'''</td>
            <td align="center">''' + HORA_DE_SALIDA + '''</td>
            <td></td> <!-- ESTA CELDA ES PARA LA FIRMA DEL SUPERVISOR-->
            <td align="center">''' + OBSERVACION + '''</td>
            <td align="center"></td>
            </tr>
            '''

    lista_de_trabajadores = leew.consulta_lista('worker.db','id','info','Estatus','"Activo"')
    for trabajador in lista_de_trabajadores:
        NOMBRE = leew.consulta_gen('worker.db','Nombre','info','id',str(trabajador)) + ' ' + \
                 leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', str(trabajador))
        CEDULA = leew.consulta_gen('worker.db','Identificacion','info','id',str(trabajador))
        dict_meses = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',7:'julio',8:'agosto',
                      9:'septiembre',10:'octubre',11:'noviembre',12:'diciembre'}
        MES = dict_meses[int(mes)]
        ANO = ano

        mensaje = '''
        <!DOCTYPE html>
        <html lang="sp">
        <head>
        <meta charset="UTF-8">
        <title>Formato de asistencia</title>
        </head>
        <body>
        <p><big>Nombre del trabajador: ''' + NOMBRE + ''', Cedula:''' + CEDULA + '''<br>
        Mes: ''' + MES + ''', Ano: ''' + ANO + '''</big></p>
        <hr/>
        <table border="1">
        <tr>
        <td width="100" align="center"><p><b>FECHA</b></p></td>
        <td width="200" align="center"><p><b>DIA DE LA SEMANA</b></p></td>
        <td width="300" align="center"><p><b>HORA DE LLEGADA</b></p></td>
        <td width="300" align="center"><p><b>HORA DE SALIDA</b></p></td>
        <td width="100" align="center"><p><b>FIRMA DEL SUPERVISOR</b></p></td>
        <td width="250" align="center"><p><b>OBSERVACION</b></p></td>
        <td width="250" align="center"><p><b>NOTA</b></p></td>
        </tr>
        ''' + FILAS_DE_FECHAS + '''

        </table>
        <hr/>
        <p> Nota: ''' + nota + ''' </p>
        </body>
        </html>
        '''
        f = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\formatos_asistencia\\formato_' + NOMBRE + MES + ANO + '.html', 'w',encoding='utf-8')
        f.write(mensaje)
        f.close()

        webbrowser.open_new_tab(
            f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\formatos_asistencia\\formato_' + NOMBRE + MES + ANO + '.html')

