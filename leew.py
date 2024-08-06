import sqlite3, os #importa el modulo
#import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time, timedelta


def tambd(bd):                       #para determinar el numero de filas o registros de la BD
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)         # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()    # crea el cursor
    cursor_info.execute("SELECT count(*) FROM info")  # hacer consultas
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa
        a,=reg
        return (a)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def tambd_par(bd,tabla,par):                     #para determinar el numero de filas o registros de la BD
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)                 # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()            # crea el cursor
    cursor_info.execute("SELECT count(*) FROM "+tabla+" WHERE ID="+par)  # hacer consultas
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa
        a,=reg
        return (a)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def consultaP(bd,p1,p2,p3):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM "+p2+" WHERE ID="+p3) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def consulta_clave(bd,p1,p2,p3):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM "+p2+" WHERE nombre='"+p3+"'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def consultaPS(bd,p1,p2,p3):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM "+p2+" WHERE ID="+p3+" AND STATUS='Vigente'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def consulta_legal(p1):

    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM legales WHERE STATUS='Vigente'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def introduce_legal(val):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO legales VALUES ("+val+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def update_legal():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE legales SET status='Anterior'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consulta_salmin(p1):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM salario_min WHERE STATUS='Vigente'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def introduce_salmin(val):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO salario_min VALUES ("+val+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def update_salmin():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE salario_min SET status='Anterior'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def con_ina_p(bd,p1,p2): #numero de dias de inasistencias a partir del ID y el periodo del año
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT sum(dias) FROM inasis WHERE ID="+p1+" AND periodo="+p2) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def con_ina(bd,p1): #numero de dias de inasistencias a partir del ID
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT sum(dias) FROM inasis WHERE ID="+p1) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def introduce_info(info):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO info VALUES ("+info+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def introduce_salario(sal):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO salario VALUES (" +sal+ ")") # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def actualiza_salario(val_1):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE salario SET status = 'Anterior' WHERE id="+val_1+" AND status = 'Vigente'")  # introducir salario
    con_bd.commit()  # ejecuta la instrucción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def del_reg(tabla,id):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM "+tabla+" WHERE id="+id)  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def introduce_inasis(ina):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO inasis VALUES ("+ina+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def introduce_carga_fam(carga_fam):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO carga_fam VALUES ("+carga_fam+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def edita_carga_fam(carga_fam):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE carga_fam SET ("+carga_fam+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def tambd_acceso(bd):                       #para determinar el numero de filas o registros de la BD
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)         # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()    # crea el cursor
    cursor_info.execute("SELECT count(*) FROM usu")  # hacer consultas
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa
        a,=reg
        return (a)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consultaPer(bd):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT idp FROM periodo WHERE status= 'ABIERTO'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)

def consultaPer_top(bd):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT idp FROM periodo WHERE status= 'ABIERTO' LIMIT 1") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)

def update_periodo(per):

    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE periodo SET status='CERRADO' WHERE idp='"+per+"'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consulta_IDF(bd,trab):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT id_i FROM inasis WHERE computado= 0 AND id="+trab) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)


def consulta_IDF2(bd,trab):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT id_i FROM inasis WHERE id="+trab) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)

def consulta_inasis_nom(bd,col,id_h):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+col+" FROM inasis WHERE id_i="+id_h) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        return (val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def del_inasis(id_i):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM inasis WHERE id_i="+id_i)  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def update_inasis():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE inasis SET computado=1")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def introduce_h_e(he):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO horas_extras VALUES ("+he+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consulta_IDF3(bd,trab):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT id_h FROM horas_extras WHERE computado= 0 AND id="+trab) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)


