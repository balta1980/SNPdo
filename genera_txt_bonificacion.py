import leew, os

def generar_txt(periodo_fiscal):
    # esta funcion solo recibe segundos periodos
    # con esta función se hacen los archivos TXT de la TSS

    rnc = leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'Estatus', '"Vigente"')
    rnc_fixed = (11 - len(rnc)) * ' ' + rnc

    MMAAAA = leew.consulta_gen('worker.db', 'MMAAAA', 'nomina_beneficios', 'idp_fiscal', f'"{periodo_fiscal}" LIMIT 1')

    # creando el archivo txt bonificacion

    txt_bonificacion = open(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\{rnc}_{MMAAAA}_BO.txt', 'w')
    encabezado = f'EBO{rnc_fixed}{MMAAAA}\n'
    txt_bonificacion.write(encabezado)

    listado_trabajadores_en_nomina = leew.consulta_lista('worker.db', 'idt', 'nomina_beneficios','idp_fiscal',
                                                         f'"{periodo_fiscal}"')
    # print(listado_trabajadores_en_nomina)

    for id_trabajador in listado_trabajadores_en_nomina:
        clave_nomina = leew.consulta_gen('worker.db', 'clave_de_nomina','info','id',str(id_trabajador))
        tipo_documento = leew.consulta_gen('worker.db', 'tipo_doc','info','id',str(id_trabajador))
        num_de_documento = leew.consulta_gen('worker.db', 'Identificacion','info','id',str(id_trabajador))
        num_de_documento = num_de_documento + (25 - len(num_de_documento)) * " " # para rellenar con espacios hasta 25 de longitud
        primer_nombre = leew.consulta_gen('worker.db', 'Nombre','info','id',str(id_trabajador))
        segundo_nombre = leew.consulta_gen('worker.db', 'nombre2','info','id',str(id_trabajador))
        nombres = f'{primer_nombre} {segundo_nombre}'
        nombres = nombres + (50 - len(nombres)) * " "
        primer_apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', str(id_trabajador))
        primer_apellido = primer_apellido + (40 - len(primer_apellido)) * " "
        segundo_apelido = leew.consulta_gen('worker.db', 'apellido2', 'info', 'id', str(id_trabajador))
        segundo_apelido = segundo_apelido + (40 - len(segundo_apelido)) * " "
        sexo = leew.consulta_gen('worker.db', 'Sexo', 'info', 'id', str(id_trabajador))[0] # la primera letra es F o M
        fecha_de_nacimiento = leew.consulta_gen('worker.db', 'Fecha_nacimiento', 'info', 'id', str(id_trabajador)).replace("-", "")
        monto_bonificacion = float(leew.consulta_gen('worker.db', 'monto_ajustado','nomina_beneficios', 'idt',
                                               f'{id_trabajador} AND idp_fiscal = "{periodo_fiscal}"').replace('RD$','').replace(',',''))
        monto_bonificacion = str("{:.2f}".format(monto_bonificacion)).zfill(16)

        linea_txt = f'D{tipo_documento}{num_de_documento}{nombres}{primer_apellido}{segundo_apelido}' \
                            f'{sexo}{fecha_de_nacimiento}{monto_bonificacion}\n'
        txt_bonificacion.write(linea_txt)


        # TXT RECTIFICATIVA FIN ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

    lineas_txt = str(len(listado_trabajadores_en_nomina) + 2) # la suma del 2 es 1 por el encabezado y 1 por el sumario mismo
    lineas_txt = (6 - len(lineas_txt)) * '0' + str(lineas_txt)
    sumario = f'S{lineas_txt}'
    txt_bonificacion.write(sumario)
    txt_bonificacion.close()
    os.startfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\txt\\{rnc}_{MMAAAA}_BO.txt')
