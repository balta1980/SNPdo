from primerPeriodo import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_pPeriodo):
    def __init__(self,cmd, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        #super().__init__(self) lo comenté porque no se qué hace
        self.setupUi(self)

        self.actualizar_per_abierto_main = cmd

        self.ppaceptar.clicked.connect(self.agrega_perido)
        self.ppcancelar.clicked.connect(self.close_cmd)


    def agrega_perido(self):
        ''' función para agregar el primer periodo'''

        mes = self.ppdateEdit.date().toString("MM")
        anio = self.ppdateEdit.date().toString("yyyy")

        idp = '1Q' + mes + anio
        f_inicio = '01' + '-' + mes + '-' + anio
        f_fin = '15' + '-' + mes + '-' + anio
        status = 'ABIERTO'

        self.close_cmd()
        # print(idp);print(f_inicio);print(f_fin);print(status)
        try:
            #leew.introduce_periodo('"' + idp + '","' + f_inicio + '","' + f_fin + '","' + status + '", NULL')
            leew.introduce_gen('worker.db', 'periodo', f'"{idp}", "{f_inicio}", "{f_fin}", "{status}", NULL')
            QtWidgets.QMessageBox.information(self, "Atención", "Primer período agregado satisfactoriamente",
                                              QtWidgets.QMessageBox.Ok)
            self.actualizar_per_abierto_main()
        except:
            QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                          QtWidgets.QMessageBox.Ok)

    def close_cmd(self):
        self.parentWidget().close()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()