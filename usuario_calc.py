from usuario import *

import leew

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,cmd, obj3, *args, idw="",user='', **kwargs):

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)
        self.idw = idw # idw se usa es este modulo para almacenar id de usuario nuevo o ya registrado
        self.obj3 = obj3 # el cual es menubar
        self.refrescar_tabla_list_usu = cmd # este comando viene del listado de trabajadores y es para refrescar la tabla
        self.user = user #esta variable tiene que tener los datos del usuario que hace la edicion para efectos de guardar quien cambio que en la bd

        self.listado_de_modificaciones = []

        self.cargar_info()
        self.guardar.setDisabled(1)

        self.nombre.textChanged.connect(self.enable_guardar)
        self.usuario.textChanged.connect(self.enable_guardar)
        self.clave.textChanged.connect(self.enable_guardar)
        self.listWidget.clicked.connect(self.enable_guardar)

        self.cancelar.clicked.connect(self.close)
        self.guardar.clicked.connect(self.guardar_info)

    def cargar_info(self):

        submenus_nombres = []
        submenus_objetos = self.obj3.actions()
        for item in submenus_objetos:
            submenus_nombres.append(item.text())
        self.listWidget.addItems(submenus_nombres)

        if self.idw == "":
            pass
        else:
            nombreyapellido = leew.consulta_gen('worker.db','nombre_apellido','usu','id',f"{self.idw}")
            self.nombre.setText(nombreyapellido)
            usuario = leew.consulta_gen('worker.db', 'nombre', 'usu', 'id', f"{self.idw}")
            self.usuario.setText(usuario)
            clave = leew.consulta_gen('worker.db', 'clave', 'usu', 'id', f"{self.idw}")
            self.clave.setText(clave)
            lista_accesos_en_bd = leew.consulta_gen('worker.db', 'accesos', 'usu', 'id', f"{self.idw}")
            lista_accesos_en_bd = lista_accesos_en_bd[1:len(lista_accesos_en_bd) -1].replace("'",'').replace(" ","").split(',')

            for item in [self.listWidget.item(x) for x in range(self.listWidget.count())]:
                if item.text() in lista_accesos_en_bd:
                    item.setSelected(True)

    def guardar_info(self):
        texto = ""
        # abajo vuelvo un cojunto (set en ingles) para quitar elementos repetidos
        self.conjunto_de_modificaciones = set(self.listado_de_modificaciones)
        for modificacion in self.conjunto_de_modificaciones:
            texto = f"{modificacion}, " + texto

        texto = f"¿Desea confirmar la modificación de los siguientes campos?:\n{texto}"
        texto = texto[0:len(texto) - 2] + "."  # esto para eliminar la ultima coma y poner un punto (.)
        reply = QtWidgets.QMessageBox.question(self, "Conformación de moficaciones", texto
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            accesos = []
            for acceso in self.listWidget.selectedItems():  # para convertir a lista leible
                accesos.append(acceso.text())

            if self.idw != "":  # cuando es una edición de una ficha de un usuario

                self.entrada = f'"{self.idw}","{self.usuario.text()}","{self.clave.text()}","2",' \
                               f'"{accesos}","{self.nombre.text()}", ' \
                               f'"{QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, hh:mm:ss")}"'
                #print(self.entrada)
                leew.del_gen('worker.db','usu','id',f'"{self.idw}"')
                leew.introduce_gen('worker.db','usu',self.entrada)

                self.listado_de_modificaciones = []  # para que no muestre mensaje de que falta algo

                self.close()
                QtWidgets.QMessageBox.information(self, "Aviso", "Se han grabado las modificaciones satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)

                try:
                    self.refrescar_tabla_list_usu()  # refresco la tabla del listado de usuarios

                except:
                    pass  # esto es por si cierran el listado que se trata de actualizar
            else:  # cuando es un trabajador nuevo

                confirma = self.confirma_datos_basicos()
                # print(confirma)
                if confirma == 1:
                    self.entrada = f'NULL,"{self.usuario.text()}","{self.clave.text()}","2",' \
                               f'"{accesos}","{self.nombre.text()}", ' \
                                   f'"{QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, hh:mm:ss")}"'

                    #print(self.entrada)
                    leew.introduce_gen('worker.db','usu',self.entrada)

                    self.listado_de_modificaciones = [] # para que no muestre mensaje de que falta algo

                    self.close()

                    QtWidgets.QMessageBox.information(self, "Aviso",
                                                      "Se ha creado el nuevo usuario satisfactoriamente",
                                                      QtWidgets.QMessageBox.Ok)
                    try:
                        self.refrescar_tabla_list_usu()  # refresco la tabla del listado de trabajadores
                    except:
                        pass  # esto es por si cierran el listado que se trata de actualizar

    def enable_guardar(self):
        '''esta funcion debió llamarse enable guardar,pero como ya la usé mucho...'''
        self.guardar.setDisabled(0)
        if self.nombre.isModified():  # si el nombre es modificado
            self.listado_de_modificaciones.append('Nombre')  # se agraga nombre a la lista de campos modificados
            self.nombre.setStyleSheet("background: #ffbcbd;")  # le pongo fondo rosado
        if self.usuario.isModified():  # si el nombre es modificado
            self.listado_de_modificaciones.append('Usuario')

            self.verifica_usuario_repetido()  # para evitar que se cree un usuario repetido
        if self.clave.isModified():
            self.listado_de_modificaciones.append('Clave')
            self.clave.setStyleSheet("background: #ffbcbd;")

        if self.listWidget.hasFocus():
            self.listado_de_modificaciones.append('Accesos')
            self.listWidget.setStyleSheet("background: #ffbcbd;")

        #print(list(set(self.listado_de_modificaciones)))

    def confirma_datos_basicos(self):
        #print(self.listado_de_modificaciones)
        self.datos_faltantes = [] # datos que deben ser llenados obligatorio
        if 'Nombre' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Nombre')
        if 'Usuario' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Usuario')
        if 'Clave' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Clave')
        if 'Accesos' not in self.listado_de_modificaciones:
            self.datos_faltantes.append('Accesos')

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

    def verifica_usuario_repetido(self):
        usuarios_en_bd = leew.consulta_lista("worker.db",'nombre','usu','id>','0')
        if self.usuario.text() in usuarios_en_bd:
            self.usuario.setStyleSheet("background: red; color: yellow;")
            self.usuario.setToolTip("Usuario repetido, use otro nombre de usuario")
            self.guardar.setDisabled(1)
            return 1
        else:
            self.usuario.setStyleSheet("background: #ffbcbd;")
            self.usuario.setToolTip("Introduzca un nombre usuario, preferiblemente una sola palabra")
            return 0

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
