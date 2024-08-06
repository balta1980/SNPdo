from list_usuarios import *

import leew, usuario_calc

class MainWindow(QtWidgets.QMainWindow, Ui_list_usu):

    def __init__(self,obj,obj2, obj3, *args, user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador
        self.obj = obj # para que las fichas sea subwindows mdi
        self.obj2 = obj2 # para poder habilitar de nuevo el menu de listado de trabajaodes
        self.obj3 = obj3 # que es el menubar
        #print(self.obj)
        # Carga de data
        self.borrar.setDisabled(True)
        self.numero_ficha = ""
        self.refresh_tabla()

        # conexiones

        self.cerrar.clicked.connect(self.cerrar_cmd)
        self.tableWidget.clicked.connect(self.cambia_nombre)
        self.verFicha.setDisabled(1)
        self.crear.clicked.connect(self.cmd_crear)
        self.verFicha.clicked.connect(self.ver_ficha)
        self.tableWidget.doubleClicked.connect(self.ver_ficha)
        self.borrar.clicked.connect(self.borrar_usuario)

        # hacer visible
        # self.show() no se usa con mdi

    def cmd_crear(self):
        #self.close() ya no lo uso
        #self.parentWidget().close()
        self.obj.addSubWindow(usuario_calc.MainWindow(self.refresh_tabla, self.obj3, self,user=self.user)).show()

        #ficha_calc.MainWindow(self,user=self.user) en caso de ventana flotante

    def borrar_usuario(self):
        texto = f"¿Desea borrar el usuario {self.numero_ficha}?"
        reply = QtWidgets.QMessageBox.question(self, "Conformación de eliminación", texto
                                               , QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            leew.del_gen('worker.db','usu', 'id', f'"{self.numero_ficha}"')
            self.refresh_tabla()

    def ver_ficha(self):
        self.obj.addSubWindow(usuario_calc.MainWindow(self.refresh_tabla,self.obj3,self, idw=self.numero_ficha,user=self.user)).show()

    def refresh_tabla(self):

        # Llenando las filas
        lista_id = []

        try:  # para atrapar una BD de vacia
            lista_id = leew.consulta_lista('worker.db', 'id', 'usu', 'nivel>', '"2"')
            n = len(lista_id)
        except:
            n = 0

        self.tableWidget.setRowCount(n)

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        fila = 0
        for i in lista_id:
            item = str(i)
            self.tableWidget.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item)))
            item = leew.consulta_gen('worker.db','nombre_apellido','usu','id',f'"{i}"')
            self.tableWidget.setItem(fila, 1, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db','nombre','usu','id',f'"{i}"')
            self.tableWidget.setItem(fila, 2, QtWidgets.QTableWidgetItem(item))
            item = leew.consulta_gen('worker.db','accesos','usu','id',f'"{i}"')
            self.tableWidget.setItem(fila, 3, QtWidgets.QTableWidgetItem(item))
            fila = fila + 1

    def cambia_nombre(self):

        self.verFicha.setDisabled(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.numero_ficha = self.tableWidget.item(currentQTableWidgetItem.row(), 0).text()
            self.verFicha.setText("Ver usuario: " + self.numero_ficha)
            self.borrar.setText("Borrar usuario: " + self.numero_ficha)
            self.borrar.setDisabled(False)

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def closeEvent(self, QCloseEvent):
        # esta funcion es para que el boton cerrar y la X de la ventana reactiven el menu de listado de trabajadores
        self.close()
        self.parentWidget().close()
        self.obj2.setDisabled(False)