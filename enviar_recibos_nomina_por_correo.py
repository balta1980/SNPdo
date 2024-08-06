import leew, google_correo, os


def enviar(periodo):
    lista_de_recibos_en_nomina = leew.consulta_lista('worker.db', 'ID_NOM', 'nomina', 'PERIODO', f'"{periodo}"')
    for recibo in lista_de_recibos_en_nomina:
        id_trab = leew.consulta_gen('worker.db', 'ID_TRABAJADOR', 'nomina', 'ID_NOM', f'"{recibo}"')
        correo = leew.consulta_gen('worker.db', 'email', 'info', 'id', f'"{id_trab}"')

        archivo_anexo = f'{os.path.dirname(os.path.abspath(__file__))}\\impresiones\\nomina{recibo}.html'
        google_correo.manejo_gmail(correo, 'Filtertech SRL Recibo de nómina', 'Apreciado colaborador'
                                                                              'el presente correo es para hacerle '
                                                                              'entrega de su recibo de nómina',
                                   archivo_anexo).gmail_create_draft_with_attachment()
