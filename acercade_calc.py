from acercade import *
import globales, leew

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self, *args, **kwargs):
        # cuando bloqueo vale 0 esporque se usa para el primer ingreo
        # cuando bloqueo vale 1 esporque se instó para bloquear
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        version_base_datos = leew.consulta_gen('worker.db', 'version', 'datos_bd', 'estatus', '"Vigente"')
        fecha_base_datos = leew.consulta_gen('worker.db', 'fecha', 'datos_bd', 'estatus', '"Vigente"')
        self.texto.setText(f"Baltazar José Díaz Suárez\nCorreo: snpnomina@gmail.com\n"
                           f"SNPDO y su logo son marcas registradas\nVersión: {globales.version}\nVersión BD: "
                           f"{version_base_datos}\n{fecha_base_datos}")

        self.show()