#calcula aniversarios: https://steemit.com/spanish/@eniolw/calculo-exacto-de-la-edad-en-python-snippet-para-aprendices-de-programacion-y-developers

from datetime import date
import calendar

def calcular_ano_hoy(f1):

    hoy = date.today()
    try:
        f2 = f1.replace(year=hoy.year)

    except ValueError:
        f2 = f1.replace(year=hoy.year, day=f1.day - 1)


    if f2 > hoy:
        return hoy.year - f1.year - 1
    else:
        return hoy.year - f1.year

def calcular_ano_f(f1,f2):

    try:
        f3 = f1.replace(year=f2.year)

    except ValueError:
        f3 = f1.replace(year=f2.year, day=f1.day - 1)

    if f3 > f2:
        return f2.year - f1.year - 1
    else:
        return f2.year - f1.year

def calc_dif_fecha(f1,f2):
    #anio
    try:
        f3 = f1.replace(year=f2.year)

    except ValueError:
        f3 = f1.replace(year=f2.year, day=f1.day - 1)

    #print(f1, f2)
    if f3 > f2:
        anios = f2.year - f1.year - 1
    else:
        anios = f2.year - f1.year

    #mes
    if f1.month > f2.month:

        if f1.day > f2.day:
            meses = 12 - f1.month +  f2.month - 1
        else:
            meses = 12 - f1.month +  f2.month
    elif f1.month == f2.month:
        meses = 0
    else:
        if f1.day > f2.day:
            meses = f2.month - f1.month - 1
        else:
            meses = f2.month - f1.month

    # dias
    dias_del_mes = calendar.monthlen(f1.year,f1.month)
    if f1.day > f2.day:
        dias = dias_del_mes - f1.day + f2.day + 1
    else:
        dias = f2.day - f1.day + 1

    return anios, meses, dias



#p = date(2018,1,22)
#p2 = date(2020,1,19)
#print(calc_dif_fecha(p,p2))
