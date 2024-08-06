from primer_usuario import *
import leew, os, shutil

class MainWindowApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,main, *args, **kwargs):
        # cuando bloqueo vale 0 esporque se usa para el primer ingreo
        # cuando bloqueo vale 1 esporque se instó para bloquear
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.aceptar.setDisabled(True)

        self.ventana_main = main
        self.acceder = 0
        self.usuario.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("\\S{4,8}")))
        self.clave1.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("\\S{4,8}")))
        self.clave2.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("\\S{4,8}")))

        #conexiones
        self.nombre.textChanged.connect(self.activa_aceptar)
        self.apellido.textChanged.connect(self.activa_aceptar)
        self.nombre_empresa.textChanged.connect(self.activa_aceptar)
        self.usuario.textChanged.connect(self.activa_aceptar)
        self.clave1.textChanged.connect(self.activa_aceptar)
        self.clave2.textChanged.connect(self.activa_aceptar)
        self.cierre_fiscal.currentTextChanged.connect(self.activa_aceptar)
        self.cancelar.clicked.connect(self.cerrar_cmd)
        self.aceptar.clicked.connect(self.guarda_usuario)
        self.importarBD.clicked.connect(self.importar)

        # para ayudar al usuario a llenar toda la información
        # información primer periodo abierto

        self.mensaje = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.mensaje)
        self.mensaje2 = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.mensaje2)

        self.activa_aceptar()

        # creación de las carpetas............................................................................
        if not os.path.isdir(
                f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo'):  # verifico que exista la carpeta datosSNPdo
            try:
                os.mkdir(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo')  # creo la carpeta
            except:
                pass

        if not os.path.isdir(
                f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\respaldo_bd'):  # verifico que exista la carpeta datosSNPdo\respaldo_bd
            try:
                os.mkdir(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\respaldo_bd')  # creo la carpeta
            except:
                pass

        carpetas_para_archivos = ['carnets', 'formatos_asistencia', 'img_trab', 'impresiones', 'impresiones\\logos',
                                  'informe_tss', 'ordenes', 'recibos_dotaciones', 'resumen_recibos', 'txt']
        for carpeta in carpetas_para_archivos:
            if not os.path.isdir(
                    f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{carpeta}'):  # verifico que exista la carpeta
                try:
                    os.mkdir(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\{carpeta}')  # creo la carpeta
                except:
                    pass
        # creación de las carpetas............................................................................
        # copia de la base de datos, logos e imagenes de trabajadores.........................................
        ruta1 = f'{os.path.dirname(os.path.abspath(__file__))}\\worker.db'  # BD virgen en la ruta de la carpeta de instalación del programa, que pudiera ser la misma que la de trabajo en versiones hasta la 1.1.7
        ruta2 = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo'  # ruta para la carpeta de trabajo de la bd
        comando = f'copy "{ruta1}" "{ruta2}"'
        os.system(comando)
        # logos
        ruta1 = f'{os.path.dirname(os.path.abspath(__file__))}\\impresiones\\logos\\*.*'  # BD virgen en la ruta de la carpeta de instalación del programa, que pudiera ser la misma que la de trabajo en versiones hasta la 1.1.7
        ruta2 = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\impresiones\\logos\\'  # ruta para la carpeta de trabajo de la bd
        comando = f'copy "{ruta1}" "{ruta2}"'
        os.system(comando)
        # imagenes trabajadores
        ruta1 = f'{os.path.dirname(os.path.abspath(__file__))}\\img_trab\\*.*'  # BD virgen en la ruta de la carpeta de instalación del programa, que pudiera ser la misma que la de trabajo en versiones hasta la 1.1.7
        ruta2 = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\img_trab\\'  # ruta para la carpeta de trabajo de la bd
        comando = f'copy "{ruta1}" "{ruta2}"'
        os.system(comando)

        # copia de la base de datos..........................................................................

        # en el caso de que sea una actualización de la versión 1.1.1 hasta la 1.1.7  que se guardaba la bd y carpetas
        # en la misma carpeta de instalación, cosa que cambió a partir de 1.1.8
        # al ser una actualización debe haber usuarios en la BD
        self.listado_usuarios = leew.consulta_lista('worker.db', 'nombre', 'usu', 'id>', '0')
        if self.listado_usuarios == []:
            self.show()
        else:
            self.acceder = 1
            self.close()
            self.parentWidget().__init__(self.ventana_main)

    def activa_aceptar(self):
        if self.cierre_fiscal.currentIndex() != 0 and self.nombre_empresa.text() != '' and self.usuario.text() != '' and\
                self.nombre.text() != '' and self.apellido.text() != '' and self.verifica_clave() == True:
            self.aceptar.setDisabled(False)
            self.mensaje.setText("Información completada")
            self.mensaje.setStyleSheet("background:None ;border-radius:3;")

        else:
            self.aceptar.setDisabled(True)
            self.mensaje.setText("Rellene los campos resaltados")
            self.mensaje.setStyleSheet("background:#f7f76c ;border-radius:3;")


        if self.cierre_fiscal.currentIndex() != 0:

            self.cierre_fiscal.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.cierre_fiscal.setStyleSheet("background:#f7f76c ;border-radius:3;")


        if self.nombre_empresa.text() != '':

            self.nombre_empresa.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.nombre_empresa.setStyleSheet("background:#f7f76c ;border-radius:3;")


        if self.usuario.text() != '':

            self.usuario.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.usuario.setStyleSheet("background:#f7f76c ;border-radius:3;")


        if self.nombre.text() != '':

            self.nombre.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.nombre.setStyleSheet("background:#f7f76c ;border-radius:3;")

        if self.apellido.text() != '':

            self.apellido.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.apellido.setStyleSheet("background:#f7f76c ;border-radius:3;")

        if self.clave1.text() != '':


            self.clave1.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.clave1.setStyleSheet("background:#f7f76c ;border-radius:3;")

        if self.clave2.text() != '':

            self.clave2.setStyleSheet("background:None ;border-radius:3;")
        else:

            self.clave2.setStyleSheet("background:#f7f76c ;border-radius:3;")

        if self.verifica_clave() == True:
            self.mensaje2.setText('')
            self.mensaje2.setStyleSheet("background:None ;border-radius:3;")
        else:
            self.mensaje2.setText('Las claves no coinciden o no tienen un mínimo de 4 caracteres')
            self.mensaje2.setStyleSheet("background:#f7f76c ;border-radius:3;")

    def verifica_clave(self):
        if self.clave1.text() == self.clave2.text() and len(self.clave1.text()) >= 4:#como se compara la igualdad con solo uno que sea mayor oigual a 4 es suficiente
            return True
        else:
            return False

    def guarda_usuario(self):
        cierres = {1: "2Q12", 2: "2Q03", 3: "2Q06", 4: "2Q09"}
        cierre_fiscal_bd = cierres[self.cierre_fiscal.currentIndex()]
        leew.introduce_gen('worker.db', 'usu', f'NULL, "{self.usuario.text()}", "{self.clave1.text()}","1", NULL, '
                                               f'"{self.nombre.text()} {self.apellido.text()}", '
                                               f'"{QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, hh:mm:ss")}"')
        leew.introduce_gen('worker.db', 'info_sociedad', f'NULL, "{self.nombre_empresa.text()}",NULL,NULL,NULL,NULL,'
                                                         f'NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL'
                                                         f',"{cierre_fiscal_bd}",NULL,NULL, "Vigente"')
        self.colocar_widget()
        self.acceder = 1
        self.close()

    def colocar_widget(self):

        self.ventana_main.statusbar.addWidget(
        QtWidgets.QLabel(f"Usuario conectado: {self.usuario.text()}"))  # este es el status bar del main


        self.ventana_main.usuario = self.usuario.text()  # para que esté disponible para otros modulos

        self.ventana_main.carga_empresa_activa()

    def importar(self):
        self.ventana_main.importar_base_datos()
        self.acceder = 1

    def cerrar_cmd(self):

        self.close()


    def closeEvent(self, QCloseEvent):
        if self.acceder == 1:
            QCloseEvent.accept()
        else:

            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   'No ha configurado los datos básicos ¿Está usted seguro de cerrar la aplicación? Se perderán los datos '
                                                   'no guardados',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()
                self.parentWidget().preguntar_para_cerrar = False
                self.parentWidget().close()
                # borro las carpetas y la base de datos creadas en __init__ porque el usuario cancelo el llegado de datos
                shutil.rmtree(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo')


            else:

                QCloseEvent.ignore()

