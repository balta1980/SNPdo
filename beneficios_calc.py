from beneficios import *
import leew
#todo a este ventana y a la bd de datos falta agregar el máxmimo de ley de horas extras por trimestre que son 80

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        if len(leew.consulta_lista('worker.db', 'idb', 'beneficios', 'idb>', '1')) > 0:# para evitar error por no existir data

            self.carga_data()

        self.ya_se_puede_cerrar = False

        self.cancelar.clicked.connect(self.close_cmd)

        self.fecha = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss AP")

        self.guardar.clicked.connect(self.add_data)

        self.guardar.setDisabled(1)

        self.valor_h_extra.valueChanged.connect(self.activa)
        self.rango_exceso.valueChanged.connect(self.activa)
        self.valor_he_exceso.valueChanged.connect(self.activa)
        self.info_he.textChanged.connect(self.activa) #forzando el mmetodo textChanged.connect

        self.valor_h_nocturna.valueChanged.connect(self.activa)
        self.inicio_h_nocturna.timeChanged.connect(self.activa)
        self.fin_h_nocturna.timeChanged.connect(self.activa)
        self.info_hora_nocturna.textChanged.connect(self.activa)

        self.valor_trab_descanso.valueChanged.connect(self.activa)
        self.info_trab_descanso.textChanged.connect(self.activa)

        self.dias_por_mes.valueChanged.connect(self.activa)
        self.info_dias_mes.textChanged.connect(self.activa)

        self.horas_por_dia.valueChanged.connect(self.activa)
        self.info_horas_dia.textChanged.connect(self.activa)

    def carga_data(self):
        ''' Esta funcion carga la data de la planilla'''

        last_fecha = leew.consulta_gen('worker.db','fecha','beneficios','status','"Vigente"')
        self.statusbar.addWidget(QtWidgets.QLabel(f'  Última vez modificado el: {last_fecha}'))
        self.valor_h_extra.setValue(leew.consulta_gen('worker.db','valor_h_extra1','beneficios','status','"Vigente"'))
        self.rango_exceso.setValue(leew.consulta_gen('worker.db', 'rango_h_e1', 'beneficios', 'status', '"Vigente"'))
        self.valor_he_exceso.setValue(leew.consulta_gen('worker.db', 'valor_h_extra2', 'beneficios', 'status', '"Vigente"'))
        self.info_he.setPlainText(
            leew.consulta_gen('worker.db', 'info_h_extra', 'beneficios', 'status', '"Vigente"'))

        self.valor_h_nocturna.setValue(leew.consulta_gen('worker.db','valor_h_noct','beneficios','status','"Vigente"'))
        hora_inicio = leew.consulta_gen('worker.db', 'h_i_noct_hora', 'beneficios', 'status', '"Vigente"')
        min_inicio = leew.consulta_gen('worker.db', 'h_i_noct_min', 'beneficios', 'status', '"Vigente"')
        self.inicio_h_nocturna.setTime(QtCore.QTime(hora_inicio,min_inicio,0,0))
        hora_fin = leew.consulta_gen('worker.db', 'h_f_noct_hora', 'beneficios', 'status', '"Vigente"')
        min_fin = leew.consulta_gen('worker.db', 'h_f_noct_min', 'beneficios', 'status', '"Vigente"')
        self.fin_h_nocturna.setTime(QtCore.QTime(hora_fin, min_fin, 0, 0))
        self.info_hora_nocturna.setPlainText(
            leew.consulta_gen('worker.db', 'info_h_noct', 'beneficios', 'status', '"Vigente"'))

        self.valor_trab_descanso.setValue(
            leew.consulta_gen('worker.db', 'valor_trab_desc', 'beneficios', 'status', '"Vigente"'))
        self.info_trab_descanso.setPlainText(
            leew.consulta_gen('worker.db', 'info_trab_desc', 'beneficios', 'status', '"Vigente"'))

        self.dias_por_mes.setValue(
            leew.consulta_gen('worker.db', 'dias_mes', 'beneficios', 'status', '"Vigente"'))
        self.info_dias_mes.setPlainText(
            leew.consulta_gen('worker.db', 'info_dias_mes', 'beneficios', 'status', '"Vigente"'))
        self.horas_por_dia.setValue(leew.consulta_gen('worker.db', 'horas_dia', 'beneficios', 'status', '"Vigente"'))
        self.info_horas_dia.setPlainText(leew.consulta_gen('worker.db', 'info_horas_dia', 'beneficios', 'status', '"Vigente"'))

    def add_data(self):
        reply = QtWidgets.QMessageBox.question(self,"Para continuar","Desea usted modificar la información?"
                                               ,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            try:

                self.entrada = f'NULL, "{self.valor_h_extra.text()}","{self.rango_exceso.text()}","{self.valor_he_exceso.text()}","{self.info_he.toPlainText()}","{self.valor_h_nocturna.text()}",' \
                               f'"{str(self.inicio_h_nocturna.time().hour())}","{str(self.inicio_h_nocturna.time().minute())}","{str(self.fin_h_nocturna.time().hour())}","{str(self.fin_h_nocturna.time().minute())}",' \
                               f'"{self.info_hora_nocturna.toPlainText()}", "{self.valor_trab_descanso.text()}","{self.info_trab_descanso.toPlainText()}","{self.dias_por_mes.text()}","{self.info_dias_mes.toPlainText()}",' \
                               f'"{self.horas_por_dia.text()}", "{self.info_horas_dia.toPlainText()}", "{self.fecha}","Vigente"'
                leew.update_beneficios()
                leew.introduce_gen('worker.db','beneficios',self.entrada)

                QtWidgets.QMessageBox.information(self, "Atención", "Modificación guardada satisfactoriamente",
                                                  QtWidgets.QMessageBox.Ok)
                self.ya_se_puede_cerrar = True
                self.close()

            except:
                QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def activa(self):
        self.guardar.setDisabled(0)
        if self.valor_h_extra.hasFocus():
            self.valor_h_extra.setStyleSheet("background: #ffbcbd;")
        if self.rango_exceso.hasFocus():
            self.rango_exceso.setStyleSheet("background: #ffbcbd;")
        if self.valor_he_exceso.hasFocus():
            self.valor_he_exceso.setStyleSheet("background: #ffbcbd;")
        if self.valor_he_exceso.hasFocus():
            self.valor_he_exceso.setStyleSheet("background: #ffbcbd;")
        if self.info_he.hasFocus():
            self.info_he.setStyleSheet("background: #ffbcbd;")
        if self.valor_h_nocturna.hasFocus():
            self.valor_h_nocturna.setStyleSheet("background: #ffbcbd;")
        if self.inicio_h_nocturna.hasFocus():
            self.inicio_h_nocturna.setStyleSheet("background: #ffbcbd;")
        if self.fin_h_nocturna.hasFocus():
            self.fin_h_nocturna.setStyleSheet("background: #ffbcbd;")
        if self.info_hora_nocturna.hasFocus():
            self.info_hora_nocturna.setStyleSheet("background: #ffbcbd;")
        if self.valor_trab_descanso.hasFocus():
            self.valor_trab_descanso.setStyleSheet("background: #ffbcbd;")
        if self.info_trab_descanso.hasFocus():
            self.info_trab_descanso.setStyleSheet("background: #ffbcbd;")
        if self.dias_por_mes.hasFocus():
            self.dias_por_mes.setStyleSheet("background: #ffbcbd;")
        if self.info_dias_mes.hasFocus():
            self.info_dias_mes.setStyleSheet("background: #ffbcbd;")
        if self.horas_por_dia.hasFocus():
            self.horas_por_dia.setStyleSheet("background: #ffbcbd;")
        if self.info_horas_dia.hasFocus():
            self.info_horas_dia.setStyleSheet("background: #ffbcbd;")

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