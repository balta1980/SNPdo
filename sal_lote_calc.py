from sal_lote import *
import leew, os
from openpyxl import Workbook


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,obj, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.obj = obj  # para habilitar otras vez el menu

        self.carga_data()

        self.ya_se_puede_cerrar = False

        self.cancelar.clicked.connect(self.close_cmd)

        self.fecha.setDate(QtCore.QDate.currentDate())

        self.valor_absoluto.valueChanged.connect(self.calcula_aumento)
        self.aumento_abs.clicked.connect(self.resetear_val_porcentual)

        self.val_porcentual.valueChanged.connect(self.calcula_aumento)
        self.aumento_porc.clicked.connect(self.resetear_valor_absoluto)

        self.calcula_aumento()

        self.aceptar.clicked.connect(self.add_salario)

        self.aceptar.setDisabled(1)

        self.val_porcentual.valueChanged.connect(self.activa)
        self.valor_absoluto.valueChanged.connect(self.activa)

        self.nota.textChanged.connect(self.activa)

        self.fecha.dateChanged.connect(self.activa)

        self.exportar.clicked.connect(self.exportar_cmd)

    def carga_data(self):
        # llenado de filas tabla
        contador_de_filas = 0

        # Las cuatro lineas que siguen se usan para mejorar el aspecto de la tabla
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)

        idies = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')

        # esto lo hago para el caso extremo de que no hayan trabajadores activos
        if idies == []:
            self.aumento_abs.setDisabled(1)
            self.aumento_porc.setDisabled(1)
            self.nota.setDisabled(1)
            self.fecha.setDisabled(1)

        self.tableWidget.setRowCount(len(idies))

        # print(idies)
        for id in idies:
            id = str(id)
            nombre = leew.consulta_gen('worker.db', 'Nombre', 'info', 'id', f'"{id}"')
            apellido = leew.consulta_gen('worker.db', 'Apellido', 'info', 'id', f'"{id}"')
            cedula = leew.consulta_gen('worker.db', 'Identificacion', 'info', 'id', f'"{id}"')
            trabajador = f"{id} {nombre} {apellido} {cedula}"
            self.tableWidget.setItem(contador_de_filas, 0, QtWidgets.QTableWidgetItem(trabajador))
            salario_actual = leew.consulta_gen('worker.db','salario','salario','id',f'{id} AND status = "Vigente"')
            self.tableWidget.setItem(contador_de_filas, 1, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(salario_actual))))
            contador_de_filas = contador_de_filas + 1


    def calcula_aumento(self):
        contador_de_filas = 0
        lineas = self.tableWidget.rowCount()
        for linea in range(lineas):

            salario_actual = float(self.tableWidget.item(contador_de_filas,1).text().replace(',','')) # aqui tomo un strin tipo 1,000.00 y lo vuelvo 1000.00 eliminando la coma (,)
            salario_nuevo = salario_actual + self.valor_absoluto.value() + salario_actual * \
                            self.val_porcentual.value() / 100
            self.tableWidget.setItem(contador_de_filas, 2, QtWidgets.QTableWidgetItem(str("{:,.2f}".format(salario_nuevo))))
            contador_de_filas = contador_de_filas + 1

    def resetear_valor_absoluto(self):
        self.valor_absoluto.setValue(0.0)

    def resetear_val_porcentual(self):
        self.val_porcentual.setValue(0.0)

    def add_salario(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar","Desea usted procesar el aumento por lote a los trabajadores?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:
                leew.backup_bd('salario_lote')
                for linea in range(self.tableWidget.rowCount()):
                    self.id = self.tableWidget.item(linea, 0).text().split(' ')[
                        0]  # con esta linea saco el id de una cadena de texto
                    salario_nuevo = self.tableWidget.item(linea, 2).text().replace(',', '')
                    leew.actualiza_salario(self.id)
                    self.entrada = f'"{self.id}","{self.fecha.date().toString("dd-MM-yyyy")}",' \
                                   f'"{salario_nuevo}","Vigente",NULL,' \
                                   f'"{self.nota.text()}"'
                    #print(self.entrada)
                    leew.introduce_gen('worker.db','salario',self.entrada)

                QtWidgets.QMessageBox.information(self, "Atención", "Salario agregado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def activa(self):

        if self.tableWidget.item(0,1).text() != self.tableWidget.item(0,2).text() and self.nota.text() != '':
            self.aceptar.setDisabled(0)
        else:
            self.aceptar.setDisabled(1)

    def exportar_cmd(self):
        libro = Workbook() # crea un libro de excel
        hoja = libro.create_sheet("Trabajadores con salarios",0) # se fija la hoja activa del libro
        lineas = self.tableWidget.rowCount() # calcula cuantas lineas tiene la tabla que se está mostrando
        for linea in range(lineas):
            fila = [self.tableWidget.item(linea,0).text(),self.tableWidget.item(linea,1).text()]
            hoja.append(fila)

        ruta = \
        QtWidgets.QFileDialog.getSaveFileName(self, 'Ruta de exportación', f'C:\\Users\\{os.environ.get("USERNAME")}',
                                              '')[0]  # *.png *.svg*.jpg

        if ruta != '':
            ruta = os.path.abspath(ruta)  # pone la ruta tipo msdos requerido por os.system
            #print(ruta)
            libro.save(ruta + '.xlsx')
            os.startfile(ruta + '.xlsx')
        else:
            libro.close()

    def close_cmd(self):
        self.close()

    def closeEvent(self, QCloseEvent):

        if self.ya_se_puede_cerrar == False:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de salir? Se perderán los datos '
                                                   'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()
                self.parentWidget().close()
                self.obj.setDisabled(False)
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()
            self.obj.setDisabled(False)