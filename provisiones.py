from datetime import date
from dateutil.relativedelta import relativedelta

#las entradas a estas funciones deben ser objetos datetime.date(aaaa,m,d)

# las salidas o returns son listas y el primer valor es la cantidad de dias  segun el periodo y el segundo para costos

def cesantia(fecha_ingreso,fecha_nomina):
    ''''print(fecha_ingreso + relativedelta(months=3))
    print(fecha_ingreso + relativedelta(months=6))
    print(fecha_ingreso + relativedelta(months=12))
    print(fecha_ingreso + relativedelta(months=60))'''

    if fecha_nomina < fecha_ingreso + relativedelta(months=3):
        dias = 0
        ped = 6 / 3
    else:
        if fecha_nomina < fecha_ingreso + relativedelta(months=6):
            dias = 6
            ped = (13 - 6) / 3
        else:
            if fecha_nomina < fecha_ingreso + relativedelta(months=12):
                dias = 13
                ped = (21 - 13) / 6
            else:
                if fecha_nomina < fecha_ingreso + relativedelta(months=60):
                    dias = 21
                    ped = 23 / 12
                else:
                    dias = 23
                    ped = 23 / 12
    return [dias, ped]


def vacaciones(fecha_ingreso,fecha_nomina):

    if fecha_nomina < fecha_ingreso + relativedelta(months=5):
        dias = 0
        ped = 6 / 5
    else:
        if fecha_nomina < fecha_ingreso + relativedelta(months=6):
            dias = 6
            ped = 7 / 6
        else:
            if fecha_nomina < fecha_ingreso + relativedelta(months=7):
                dias = 7
                ped = 8 / 7
            else:
                if fecha_nomina < fecha_ingreso + relativedelta(months=8):
                    dias = 8
                    ped = 9 / 8
                else:
                    if fecha_nomina < fecha_ingreso + relativedelta(months=9):
                        dias = 9
                        ped = 10 / 9
                    else:
                        if fecha_nomina < fecha_ingreso + relativedelta(months=10):
                            dias = 10
                            ped = 11 / 10
                        else:
                            if fecha_nomina < fecha_ingreso + relativedelta(months=11):
                                dias = 11
                                ped = 12 / 11
                            else:
                                if fecha_nomina < fecha_ingreso + relativedelta(months=12):
                                    dias = 12
                                    ped = 14 / 12
                                else:
                                    if fecha_nomina < fecha_ingreso + relativedelta(months=60):
                                        dias = 14
                                        ped = 18 / 12
                                    else:
                                        dias = 18
                                        ped = 18 / 12
    return [dias, ped]


def part_beneficios(fecha_ingreso,fecha_nomina):

    if fecha_nomina < fecha_ingreso + relativedelta(months=12):
        dias = 0
        ped = 45 / 12
    else:
        if fecha_nomina < fecha_ingreso + relativedelta(months=36):
            dias = 45
            ped = 60 / 12
        else:
            dias = 60
            ped = 60 / 12
    return [dias, ped]


def pre_aviso(fecha_ingreso,fecha_nomina):

    if fecha_nomina < fecha_ingreso + relativedelta(months=3):
        dias = 0
        ped = 7 / 3
    else:
        if fecha_nomina < fecha_ingreso + relativedelta(months=6):
            dias = 7
            ped = (14 - 7) / 3
        else:
            if fecha_nomina < fecha_ingreso + relativedelta(months=12):
                dias = 14
                ped = (28 - 14) / 6
            else:
                dias = 28
                ped = 28 / 12
    return [dias, ped]

'''
print(pre_aviso(date(2018,1,22),date(2032,6,28)))
print(cesantia(date(2018,1,22),date(2018,12,1)))
print(vacaciones(date(2018,1,22),date(2032,6,28)))
print(part_beneficios(date(2018,1,22),date(2032,6,28)))'''