def consulta_h_extra(bd,col,id_h):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+col+" FROM horas_extras WHERE id_h="+id_h) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        return (val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def del_h_extra(id):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM horas_extras WHERE id_h="+id)  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def update_h_extra():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE horas_extras SET computado=1")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def tambd_par2(bd,tabla):                     #para determinar el numero de filas o registros de la BD en periodo
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)                 # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()            # crea el cursor
    cursor_info.execute("SELECT count(*) FROM "+tabla)  # hacer consultas
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa
        a,=reg
        return (a)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consultaP2(bd,p1,p2,p3): #usada en periodo
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM "+p2+" WHERE indice="+p3) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return reg
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def introduce_periodo(per):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO periodo VALUES ("+per+")")  # introducir periodo
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def primer_dia_periodo(per):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("SELECT f_inicio FROM periodo WHERE idp="+per)  # introducir periodo
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return reg
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def ultimo_dia_periodo(per):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("SELECT f_fin FROM periodo WHERE idp="+per)  # introducir periodo
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return reg
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def introduce_par(tabla,val):     #para usar cuando sea necesario
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO "+tabla+" VALUES ("+val+")")  # introducir periodo
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def cant_dia_no_lab(bd):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT indice FROM dia_no_laborables") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)


def lista_dia_no_lab():
    lista =[]
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT fecha FROM dia_no_laborables") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)


def del_dia_no_lab(fecha):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM dia_no_laborables WHERE fecha= '"+fecha + "'")  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consulta_benef(p1):

    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM beneficios WHERE status='Vigente'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def update_beneficios():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE beneficios SET status='Anterior'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def consulta_islr(p1):

    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM islr WHERE status='Vigente'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd


def update_islr():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE islr SET status='Anterior'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def tambd_nom(bd):                       #para determinar el numero de filas o registros de la BD
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista = []
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("SELECT id FROM info WHERE Estatus='Activo'")  # hacer consultas
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa
        val, = reg
        lista.append(val)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd
    return (lista)


def consulta_tss(p1):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+p1+" FROM tss WHERE STATUS='Vigente'") #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        return(reg)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def introduce_tss(val):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO tss VALUES ("+val+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def update_tss():
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE tss SET status='Anterior'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd


def ff2(ano,mes,dia, lista_fecha, lista_sal):  # formula inicial para obtener el salario entre rango de fechas
    i = 0
    for n in lista_fecha:
        d, m, a = [int(v) for v in n.split("-")]
        while i < len(lista_fecha):
            d1, m1, a1 = [int(v) for v in lista_fecha[i].split("-")]
            if date(a,m,d) <= date(ano,mes,dia) and date(a1,m1,d1) > date(ano,mes,dia):
                return lista_sal[i-1]
            else:
                i = i + 1

def ff3(ano, mes, dia, lista_fecha, lista_sal): #formula definitiva para obtener el salario entre rango de fechas
    if ff2(ano,mes,dia, lista_fecha, lista_sal) == None:
        df, mf, af = [int(v) for v in lista_fecha[len(lista_fecha) - 1].split("-")]
        if date(af,mf,df) <= date(ano,mes,dia):
            return lista_sal[len(lista_fecha) - 1]
        else:
            return None
    else:
         return ff2(ano,mes,dia, lista_fecha, lista_sal)

def consulta_lista(bd,col,tabla,col_cond,cond):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT "+col+" FROM "+tabla+" WHERE "+col_cond+"= "+cond) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)

def introduce_nomina(datos):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO nomina VALUES ("+datos+")")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def del_vac(indice):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM vacaciones WHERE indice="+indice)  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def update_vac(indice):
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("UPDATE vacaciones SET status='CERRADO' WHERE indice='"+indice+"'")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def difrencia_fechas_habiles(fecha1,fecha2): # fecha1 debe ser mayor a fecha2
    ''' función que calcula los días hábiles pagables, es decir solo saca los domingos y 1/2 jornada del sabado
    pero no saca los feriados porque a fin de cuenta los feriados se deben pagar
    '''
    descuenta = 0.0
    dif_bruta = fecha1 - fecha2
    fecha_test = fecha2
    #print(dif_bruta.days)
    for n in range(dif_bruta.days):

        #print('fecha test',fecha_test)
        if datetime.weekday(fecha_test) == 6:
                    #0-Lunes, 1-Martes, 2-Miércoles, 3-Jueves, 4-Viernes , 5-Sábado y 6-Domingo :
            descuenta = descuenta + 1.0
        elif datetime.weekday(fecha_test) == 5:# sabado es media jornada
            descuenta = descuenta + 0.5
        fecha_test = fecha_test + relativedelta(days=1)

    diferencia_neta = float(dif_bruta.days) - descuenta + 1 # le sumo 1 porque esa operacion da por ejem 01/01/2000 al 15/01/2000 da 14 dias en vez de 15
    #print(diferencia_neta)
    return diferencia_neta

