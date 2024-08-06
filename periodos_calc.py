from periodos import *


import leew, calendar, primerPeriodo_calc

class MainWindow(QtWidgets.QMainWindow, Ui_Periodos):
    def __init__(self,cmd, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # para usar objetos del widget padre, en este caso main
        self.main_instancia = args[0]

        self.actualizar_per_abierto_main = cmd


        # Llenando las filas
        try: # para atrapar una BD de vacia
            indices_en_bd = leew.consulta_lista('worker.db','indice','periodo','indice>','1')
            #print(indices_en_bd)
        except:
            indices_en_bd = []
        #print(indices_en_bd)
        self.tableWidget.setRowCount(len(indices_en_bd))

        indices_en_bd.reverse() # esto para que el ultimo periodo salga de primero

        # estas lineas de abajo son para estirar las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        contador = 0
        for indice in indices_en_bd:
            indice = str(indice)
            idp = leew.consulta_gen('worker.db', 'idp', 'periodo','indice', indice)
            self.tableWidget.setItem(contador, 0, QtWidgets.QTableWidgetItem(idp))
            fecha_i = leew.consulta_gen('worker.db', 'f_inicio', 'periodo','indice', indice)
            self.tableWidget.setItem(contador, 1, QtWidgets.QTableWidgetItem(fecha_i))
            fecha_f = leew.consulta_gen('worker.db', 'f_fin', 'periodo','indice', indice)
            self.tableWidget.setItem(contador, 2, QtWidgets.QTableWidgetItem(fecha_f))
            estatus = leew.consulta_gen('worker.db', 'status', 'periodo','indice', indice)
            self.tableWidget.setItem(contador, 3, QtWidgets.QTableWidgetItem(estatus))
            contador = contador + 1

        self.Crear_periodo.clicked.connect(self.add_periodo)
        self.cerrar.clicked.connect(self.close_cmd)
        self.Crear_periodo.setFocus()
        self.Crear_periodo.setDefault(1)

        #self.show() no se usa show cuando se usa mdi

    def add_periodo(self):

        if leew.consulta_lista('worker.db','indice','periodo','indice>','0') == []:
            self.pop_up() # en el caso de que la base de datos esté vacía
        else:

            list_peridos = leew.consulta_lista('worker.db','f_fin','periodo','indice>','1') # ojo mayor o igual
            #print(list_peridos)
            ultimo_periodo = list_peridos[len(list_peridos) - 1] # mas que ultimo periodo es ultimo f_fin
            dia, mes, anio = [str(v) for v in ultimo_periodo.split("-")]

            # dia, mes, anio = (31,12,2018)
            if int(dia) < 16:
                idp = '2Q' + mes + anio
                f_inicio = '16-' + mes + '-' + anio
                f_fin = str(calendar.monthlen(int(anio), int(mes))) + '-' + mes + '-' + anio
                status = 'ABIERTO'
            else:
                if int(mes) > 0 and int(mes) < 9 or int(mes) == 12:
                    anio, mes, = calendar.nextmonth(int(anio), int(mes))
                    idp = '1Q' + '0' + str(mes) + str(anio)
                    f_inicio = '1-' + '0' + str(mes) + '-' + str(anio)
                    f_fin = '15' + '-' + '0' + str(mes) + '-' + str(anio)
                    status = 'ABIERTO'
                else:
                    anio, mes, = calendar.nextmonth(int(anio), int(mes))
                    idp = '1Q' + str(mes) + str(anio)
                    f_inicio = '1-' + str(mes) + '-' + str(anio)
                    f_fin = '15' + '-' + str(mes) + '-' + str(anio)
                    status = 'ABIERTO'

            # print(idp);print(f_inicio);print(f_fin);print(status)
            try:
                leew.introduce_periodo('"' + idp + '","' + f_inicio + '","' + f_fin + '","' + status + '", NULL')
                QtWidgets.QMessageBox.information(self, "Atención", "Período agregado satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)
            self.close()
            self.parentWidget().close()
            self.actualizar_per_abierto_main()

    def pop_up(self):
        #self.close()
        #self.parentWidget().close()
        #primerPeriodo_calc.MainWindow(self)
        self.main_instancia.mdiArea.addSubWindow(primerPeriodo_calc.MainWindow(self.actualizar_per_abierto_main,self)).show()
        self.actualizar_per_abierto_main()
        self.close_cmd()

    def close_cmd(self):
        self.parentWidget().close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()