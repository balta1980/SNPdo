from ficha import *
from datetime import date
import leew, trat_fecha, os, webbrowser, imp_dotacion, imp_carnet, valid_correo, ver_recibos

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,cmd, *args, idw="",user='', **kwargs):

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)


        self.setupUi(self)
        self.idw = idw

        self.refrescar_tabla_list_trab = cmd # este comando viene del listado de trabajadores y es para refrescar la tabla
        self.user = user #esta variable tiene que tener los datos del usuario
        self.se_edito_foto = 0
        self.se_edito_cedula = 0
        self.se_edito_tabla_carga_fam = 0

        self.ruta_foto_enBD = ''
        self.ruta_cedula_enBD = ''

        # carga de la BD  el listado de nacionalidades y las pone en el combox para que se vea para nuevos ingresos y trabajadores actuales
        self.listado_de_nacionalidades = leew.consulta_lista('worker.db', 'nacionalidad', 'listado_nacionalidades', 'id>',
                                                        '1')
        self.nacionalidad.addItems(self.listado_de_nacionalidades)

        self.tipos_doc = {'C': 0, 'P': 1, 'N': 2, 0: 'C', 1: 'P',
                          2: 'N'}  # con este diccionario convierto lo que viene y va a la BD respecto al combo box
        self.rnc_agente_ret.setText(str(leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'Estatus', '"Vigente"')))

        # Carga de data

        if self.idw == "": # este es el valor cuando es un trabajador nuevo
            QtWidgets.QMessageBox.information(self, "Atención", "Los campos obligatorios para crear al nuevo trabajador"
                                                                " son: \nNombre, Apellido, Fecha de Nacimiento, "
                                                                "tipo de documento, número de documento, la Fecha"
                                                                " de Ingreso, nacionalidad, el Salario, tipo de nómina "
                                                                "y clave de nómina en la TSS.", QtWidgets.QMessageBox.Ok)
            #self.titulo.setText("Ficha de trabajador NUEVO INGRESO")
            self.setWindowTitle("Ficha de trabajador NUEVO INGRESO")

            # para que se vea bonita la tabla mientras se carga un nuevo trabajador
            header = self.tabla_carga_fam.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)


            self.id.setDisabled(1)
            self.edad.setDisabled(1)
            self.estatus_combo.setDisabled(1)
            self.ver_foto.setDisabled(1)
            self.ver_cedula.setDisabled(1)
            self.imprime_dota.setDisabled(1)
            self.borra_dota.setDisabled(1)
            self.borra_carga.setDisabled(1)
            self.inasistencias.setDisabled(1)
            self.ano_servicios.setDisabled(1)
            self.fecha_egreso.setReadOnly(1)
            self.imp_carnet.setDisabled(1)
            self.ver_solo_adelantos_pendientes.setDisabled(1)

        else:
            self.cargar_info()
            #self.titulo.setText("Ficha de trabajador " + self.idw + " " + self.nombre_completo)
            self.setWindowTitle("Ficha de trabajador " + self.idw + " " + self.nombre_completo)
            self.imprime_dota.setDisabled(1)
            self.borra_dota.setDisabled(1)
            self.borra_carga.setDisabled(1)


        # conexiones
        self.cerrar.clicked.connect(self.close)
        self.guarda.clicked.connect(self.guardar_info)
        self.guarda.setDisabled(1)
        self.editar_foto.clicked.connect(self.editar_foto_cmd)
        self.editar_cedula.clicked.connect(self.editar_cedula_cmd)
        self.ver_foto.clicked.connect(self.ver_foto_cmd)
        self.ver_cedula.clicked.connect(self.ver_cedula_cmd)
        self.table_dotacion.clicked.connect(self.on_click_dota)
        self.imprime_dota.clicked.connect(self.imprime_dota_cmd)
        self.borra_dota.clicked.connect(self.borra_dota_cmd)
        self.tabla_carga_fam.clicked.connect(self.on_click_carga_fam)
        self.borra_carga.clicked.connect(self.borra_carga_cmd)
        self.agrega_cargaf.clicked.connect(self.agregar_carga_cmd)
        self.imp_carnet.clicked.connect(self.imprime_carnet_cmd)
        self.tabla_nomina.doubleClicked.connect(self.genera_recibo)
        self.ver_solo_adelantos_pendientes.clicked.connect(self.oculta_adelantos_ya_cobrados)
        self.ver_solo_adelantos_pendientes.clicked.connect(self.refresh_tabla_detalles_prestamo)
        self.tabla_adelantos.clicked.connect(self.refresh_tabla_detalles_prestamo)


        # conexiones para habilitar el botón guardar y poner el fondo en rojo
        self.listado_de_modificaciones = []
        self.nombre.textChanged.connect(self.disable_guardar)
        self.apellido.textChanged.connect(self.disable_guardar)
        self.seg_nombre.textChanged.connect(self.disable_guardar)
        self.seg_apellido.textChanged.connect(self.disable_guardar)
        self.fecha_nac.dateChanged.connect(self.disable_guardar) # el metodo datechanged no aparece pero yo lo forzo
        self.sexo.currentTextChanged.connect(self.disable_guardar)
        self.tipo_doc.currentTextChanged.connect(self.disable_guardar)
        self.num_doc.textChanged.connect(self.disable_guardar)
        self.nacionalidad.currentTextChanged.connect(self.disable_guardar)
        self.telf.textChanged.connect(self.disable_guardar)
        self.nivel_academico.currentTextChanged.connect(self.disable_guardar)
        self.profesion.textChanged.connect(self.disable_guardar)
        # INICIO carga familiar
        self.borra_carga.clicked.connect(self.disable_guardar)
        self.agrega_cargaf.clicked.connect(self.disable_guardar)
        # FIN carga familiar
        self.direccion_hab.textChanged.connect(self.disable_guardar) # el metodo textchanged no aparece pero yo lo forzo
        self.num_cuenta.textChanged.connect(self.disable_guardar)
        self.banco.textChanged.connect(self.disable_guardar)
        self.tipo_cuenta.textChanged.connect(self.disable_guardar)
        self.correo_e.textChanged.connect(self.disable_guardar)
        self.talla_camisa.textChanged.connect(self.disable_guardar)
        self.talla_zap.textChanged.connect(self.disable_guardar)
        self.talla_pantalon.textChanged.connect(self.disable_guardar)
        self.lic_cond.textChanged.connect(self.disable_guardar)
        self.fecha_venc_lic.dateChanged.connect(self.disable_guardar)
        self.salario_actual.valueChanged.connect(self.disable_guardar)
        self.fecha_ing.dateChanged.connect(self.disable_guardar)
        self.notas.textChanged.connect(self.disable_guardar)
        self.cargo.textChanged.connect(self.disable_guardar)
        self.tipo_nomina.currentTextChanged.connect(self.disable_guardar)
        self.emp_seguros.textChanged.connect(self.disable_guardar)
        self.num_carnet_seg.textChanged.connect(self.disable_guardar)
        self.clave_nomina.textChanged.connect(self.disable_guardar)
        self.tipo_ingreso.currentTextChanged.connect(self.disable_guardar)
        self.tipo_de_persona.currentTextChanged.connect(self.disable_guardar)
        self.primera_vac_2.dateChanged.connect(self.disable_guardar)
        self.seg_vac_2.dateChanged.connect(self.disable_guardar)
        self.tercera_vac_2.dateChanged.connect(self.disable_guardar)
        #legales
        self.ret_tss.clicked.connect(self.disable_guardar)
        self.ret_infotep.clicked.connect(self.disable_guardar)
        self.ret_isr.clicked.connect(self.disable_guardar)
        self.calc_sal_navidad.clicked.connect(self.disable_guardar)
        self.saldo_a_favor.valueChanged.connect(self.disable_guardar)
        self.rnc_agente_ret.textChanged.connect(self.disable_guardar)
        self.aporte_vol_empresa.valueChanged.connect(self.disable_guardar)
        self.aporte_vol_trabajador.valueChanged.connect(self.disable_guardar)
        self.retencion_pension.valueChanged.connect(self.disable_guardar)
        self.saldo_a_favor.setValue(0.0) # en el caso de que cuando se cree un trab no see toque la pestaña legales
        self.aporte_vol_empresa.setValue(0.0) # en el caso de que cuando se cree un trab no see toque la pestaña legales
        self.aporte_vol_trabajador.setValue(0.0) # en el caso de que cuando se cree un trab no see toque la pestaña legales
        self.retencion_pension.setValue(0.0) # en el caso de que cuando se cree un trab no see toque la pestaña legales

        # regex necesarios

        self.num_doc.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9A-Za-z]{1,25}"))) # de uno a 25 caracteres mayusculas o minusculas sin espacios ni caracters especiales

    def cargar_info(self):
        # para cargar la informacion en el formulario
        # ID
        self.id.setText(self.idw)
        self.id.setReadOnly(1)
        # NOMBRE
        self.nombre.setText(leew.consulta_gen('worker.db', 'nombre', 'info', 'id', self.idw))
        # APELLIDO
        self.apellido.setText(leew.consulta_gen('worker.db', 'apellido', 'info', 'id', self.idw))
        # NOMBRE2
        self.seg_nombre.setText(leew.consulta_gen('worker.db', 'nombre2', 'info', 'id', self.idw))
        # APELLIDO 2
        self.seg_apellido.setText(leew.consulta_gen('worker.db', 'apellido2', 'info', 'id', self.idw))
        # NOMBRE COMPLETO DEL TRABAJADOR para el titulo
        self.nombre_completo = leew.consulta_gen('worker.db', 'nombre', 'info', 'id', self.idw) + \
            " " + leew.consulta_gen('worker.db', 'apellido', 'info', 'id', self.idw)
        # FECHA DE NACIMIENTO
        fecha_nacimiento = leew.consulta_gen('worker.db', 'Fecha_nacimiento', 'info', 'id', self.idw)
        dia, mes, ano = [int(n) for n in fecha_nacimiento.split('-')]
        #print(type(dia), type(mes), type(ano))
        self.fecha_nac.setDate(QtCore.QDate(ano,mes,dia))
        # EDAD (CALCULO)
        fecha_nac = leew.consulta_gen('worker.db', 'Fecha_nacimiento', 'info','id', self.idw)
        dia, mes, anio = [int(v) for v in fecha_nac.split("-")]
        fecha_nac_date = date(anio, mes, dia)
        edad = str(trat_fecha.calcular_ano_hoy(fecha_nac_date))
        self.edad.setText(edad)
        self.edad.setReadOnly(1)
        # SEXO
        sexo_en_bd = leew.consulta_gen('worker.db', 'Sexo', 'info','id', self.idw)
        sexos = {'Masculino': 0, 'Femenino': 1}
        self.sexo.setCurrentIndex(sexos.get(sexo_en_bd))
        # Tipo_doc
        tipo_doc_en_bd = leew.consulta_gen('worker.db', 'Tipo_doc', 'info', 'id', self.idw)
        # print(niveles.get(nivel_en_bd))
        self.tipo_doc.setCurrentIndex(self.tipos_doc.get(tipo_doc_en_bd))

        # numero doc
        self.num_doc.setText(leew.consulta_gen('worker.db', 'Identificacion', 'info','id', self.idw))
        # NACIONALIDAD
        nacionalidades = {}
        index = 0
        for nac in self.listado_de_nacionalidades:
            nacionalidades[nac] = index
            index = index + 1
        nac_en_bd = leew.consulta_gen('worker.db', 'Nacionalidad', 'info','id', self.idw)
        self.nacionalidad.setCurrentIndex(nacionalidades.get(nac_en_bd))
        # TELEFONO en la BD es un Int
        self.telf.setText(str(leew.consulta_gen('worker.db', 'Telefono', 'info','id', self.idw)))
        # Nivel_academico
        niveles = {'Básico':0,'Bachiller':1,'Técnico':2,'Universitario':3,'Postgrado':4}
        nivel_en_bd = leew.consulta_gen('worker.db', 'Nivel_academico', 'info','id', self.idw)
        #print(niveles.get(nivel_en_bd))
        self.nivel_academico.setCurrentIndex(niveles.get(nivel_en_bd))
        # profesion
        self.profesion.setText(leew.consulta_gen('worker.db', 'profesion', 'info','id', self.idw))
        # CARGA FAMILIAR

        carga_fam = leew.consulta_lista('worker.db','id_f','carga_fam','id',self.idw)

        if len(carga_fam) == 0:
            pass
        else:
            contador_de_filas = 0
            header = self.tabla_carga_fam.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            self.tabla_carga_fam.setRowCount(len(carga_fam))
            for id_carca_fam in carga_fam:
                id_carca_fam = str(id_carca_fam)
                nombre = leew.consulta_gen('worker.db', 'nombre', 'carga_fam', 'id_f', '"' + id_carca_fam + '"')
                self.tabla_carga_fam.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(nombre))
                parentesco = leew.consulta_gen('worker.db', 'parentesco', 'carga_fam', 'id_f', '"' + id_carca_fam + '"')
                self.tabla_carga_fam.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(parentesco))
                fecha_nac = leew.consulta_gen('worker.db', 'fecha_nac', 'carga_fam', 'id_f',
                                               '"' + id_carca_fam + '"')
                self.tabla_carga_fam.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(str(fecha_nac)))
                doc_id = leew.consulta_gen('worker.db', 'doc_id', 'carga_fam', 'id_f',
                                              '"' + id_carca_fam + '"')
                self.tabla_carga_fam.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem(str(doc_id)))
                telf = leew.consulta_gen('worker.db', 'telefono', 'carga_fam', 'id_f',
                                           '"' + id_carca_fam + '"')
                self.tabla_carga_fam.setItem(contador_de_filas, 4, QtWidgets.QTableWidgetItem(str(telf)))
                contador_de_filas = contador_de_filas + 1


        # DIRECCION
        self.direccion_hab.setPlainText(leew.consulta_gen('worker.db', 'Direccion', 'info','id', self.idw))
        # Numero de la cuenta. En la BD es Int
        self.num_cuenta.setText(str(leew.consulta_gen('worker.db', 'num_c', 'info','id', self.idw)))
        # Banco de la cuenta
        self.banco.setText(leew.consulta_gen('worker.db', 'Banco', 'info','id', self.idw))
        # Tipo de cuenta
        self.tipo_cuenta.setText(leew.consulta_gen('worker.db', 'tipo_cuenta', 'info','id', self.idw))
        # Email
        self.correo_e.setText(leew.consulta_gen('worker.db', 'email', 'info','id', self.idw))
        # Talla camisa
        self.talla_camisa.setText(leew.consulta_gen('worker.db', 'talla_camisa', 'info','id', self.idw))
        # Talla pantalon
        self.talla_pantalon.setText(leew.consulta_gen('worker.db', 'talla_pantalon', 'info','id', self.idw))
        # Talla Zapatos
        self.talla_zap.setText(leew.consulta_gen('worker.db', 'talla_zapatos', 'info','id', self.idw))
        # Licencia numero
        self.lic_cond.setText(leew.consulta_gen('worker.db', 'lic_conducir', 'info','id', self.idw))
        fecha_vencimiento = leew.consulta_gen('worker.db', 'fecha_ven_lc', 'info', 'id', self.idw)
        dia, mes, ano = [int(n) for n in fecha_vencimiento.split('-')]
        # print(type(dia), type(mes), type(ano))
        self.fecha_venc_lic.setDate(QtCore.QDate(ano, mes, dia))
        # Estatus
        #self.estatus.setText(leew.consulta_gen('worker.db', 'Estatus', 'info', 'id', self.idw)) esto lo usba cuando era qlinedit
        self.estatus_combo.setDisabled(1)
        estatus_en_bd = leew.consulta_gen('worker.db', 'Estatus', 'info', 'id', self.idw)
        estatus = {'Activo': 0, 'Desincorporado': 1, 'Reposo': 2}
        self.estatus_combo.setCurrentIndex(estatus.get(estatus_en_bd))
        # SALARIO debe buscar en la tabla de salario
        cant_salarios = leew.tambd_par('worker.db', 'salario', self.idw)
        sal_vigente, = leew.consultaPS('worker.db', 'salario', 'salario', self.idw)
        self.salario_actual.setValue(sal_vigente) # float ojo
        self.salario_actual.setReadOnly(1)
        # Fecha ingreso
        fecha_ingreso = leew.consulta_gen('worker.db', 'Fecha_ingreso', 'info', 'id', self.idw)
        dia, mes, ano = [int(n) for n in fecha_ingreso.split('-')]
        self.fecha_ing.setDate(QtCore.QDate(ano, mes, dia))
        # Fecha_egreso
        self.fecha_egreso.setReadOnly(1)
        fecha_egreso = leew.consulta_gen('worker.db', 'fecha_egreso', 'liquidacion', 'id_trab', self.idw)
        if fecha_egreso != None:

            dia, mes, ano = [int(n) for n in fecha_egreso.split('-')]
            self.fecha_egreso.setDate(QtCore.QDate(ano, mes, dia))
            hoy = date(ano,mes,dia) # para calcular anos de servicio, no es la fecha actual sino la retiro en date type
        else:
            #cada dia es la posible fecha de egreso
            self.fecha_egreso.setDate(QtCore.QDate.currentDate()) # para mostrar la fecha de hoy
            hoy = date.today() # para calcular con la fecha de hoy
        # Inasistencias
        cant_insistencias = leew.tambd_par('worker.db', 'inasis', self.idw)
        self.inasistencias.setText(str(cant_insistencias))
        self.inasistencias.setReadOnly(1)
        # años de servicio es la resta entre fecha de ingreso y la de egreso.
        fecha_ingreso = leew.consulta_gen('worker.db', 'fecha_ingreso', 'info', 'id', self.idw)
        dia, mes, anio = [int(v) for v in fecha_ingreso.split("-")]
        fecha_ing_datetype = date(anio, mes, dia)
        anos_serv = str(trat_fecha.calcular_ano_f(fecha_ing_datetype,hoy))
        #print(anos_serv)
        self.ano_servicios.setText(anos_serv)
        self.ano_servicios.setReadOnly(1)
        # NOTA
        self.notas.setPlainText(leew.consulta_gen('worker.db', 'Notas', 'info', 'id', self.idw))
        # Cargo
        self.cargo.setText(leew.consulta_gen('worker.db', 'cargo', 'info', 'id', self.idw))
        #tipo de nomina
        tipo_nomina_en_bd = leew.consulta_gen('worker.db', 'tipo_de_nomina', 'info', 'id', self.idw)
        tipos_de_nominas = {'Producción': 0, 'Administración': 1}
        self.tipo_nomina.setCurrentIndex(tipos_de_nominas.get(tipo_nomina_en_bd))
        # Seguro
        self.emp_seguros.setText(leew.consulta_gen('worker.db', 'seguro', 'info', 'id', self.idw))
        # Número de Seguro
        self.num_carnet_seg.setText(leew.consulta_gen('worker.db', 'num_seguro', 'info', 'id', self.idw))
        # Clave de nomina TSS
        self.clave_nomina.setText(leew.consulta_gen('worker.db', 'clave_de_nomina', 'info', 'id', self.idw))
        # Tipo de ingreso
        self.tipo_ingreso.setCurrentText(leew.consulta_gen('worker.db', 'tipo_de_ingreso', 'info', 'id', self.idw))
        # Tipo de persona
        self.tipo_de_persona.setCurrentText(leew.consulta_gen('worker.db', 'tipo_de_persona', 'info', 'id', self.idw))
        # Fecha primera dosis:
        fecha_pri_dosis = leew.consulta_gen('worker.db', 'era_vac', 'info', 'id', self.idw)
        dia, mes, ano = [int(n) for n in fecha_pri_dosis.split('-')]
        self.primera_vac_2.setDate(QtCore.QDate(ano, mes, dia))
        # Fecha segunda dosis:
        fecha_sda_dosis = leew.consulta_gen('worker.db', 'sda_vac', 'info', 'id', self.idw)
        dia, mes, ano = [int(n) for n in fecha_sda_dosis.split('-')]
        self.seg_vac_2.setDate(QtCore.QDate(ano, mes, dia))
        # Fecha tercera dosis:
        fecha_terc_dosis = leew.consulta_gen('worker.db', 'terc_vac', 'info', 'id', self.idw)
        dia, mes, ano = [int(n) for n in fecha_terc_dosis.split('-')]
        self.tercera_vac_2.setDate(QtCore.QDate(ano, mes, dia))
        # Foto carnet:
        self.ruta_foto_enBD = leew.consulta_gen('worker.db', 'foto_en_trab', 'info', 'id', self.idw)
        #print(ruta_foto_trab)
        if os.path.isfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{self.ruta_foto_enBD}'): # con este verifico que el trabajador tenga asignado foto
            pixmap = QtGui.QPixmap(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{self.ruta_foto_enBD}')
            alto_foto = pixmap.size().height()
            ancho_foto = pixmap.size().width()
            ratio = alto_foto / ancho_foto
            ancho_forzado = 100 # ancho que queda bien en pantalla
            alto_calculado = int(ancho_forzado * ratio)
            scaled = pixmap.scaled(ancho_forzado,alto_calculado,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
            #print(scaled)
            #scaledPix = self.pixmap.scaled(QtCore.QSize(100,200), QtCore.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            self.foto.setPixmap(scaled)
        # Foto cedula:
        self.ruta_cedula_enBD = leew.consulta_gen('worker.db', 'scan_cedula', 'info', 'id', self.idw)
        print(self.ruta_cedula_enBD)
        if os.path.isfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{self.ruta_cedula_enBD}'): # este funcion devuelve true or false
            pixmap_ced = QtGui.QPixmap(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{self.ruta_cedula_enBD}')
            alto_foto = pixmap_ced.size().height()
            ancho_foto = pixmap_ced.size().width()
            ratio = alto_foto / ancho_foto
            ancho_forzado = 240  # ancho que queda bien en pantalla
            alto_calculado = int(ancho_forzado * ratio)
            scaled_ced = pixmap_ced.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
            # print(scaled)
            # scaledPix = self.pixmap.scaled(QtCore.QSize(100,200), QtCore.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            self.cedula.setPixmap(scaled_ced)
        # DOTACIONES
        # Llenando las filas

        try:  # para atrapar una BD de vacia
            dotaciones_por_trab = leew.consulta_lista('worker.db', 'id', 'dotacion', 'id_trab', self.idw)
        except:
            dotaciones_por_trab = 0
        #rint(dotaciones_por_trab)
        self.table_dotacion.setRowCount(len(dotaciones_por_trab))

        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla de dotaciones
        header = self.table_dotacion.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        contador_de_filas = 0
        for id_dotacion in dotaciones_por_trab:
            id_dotacion = str(id_dotacion)
            self.table_dotacion.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(id_dotacion))
            fecha = leew.consulta_gen('worker.db', 'fecha', 'dotacion', 'id', '"' + id_dotacion + '"')
            self.table_dotacion.setItem(contador_de_filas,1,QtWidgets.QTableWidgetItem(fecha))
            camisas = str(leew.consulta_gen('worker.db', 'cant_camisas', 'dotacion', 'id', '"' + id_dotacion + '"'))
            pant = str(leew.consulta_gen('worker.db', 'cant_pantalones', 'dotacion', 'id', '"' + id_dotacion + '"'))
            zap = str(leew.consulta_gen('worker.db', 'zapatos', 'dotacion', 'id', '"' + id_dotacion + '"'))
            lent = str(leew.consulta_gen('worker.db', 'lentes', 'dotacion', 'id', '"' + id_dotacion + '"'))
            guantes = str(leew.consulta_gen('worker.db', 'guantes', 'dotacion', 'id', '"' + id_dotacion + '"'))
            dotacion = f'Camisas:  {camisas}, Pantalones:  {pant} , Zapatos:  {zap} , Lentes: {lent}, Guantes: {guantes}'
            #print(dotacion)
            self.table_dotacion.setItem(contador_de_filas,2,QtWidgets.QTableWidgetItem(dotacion))
            contador_de_filas = contador_de_filas + 1

        # historico de salarios
        contador_de_filas = 0
        id_salario_por_trab = leew.consulta_lista('worker.db','id_sal','salario','id',self.idw)

        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla de dotaciones
        header = self.tabla_hist_salario.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.tabla_hist_salario.setRowCount(len(id_salario_por_trab))
        for id_sal in id_salario_por_trab:
            id_sal = str(id_sal)
            fecha = leew.consulta_gen('worker.db','fecha','salario','id_sal',id_sal)
            self.tabla_hist_salario.setItem(contador_de_filas,0,QtWidgets.QTableWidgetItem(fecha))
            monto = leew.consulta_gen('worker.db', 'salario', 'salario', 'id_sal', id_sal)
            self.tabla_hist_salario.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(str(monto)))
            status = leew.consulta_gen('worker.db', 'status', 'salario', 'id_sal', id_sal)
            self.tabla_hist_salario.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(status))
            nota = leew.consulta_gen('worker.db', 'nota', 'salario', 'id_sal', id_sal)
            self.tabla_hist_salario.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem(nota))
            contador_de_filas = contador_de_filas + 1

        # historico de horas extra
        contador_de_filas = 0
        id_hora_extra_por_trab = leew.consulta_lista('worker.db', 'id_h', 'horas_extras', 'id', self.idw + ' and computado = "1"')
        #print(id_hora_extra_por_trab)
        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla de dotaciones
        header = self.tabla_h_extra.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        self.tabla_h_extra.setRowCount(len(id_hora_extra_por_trab))
        for id_h in id_hora_extra_por_trab:
            id_h = str(id_h)
            fecha = leew.consulta_gen('worker.db', 'fecha', 'horas_extras', 'id_h', id_h)
            self.tabla_h_extra.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(fecha))
            hora_i = leew.consulta_gen('worker.db', 'hora_i', 'horas_extras', 'id_h', id_h)
            self.tabla_h_extra.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(hora_i))
            hora_f = leew.consulta_gen('worker.db', 'hora_f', 'horas_extras', 'id_h', id_h)
            self.tabla_h_extra.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(hora_f))
            horas = leew.consulta_gen('worker.db', 'horas', 'horas_extras', 'id_h', id_h)
            self.tabla_h_extra.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem(str(horas)))
            nota = leew.consulta_gen('worker.db', 'nota', 'horas_extras', 'id_h', id_h)
            self.tabla_h_extra.setItem(contador_de_filas, 4, QtWidgets.QTableWidgetItem(nota))
            tipo = leew.consulta_gen('worker.db', 'tipo', 'horas_extras', 'id_h', id_h)
            self.tabla_h_extra.setItem(contador_de_filas, 5, QtWidgets.QTableWidgetItem(tipo))
            contador_de_filas = contador_de_filas + 1

        # historico inasistencia
        contador_de_filas = 0
        id_inasis_trab = leew.consulta_lista('worker.db', 'id_i', 'inasis', 'id', self.idw + ' and computado = "1"')
        #print(id_inasis_trab)
        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla
        header = self.tabla_inasis.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        self.tabla_inasis.setRowCount(len(id_inasis_trab))
        for id_i in id_inasis_trab:
            id_i = str(id_i)
            fecha_i = leew.consulta_gen('worker.db', 'fecha_i', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(fecha_i))
            hora_i = leew.consulta_gen('worker.db', 'hora_i', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(hora_i))
            fecha_f = leew.consulta_gen('worker.db', 'fecha_f', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(fecha_f))
            hora_f = leew.consulta_gen('worker.db', 'hora_f', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem(hora_f))
            tipo = leew.consulta_gen('worker.db', 'tipo', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 4, QtWidgets.QTableWidgetItem(tipo))
            horas = leew.consulta_gen('worker.db', 'dias', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 5, QtWidgets.QTableWidgetItem(str(horas)))
            nota = leew.consulta_gen('worker.db', 'nota', 'inasis', 'id_i', id_i)
            self.tabla_inasis.setItem(contador_de_filas, 6, QtWidgets.QTableWidgetItem(nota))
            contador_de_filas = contador_de_filas + 1

        # historico part en los beneficios
        contador_de_filas = 0
        idn_part_ben_trab = leew.consulta_lista('worker.db', 'idn', 'nomina_beneficios', 'idt', f'"{self.idw}"')
        # print(id_inasis_trab)
        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla
        header = self.tabla_part_beneficios.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeToContents)

        self.tabla_part_beneficios.setRowCount(len(idn_part_ben_trab))
        for idn in idn_part_ben_trab:
            idn = str(idn)
            item = leew.consulta_gen('worker.db', 'idp_fiscal', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'fecha_doc', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'monto_utilidades', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem("{:,.2f}".format(item)))
            item = leew.consulta_gen('worker.db', 'porcentaje', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem("{:,.2f}".format(item)))
            item = leew.consulta_gen('worker.db', 'total_a_repartir', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 4, QtWidgets.QTableWidgetItem("{:,.2f}".format(item)))
            item = leew.consulta_gen('worker.db', 'salario_mensual', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 5, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'salario_diario', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 6, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'tiempo_trabajado', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 7, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'cant_dias', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 8, QtWidgets.QTableWidgetItem(str(item)))
            item = leew.consulta_gen('worker.db', 'monto_ajustado', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 9, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'ret_infotep', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 10, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'ret_islr', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 11, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'total_pagado', 'nomina_beneficios', 'idn', idn)
            self.tabla_part_beneficios.setItem(contador_de_filas, 12, QtWidgets.QTableWidgetItem(item))
            contador_de_filas = contador_de_filas + 1

        # Pestania Costos

        self.salario_mensual_costos.setValue(self.salario_actual.value())

        tasa_afp = leew.consulta_gen('worker.db', 'afp_emp', 'legales', 'status', '"Vigente"')

        self.afp_costos.setValue(self.salario_actual.value() * tasa_afp)

        tasa_sfs = leew.consulta_gen('worker.db', 'sfs_emp', 'legales', 'status', '"Vigente"')

        self.sfs_costos.setValue(self.salario_actual.value() * tasa_sfs)

        tasa_srl = leew.consulta_gen('worker.db', 'srl', 'legales', 'status', '"Vigente"')

        self.srl_costos.setValue(self.salario_actual.value() * tasa_srl)

        tasa_infotep = leew.consulta_gen('worker.db', 'infotep', 'legales', 'status', '"Vigente"')

        self.infotep_costos.setValue(self.salario_actual.value() * tasa_infotep)

        self.total_costos.setValue(
            self.salario_mensual_costos.value() + self.afp_costos.value() + self.sfs_costos.value() +
            self.srl_costos.value() + self.infotep_costos.value())

        # Pestania costos - resumen de nominas

        recibos = leew.consulta_lista('worker.db','ID_NOM','nomina','ID_TRABAJADOR',self.idw)
        #print(recibos)

        self.tabla_nomina.setRowCount(len(recibos))
        contador_de_filas = 0
        for recibo in recibos:
            recibo = str(recibo)
            #fecha_i = leew.consulta_gen('worker.db', 'fecha_i', 'inasis', 'id_i', id_i)
            self.tabla_nomina.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(recibo))
            periodo = leew.consulta_gen('worker.db','PERIODO', 'nomina', 'ID_NOM',f'"{recibo}"')
            self.tabla_nomina.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(periodo))
            salario = leew.consulta_gen('worker.db', 'SALARIO_QUINCENA', 'nomina', 'ID_NOM', f'"{recibo}"')
            #print(salario)
            if salario == None:
                salario = 0
            otras_remun = leew.consulta_gen('worker.db', 'OTRAS_REMUN', 'nomina', 'ID_NOM', f'"{recibo}"')
            if otras_remun == None:
                otras_remun = 0
            frac_vac = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'ID_NOM', f'"{recibo}"')
            if frac_vac == None:
                frac_vac = 0
            pago_adi_vac = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'ID_NOM', f'"{recibo}"')
            if pago_adi_vac == None:
                pago_adi_vac = 0
            pago_adel_vac = leew.consulta_gen('worker.db', 'PAGO_ADELANTADO', 'nomina', 'ID_NOM', f'"{recibo}"')
            if pago_adel_vac == None:
                pago_adel_vac = 0
            horas_extra = leew.consulta_gen('worker.db', 'HORAS_EXTRA', 'nomina', 'ID_NOM', f'"{recibo}"')
            if horas_extra == None:
                horas_extra = 0
            sal_navidad = leew.consulta_gen('worker.db', 'SALARIO_DE_NAV', 'nomina', 'ID_NOM', f'"{recibo}"')
            if sal_navidad == None:
                sal_navidad = 0
            pagos = salario + otras_remun + frac_vac + pago_adi_vac + horas_extra + sal_navidad
            #print(pagos)
            self.tabla_nomina.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(pagos))))

            afp_trab = leew.consulta_gen('worker.db', 'AFP_TRAB', 'nomina', 'ID_NOM', f'"{recibo}"')
            if afp_trab == None:
                afp_trab = 0
            sfs_trab = leew.consulta_gen('worker.db', 'SFS_TRAB', 'nomina', 'ID_NOM', f'"{recibo}"')
            if sfs_trab == None:
                sfs_trab = 0
            ret_irlr = leew.consulta_gen('worker.db', 'ISLR_RETENCION', 'nomina', 'ID_NOM', f'"{recibo}"')
            if ret_irlr == None:
                ret_irlr = 0
            inas = leew.consulta_gen('worker.db', 'INASIS', 'nomina', 'ID_NOM', f'"{recibo}"')
            if inas == None:
                inas = 0
            pago_vac_adel_per_ant = leew.consulta_gen('worker.db', 'PAGO_AD_PER_ANT', 'nomina', 'ID_NOM', f'"{recibo}"')
            if pago_vac_adel_per_ant == None:
                pago_vac_adel_per_ant = 0
            descuentos = afp_trab + sfs_trab + ret_irlr + inas
            self.tabla_nomina.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(descuentos))))
            total_pagado = pagos - descuentos
            self.tabla_nomina.setItem(contador_de_filas, 4, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(total_pagado))))
            contador_de_filas = contador_de_filas + 1

        # pestania Vacaciones

        idies_vacaciones = leew.consulta_lista('worker.db', 'ID_V', 'nomina', 'ID_TRABAJADOR', f'{self.idw} AND ID_V > "0"')
        #print(idies_vacaciones)
        self.tabla_resumen_vac.setRowCount(len(idies_vacaciones))

        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla de dotaciones
        header = self.tabla_resumen_vac.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)

        contador_de_filas = 0
        for id_v in idies_vacaciones:
            id_v = str(id_v)
            self.tabla_resumen_vac.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(id_v))
            fecha_i_vac = leew.consulta_gen('worker.db', 'FECHA_INICIO_VAC', 'nomina', 'ID_TRABAJADOR',
                                            f'{self.idw} AND ID_V = "{id_v}"')
            self.tabla_resumen_vac.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(fecha_i_vac))
            fecha_f_vac = leew.consulta_gen('worker.db', 'FECHA_FIN_VAC', 'nomina', 'ID_TRABAJADOR',
                                            f'{self.idw} AND ID_V = "{id_v}"')
            self.tabla_resumen_vac.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(fecha_f_vac))
            cant_dias = leew.consulta_gen('worker.db', 'dias', 'vacaciones', 'indice',
                                            f'"{id_v}"')
            self.tabla_resumen_vac.setItem(contador_de_filas, 3, QtWidgets.QTableWidgetItem(cant_dias))
            pag_art177_1er = leew.consulta_gen('worker.db', 'FRACCION_VAC', 'nomina', 'ID_TRABAJADOR',
                                            f'{self.idw} AND ID_V = "{id_v}"')
            self.tabla_resumen_vac.setItem(contador_de_filas, 4,
                                           QtWidgets.QTableWidgetItem(str("{:,.2f}".format(pag_art177_1er))))
            pag_art177_2do = leew.consulta_gen('worker.db', 'PAGO_DE_VAC', 'nomina', 'ID_TRABAJADOR',
                                               f'{self.idw} AND ID_V = "{id_v}"')
            self.tabla_resumen_vac.setItem(contador_de_filas, 5,
                                           QtWidgets.QTableWidgetItem(str("{:,.2f}".format(pag_art177_2do))))
            total_vac_pagadas = pag_art177_1er + pag_art177_2do
            self.tabla_resumen_vac.setItem(contador_de_filas, 6,
                                           QtWidgets.QTableWidgetItem(str("{:,.2f}".format(total_vac_pagadas))))
            salario_vac = leew.consulta_gen('worker.db', 'SALARIO', 'nomina', 'ID_TRABAJADOR',
                                               f'{self.idw} AND ID_V = "{id_v}"')
            self.tabla_resumen_vac.setItem(contador_de_filas, 7,
                                           QtWidgets.QTableWidgetItem(str("{:,.2f}".format(salario_vac))))
            contador_de_filas += 1


        # pestania retiro INICIO

        consulta = leew.consulta_gen('worker.db', 'fecha_egreso', 'liquidacion', 'id_trab', self.idw)

        # fecha de retiro
        if consulta == None:
            pass
            self.fecha_retiro.setDate(QtCore.QDate.currentDate())
        else:
            consulta = str(consulta)
            dia, mes, anio, = [int(n) for n in consulta.split('-')]
            self.fecha_retiro.setDate(QtCore.QDate(anio,mes,dia))

        # tipo liquidacion rt 82
        consulta = leew.consulta_gen('worker.db','art82','liquidacion','id_trab', self.idw)
        if consulta == 'False':
            self.art82.setText('No')
        elif consulta == 'True':
            self.art82.setText('Sí')
        else:
            self.art82.setText('')

        # tiempo trabajado
        consulta = leew.consulta_gen('worker.db', 'tiempo_lab', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.tiempo_lab.setText(consulta)
        else:
            self.tiempo_lab.setText('')

        # suma de salario

        consulta = leew.consulta_gen('worker.db', 'sum_sal', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.sum_salario.setText(str("{:,.2f}".format(consulta)))
        else:
            self.sum_salario.setText('')

        # sal promedio mensual
        consulta = leew.consulta_gen('worker.db', 'sal_prom_mes', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.sal_prom_mes.setText(str("{:,.2f}".format(consulta)))
        else:
            self.sal_prom_mes.setText('')

        # sal promedio diario
        consulta = leew.consulta_gen('worker.db', 'sal_prom_dia', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.saldo_prom_diario.setText(str("{:,.2f}".format(consulta)))
        else:
            self.saldo_prom_diario.setText('')

        # fue pre avisado?
        consulta = leew.consulta_gen('worker.db', 'pre_aviso', 'liquidacion', 'id_trab', self.idw)
        if consulta == 'False':
            self.fue_preavisado.setText('No')
        elif consulta == 'True':
            self.fue_preavisado.setText('Sí')
        else:
            self.fue_preavisado.setText('')

        # monto pagado preaviso
        consulta = leew.consulta_gen('worker.db', 'monto_pre_aviso', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.monto_preaviso.setText(str("{:,.2f}".format(consulta)))
        else:
            self.monto_preaviso.setText('')

        # dias pagado preaviso
        consulta = leew.consulta_gen('worker.db', 'dias_pre_aviso', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.dias_preaviso.setText(consulta)
        else:
            self.dias_preaviso.setText('')

        # se pago cesantia?
        consulta = leew.consulta_gen('worker.db', 'cesantia', 'liquidacion', 'id_trab', self.idw)
        if consulta == 'False':
            self.pago_cesantia.setText('No')
        elif consulta == 'True':
            self.pago_cesantia.setText('Sí')
        else:
            self.pago_cesantia.setText('')

        # monto de censantia
        consulta = leew.consulta_gen('worker.db', 'cesantia_monto', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.monto_cesantia.setText(str("{:,.2f}".format(consulta)))
        else:
            self.monto_cesantia.setText('')

        # dias pagado preaviso
        consulta = leew.consulta_gen('worker.db', 'cesantia_dias', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.dias_cesantia.setText(consulta)
        else:
            self.dias_cesantia.setText('')

        # se pago vacaciones?
        consulta = leew.consulta_gen('worker.db', 'vac', 'liquidacion', 'id_trab', self.idw)
        if consulta == 'False':
            self.vac_pre_12_meses.setText('No')
        elif consulta == 'True':
            self.vac_pre_12_meses.setText('Sí')
        else:
            self.vac_pre_12_meses.setText('')

        # monto de vacaciones
        consulta = leew.consulta_gen('worker.db', 'vac_monto', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.monto_vac.setText(str("{:,.2f}".format(consulta)))
        else:
            self.monto_vac.setText('')

        # dias pagado vacaciones
        consulta = leew.consulta_gen('worker.db', 'vac_dias', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.dias_vac.setText(consulta)
        else:
            self.dias_vac.setText('')

        # se pago salario de navidad?
        consulta = leew.consulta_gen('worker.db', 'sal_nav', 'liquidacion', 'id_trab', self.idw)
        if consulta == 'False':
            self.sal_nav.setText('No')
        elif consulta == 'True':
            self.sal_nav.setText('Sí')
        else:
            self.sal_nav.setText('')

        # monto salario nav
        consulta = leew.consulta_gen('worker.db', 'sal_nav_monto', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.monto_sal_nav.setText(str("{:,.2f}".format(consulta)))
        else:
            self.monto_sal_nav.setText('')

        # dias pagado sal nav
        consulta = leew.consulta_gen('worker.db', 'sal_nav_dias', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.dias_sal_nav.setText(consulta)
        else:
            self.dias_sal_nav.setText('')

        # monto bono
        consulta = leew.consulta_gen('worker.db', 'bono_monto', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.monto_bono.setText(str("{:,.2f}".format(consulta)))
        else:
            self.monto_bono.setText('')

        # monto total liquidacion
        consulta = leew.consulta_gen('worker.db', 'total_liq', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.total_liquidacion.setText(str("{:,.2f}".format(consulta)))
        else:
            self.total_liquidacion.setText('')

        # nota liquidacion
        consulta = leew.consulta_gen('worker.db', 'nota', 'liquidacion', 'id_trab', self.idw)
        if consulta != None:
            self.nota_liquidacion.setPlainText(consulta)
        else:
            self.nota_liquidacion.setPlainText('')

        # pestania retiro LEGALES

        ret_tss = leew.consulta_gen('worker.db','ret_tss','info','id',self.idw)
        self.ret_tss.setChecked(ret_tss)
        ret_infotep = leew.consulta_gen('worker.db', 'ret_infotep', 'info', 'id', self.idw)
        self.ret_infotep.setChecked(ret_infotep)
        ret_isr = leew.consulta_gen('worker.db', 'ret_isr', 'info', 'id', self.idw)
        self.ret_isr.setChecked(ret_isr)
        calc_sal_nav = leew.consulta_gen('worker.db', 'calc_sal_navidad', 'info', 'id', self.idw)
        self.calc_sal_navidad.setChecked(calc_sal_nav)
        self.saldo_a_favor.setValue(leew.consulta_gen('worker.db', 'saldo_a_favor', 'info', 'id', self.idw))
        # abajo esta comentado porque ya no se usa el valor guardado en la BD hasta que la tss cambie de idea
        # self.rnc_agente_ret.setText(leew.consulta_gen('worker.db', 'rnc_agente', 'info', 'id', self.idw))
        self.aporte_vol_empresa.setValue(leew.consulta_gen('worker.db', 'aporte_vol_emp', 'info', 'id', self.idw))
        self.aporte_vol_trabajador.setValue(leew.consulta_gen('worker.db', 'aporte_vol_trab', 'info', 'id', self.idw))
        self.retencion_pension.setValue(leew.consulta_gen('worker.db', 'retencion_pension', 'info', 'id', self.idw))


        # pestania adelantos / prestamos

        lista_id_prestamos = leew.consulta_lista('worker.db', 'idp', 'prestamos', 'idt', self.idw)
        n = len(lista_id_prestamos)
        self.tabla_adelantos.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tabla_adelantos.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

        cont = 0
        for id_prestamo in lista_id_prestamos:
            id_prestamo = str(id_prestamo)
            item = id_prestamo
            self.tabla_adelantos.setItem(cont, 0, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'fecha', 'prestamos', 'idp', id_prestamo)
            self.tabla_adelantos.setItem(cont, 1, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'monto', 'prestamos', 'idp', id_prestamo))
            self.tabla_adelantos.setItem(cont, 2, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'cuotas', 'prestamos', 'idp', id_prestamo))
            self.tabla_adelantos.setItem(cont, 3, QtWidgets.QTableWidgetItem(item))
            monto_cuota = leew.consulta_gen('worker.db', 'monto_cuotas', 'prestamos', 'idp', id_prestamo)
            self.tabla_adelantos.setItem(cont, 4, QtWidgets.QTableWidgetItem(str(monto_cuota)))
            item = leew.consulta_gen('worker.db', 'estatus', 'prestamos', 'idp', id_prestamo)
            self.tabla_adelantos.setItem(cont, 5, QtWidgets.QTableWidgetItem(item))
            cat_cuotas_pend = len(leew.consulta_lista('worker.db', 'idc', 'prestamos_detalles', 'idp',
                                                      f'"{id_prestamo}" and estatus = "pendiente"'))
            self.tabla_adelantos.setItem(cont, 6, QtWidgets.QTableWidgetItem(str(cat_cuotas_pend)))
            monto_pendiente = round(cat_cuotas_pend * monto_cuota, 2)  # redondeo a 2 decimales
            self.tabla_adelantos.setItem(cont, 7, QtWidgets.QTableWidgetItem(str(monto_pendiente)))
            item = str(leew.consulta_gen('worker.db', 'nota', 'prestamos', 'idp', id_prestamo))
            self.tabla_adelantos.setItem(cont, 8, QtWidgets.QTableWidgetItem(item))
            cont = cont + 1

    def guardar_info(self):
        texto = ""
        # abqjo vuelvo un cojunto (set en ingles) para quitar elementos repetidos
        self.conjunto_de_modificaciones = set(self.listado_de_modificaciones)
        for modificacion in self.conjunto_de_modificaciones:
            texto = f"{modificacion}, " + texto

        texto = f"¿Desea confirmar la modificación de los siguientes campos?:\n{texto}"
        texto = texto[0:len(texto) - 2] + "." # esto para eliminar la ultima coma y poner un punto (.)
        reply = QtWidgets.QMessageBox.question(self, "Conformación de moficaciones", texto
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.idw != "": # cuando es una edición de una ficha de un trabajador

                self.entrada = '"' + self.idw + '","' + self.nombre.text() + '","' + self.apellido.text() + '","' + self.seg_nombre.text() + \
                                '","' + self.seg_apellido.text() + '","' + self.fecha_nac.date().toString("dd-MM-yyyy") + '","' + self.sexo.currentText() + '","' + \
                                self.tipos_doc.get(self.tipo_doc.currentIndex()) + '","' + self.num_doc.text() + '","' + self.nacionalidad.currentText() + '","' + self.telf.text() + \
                                '","' + self.nivel_academico.currentText() + '","' + self.profesion.text() + '","' + self.direccion_hab.toPlainText() + '","' + self.banco.text() + \
                                '","' + self.num_cuenta.text() + '","' + self.correo_e.text() + '","' + self.fecha_ing.date().toString("dd-MM-yyyy") + '","' + \
                                self.notas.toPlainText() + '","' + self.estatus_combo.currentText() + '","' + 'NULL' + '","' + self.user + '","' + self.primera_vac_2.date().toString("dd-MM-yyyy") + '","' + \
                                self.seg_vac_2.date().toString("dd-MM-yyyy") + '","' + self.tercera_vac_2.date().toString("dd-MM-yyyy") + '","' + self.cargo.text() + '","' + self.tipo_cuenta.text() + '","' + \
                                self.emp_seguros.text() + '","' + self.num_carnet_seg.text() + '","' + self.talla_camisa.text() + '","' + self.talla_pantalon.text() \
                                + '","' + self.talla_zap.text() + '","' + self.lic_cond.text() + '","' + self.fecha_venc_lic.date().toString("dd-MM-yyyy") + '","' + \
                                self.ruta_foto_enBD + '","' + self.ruta_cedula_enBD + '","' + str(self.ret_tss.checkState()) + '","' + str(self.ret_infotep.checkState()) +'","' + str(self.ret_isr.checkState()) + \
                                    '","' + str(self.calc_sal_navidad.checkState()) + '","' + self.tipo_nomina.currentText() + '","' + self.clave_nomina.text() + '","' + self.tipo_ingreso.currentText() + '","' + \
                                self.tipo_de_persona.currentText() + '","' + self.saldo_a_favor.text() + '","' + self.rnc_agente_ret.text() + '","' + self.aporte_vol_empresa.text() + '","' + self.aporte_vol_trabajador.text() + '","' + \
                                self.retencion_pension.text() + '"'
                print(self.entrada)
                leew.del_reg('info', self.idw)
                leew.introduce_info(self.entrada)
                # para la foto
                if self.se_edito_foto == 1:
                    os.system(self.cmd_guarda_foto)
                # para la cedula
                if self.se_edito_cedula == 1:
                    os.system(self.cmd_guarda_cedula)

                # para actualizar la bd de carga familiar
                self.actualizar_bd_carga_fam(self.idw)

                self.listado_de_modificaciones = [] # para que no muestre mensaje de que falta algo

                self.close()
                QtWidgets.QMessageBox.information(self, "Aviso", "Se han grabado las modificaciones satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                try:
                    self.refrescar_tabla_list_trab() # refresco la tabla del listado de trabajadores
                except:
                    pass # esto es por si cierran el listado que se trata de actualizar
            else: # cuando es un trabajador nuevo

                confirma = self.confirma_datos_basicos()
                #print(confirma)
                if confirma == 1:
                    self.entrada = 'NULL,"' + self.nombre.text() + '","' + self.apellido.text() + '","' + self.seg_nombre.text() + '","' + self.seg_apellido.text() + '","' + self.fecha_nac.date().toString("dd-MM-yyyy") + '","' + self.sexo.currentText() + '","' + self.tipos_doc.get(self.tipo_doc.currentIndex()) + '","' + self.num_doc.text() \
                                    + '","' + self.nacionalidad.currentText() + '","' + self.telf.text() + '","' + self.nivel_academico.currentText() + '","' + self.profesion.text() + '","' + self.direccion_hab.toPlainText() + '","' + self.banco.text() + '","' + self.num_cuenta.text() + '","' + self.correo_e.text() + \
                                    '","' + self.fecha_ing.date().toString("dd-MM-yyyy") + '","' + self.notas.toPlainText() + '",' + '"Activo","' + 'NULL' + '","' + self.user + '","' + self.primera_vac_2.date().toString("dd-MM-yyyy") + '","' + \
                                    self.seg_vac_2.date().toString("dd-MM-yyyy") + '","' + self.tercera_vac_2.date().toString("dd-MM-yyyy") + '","' + self.cargo.text() + '","' + self.tipo_cuenta.text() + '","' + \
                                    self.emp_seguros.text() + '","' + self.num_carnet_seg.text() + '","' + self.talla_camisa.text() + '","' + self.talla_pantalon.text() \
                                    + '","' + self.talla_zap.text() + '","' + self.lic_cond.text() + '","' + self.fecha_venc_lic.date().toString("dd-MM-yyyy") + '","' + \
                                    self.ruta_foto_enBD + '","' + self.ruta_cedula_enBD + '","' + str(self.ret_tss.checkState()) + '","' + str(self.ret_infotep.checkState()) +'","' + str(self.ret_isr.checkState()) + \
                                    '","' + str(self.calc_sal_navidad.checkState()) + '","' + self.tipo_nomina.currentText() + '","' + self.clave_nomina.text() + '","' + self.tipo_ingreso.currentText() + '","' + \
                                    self.tipo_de_persona.currentText() + '","' + self.saldo_a_favor.text() + '","' + self.rnc_agente_ret.text() + '","' + self.aporte_vol_empresa.text() + '","' + self.aporte_vol_trabajador.text() + '","' + \
                                    self.retencion_pension.text() + '"'

                    #print(self.entrada)
                    leew.introduce_info(self.entrada)
                    # para la foto
                    if self.se_edito_foto == 1:
                        os.system(self.cmd_guarda_foto)
                    # para la cedula
                    if self.se_edito_cedula == 1:
                        os.system(self.cmd_guarda_cedula)

                    # para actualizar el salario
                    self.idw = str(leew.consulta_gen('worker.db','max(id)','info','id>', '0')) # con esta consulta saco el ultimo id
                    entrada_salario = f"'{self.idw}','{self.fecha_ing.date().toString('dd-MM-yyyy')}','{self.salario_actual.text()}','Vigente',NULL,'SALARIO INICIAL'"
                    print(entrada_salario)
                    leew.introduce_gen('worker.db','salario',entrada_salario)

                    # para actualizar la bd de carga familiar
                    self.actualizar_bd_carga_fam(self.idw)

                    self.listado_de_modificaciones = []

                    self.close()

                    QtWidgets.QMessageBox.information(self, "Aviso", "Se ha creado el nuevo trabajador satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                    try:
                        self.refrescar_tabla_list_trab()  # refresco la tabla del listado de trabajadores
                    except:
                        pass  # esto es por si cierran el listado que se trata de actualizar

    def editar_foto_cmd(self):
        ruta_nueva_imagen = QtWidgets.QFileDialog.getOpenFileName(self,'','','*.png *.jpg')[0] #*.png *.svg*.jpg
        ruta_nueva_imagen = os.path.abspath(ruta_nueva_imagen) # pone la ruta tipo msdos requerido por os.system
        extencion_archivo = os.path.splitext(ruta_nueva_imagen)[1] # comando que da tupla con nom arch y su extencion separado
        #print(extencion_archivo)
        #print(ruta_nueva_imagen)
        #print(os.path.dirname(__file__))
        if  ruta_nueva_imagen != os.path.dirname(os.path.abspath(__file__)):
            #print(os.path.abspath(ruta_nueva_imagen))
            self.cmd_guarda_foto = f'copy  "{ruta_nueva_imagen}" "C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\img_trab\\foto_{self.idw}{extencion_archivo}"'
            #print(self.cmd_guarda_foto)
            self.ruta_foto_enBD = f'img_trab/foto_{self.idw}{extencion_archivo}' # se usará en guardar SQL
            #print(self.ruta_foto_enBD)
            #os.system(cmd_guarda_foto) # este comando debe ejecutarse solo si se le da al boton guardar

            pixmap = QtGui.QPixmap(ruta_nueva_imagen)
            alto_foto = pixmap.size().height()
            ancho_foto = pixmap.size().width()
            ratio = alto_foto / ancho_foto
            ancho_forzado = 100  # ancho que queda bien en pantalla
            alto_calculado = int(ancho_forzado * ratio)
            scaled = pixmap.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
            # print(scaled)
            self.foto.setPixmap(scaled)#scaled


            self.foto.setStyleSheet("background: #ffbcbd;") # para indicar al usuario que editó la foto con fodo rosado
            self.listado_de_modificaciones.append('Foto carnet') # para colocar la foto en la lista de cambios
            self.guarda.setDisabled(0) # activa boton guardar
            self.se_edito_foto = 1 # flag que dice que se edito la foto

    def editar_cedula_cmd(self):
        ruta_nueva_imagen = QtWidgets.QFileDialog.getOpenFileName(self, '', '', '*.png *.jpg')[0]  # *.png *.svg*.jpg
        ruta_nueva_imagen = os.path.abspath(ruta_nueva_imagen)  # pone la ruta tipo msdos requerido por os.system
        extencion_archivo = os.path.splitext(ruta_nueva_imagen)[
            1]  # comando que da tupla con nom arch y su extencion separado
        # print(extencion_archivo)
        # print(ruta_nueva_imagen)
        # print(os.path.dirname(__file__))
        if ruta_nueva_imagen != os.path.dirname(os.path.abspath(__file__)):
            # print(os.path.abspath(ruta_nueva_imagen))
            self.cmd_guarda_cedula = f'copy  "{ruta_nueva_imagen}" "C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\img_trab\\cedula_{self.idw}{extencion_archivo}"'
            #print(self.cmd_guarda_cedula)
            self.ruta_cedula_enBD = f'img_trab/cedula_{self.idw}{extencion_archivo}'  #  se usará en guardar SQL
            #print(self.ruta_cedula_enBD)
            # os.system(cmd_guarda_cedula) # este comando debe ejecutarse solo si se le da al boton guardar

            pixmap = QtGui.QPixmap(ruta_nueva_imagen)
            alto_foto = pixmap.size().height()
            ancho_foto = pixmap.size().width()
            ratio = alto_foto / ancho_foto
            ancho_forzado = 240  # ancho que queda bien en pantalla
            alto_calculado = int(ancho_forzado * ratio)
            scaled = pixmap.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
            # print(scaled)
            self.cedula.setPixmap(scaled)  # scaled

            self.cedula.setStyleSheet("background: #ffbcbd;")  # para indicar al usuario que editó la foto con fodo rosado
            self.listado_de_modificaciones.append('Imagen de la Cédula')  # para colocar la foto en la lista de cambios
            self.guarda.setDisabled(0)  # activa boton guardar
            self.se_edito_cedula = 1 # flag para guardar cedula en cmd_guradr

    def ver_foto_cmd(self):
        ruta_foto_trab = leew.consulta_gen('worker.db', 'foto_en_trab', 'info', 'id', self.idw)
        # print(ruta_foto_trab)
        if os.path.isfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{ruta_foto_trab}'):  # con este verifico que el trabajador tenga asignado foto
            webbrowser.open_new_tab(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\' +  ruta_foto_trab.replace('/','\\'))

    def ver_cedula_cmd(self):
        ruta_ced_trab = leew.consulta_gen('worker.db', 'scan_cedula', 'info', 'id', self.idw)
        # print(ruta_foto_trab)
        if os.path.isfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{ruta_ced_trab}'):  # con este verifico que el trabajador tenga asignado foto
            webbrowser.open_new_tab(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\' + ruta_ced_trab.replace('/','\\'))

    def imprime_dota_cmd(self):
        for currentQTableWidgetItem in self.table_dotacion.selectedItems():
            reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted imprimir la dotación : " + \
                                           currentQTableWidgetItem.text() + " con fecha "+ \
                                                   str(self.table_dotacion.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column() + 1).text()) + "?"
                                           , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    imp_dotacion.imprimir(currentQTableWidgetItem.text())
                    QtWidgets.QMessageBox.information(self, "Atención", "Dotación generada correctamente",
                                                      QtWidgets.QMessageBox.Ok)
                    self.imprime_dota.setDisabled(1)
                    self.borra_dota.setDisabled(1) # esto para que nada quede seleccionado
                except:
                    QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)
            break # esto se pone para que no siga iterando si se selecciona una fila y no una celda

    def on_click_dota(self):
        '''Funcion para hacer que siempres esté desactivado el boton de imprimir dotacion hasta que alguna esté seleccionada'''
        for currentQTableWidgetItem in self.table_dotacion.selectedItems():
            if currentQTableWidgetItem.column() == 0:
                self.imprime_dota.setDisabled(0)
                self.borra_dota.setDisabled(0)
                #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            else:
                self.imprime_dota.setDisabled(1)
                self.borra_dota.setDisabled(1)

    def borra_dota_cmd(self):
        for currentQTableWidgetItem in self.table_dotacion.selectedItems():
            reply = QtWidgets.QMessageBox.question(self, "Para continuar", "Desea usted borrar la dotación : " + \
                                           currentQTableWidgetItem.text() + " con fecha "+ \
                                                   str(self.table_dotacion.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column() + 1).text()) + "?. \nEsta operación es irreversible."
                                           , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    leew.del_gen('worker.db','dotacion','id',currentQTableWidgetItem.text())
                    QtWidgets.QMessageBox.information(self, "Atención", "Dotación borrada correctamente",
                                                      QtWidgets.QMessageBox.Ok)
                    self.borra_dota.setDisabled(1)
                    self.imprime_dota.setDisabled(1)
                    # Llenando las filas (refrescado de tabla INICIO)

                    try:  # para atrapar una BD de vacia
                        dotaciones_por_trab = leew.consulta_lista('worker.db', 'id', 'dotacion', 'id_trab', self.idw)
                    except:
                        dotaciones_por_trab = 0
                    # rint(dotaciones_por_trab)
                    self.table_dotacion.setRowCount(len(dotaciones_por_trab))

                    # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla de dotaciones
                    header = self.table_dotacion.horizontalHeader()
                    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

                    contador_de_filas = 0
                    for id_dotacion in dotaciones_por_trab:
                        id_dotacion = str(id_dotacion)
                        self.table_dotacion.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(id_dotacion))
                        fecha = leew.consulta_gen('worker.db', 'fecha', 'dotacion', 'id', '"' + id_dotacion + '"')
                        self.table_dotacion.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(fecha))
                        camisas = str(
                            leew.consulta_gen('worker.db', 'cant_camisas', 'dotacion', 'id', '"' + id_dotacion + '"'))
                        pant = str(leew.consulta_gen('worker.db', 'cant_pantalones', 'dotacion', 'id',
                                                     '"' + id_dotacion + '"'))
                        zap = str(leew.consulta_gen('worker.db', 'zapatos', 'dotacion', 'id', '"' + id_dotacion + '"'))
                        lent = str(leew.consulta_gen('worker.db', 'lentes', 'dotacion', 'id', '"' + id_dotacion + '"'))
                        guantes = str(
                            leew.consulta_gen('worker.db', 'guantes', 'dotacion', 'id', '"' + id_dotacion + '"'))
                        dotacion = f'Camisas:  {camisas}, Pantalones:  {pant} , Zapatos:  {zap} , Lentes: {lent}, Guantes: {guantes}'
                        # print(dotacion)
                        self.table_dotacion.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(dotacion))
                        contador_de_filas = contador_de_filas + 1
                    #(refrescado de tabla FIN)

                except:
                    QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)
            break # esto se pone para que no siga iterando si se selecciona una fila y no una celda

    def borra_carga_cmd(self):
        self.tabla_carga_fam.removeRow(self.tabla_carga_fam.currentRow())
        self.se_edito_tabla_carga_fam = 1

    def on_click_carga_fam(self):
        '''Funcion para hacer que  alguna esté seleccionada'''

        for currentQTableWidgetItem in self.tabla_carga_fam.selectedItems():
            if currentQTableWidgetItem.column() >= 0:
                self.borra_carga.setDisabled(0)

    def agregar_carga_cmd(self):
        if self.nombre_fam.text() != '' and self.parentesco.text() != '':
            cuenta = self.tabla_carga_fam.rowCount()
            self.tabla_carga_fam.insertRow(cuenta)
            self.tabla_carga_fam.setItem(cuenta, 0, QtWidgets.QTableWidgetItem(self.nombre_fam.text()))
            self.tabla_carga_fam.setItem(cuenta, 1, QtWidgets.QTableWidgetItem(self.parentesco.text()))
            self.tabla_carga_fam.setItem(cuenta, 2, QtWidgets.QTableWidgetItem(self.f_nac_fam.text()))
            self.tabla_carga_fam.setItem(cuenta, 3, QtWidgets.QTableWidgetItem(self.doc_fam.text()))
            self.tabla_carga_fam.setItem(cuenta, 4, QtWidgets.QTableWidgetItem(self.telf_fam.text()))
            self.nombre_fam.clear()
            self.parentesco.clear()
            self.f_nac_fam.setDate(QtCore.QDate(2000,1,1))
            self.doc_fam.clear()
            self.telf_fam.clear()
            self.se_edito_tabla_carga_fam = 1
        else:
            QtWidgets.QMessageBox.warning(self, "Falta Información",
                                          "Debe colocar el nombre completo y parentesco del familiar. Se recomienda que complete la información del familiar completamente",
                                          QtWidgets.QMessageBox.Ok)

    def disable_guardar(self):
        '''esta funcion debió llamarse enable guardar,pero como ya la usé mucho...'''
        self.guarda.setDisabled(0)
        if self.nombre.isModified(): # si el nombre es modificado
            self.listado_de_modificaciones.append('Nombre') # se agraga nombre a la lista de campos modificados
            self.nombre.setStyleSheet("background: #ffbcbd;") # le pongo fondo rosado
        if self.apellido.isModified():
            self.listado_de_modificaciones.append('Apellido')
            self.apellido.setStyleSheet("background: #ffbcbd;")
        if self.seg_nombre.isModified():
            self.listado_de_modificaciones.append('Segundo Nombre')
            self.seg_nombre.setStyleSheet("background: #ffbcbd;")
        if self.seg_apellido.isModified():
            self.listado_de_modificaciones.append('Segundo Apellido')
            self.seg_apellido.setStyleSheet("background: #ffbcbd;")
        if self.fecha_nac.hasFocus():
            self.listado_de_modificaciones.append('Fecha de Nacimiento')
            self.fecha_nac.setStyleSheet("background: #ffbcbd;")
        if self.sexo.hasFocus(): # se usa para combobox
            self.listado_de_modificaciones.append('Sexo')
            self.sexo.setStyleSheet("background: #ffbcbd;")
        if self.tipo_doc.hasFocus():
            self.listado_de_modificaciones.append('Tipo de documento')
            self.tipo_doc.setStyleSheet("background: #ffbcbd;")
        if self.num_doc.isModified():
            self.listado_de_modificaciones.append('Número de documento')
            self.num_doc.setStyleSheet("background: #ffbcbd;")
        if self.nacionalidad.hasFocus():
            self.listado_de_modificaciones.append('Nacionalidad')
            self.nacionalidad.setStyleSheet("background: #ffbcbd;")
        if self.telf.isModified():
            self.listado_de_modificaciones.append('Teléfono')
            self.telf.setStyleSheet("background: #ffbcbd;")
        if self.nivel_academico.hasFocus():
            self.listado_de_modificaciones.append('Nivel académico')
            self.nivel_academico.setStyleSheet("background: #ffbcbd;")
        if self.profesion.isModified():
            self.listado_de_modificaciones.append('Profesión')
            self.profesion.setStyleSheet("background: #ffbcbd;")
        if self.direccion_hab.hasFocus():
            self.listado_de_modificaciones.append('Dirección de Habitación')
            self.direccion_hab.setStyleSheet("background: #ffbcbd;")
        if self.borra_carga.hasFocus() or self.agrega_cargaf.hasFocus():
            self.listado_de_modificaciones.append('Carga familiar')
            self.tabla_carga_fam.setStyleSheet("background: #ffbcbd;")
        if self.num_cuenta.isModified():
            self.listado_de_modificaciones.append('Número de cuenta')
            self.num_cuenta.setStyleSheet("background: #ffbcbd;")
        if self.banco.isModified():
            self.listado_de_modificaciones.append('Nombre del banco')
            self.banco.setStyleSheet("background: #ffbcbd;")
        if self.tipo_cuenta.isModified():
            self.listado_de_modificaciones.append('Tipo de cuenta')
            self.tipo_cuenta.setStyleSheet("background: #ffbcbd;")
        if self.correo_e.isModified():
            self.listado_de_modificaciones.append('Correo electrónico')
            if valid_correo.is_valid_email(self.correo_e.text()) is False:
                self.correo_e.setStyleSheet("color: red;background: #ffbcbd;")
            else:
                self.correo_e.setStyleSheet("color: black;background: #ffbcbd;")
            #self.correo_e.setStyleSheet("background: #ffbcbd;")
        if self.talla_camisa.isModified():
            self.listado_de_modificaciones.append('Talla de camisa')
            self.talla_camisa.setStyleSheet("background: #ffbcbd;")
        if self.talla_zap.isModified():
            self.listado_de_modificaciones.append('Talla de zapatos')
            self.talla_zap.setStyleSheet("background: #ffbcbd;")
        if self.talla_pantalon.isModified():
            self.listado_de_modificaciones.append('Talla de pantalón')
            self.talla_pantalon.setStyleSheet("background: #ffbcbd;")
        if self.lic_cond.isModified():
            self.listado_de_modificaciones.append('Número de licencia de conducir')
            self.lic_cond.setStyleSheet("background: #ffbcbd;")
        if self.fecha_venc_lic.hasFocus():
            self.listado_de_modificaciones.append('Vencimiento licencia de conducir')
            self.fecha_venc_lic.setStyleSheet("background: #ffbcbd;")
        if self.salario_actual.hasFocus():
            self.listado_de_modificaciones.append('Salario')
            self.salario_actual.setStyleSheet("background: #ffbcbd;")
        if self.fecha_ing.hasFocus():
            self.listado_de_modificaciones.append('Fecha de ingreso')
            self.fecha_ing.setStyleSheet("background: #ffbcbd;")
        if self.notas.hasFocus():
            self.listado_de_modificaciones.append('Nota')
            self.notas.setStyleSheet("background: #ffbcbd;")
        if self.cargo.isModified():
            self.listado_de_modificaciones.append('Cargo')
            self.cargo.setStyleSheet("background: #ffbcbd;")
        if self.tipo_nomina.hasFocus(): # se usa para combobox
            self.listado_de_modificaciones.append('Tipo de nómina')
            self.tipo_nomina.setStyleSheet("background: #ffbcbd;")
        if self.tipo_ingreso.hasFocus():
            self.listado_de_modificaciones.append('Tipo de Ingreso')
            self.tipo_ingreso.setStyleSheet("background: #ffbcbd;")
        if self.tipo_de_persona.hasFocus():
            self.listado_de_modificaciones.append('Tipo de Persona')
            self.tipo_de_persona.setStyleSheet("background: #ffbcbd;")
        if self.emp_seguros.isModified():
            self.listado_de_modificaciones.append('Aseguradora')
            self.emp_seguros.setStyleSheet("background: #ffbcbd;")
        if self.num_carnet_seg.isModified():
            self.listado_de_modificaciones.append('Número de seguro')
            self.num_carnet_seg.setStyleSheet("background: #ffbcbd;")
        if self.clave_nomina.isModified():
            self.listado_de_modificaciones.append('Clave de nómina en TSS')
            self.clave_nomina.setStyleSheet("background: #ffbcbd;")
        if self.primera_vac_2.hasFocus():
            self.listado_de_modificaciones.append('Fecha de 1era vacuna')
            self.primera_vac_2.setStyleSheet("background: #ffbcbd;")
        if self.seg_vac_2.hasFocus():
            self.listado_de_modificaciones.append('Fecha de 2da vacuna')
            self.seg_vac_2.setStyleSheet("background: #ffbcbd;")
        if self.tercera_vac_2.hasFocus():
            self.listado_de_modificaciones.append('Fecha de 3era vacuna')
            self.tercera_vac_2.setStyleSheet("background: #ffbcbd;")
        if self.estatus_combo.hasFocus(): # esto se debe manejar automatico por el programa
            self.listado_de_modificaciones.append('Estatus')
            self.estatus_combo.setStyleSheet("background: #ffbcbd;")
        if self.ret_tss.hasFocus():
            self.listado_de_modificaciones.append('Retención de la TSS')
            self.ret_tss.setStyleSheet("background: #ffbcbd;")
        if self.ret_infotep.hasFocus():
            self.listado_de_modificaciones.append('Retención de la INFOTEP')
            self.ret_infotep.setStyleSheet("background: #ffbcbd;")
        if self.ret_isr.hasFocus():
            self.listado_de_modificaciones.append('Retención de la ISR')
            self.ret_isr.setStyleSheet("background: #ffbcbd;")
        if self.calc_sal_navidad.hasFocus():
            self.listado_de_modificaciones.append('Calculo de salario de navidad')
            self.calc_sal_navidad.setStyleSheet("background: #ffbcbd;")
        if self.saldo_a_favor.hasFocus():
            self.listado_de_modificaciones.append('Saldo a favor')
            self.saldo_a_favor.setStyleSheet("background: #ffbcbd;")
        if self.aporte_vol_empresa.hasFocus():
            self.listado_de_modificaciones.append('Aporte voluntario empresa')
            self.aporte_vol_empresa.setStyleSheet("background: #ffbcbd;")
        if self.aporte_vol_trabajador.hasFocus():
            self.listado_de_modificaciones.append('Aporte voluntario trabajador')
            self.aporte_vol_trabajador.setStyleSheet("background: #ffbcbd;")
        if self.retencion_pension.hasFocus():
            self.listado_de_modificaciones.append('Retención pensión alimentaria')
            self.retencion_pension.setStyleSheet("background: #ffbcbd;")
        if self.rnc_agente_ret.isModified():
            self.listado_de_modificaciones.append('RNC agente de retención')
            self.rnc_agente_ret.setStyleSheet("background: #ffbcbd;")


        #print(list(set(self.listado_de_modificaciones)))

    def actualizar_bd_carga_fam(self,id_trabjador):
        if self.se_edito_tabla_carga_fam == 1:
            leew.del_gen('worker.db','carga_fam','id',id_trabjador) # borro toda la información vieja
            filas_en_tabla = self.tabla_carga_fam.rowCount()
            for fila in range(filas_en_tabla):
                nombre = self.tabla_carga_fam.item(fila,0).text()
                parentesco = self.tabla_carga_fam.item(fila,1).text()
                fecha_nac = self.tabla_carga_fam.item(fila,2).text()
                doc_id = self.tabla_carga_fam.item(fila,3).text()
                telf = self.tabla_carga_fam.item(fila,4).text()
                # abajo para meter la informacion tal cual se muestra
                leew.introduce_gen('worker.db','carga_fam',f"'{self.idw}','{nombre}','{parentesco}','{fecha_nac}','{doc_id}','{telf}',NULL")

    def confirma_datos_basicos(self):
        #print(self.listado_de_modificaciones)
        self.datos_faltantes = []
        if 'Nombre' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Nombre')
        if 'Apellido' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Apellido')
        if 'Fecha de Nacimiento' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Fecha de Nacimiento')
        if 'Fecha de ingreso' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Fecha de ingreso')
        if 'Salario' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Salario')
        if 'Tipo de documento' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Tipo de documento')
        if 'Número de documento' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Número de documento')
        if 'Tipo de nómina' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Tipo de nómina')
        if 'Clave de nómina en TSS' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Clave de nómina en TSS')
        if 'Tipo de Ingreso' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Tipo de Ingreso')
        if 'Tipo de Persona' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Tipo de Persona')

        #print(self.datos_faltantes)
        if self.datos_faltantes != []:
            datos = ''
            for dato in self.datos_faltantes:
                datos = datos + dato + '\n'
            QtWidgets.QMessageBox.warning(self, "Atención", f"Debe llenar la siguiente información "
                                                                f"obligatoriamente:\n{datos}", QtWidgets.QMessageBox.Ok)
            return 0
        else:
            return 1

    def imprime_carnet_cmd(self):
        imp_carnet.imprimir(self.idw)

    def genera_recibo(self):
        '''Genera el recibo del trabajador al dar dobleclick en tabla de costos'''
        for currentQTableWidgetItem in self.tabla_nomina.selectedItems():
            periodo = self.tabla_nomina.item(currentQTableWidgetItem.row(), 1).text()
            ver_recibos.ver_recibo(self.idw, periodo)

    def oculta_adelantos_ya_cobrados(self):
        #funcion para mostrar u ocultar trabajadores desincorporados
        if self.ver_solo_adelantos_pendientes.isChecked() == 1: # si esta activado o tildado checked
            for row in range(self.tabla_adelantos.rowCount()):# corre por todas las row de la tabla
                if self.tabla_adelantos.item(row,5).text() != "PENDIENTE":
                    self.tabla_adelantos.hideRow(row)
        else:# si no está activado o checked muestra todas las columnas
            for row in range(self.tabla_adelantos.rowCount()):
                self.tabla_adelantos.showRow(row)

    def refresh_tabla_detalles_prestamo(self):
        idp = 0# esto para quitar el mensaje de alerta de pycharm de que idp se podí usar sin estar declarada
        for currentQTableWidgetItem in self.tabla_adelantos.selectedItems():
            idp = self.tabla_adelantos.item(currentQTableWidgetItem.row(), 0).text()

        lista_idc = leew.consulta_lista('worker.db', 'idc', 'prestamos_detalles', 'idp', f'"{idp}"')
        n = len(lista_idc)
        self.tabla_detalles_adelantos.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tabla_detalles_adelantos.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)


        cont = 0
        for id_prestamo in lista_idc:
            id_prestamo = str(id_prestamo)
            item = id_prestamo
            self.tabla_detalles_adelantos.setItem(cont, 0, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db', 'periodo', 'prestamos_detalles', 'idc', f'"{id_prestamo}"')
            self.tabla_detalles_adelantos.setItem(cont, 1, QtWidgets.QTableWidgetItem(item))
            item = str(leew.consulta_gen('worker.db', 'estatus', 'prestamos_detalles', 'idc', f'"{id_prestamo}"'))
            self.tabla_detalles_adelantos.setItem(cont, 2, QtWidgets.QTableWidgetItem(item))

            cont = cont + 1

    def closeEvent(self, QCloseEvent):

        if len(self.listado_de_modificaciones) != 0:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia', '¿Está usted seguro de salir? Se perderán los datos '
                                                                        'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                         QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()
                self.parentWidget().close()

            else:

                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()
