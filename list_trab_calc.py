from list_trab import *

import leew, ficha_calc

class MainWindow(QtWidgets.QMainWindow, Ui_list_trab):

    def __init__(self,obj,obj2, *args, user='', **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.user = user # este usuario es para grabarlo en la bd cuando se crea o edita un trbajador
        self.obj = obj # para que las fichas sea subwindows mdi
        self.obj2 = obj2 # para poder habilitar de nuevo el menu de listado de trabajaodes
        #print(self.obj)
        # Carga de data
        self.numero_ficha = ""
        self.refresh_tabla()
        self.oculta_desincorporados()

        # conexiones

        self.cerrar.clicked.connect(self.cerrar_cmd)
        self.tableWidget.clicked.connect(self.cambia_nombre)
        self.verFicha.setDisabled(1)
        self.crear.clicked.connect(self.cmd_crear)
        self.verFicha.clicked.connect(self.ver_ficha)
        self.tableWidget.doubleClicked.connect(self.ver_ficha)
        self.trab_ret.clicked.connect(self.oculta_desincorporados)

        #shortcuts
        self.crear.setText("Crear (N)")
        self.crear.setShortcut("N")


    def cmd_crear(self):
        #self.close() ya no lo uso
        #self.parentWidget().close()
        self.obj.addSubWindow(ficha_calc.MainWindow(self.refresh_tabla,self,user=self.user)).show()

        #ficha_calc.MainWindow(self,user=self.user) en caso de ventana flotante

    def ver_ficha(self):
        #self.close() # ya no lo uso
        #self.parentWidget().close() ya no lo uso
        #ficha_calc.MainWindow(self, idw=self.numero_ficha,user=self.user) en caso de ventana flotante
        self.obj.addSubWindow(ficha_calc.MainWindow(self.refresh_tabla,self, idw=self.numero_ficha,user=self.user)).show()

    def refresh_tabla(self):

        lista_idies = leew.consulta_lista('worker.db','id','info','id >', '0')

        num_filas = len(lista_idies)

        self.tableWidget.setRowCount(num_filas)

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        for i in range(num_filas):
            text = str(1 + i)
            item, = leew.consultaP('worker.db', 'id', 'info', text)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item)))
            item, = leew.consultaP('worker.db', 'Nombre', 'info', text)
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP('worker.db', 'Apellido', 'info', text)
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(item))
            item, = leew.consultaP('worker.db', 'Estatus', 'info', text)
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(item))

    def oculta_desincorporados(self):
        #funcion para mostrar u ocultar trabajadores desincorporados
        if self.trab_ret.isChecked() == 0: # si no es esta activado o tildado checked
            for row in range(self.tableWidget.rowCount()):# corre por todas las row de la tabla
                if self.tableWidget.item(row,3).text() == "Desincorporado":
                    self.tableWidget.hideRow(row)
        else:# si sí esta acticado o checked muestra todas las columnas
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.showRow(row)

    def cambia_nombre(self):

        self.verFicha.setDisabled(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.numero_ficha = self.tableWidget.item(currentQTableWidgetItem.row(), 0).text()
            self.verFicha.setText("Ver ficha: " + self.numero_ficha)

    def cerrar_cmd(self):
        self.close()
        self.parentWidget().close()

    def closeEvent(self, QCloseEvent):
        # esta funcion es para que el boton cerrar y la X de la ventana reactiven el menu de listado de trabajadores
        self.close()
        self.parentWidget().close()
        self.obj2.setDisabled(False)