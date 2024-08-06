from costos_legales import *
import leew


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.carga_data()

        self.ya_se_puede_cerrar = False

        self.cancelar.clicked.connect(self.close_cmd)

        self.fecha = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss AP")

        self.guardar.clicked.connect(self.add_data)

        self.guardar.setDisabled(1)

        self.AFP_emp.valueChanged.connect(self.activa)
        self.AFP_trab.valueChanged.connect(self.activa)
        self.tope_sal_afp.valueChanged.connect(self.activa)
        self.nota_afp.textChanged.connect(self.activa)
        self.sfs_emp.valueChanged.connect(self.activa)
        self.sfs_trab.valueChanged.connect(self.activa)
        self.sfs_nota.textChanged.connect(self.activa)
        self.tope_sal_sfs.valueChanged.connect(self.activa)
        self.srl.valueChanged.connect(self.activa)
        self.nota_srl.textChanged.connect(self.activa)
        self.tope_sal_srl.valueChanged.connect(self.activa)
        self.infotep.valueChanged.connect(self.activa)
        self.infotep_nota.textChanged.connect(self.activa)
        self.infotep_trabajador.valueChanged.connect(self.activa)

    def carga_data(self):
        if leew.consulta_lista('worker.db', 'esquema', 'legales', 'esquema>', '"0"') != []: # verifico que hay datos antes de cargar
            last_fecha = leew.consulta_gen('worker.db','fecha','legales','status','"Vigente"')
            self.statusbar.addWidget(QtWidgets.QLabel(f'  Última vez modificado el: {last_fecha}'))
            self.AFP_emp.setValue(leew.consulta_gen('worker.db','afp_emp','legales','status','"Vigente"'))
            self.AFP_trab.setValue(leew.consulta_gen('worker.db', 'afp_trab', 'legales', 'status', '"Vigente"'))
            self.tope_sal_afp.setValue(leew.consulta_gen('worker.db', 'tope_sal_afp', 'legales', 'status', '"Vigente"'))
            self.nota_afp.setText(leew.consulta_gen('worker.db', 'afp_info', 'legales', 'status', '"Vigente"'))
            self.sfs_emp.setValue(leew.consulta_gen('worker.db', 'sfs_emp', 'legales', 'status', '"Vigente"'))
            self.sfs_trab.setValue(leew.consulta_gen('worker.db', 'sfs_trab', 'legales', 'status', '"Vigente"'))
            self.tope_sal_sfs.setValue(leew.consulta_gen('worker.db', 'tope_sal_sfs', 'legales', 'status', '"Vigente"'))
            self.sfs_nota.setText(leew.consulta_gen('worker.db', 'sfs_info', 'legales', 'status', '"Vigente"'))
            self.srl.setValue(leew.consulta_gen('worker.db', 'srl', 'legales', 'status', '"Vigente"'))
            self.tope_sal_srl.setValue(leew.consulta_gen('worker.db', 'tope_sal_srl', 'legales', 'status', '"Vigente"'))
            self.nota_srl.setText(leew.consulta_gen('worker.db', 'srl_info', 'legales', 'status', '"Vigente"'))
            self.infotep.setValue(leew.consulta_gen('worker.db', 'infotep', 'legales', 'status', '"Vigente"'))
            self.infotep_nota.setText(leew.consulta_gen('worker.db', 'infotep_info', 'legales', 'status', '"Vigente"'))
            self.infotep_trabajador.setValue(leew.consulta_gen('worker.db', 'infotep_trab', 'legales', 'status', '"Vigente"'))

    def add_data(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar","Desea usted modificar la información?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:

                self.entrada = f'NULL, "{self.AFP_emp.text()}","{self.AFP_trab.text()}","{self.tope_sal_afp.text()}","{self.nota_afp.text()}","{self.sfs_emp.text()}","{self.sfs_trab.text()}",' \
                               f'"{self.tope_sal_sfs.text()}","{self.sfs_nota.text()}","{self.srl.text()}","{self.tope_sal_srl.text()}","{self.nota_srl.text()}","{self.fecha}","Vigente",' \
                               f'"{self.infotep.text()}", "{self.infotep_nota.text()}", "{self.infotep_trabajador.text()}"'
                leew.update_legal()
                leew.introduce_gen('worker.db','legales',self.entrada)

                QtWidgets.QMessageBox.information(self, "Atención", "Modificación guardada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def activa(self):
        if self.AFP_emp.hasFocus():
            self.AFP_emp.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.AFP_trab.hasFocus():
            self.AFP_trab.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.nota_afp.hasFocus():
            self.nota_afp.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.sfs_emp.hasFocus():
            self.sfs_emp.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.sfs_trab.hasFocus():
            self.sfs_trab.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.sfs_nota.hasFocus():
            self.sfs_nota.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.srl.hasFocus():
            self.srl.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.nota_srl.hasFocus():
            self.nota_srl.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.infotep.hasFocus():
            self.infotep.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.infotep_nota.hasFocus():
            self.infotep_nota.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.infotep_trabajador.hasFocus():
            self.infotep_trabajador.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.tope_sal_srl.hasFocus():
            self.tope_sal_srl.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.tope_sal_sfs.hasFocus():
            self.tope_sal_sfs.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)
        if self.tope_sal_afp.hasFocus():
            self.tope_sal_afp.setStyleSheet("background: #ffbcbd;")
            self.guardar.setDisabled(0)

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
            else:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
            self.parentWidget().close()