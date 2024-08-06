import primer_usuario_calc, os
from acceso import *
import leew, globales

class MainWindowApp(QtWidgets.QMainWindow, Ui_acceso):


    def __init__(self, *args,bloqueo = 0, **kwargs):
        # cuando bloqueo vale 0 esporque se usa para el primer ingreo
        # cuando bloqueo vale 1 esporque se instó para bloquear
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.bloqueo = bloqueo
        #self.parentWidget().menubar.actions()[0].setDisabled(1)
        self.clave_en_bd = 'un valor que no sirve de nada'
        self.acceder = 0
        self.preguntar_para_cerrar = True

        if not os.path.isfile(f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo\\worker.db'): # verifico que exista la BD en la carpeta datosSNPdo
            primer_usuario_calc.MainWindowApp(self.parentWidget(),self)# aquí le mando en el parentwidget la instancia de la ventana principal
        else:# se deja continuar al init para que muestre la ventana de acceso
            version_base_datos = leew.consulta_gen('worker.db', 'version', 'datos_bd', 'estatus', '"Vigente"')
            fecha_base_datos = leew.consulta_gen('worker.db', 'fecha', 'datos_bd', 'estatus', '"Vigente"')
            self.version.setText(f"Versión: {globales.version}\nVersión BD: {version_base_datos}\n{fecha_base_datos}")
            self.listado_usuarios = leew.consulta_lista('worker.db', 'nombre', 'usu', 'id>', '0')
            self.aceptar.clicked.connect(self.aceptar_cmd)
            self.cerrar.clicked.connect(self.cerrar_cmd)

            self.show()

    def implementar_nivel_acceso(self):
        nivel_de_acceso = leew.consulta_gen('worker.db','nivel','usu','nombre',f'"{self.usuario.text()}"')

        if nivel_de_acceso != 1:
            # accesos_en_bd son los accesos que tiene el usuario aprobados
            accesos_en_bd = leew.consulta_gen('worker.db','accesos','usu','nombre',f'"{self.usuario.text()}"')
            accesos_en_bd = accesos_en_bd[1:len(accesos_en_bd) -1].replace("'",'').replace(" ","").split(',') # aquí covierto en lista de verdad
            #print(accesos_en_bd)

            submenus_objetos = self.parentWidget().menubar.actions() # estos son los modulos o menus
            for item in submenus_objetos:
                #
                if item.text() in accesos_en_bd: # compara los menus disponibles vs los autorizados
                    pass
                else:
                    item.setDisabled(1)

            self.parent().toolBar.setDisabled(1)

    def aceptar_cmd(self):
        if self.usuario.text() in self.listado_usuarios:
            self.clave_en_bd = leew.consulta_gen('worker.db','clave','usu','nombre','"' + self.usuario.text() + '"')
            if self.clave.text() == self.clave_en_bd:
                self.acceder = 1
                self.colocar_widget()
                self.implementar_nivel_acceso()
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error en acceso", "Clave incorrecta",
                                              QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Error en acceso", "Usuario incorrecto",
                                          QtWidgets.QMessageBox.Ok)

    def colocar_widget(self):
        if self.bloqueo == 0:
            self.parentWidget().statusbar.addWidget(
            QtWidgets.QLabel(f"Usuario conectado: {self.usuario.text()}"))  # este es el status bar del main


            self.parentWidget().usuario = self.usuario.text()  # para que esté disponible para otros modulos

    def cerrar_cmd(self):
        self.close()

    def closeEvent(self, QCloseEvent):

        if self.acceder == 1:
            QCloseEvent.accept()

        else:
            if self.preguntar_para_cerrar == False: # es False cuando se cierra desde "primer_usuario_calc.py"
                self.parentWidget().ya_se_puede_cerrar = True # para se cierra main sin advertir perdida de datos
                self.parentWidget().close()
                QCloseEvent.accept()
            else:
                reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                       '¿Está usted seguro de cerrar la aplicación? Se perderán los datos '
                                                       'no guardados',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.Yes:
                    self.parentWidget().ya_se_puede_cerrar = True  # para cerrar main sin advertir perdida de datos
                    self.parentWidget().close()
                    QCloseEvent.accept()


                else:

                    QCloseEvent.ignore()