def consulta_gen(bd,col,tabla,col_cond,cond):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    #print("SELECT "+col+" FROM "+tabla+" WHERE "+col_cond+"= "+cond)
    cursor_info.execute("SELECT "+col+" FROM "+tabla+" WHERE "+col_cond+"= "+cond) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        return (val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def consulta_lista_distintc(bd,col,tabla,col_cond,cond):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    lista =[]
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    cursor_info.execute("SELECT DISTINCT "+col+" FROM "+tabla+" WHERE "+col_cond+"= "+cond) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        lista.append(val)
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd
    return (lista)

def consulta_gen_sum(bd,col,tabla,col_cond,cond):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)        # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()       # crea el cursor
    #print("SELECT "+col+" FROM "+tabla+" WHERE "+col_cond+"= "+cond)
    cursor_info.execute("SELECT SUM("+col+") FROM "+tabla+" WHERE "+col_cond+"= "+cond) #hacer consultas
    for reg in cursor_info:             #iterando por toda la bd pero con una consulta sql bellaaa
        val,=reg
        return val
    cursor_info.close()                 # cierra cursor
    con_bd.close()                      # cierra bd

def ultimos_22_per():
    lista = []
    con_bd = sqlite3.connect(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db')  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute('SELECT idp from periodo WHERE status = "CERRADO" ORDER by indice DESC LIMIT 22')  # hacer consultas
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa
        val, = reg
        lista.append(val)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd
    return (lista)

def introduce_gen(bd,tabla, valores):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("INSERT INTO " + tabla + " VALUES ("+valores+")")  # introducir periodo
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def del_gen(bd,tabla,par,valor):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM " + tabla + " WHERE " + par + "="+valor)  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def update_gen(bd,tabla,col,valor='"Anterior"'):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute(f"UPDATE {tabla} SET {col}={valor}")  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def update_linea_gen(bd,tabla,col,valor, col_cond, cond):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute(f'UPDATE {tabla} SET {col}="{valor}" WHERE {col_cond} = "{cond}"')  # introducir trabajador
    con_bd.commit() #ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def backup_bd(motivo='BU'):
    # funcion incompleta pensada para hacer backup general de la BD
    try:
        formato = "%d-%m-%y %I %M %S %p" # formato de fecha usado por el comando strftime
        fecha_y_hora = str(datetime.today().strftime(formato))
        ruta1 = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db'
        ruta2 = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\respaldo_bd\\worker_{motivo}_{fecha_y_hora}.db'
        comando = f'copy "{ruta1}" "{ruta2}"'
        #print(comando)
        os.system(comando)
    except:
        print("algo salio mal en el backup de la base de datos")

def del_gen_todas_las_filas(bd,tabla):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    cursor_info.execute("DELETE FROM " + tabla)  # introducir salario
    con_bd.commit()  # ejecuta la inserción
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd

def crea_periodo_fiscal(periodo):
    # esta función crea un texto separado por comas con el listado de todos los meses del año fiscal con formato MMAAAA
    # y crea una entrada en la tabla periodo_fiscal

    anio_cierre = periodo[4:8]
    mes_cierre = periodo[2:4]
    dia_fin_cierre = consulta_gen('worker.db', 'f_fin', 'periodo', 'idp', f'"{periodo}"')[0:2]
    #print(anio_cierre)
    #print(mes_cierre)
    #print(dia_fin_cierre)
    fecha_fin_per_fiscal = f'{dia_fin_cierre}-{mes_cierre}-{anio_cierre}'
    #print(fecha_fin_per_fiscal)
    date_fecha_fin_per_fiscal = date(int(anio_cierre), int(mes_cierre), int(dia_fin_cierre))
    lista_en_texto_MMAAAA = ''
    for n in range(11,0,-1):
        #print(date_fecha_fin_per_fiscal - relativedelta(months=n))
        mmaaaa = date_fecha_fin_per_fiscal - relativedelta(months=n)
        lista_en_texto_MMAAAA = lista_en_texto_MMAAAA + f"{mmaaaa.strftime('%m%Y')},"
    lista_en_texto_MMAAAA = lista_en_texto_MMAAAA + date_fecha_fin_per_fiscal.strftime('%m%Y')
    idp_fiscal = f"01{(date_fecha_fin_per_fiscal - relativedelta(months=11)).strftime('%m%Y')}-{dia_fin_cierre}{mes_cierre}{anio_cierre}"
    fecha_inicio_per_fiscal = f"01-{(date_fecha_fin_per_fiscal - relativedelta(months=11)).strftime('%m-%Y')}"
    status = 'ABIERTO'
    #print(lista_en_texto_MMAAAA)
    #print(idp_fiscal)
    #print(fecha_inicio_per_fiscal)

    introduce_gen('worker.db','periodo_fiscal',f'"{idp_fiscal}","{status}", NULL, "{fecha_inicio_per_fiscal}",'
                                               f' "{fecha_fin_per_fiscal}", "{lista_en_texto_MMAAAA}"')

def exporta_filas_tabla(bd, tabla):
    bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{bd}'
    con_bd = sqlite3.connect(bd)  # conecta la base de datos y la vuelve el objeto
    cursor_info = con_bd.cursor()  # crea el cursor
    # print("SELECT "+col+" FROM "+tabla+" WHERE "+col_cond+"= "+cond)
    cursor_info.execute(f"select * from {tabla}")  # hacer consultas
    lista_de_filas = []
    for reg in cursor_info:  # iterando por toda la bd pero con una consulta sql bellaaa

        lista_de_filas.append(reg)
    cursor_info.close()  # cierra cursor
    con_bd.close()  # cierra bd
    return lista_de_filas

def calculo_retencion_islr(base):
    # funcion para calcular y retornar el valor del ISLR dependiendo de un valor dado
    '''Para el tema de la retencion del ISLR se debe tomar en cuenta que hay varias nominas que forman base de calculo
    1) Cuando se haga una nómina quincenal se debe verificar:
    -la base de ISLR en nómina bonificacion y su retencion
    2) cuando se haga una nómina de bonificación o utilidad se debe revisar:
    - La base de ISLR en la nómina de quincena de la 1q(en la 1q no se retiene) y la 2q y su retención
    - La base de ISLR y su retencion en la nómina de liquidacion-retiro
    3) Cuando se haga una nómina de liquidacion-retiro se debe revisar:
    - La base de ISLR en la nómina de quincena de la 1q(en la 1q no se retiene) y la 2q y su retención
    - La base de ISLR y su retencion en la nómina de bonificacion utilidad'''
    rango1, = consulta_islr('rango1')
    rango2, = consulta_islr('rango2')
    rango3, = consulta_islr('rango3')
    tasa1, = consulta_islr('tasa1')
    tasa2, = consulta_islr('tasa2')
    tasa3, = consulta_islr('tasa3')
    valor1, = consulta_islr('valor1')
    valor2, = consulta_islr('valor2')
    if base * 12 <= rango1:
        RETENCION = 0
    else:
        if base * 12 <= rango2:
            RETENCION = ((12 * base + 0.01) - rango1) * tasa1 / 100 / 12
        else:
            if base * 12 <= rango3:
                RETENCION = valor1 / 12 + ((12 * base + 0.01) - rango2) * tasa2 / 100 / 12
            else:
                RETENCION = valor2 / 12 + ((12 * base + 0.01) - rango3) * tasa3 / 100 / 12
    return RETENCION



if __name__ == "__main__":
    print(calculo_retencion_islr(760000))




