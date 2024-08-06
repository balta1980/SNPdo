from correo import *
import leew, google_correo, os
import requests

class Worker(QtCore.QObject):
    # finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(bool) #lo uso para habiltar o deshablitar boton

    def run(self):
        """Long-running task."""

        #while True:
        try:
            request = requests.get("http://www.google.com", timeout=5)

        except (requests.ConnectionError, requests.Timeout):
            print("Sin conexión a internet")
            self.progress.emit(False)

        else:
            print("Con conexión a internet")
            self.progress.emit(True)


        #self.finished.emit()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.carga_data()

        self.iniciador_verificacion()

        self.dir_correo_prueba.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")))

        self.ya_se_puede_cerrar = False

        self.verificador_de_toke_json()

        self.cancelar.clicked.connect(self.close_cmd)

        self.cambiar.clicked.connect(self.cambiar_cmd)
        self.conectar.clicked.connect(self.conectar_cmd)

        self.enviar_correo.clicked.connect(self.envia_correo_prueba)

    def iniciador_verificacion(self):
        # Step 2: Create a QThread object
        self.thread = QtCore.QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        #self.worker.finished.connect(self.thread.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.habilitador_boton)
        # Step 6: Start the thread
        self.thread.start()

    def habilitador_boton(self, n):
        if n == True:
            self.enviar_correo.setText("Enviar correo de prueba")
        else:
            self.enviar_correo.setText("No hay Internet")
            self.conectar.setDisabled(1)
            self.cambiar.setDisabled(1)
        self.enviar_correo.setDisabled(not n)

    def envia_correo_prueba(self):

        try:

            google_correo.manejo_gmail(self.dir_correo_prueba.text(),self.titulo.text(),self.mensaje.text()).gmail_create_draft_with_attachment()

            QtWidgets.QMessageBox.information(self, "Atención", "Correo enviado satisfactoriamente, revise el buzón de su correo",
                                              QtWidgets.QMessageBox.Ok)
        except:
            QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                          QtWidgets.QMessageBox.Ok)

    def carga_data(self):

        last_fecha = leew.consulta_gen('worker.db','fecha','correo','status','"Vigente"')
        self.fecha_conexion.setText(last_fecha)
        self.correo_conectado.setText(leew.consulta_gen('worker.db', 'dir_correo','correo', 'status','"Vigente"'))

    def add_data(self):

        try:

            self.entrada = f'NULL, "{self.fecha_conexion.text()}","{self.correo_conectado.text()}",NULL,NULL,"Vigente"'
            #print(self.entrada)
            leew.update_gen('worker.db','correo','status')
            leew.introduce_gen('worker.db','correo',self.entrada)

            self.ya_se_puede_cerrar = True


        except:
            QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                              QtWidgets.QMessageBox.Ok)

    def verificador_de_toke_json(self):
        if os.path.exists('token.json'):
            self.conectar.setDisabled(1)
            self.cambiar.setDisabled(0)
            self.groupBox_mensaje_prueba.setDisabled(0)

        else:
            self.conectar.setDisabled(0)
            self.cambiar.setDisabled(1)
            self.groupBox_mensaje_prueba.setDisabled(1)
            self.correo_conectado.setText("No hay un correo conectado")
            self.fecha_conexion.setText("No hay fecha para mostrar")

    def conectar_cmd(self):
        try:

            conexion = google_correo.manejo_gmail('baltazar.diaz@gmail.com', "hola 7hghg878787", 'kdkdkdkdkdk',).login_gmail()
            self.correo_conectado.setText(conexion) # en coexion está la direccion de correo que se conecta
            self.fecha_conexion.setText(QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss AP"))
            self.verificador_de_toke_json()
            self.add_data()

        except:
            QtWidgets.QMessageBox.warning(self, 'Advertencia',
                                           f'Ocurrió un error inesperado. Por favor verifique que tildó los dos permisos '
                                           f'solicitados en la página de Gmail', QtWidgets.QMessageBox.Ok)

    def cambiar_cmd(self):
        reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                               '¿Está usted seguro de borrar el correo que está configurado actualmente?'
                                               ' Se tendrá que configurar otro correo para poder enviar los recibos de nómina'
                                               , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            os.remove('token.json')
            self.conectar.setDisabled(0)
            self.cambiar.setDisabled(1)
            self.groupBox_mensaje_prueba.setDisabled(1)

    def activa(self):
        self.guardar.setDisabled(0)
        if self.dir_correo_nomina.isModified():
            self.dir_correo_nomina.setStyleSheet("background: #ffbcbd;")

        if self.clave_correo_nomina.isModified():
            self.clave_correo_nomina.setStyleSheet("background: #ffbcbd;")

        if self.nota.isModified():
            self.nota.setStyleSheet("background: #ffbcbd;")

    def close_cmd(self):
        self.close()

    def closeEvent(self, QCloseEvent):

        if self.ya_se_puede_cerrar == False:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de salir? Se perderán los datos '
                                                   'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:


                self.thread.quit()
                self.worker.deleteLater()
                QCloseEvent.accept()
                self.parentWidget().close()
            else:
                QCloseEvent.ignore()
        else:


            self.thread.quit()
            self.worker.deleteLater()
            QCloseEvent.accept()
            self.parentWidget().close()