from info_empresa import *
import leew, os


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # variable de control para close
        self.cerrar = 0

        self.listado_de_modificaciones = []

        self.dia = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, hh:mm:ss AP")

        self.se_edito_logo = 0
        self.se_edito_logo_pie = 0
        self.rnc.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("\\d{1,11}")))

        self.carga_data()

        # conexiones

        self.cancelar.clicked.connect(self.close)

        self.aceptar.clicked.connect(self.guardar_data)

        self.boton_logo.clicked.connect(self.editar_logo_cmd)
        self.boton_logo_pie.clicked.connect(self.editar_logo_pie_cmd)

        # conexiones para habilitar el botón guardar y poner el fondo en rojo

        self.nombre.textChanged.connect(self.activa_aceptar)
        self.direccion.textChanged.connect(self.activa_aceptar)
        self.ciudad.textChanged.connect(self.activa_aceptar)
        self.estado.textChanged.connect(self.activa_aceptar)
        self.pais.textChanged.connect(self.activa_aceptar)
        self.tel_fijo.textChanged.connect(self.activa_aceptar)
        self.tel_cel.textChanged.connect(self.activa_aceptar)
        self.web.textChanged.connect(self.activa_aceptar)
        self.email.textChanged.connect(self.activa_aceptar)
        self.rep_legal.textChanged.connect(self.activa_aceptar)
        self.rnc.textChanged.connect(self.activa_aceptar)
        self.reg_comercio.textChanged.connect(self.activa_aceptar)
        self.reg_mt.textChanged.connect(self.activa_aceptar)
        self.reg_mt.textChanged.connect(self.activa_aceptar)
        self.reg_tss.textChanged.connect(self.activa_aceptar)
        self.reg_infotep.textChanged.connect(self.activa_aceptar)
        self.boton_logo.clicked.connect(self.activa_aceptar)
        self.cierre_fiscal.currentTextChanged.connect(self.activa_aceptar)
        # inactiva guardar

        self.aceptar.setDisabled(1)

    def carga_data(self):
        # Carga de data
        if leew.tambd_par2("worker.db", "info_sociedad") == 0:
            pass  # esto para evitar problemas con tablas vacias
        else:
            last_fecha = leew.consulta_gen('worker.db', 'fecha', 'info_sociedad', 'estatus', '"Vigente"')
            self.barra.addWidget(QtWidgets.QLabel(f'  Última vez modificado el: {last_fecha}'))
            # se cargan los valores que estan en la tabla
            data = leew.consulta_gen('worker.db','nombre_sociedad','info_sociedad','estatus','"Vigente"')
            self.nombre.setText(data)
            data = leew.consulta_gen('worker.db', 'direccion', 'info_sociedad', 'estatus', '"Vigente"')
            self.direccion.setText(data)
            data = leew.consulta_gen('worker.db', 'ciudad', 'info_sociedad', 'estatus', '"Vigente"')
            self.ciudad.setText(data)
            data = leew.consulta_gen('worker.db', 'estado', 'info_sociedad', 'estatus', '"Vigente"')
            self.estado.setText(data)
            data = leew.consulta_gen('worker.db', 'pais', 'info_sociedad', 'estatus', '"Vigente"')
            self.pais.setText(data)
            data = leew.consulta_gen('worker.db', 'tel_fijo', 'info_sociedad', 'estatus', '"Vigente"')
            self.tel_fijo.setText(data)
            data = leew.consulta_gen('worker.db', 'tel_movil', 'info_sociedad', 'estatus', '"Vigente"')
            self.tel_cel.setText(data)
            data = leew.consulta_gen('worker.db', 'pag_web', 'info_sociedad', 'estatus', '"Vigente"')
            self.web.setText(data)
            data = leew.consulta_gen('worker.db', 'email', 'info_sociedad', 'estatus', '"Vigente"')
            self.email.setText(data)
            data = leew.consulta_gen('worker.db', 'rep_legal', 'info_sociedad', 'estatus', '"Vigente"')
            self.rep_legal.setText(data)
            data = leew.consulta_gen('worker.db', 'rnc', 'info_sociedad', 'estatus', '"Vigente"')
            self.rnc.setText(data)
            data = leew.consulta_gen('worker.db', 'reg_comercio', 'info_sociedad', 'estatus', '"Vigente"')
            self.reg_comercio.setText(data)
            data = leew.consulta_gen('worker.db', 'reg_mt', 'info_sociedad', 'estatus', '"Vigente"')
            self.reg_mt.setText(data)
            data = leew.consulta_gen('worker.db', 'reg_tss', 'info_sociedad', 'estatus', '"Vigente"')
            self.reg_tss.setText(data)
            data = leew.consulta_gen('worker.db', 'reg_infotep', 'info_sociedad', 'estatus', '"Vigente"')
            self.reg_infotep.setText(data)
            data = leew.consulta_gen('worker.db', 'opcional2', 'info_sociedad', 'estatus', '"Vigente"')
            cierre = {"2Q12": 0, "2Q03": 1, "2Q06": 2, "2Q09": 3}[data]
            self.cierre_fiscal.setCurrentIndex(cierre)

            # Logo:
            self.ruta_logo = leew.consulta_gen('worker.db', 'ruta_logo', 'info_sociedad', 'estatus', '"Vigente"')
            self.ruta_logo = f"{self.ruta_logo}"
            print(self.ruta_logo)
            #print(os.path.exists(self.ruta_logo))
            if os.path.isfile(self.ruta_logo):  # con este verifico que la empresa tenga asignado un logo
                #print('paso')
                pixmap = QtGui.QPixmap(self.ruta_logo)
                alto_foto = pixmap.size().height()
                ancho_foto = pixmap.size().width()
                ratio = alto_foto / ancho_foto
                ancho_forzado = 400  # ancho que queda bien en pantalla
                alto_calculado = int(ancho_forzado * ratio)
                scaled = pixmap.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                       transformMode=QtCore.Qt.SmoothTransformation)
                # print(scaled)
                # scaledPix = self.pixmap.scaled(QtCore.QSize(100,200), QtCore.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
                self.logo.setPixmap(scaled)

            # Logo pie:
            self.ruta_logo_pie = leew.consulta_gen('worker.db', 'opcional1', 'info_sociedad', 'estatus', '"Vigente"')
            self.ruta_logo_pie = f"{self.ruta_logo_pie}"
            #print(self.ruta_logo_pie)
            #print(os.path.exists(self.ruta_logo))
            if os.path.exists(self.ruta_logo_pie):  # con este verifico que el trabajador tenga asignado foto
                #print('paso')
                pixmap = QtGui.QPixmap(self.ruta_logo_pie)
                alto_foto = pixmap.size().height()
                ancho_foto = pixmap.size().width()
                ratio = alto_foto / ancho_foto
                ancho_forzado = 400  # ancho que queda bien en pantalla
                alto_calculado = int(ancho_forzado * ratio)
                scaled = pixmap.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                       transformMode=QtCore.Qt.SmoothTransformation)
                # print(scaled)
                # scaledPix = self.pixmap.scaled(QtCore.QSize(100,200), QtCore.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
                self.logo_pie.setPixmap(scaled)

    def editar_logo_cmd(self):
        ruta_nueva_imagen = QtWidgets.QFileDialog.getOpenFileName(self, 'Logo de la empresa', f'C:\\Users\\{os.environ.get( "USERNAME" )}','*.png *.jpg *.svg *jpeg')[0] #*.png *.svg*.jpg
        ruta_nueva_imagen = os.path.abspath(ruta_nueva_imagen) # pone la ruta tipo msdos requerido por os.system
        extencion_archivo = os.path.splitext(ruta_nueva_imagen)[1] # comando que da tupla con nom arch y su extencion separado
        #print(extencion_archivo)
        #print(ruta_nueva_imagen)
        #print(os.path.dirname(__file__))
        if  ruta_nueva_imagen != os.path.dirname(os.path.abspath(__file__)):
            #print(os.path.abspath(ruta_nueva_imagen))
            self.cmd_guarda_logo = f'copy  "{ruta_nueva_imagen}" "C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\logos\\logo{extencion_archivo}"'
            #print(self.cmd_guarda_logo)
            self.ruta_logo = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\logos\\logo{extencion_archivo}' # se usará en guardar SQL
            #print(self.ruta_logo)
            #os.system(cmd_guarda_foto) # este comando debe ejecutarse solo si se le da al boton guardar

            pixmap = QtGui.QPixmap(ruta_nueva_imagen)
            alto_foto = pixmap.size().height()
            ancho_foto = pixmap.size().width()
            ratio = alto_foto / ancho_foto
            ancho_forzado = 400  # ancho que queda bien en pantalla todo asociar este valor a resolucion cliente
            alto_calculado = int(ancho_forzado * ratio)
            scaled = pixmap.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
            # print(scaled)
            self.logo.setPixmap(scaled)#scaled

            self.logo.setStyleSheet("background: #ffbcbd;") # para indicar al usuario que editó la foto con fodo rosado
            self.listado_de_modificaciones.append('Logo') # para colocar la foto en la lista de cambios
            self.aceptar.setDisabled(0) # activa boton guardar
            self.se_edito_logo = 1 # flag que dice que se edito el logo

    def editar_logo_pie_cmd(self):
        ruta_nueva_imagen = QtWidgets.QFileDialog.getOpenFileName(self, 'Logo pie de página', f'C:\\Users\\{os.environ.get( "USERNAME" )}','*.png *.jpg *.svg')[0] #*.png *.svg*.jpg
        ruta_nueva_imagen = os.path.abspath(ruta_nueva_imagen) # pone la ruta tipo msdos requerido por os.system
        extencion_archivo = os.path.splitext(ruta_nueva_imagen)[1] # comando que da tupla con nom arch y su extencion separado
        #print(extencion_archivo)
        #print(ruta_nueva_imagen)
        #print(os.path.dirname(__file__))
        if  ruta_nueva_imagen != os.path.dirname(os.path.abspath(__file__)):
            #print(os.path.abspath(ruta_nueva_imagen))
            self.cmd_guarda_logo_pie = f'copy  "{ruta_nueva_imagen}" "C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\logos\\logo_pie{extencion_archivo}"'
            #print(self.cmd_guarda_logo_pie)
            self.ruta_logo_pie = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\logos\\logo_pie{extencion_archivo}' # se usará en guardar SQL
            #print(self.ruta_logo)


            pixmap = QtGui.QPixmap(ruta_nueva_imagen)
            alto_foto = pixmap.size().height()
            ancho_foto = pixmap.size().width()
            ratio = alto_foto / ancho_foto
            ancho_forzado = 400  # ancho que queda bien en pantalla todo asociar este valor a resolucion cliente
            alto_calculado = int(ancho_forzado * ratio)
            scaled = pixmap.scaled(ancho_forzado, alto_calculado, QtCore.Qt.KeepAspectRatio,
                                   transformMode=QtCore.Qt.SmoothTransformation)
            # print(scaled)
            self.logo_pie.setPixmap(scaled)#scaled

            self.logo_pie.setStyleSheet("background: #ffbcbd;") # para indicar al usuario que editó la foto con fodo rosado
            self.listado_de_modificaciones.append('Logo pie de página') # para colocar la foto en la lista de cambios
            self.aceptar.setDisabled(0) # activa boton guardar
            self.se_edito_logo_pie = 1 # flag que dice que se edito el logo

    def activa_aceptar(self):
        self.aceptar.setDisabled(0)
        if self.nombre.isModified():
            self.listado_de_modificaciones.append('Nombre de la sociedad')  # se agraga nombre a la lista de campos modificados
            self.nombre.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.direccion.isModified():
            self.listado_de_modificaciones.append('Dirección')  # se agraga nombre a la lista de campos modificados
            self.direccion.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.ciudad.isModified():
            self.listado_de_modificaciones.append('Ciudad')  # se agraga nombre a la lista de campos modificados
            self.ciudad.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.estado.isModified():
            self.listado_de_modificaciones.append('Estado')  # se agraga nombre a la lista de campos modificados
            self.estado.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.pais.isModified():
            self.listado_de_modificaciones.append('País')  # se agraga nombre a la lista de campos modificados
            self.pais.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.tel_fijo.isModified():
            self.listado_de_modificaciones.append('Teléfono fijo')  # se agraga nombre a la lista de campos modificados
            self.tel_fijo.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.tel_cel.isModified():
            self.listado_de_modificaciones.append('Teléfono celular')  # se agraga nombre a la lista de campos modificados
            self.tel_cel.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.web.isModified():
            self.listado_de_modificaciones.append('Página web')  # se agraga nombre a la lista de campos modificados
            self.web.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.email.isModified():
            self.listado_de_modificaciones.append('Correo electrónico')  # se agraga nombre a la lista de campos modificados
            self.email.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.rep_legal.isModified():
            self.listado_de_modificaciones.append('Representante legal')  # se agraga nombre a la lista de campos modificados
            self.rep_legal.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.rnc.isModified():
            self.listado_de_modificaciones.append('RNC')  # se agraga nombre a la lista de campos modificados
            self.rnc.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.reg_comercio.isModified():
            self.listado_de_modificaciones.append('Registro de comercio')  # se agraga nombre a la lista de campos modificados
            self.reg_comercio.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.reg_mt.isModified():
            self.listado_de_modificaciones.append('Registro Ministerio de trabajo')  # se agraga nombre a la lista de campos modificados
            self.reg_mt.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.reg_tss.isModified():
            self.listado_de_modificaciones.append('Registro TSS')  # se agraga nombre a la lista de campos modificados
            self.reg_tss.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.reg_infotep.isModified():
            self.listado_de_modificaciones.append('Registro INFOTEP')  # se agraga nombre a la lista de campos modificados
            self.reg_infotep.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.cierre_fiscal.hasFocus():
            self.listado_de_modificaciones.append('Cierre fiscal')
            self.cierre_fiscal.setStyleSheet("background: #ffbcbd;")

    def guardar_data(self):
        texto = ""
        # abqjo vuelvo un cojunto (set en ingles) para quitar elementos repetidos
        self.conjunto_de_modificaciones = set(self.listado_de_modificaciones)
        for modificacion in self.conjunto_de_modificaciones:
            texto = f"{modificacion}, " + texto

        texto = f"¿Desea confirmar la modificación de los siguientes campos?:\n{texto}"
        texto = texto[0:len(texto) - 2] + "."  # esto para eliminar la ultima coma y poner un punto (.)
        reply = QtWidgets.QMessageBox.warning(self, "Advertencia!", texto,
                                              QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            cierres = {0: "2Q12", 1: "2Q03", 2: "2Q06", 3: "2Q09"}
            cierre_fiscal = cierres[self.cierre_fiscal.currentIndex()]
            try:
                # para el logo
                if self.se_edito_logo == 1:
                    os.system(self.cmd_guarda_logo)

                if self.se_edito_logo_pie == 1:
                    os.system(self.cmd_guarda_logo_pie)

                leew.update_gen('worker.db','info_sociedad','estatus') # aqui pongo toda la tabla con estatus Anterior

                self.entrada = f'NULL,"{self.nombre.text()}","{self.direccion.text()}","{self.ciudad.text()}",' \
                               f'"{self.estado.text()}","{self.pais.text()}","{self.tel_fijo.text()}","{self.tel_cel.text()}",' \
                               f'"{self.web.text()}","{self.email.text()}","{self.rep_legal.text()}","{self.rnc.text()}",' \
                               f'"{self.reg_comercio.text()}","{self.reg_mt.text()}","{self.reg_tss.text()}",' \
                               f'"{self.reg_infotep.text()}","{self.ruta_logo}", "{self.ruta_logo_pie}","{cierre_fiscal}",NULL,"{self.dia}","Vigente"'

                #print(self.entrada)
                leew.introduce_gen('worker.db','info_sociedad',self.entrada)
                QtWidgets.QMessageBox.information(self, "Atención", "Tabla modificada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.cerrar = 1
                self.close()
                self.parentWidget().close()


            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)
        else:
            pass

    def closeEvent(self, QCloseEvent):

        if self.cerrar == 0:
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
