#pyuic5 segunda.ui -o segunda.py
#pyrcc5 -o recurso_rc.py recurso.qrc


from inicio_ui import *

import leew, webbrowser, os, temas, globales, shutil
import periodos_calc, diaNoLaborables_calc, vacaciones_calc, sal_min_calc, islr_calc,\
list_trab_calc, acceso_calc, correo_calc, list_hora_extra_calc, horas_extra_calc, list_inasis_calc, inasis_calc, salario_nuevo_calc,\
dotacion_calc, costos_legales_calc, beneficios_calc, tabla_nomina_calc, control_asistencia_calc, inf_tss_calc,\
comisiones_calc, list_comisiones_calc, list_otras_rem_calc, otras_rem_calc, tabla_nomina_individual_calc, sal_lote_calc, info_empresa_calc,\
list_usuarios_calc, listado_nacionalidades_calc, resumen_recibos_calc, carta_trabajo_calc, prestamos_calc, acercade_calc,\
list_rem_otros_empleadores_calc, rem_otros_empleadores_calc, indemnizaciones_calc, list_indemnizaciones_calc,\
tabla_part_beneficios_calc, tabla_liquidacion_calc

''' en QT6 esto viene por defecto
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
'''
QtWidgets.QApplication.setStyle("fusion")
class MainWindowApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.showMaximized()
        self.setWindowTitle(f"Programa de nómina SNPdo versión {globales.version}")

        self.ya_se_puede_cerrar = False
        self.usuario = '' # este valor será sobre escrito con el modulo acceso llamado más abajo

        self.actionCerrar.triggered.connect(self.actualizar)
        self.actionDatos_de_la_sociedad.triggered.connect(self.cmd_info_emp)
        self.actionPeriodos.triggered.connect(self.periodos_calc)
        self.actionD_as_No_laborables.triggered.connect(self.diaNoLab)
        self.actionDefinir_vacaciones.triggered.connect(self.vac)
        self.actionDefinir_salario_m_nimo.triggered.connect(self.sal_min)
        self.actionListado_de_nacionalidades.triggered.connect(self.listado_nac)
        self.actionDefinir_tabla_ISLR.triggered.connect(self.islr)
        self.actionDefinici_n_de_riesgo_laboral.setVisible(False)
        self.actionListado_de_trabajadores.triggered.connect(self.list_trab)
        self.actionCascada.triggered.connect(self.mdiArea.cascadeSubWindows)
        self.actionMosaico.triggered.connect(self.mdiArea.tileSubWindows)
        self.actionClaro.triggered.connect(self.tema_plano)
        self.actionObscuro_2.triggered.connect(self.tema_obscuro)
        self.actionConfigurar_correo_de_n_mina.triggered.connect(self.correo)
        self.actionPantalla_completa.triggered.connect(self.toggleFullScreen)
        self.actionBloquear.triggered.connect(self.bloquear)
        self.actionListado_de_horas_extra.triggered.connect(self.listado_horas_extras)
        self.actionRegistro_de_horas_extra.triggered.connect(self.registro_horas_extras)
        self.actionRegistro_de_inasistencia_2.triggered.connect(self.registro_inasistencia)
        self.actionListado_de_inasistencias.triggered.connect(self.listado_inasis)
        self.actionRegistro_de_salario_nuevo.triggered.connect(self.nuevo_salario_cmd)
        self.actionRegistro_de_dotaci_n.triggered.connect(self.dotacion)
        self.actionCostos_laborales.triggered.connect(self.costos_legales)
        self.actionBeneficios_seg_n_ley.triggered.connect(self.beneficios)
        self.actionN_mina_quincenal.triggered.connect(self.tabla_nomina)
        self.actionFormato_de_asistencia.triggered.connect(self.formato_asistencia)
        self.actionInforme_TSS.triggered.connect(self.informe_tss)
        self.actionResumen_de_recibos.triggered.connect(self.resumen_de_recibos)
        self.actionRegistro_de_otra_remuneraci_n_2.triggered.connect(self.registro_otras_remuneraciones)
        self.actionListado_otras_remun.triggered.connect(self.listado_otras_remuneraciones)
        self.actionRegistro_de_comisi_n.triggered.connect(self.registro_comisiones)
        self.actionListado_de_comisiones.triggered.connect(self.listado_comisiones)
        self.actionLiquidaci_n.triggered.connect(self.tabla_terminacion_cotrato)
        self.actionN_mina_Individual.triggered.connect(self.tabla_nomina_individual)
        self.actionPago_utilidades.triggered.connect(self.tabla_part_beneficios_cmd)
        self.actionVer_info.triggered.connect(self.comportamiento_info)
        self.actionRegistro_de_salario_por_lote.triggered.connect(self.salario_lote)
        self.actionRegistro_de_pr_stamo_adelanto.triggered.connect(self.listado_prestamos)
        self.actionListado_de_usuarios.triggered.connect(self.list_usuarios)
        self.actionCarta_de_trabajo.triggered.connect(self.carta_de_trabajo)
        self.actionContenido_de_la_Ayuda.triggered.connect(self.abrir_ayuda)
        self.actionHaga_una_donaci_n.triggered.connect(self.donacion)
        self.actionAcerca_de_SNP.triggered.connect(self.muestra_acercade)
        self.actionListado_rem_otro_empleador.triggered.connect(self.listado_remun_otros_empleadores)
        self.actionRegistro_rem_otro_empleador.triggered.connect(self.registro_remun_otro_empleador)
        self.actionRegistro_indemnizaciones.triggered.connect(self.registro_indemnizacion)
        self.actionListado_de_indemnizaciones_abiertas.triggered.connect(self.listado_indemnizaciones)
        self.actionImportar_BD.triggered.connect(self.importar_base_datos)
        self.actionGuardar_BD_como.triggered.connect(self.exportar_base_datos)
        self.crea_acciones()
        self.toolBar_nav.setDisabled(1)
        self.mdiArea.subWindowActivated.connect(self.verifica_menu)


        #short cuts
        self.actionPantalla_completa.setShortcut("F11")
        self.actionBloquear.setShortcut("F12")
        self.actionPeriodos.setShortcut("F2")
        self.actionListado_de_trabajadores.setShortcut("F3")
        self.actionN_mina_quincenal.setShortcut("F4")
        self.actionContenido_de_la_Ayuda.setShortcut("F1")

        #proceso de log in

        acceso_calc.MainWindowApp(self)
        #print(self.usuario) # aqui el valor es igual a '', pero cuando se ejecutan los comandos de abajo ya está actualizado al usuario loggeado


        # informacion primer periodo abierto

        self.info_primer_per_abierto = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.info_primer_per_abierto)
        self.carga_inf_primer_per_abierto()

        # para mostrar nombre de la empresa

        self.empresa_activa = QtWidgets.QLabel("")
        self.statusbar.addWidget(self.empresa_activa)
        self.carga_empresa_activa()


        self.actualiza_info() # actualiza info cumpleanios y dias feriados

    def crea_acciones(self):
        self.toolBar_nav = self.addToolBar("Navegación")

        self.flecha_izq = QtWidgets.QAction(QtGui.QIcon('iconos/flecha_izq.png'), '')
        self.flecha_izq.setToolTip("Retrocede un registro")
        self.toolBar_nav.addAction(self.flecha_izq)

        self.flecha_der = QtWidgets.QAction(QtGui.QIcon('iconos/flecha_derecha.png'),'')
        self.flecha_der.setToolTip("Avanza un registro")
        self.toolBar_nav.addAction(self.flecha_der)

        self.flecha_izq_fin = QtWidgets.QAction(QtGui.QIcon('iconos/flecha_izq_fin.png'), '')
        self.flecha_izq_fin.setToolTip("Muestra el primer registro")
        self.toolBar_nav.addAction(self.flecha_izq_fin)

        self.flecha_der_fin = QtWidgets.QAction(QtGui.QIcon('iconos/flecha_der_fin.png'), '')
        self.flecha_der_fin.setToolTip("Muestra el último registro")
        self.toolBar_nav.addAction(self.flecha_der_fin)

        self.nuevo_doc = QtWidgets.QAction(QtGui.QIcon('iconos/nuevo.png'),'')
        self.nuevo_doc.setToolTip("Crea un registro o documento nuevo")
        self.toolBar_nav.addAction(self.nuevo_doc)

        self.letrero = QtWidgets.QLabel('')
        self.letrero.setToolTip("Muestra la ventana que es controlada por los botones del menú")
        self.letrero.setStyleSheet('font: italic 12pt "MS Sans Serif";color: blue;')
        self.toolBar_nav.addWidget(self.letrero)

    def verifica_menu(self):
        subwindows_activas = self.mdiArea.subWindowList()
        subwindows_autorizadas = ["Registro de inasistencia", "Registro de horas extras", "Registro de comisión",
                                  'Registro de otras remuneraciones', "Registro de remuneración de otros empleadores",
                                  "Registro de indemnizaciones"]
        if subwindows_activas != []:  # verifico que haya al menos una subwindows abierta
            if self.mdiArea.currentSubWindow().windowTitle() in subwindows_autorizadas: # para activat toolbar cuando me interese
                self.toolBar_nav.setDisabled(0)
                self.letrero.setText(self.mdiArea.currentSubWindow().windowTitle())
            else:
                self.toolBar_nav.setDisabled(1)
                self.letrero.setText('')

        else:
            self.toolBar_nav.setDisabled(1)

    def carga_empresa_activa(self):
        nombre_empre_en_bd = leew.consulta_gen('worker.db', 'nombre_sociedad','info_sociedad', 'estatus', '"Vigente"')
        if nombre_empre_en_bd == None:
            self.empresa_activa.setText(" Empresa Nueva ")
        else:
            self.empresa_activa.setText(f" {nombre_empre_en_bd} ")
            self.empresa_activa.setStyleSheet("background: #0088AA;border-radius:3;")

    def carga_inf_primer_per_abierto(self):
        if leew.consultaPer_top('worker.db') != []:
            primer_per_abierto = leew.consultaPer_top('worker.db')[0]
            self.info_primer_per_abierto.setStyleSheet("background: #58FA82;border-radius:3;")
        else:
            primer_per_abierto = 'No hay periodos abiertos'
            self.info_primer_per_abierto.setStyleSheet("background:#FA5858 ;border-radius:3;")

        self.info_primer_per_abierto.setText(f"Primer periodo abierto: {primer_per_abierto}")

    def correo(self):
        ventana_correo = self.mdiArea.addSubWindow((correo_calc.MainWindow(self)))
        #ventana_correo.setWindowFlags(QtCore.Qt.WindowFrameSection)
        ventana_correo.show()

    def actualizar(self):
        self.close()

    def cmd_info_emp(self):
        self.mdiArea.addSubWindow(info_empresa_calc.MainWindow(self)).show()

    def periodos_calc(self):
        self.mdiArea.addSubWindow(periodos_calc.MainWindow(self.carga_inf_primer_per_abierto, self)).show()

    def diaNoLab(self):

        self.mdiArea.addSubWindow(diaNoLaborables_calc.MainWindow(self)).show()
        #diaNoLaborables_calc.MainWindow(self) este comando lo usaba cuando no usaba MDI

    def vac(self):
        self.mdiArea.addSubWindow(vacaciones_calc.MainWindow(self)).show()

    def sal_min(self):
        self.mdiArea.addSubWindow(sal_min_calc.MainWindow(self)).show()

    def islr(self):
        self.mdiArea.addSubWindow(islr_calc.MainWindow(self)).show()

    def listado_nac(self):
        self.obj =self.actionListado_de_nacionalidades  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(listado_nacionalidades_calc.MainWindow(self.obj,self,user = self.usuario)).show()
        self.obj = self.actionListado_de_nacionalidades.setDisabled(True)

    def list_trab(self):

        self.obj = self.mdiArea # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionListado_de_trabajadores # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(list_trab_calc.MainWindow(self.obj,self.obj2,self, user = self.usuario)).show()
        self.actionListado_de_trabajadores.setDisabled(True)
        #print(self.usuario) # aqui ya tiene el valor del usuario logeado

    def tema_obscuro(self):
        self.setStyleSheet(temas.oscuro)

    def tema_plano(self):
        self.setStyleSheet(temas.plano)

    def toggleFullScreen(self):#para hacer el programa full screen o no
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen()

    def bloquear(self):
        bloqueo = acceso_calc.MainWindowApp(self,bloqueo=1)
        bloqueo.usuario.setText(self.usuario)
        bloqueo.usuario.setReadOnly(True)
        bloqueo.usuario.setStyleSheet("background-color: #0088AA;")
        bloqueo.cerrar.setDisabled(1)

    def listado_horas_extras(self):

        self.obj = self.actionListado_de_horas_extra  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.obj2 = self.actionRegistro_de_horas_extra
        self.mdiArea.addSubWindow(list_hora_extra_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.actionListado_de_horas_extra.setDisabled(True)
        self.actionRegistro_de_horas_extra.setDisabled(True)
        #print(self.mdiArea.currentSubWindow().windowTitle())

    def registro_horas_extras(self):

        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionListado_de_horas_extra  # para poder habilitarlo de nuevo desde el listado de trabajadores
            self.obj2 = self.actionRegistro_de_horas_extra
            self.mdiArea.addSubWindow(horas_extra_calc.MainWindow(self.obj,self.obj2, self)).show()
            self.actionListado_de_horas_extra.setDisabled(True)
            self.actionRegistro_de_horas_extra.setDisabled(True)
            #print(self.mdiArea.currentSubWindow().windowTitle())

    def listado_inasis(self):
        self.obj = self.actionListado_de_inasistencias
        self.obj2 = self.actionRegistro_de_inasistencia_2  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(list_inasis_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.actionListado_de_inasistencias.setDisabled(True)
        self.actionRegistro_de_inasistencia_2.setDisabled(True)

    def registro_inasistencia(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionListado_de_inasistencias  # para poder habilitarlo de nuevo desde el listado de trabajadores
            self.obj2 = self.actionRegistro_de_inasistencia_2
            self.mdiArea.addSubWindow(inasis_calc.MainWindow(self.obj, self.obj2, self)).show()
            self.actionListado_de_inasistencias.setDisabled(True)
            self.actionRegistro_de_inasistencia_2.setDisabled(True)

    def listado_comisiones(self):
        self.obj = self.actionListado_de_comisiones
        self.obj2 = self.actionRegistro_de_comisi_n
        self.mdiArea.addSubWindow(list_comisiones_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.obj = self.actionListado_de_comisiones.setDisabled(True)
        self.obj2 = self.actionRegistro_de_comisi_n.setDisabled(True)

    def registro_comisiones(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionListado_de_comisiones
            self.obj2 = self.actionRegistro_de_comisi_n
            self.mdiArea.addSubWindow(comisiones_calc.MainWindow(self.obj, self.obj2, self)).show()
            self.obj = self.actionListado_de_comisiones.setDisabled(True)
            self.obj2 = self.actionRegistro_de_comisi_n.setDisabled(True)

    def listado_otras_remuneraciones(self):
        self.obj = self.actionListado_otras_remun
        self.obj2 = self.actionRegistro_de_otra_remuneraci_n_2
        self.mdiArea.addSubWindow(list_otras_rem_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.obj.setDisabled(True)
        self.obj2.setDisabled(True)

    def registro_otras_remuneraciones(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionListado_otras_remun
            self.obj2 = self.actionRegistro_de_otra_remuneraci_n_2
            self.mdiArea.addSubWindow(otras_rem_calc.MainWindow(self.obj, self.obj2, self)).show()
            self.obj.setDisabled(True)
            self.obj2.setDisabled(True)

    def listado_remun_otros_empleadores(self):
        self.obj = self.actionListado_rem_otro_empleador
        self.obj2 = self.actionRegistro_rem_otro_empleador
        self.mdiArea.addSubWindow(list_rem_otros_empleadores_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.obj.setDisabled(True)
        self.obj2.setDisabled(True)

    def registro_remun_otro_empleador(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionListado_rem_otro_empleador
            self.obj2 = self.actionRegistro_rem_otro_empleador
            self.mdiArea.addSubWindow(rem_otros_empleadores_calc.MainWindow(self.obj, self.obj2, self)).show()
            self.obj.setDisabled(True)
            self.obj2.setDisabled(True)

    def listado_indemnizaciones(self):
        self.obj = self.actionListado_de_indemnizaciones_abiertas
        self.obj2 = self.actionRegistro_indemnizaciones
        self.mdiArea.addSubWindow(list_indemnizaciones_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.obj.setDisabled(True)
        self.obj2.setDisabled(True)

    def registro_indemnizacion(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionListado_de_indemnizaciones_abiertas
            self.obj2 = self.actionRegistro_indemnizaciones
            self.mdiArea.addSubWindow(indemnizaciones_calc.MainWindow(self.obj, self.obj2, self)).show()
            self.obj.setDisabled(True)
            self.obj2.setDisabled(True)

    def listado_prestamos(self):
        self.obj = self.mdiArea  # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionRegistro_de_pr_stamo_adelanto  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(prestamos_calc.MainWindow(self.obj, self.obj2, self)).show()
        self.actionRegistro_de_pr_stamo_adelanto.setDisabled(True)

    def nuevo_salario_cmd(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.mdiArea.addSubWindow(salario_nuevo_calc.MainWindow(self)).show()

    def salario_lote(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.obj = self.actionRegistro_de_salario_por_lote
            self.mdiArea.addSubWindow(sal_lote_calc.MainWindow(self.obj,self)).show()
            self.actionRegistro_de_salario_por_lote.setDisabled(True)

    def dotacion(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')
        lista_trabajadores_activos = leew.consulta_lista('worker.db', 'id', 'info', 'Estatus', '"Activo"')
        if lista_de_trabajadores_registrados == [] or lista_trabajadores_activos == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados o activos, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.mdiArea.addSubWindow(dotacion_calc.MainWindow(self)).show()

    def costos_legales(self):
        self.mdiArea.addSubWindow(costos_legales_calc.MainWindow(self)).show()

    def beneficios(self):
        self.mdiArea.addSubWindow(beneficios_calc.MainWindow(self)).show()

    def tabla_nomina(self):

        self.obj = self.mdiArea # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionN_mina_quincenal # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(tabla_nomina_calc.MainWindow(self.carga_inf_primer_per_abierto,self.obj,self.obj2,self, user = self.usuario)).show()
        self.actionN_mina_quincenal.setDisabled(True)

    def tabla_nomina_individual(self):
        self.obj = self.mdiArea  # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionN_mina_Individual  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(
            tabla_nomina_individual_calc.MainWindow(self.carga_inf_primer_per_abierto, self.obj, self.obj2, self,
                                         user=self.usuario)).show()
        self.actionN_mina_Individual.setDisabled(True)

    def tabla_part_beneficios_cmd(self):# pago de utilidades
        self.obj = self.mdiArea  # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionPago_utilidades  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(
            tabla_part_beneficios_calc.MainWindow(self.obj, self.obj2, self,
                                                    user=self.usuario)).show()
        self.actionPago_utilidades.setDisabled(True)

    def formato_asistencia(self):
        self.mdiArea.addSubWindow(control_asistencia_calc.MainWindow(self)).show()

    def informe_tss(self):
        self.mdiArea.addSubWindow(inf_tss_calc.MainWindow(self)).show()

    def resumen_de_recibos(self):
        self.mdiArea.addSubWindow(resumen_recibos_calc.MainWindow(self)).show()

    def carta_de_trabajo(self):
        lista_de_trabajadores_registrados = leew.consulta_lista('worker.db', 'id', 'info', 'id >', '"0"')

        if lista_de_trabajadores_registrados == []:
            QtWidgets.QMessageBox.warning(self, "Alerta",
                                          "No hay trabajadores registrados, registre a un nuevo trabajador"
                                          , QtWidgets.QMessageBox.Ok)
        else:
            self.mdiArea.addSubWindow(carta_trabajo_calc.MainWindow(self)).show()

    def tabla_terminacion_cotrato(self):
        self.obj = self.mdiArea  # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionLiquidaci_n  # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.mdiArea.addSubWindow(
            tabla_liquidacion_calc.MainWindow( self.obj, self.obj2, self,
                                                    user=self.usuario)).show()
        self.actionLiquidaci_n.setDisabled(True)


    def actualiza_info(self):

        fecha_hoy = QtCore.QDate.currentDate().toString('dd-MM-yyyy')
        hoy_dia, hoy_mes, hoy_anio = fecha_hoy.split('-')
        # dias no laborables
        lista_dias_no_laborables = leew.consulta_lista('worker.db','fecha','dia_no_laborables','indice >','0')
        #print(lista_dias_no_laborables)
        self.feriados_mes.clear()
        for dia_no_lab in lista_dias_no_laborables:
            dia,mes, anio, = dia_no_lab.split('-')
            if mes == hoy_mes and anio == hoy_anio:
                nombre = leew.consulta_gen('worker.db','nombre','dia_no_laborables','fecha',f'"{dia_no_lab}"')
                self.feriados_mes.addItem(f'{dia_no_lab} {nombre}')
        # cumpleanios
        self.cumple_mes.clear()
        lista_trab_activos = leew.consulta_lista('worker.db','id','info','Estatus', '"Activo"')
        for id_trab_activo in lista_trab_activos:
            id_trab_activo = str(id_trab_activo)
            cumple_anios = leew.consulta_gen('worker.db', 'fecha_nacimiento', 'info', 'id', id_trab_activo)
            dia,mes,anio, = cumple_anios.split('-')
            if mes == hoy_mes:
                nombre = leew.consulta_gen('worker.db', 'nombre', 'info', 'id', f'"{id_trab_activo}"')
                apellido = leew.consulta_gen('worker.db', 'apellido', 'info', 'id', f'"{id_trab_activo}"')
                self.cumple_mes.addItem(f'{nombre} {apellido}, {cumple_anios}')

        # proximo periodo de vacacion abierto
        dias_vac_lista = leew.consulta_gen('worker.db','lista_dias','vacaciones','status','"ABIERTO" LIMIT 1')
        #print(dias_vac_lista)
        self.prox_per_vac.clear()
        if dias_vac_lista != None:
            dias_vac_lista = dias_vac_lista[1:len(dias_vac_lista) - 1]
            self.prox_per_vac.addItem(f'días de vacaciones: {dias_vac_lista}')

        else:
            self.prox_per_vac.addItem('No hay periodos de vacaciones abiertos')

        # trabajadores activos, reposo.
        self.estatus_trab_info.clear()
        cant_trab_activos = str(len(leew.consulta_lista('worker.db','id','info','Estatus','"Activo"')))
        cant_trad_desin = str(len(leew.consulta_lista('worker.db','id','info','Estatus','"Desincorporado"')))
        cant_trad_reposo = str(len(leew.consulta_lista('worker.db', 'id','info','Estatus', '"Reposo"')))
        self.estatus_trab_info.addItem(f'Trabajadores activos: {cant_trab_activos}')
        self.estatus_trab_info.addItem(f'Trabajadores en reposo: {cant_trad_reposo}')
        self.estatus_trab_info.addItem(f'Trabajadores desincorporados: {cant_trad_desin}')

    def comportamiento_info(self):
        # funcion para ocultar o no el dock info
        if self.actionVer_info.isChecked() != True:
            self.dockWidget.hide()
        else:
            self.dockWidget.setHidden(0)

    def list_usuarios(self):

        self.obj = self.mdiArea # este widget se manda como argumento en la funcion de abajo
        self.obj2 = self.actionListado_de_usuarios # para poder habilitarlo de nuevo desde el listado de trabajadores
        self.obj3 = self.menubar
        self.mdiArea.addSubWindow(list_usuarios_calc.MainWindow(self.obj,self.obj2, self.obj3,self, user = self.usuario)).show()
        self.actionListado_de_usuarios.setDisabled(True)

    def abrir_ayuda(self):
        #print(os.path.dirname(os.path.abspath(__file__)) + '\\ayuda\\ayuda.html')
        webbrowser.open_new_tab('https://www.snpdo.com')

    def donacion(self):
        webbrowser.open_new_tab('https://www.paypal.com/donate/?hosted_button_id=8BXHU2CADSHEY')

    def muestra_acercade(self):
        ventana_acercade = acercade_calc.MainWindow(self)

    def importar_base_datos(self):
        ruta_bd_a_importar = QtWidgets.QFileDialog.getOpenFileName(self,'', f'C:\\Users\\{os.environ.get("USERNAME")}', '*.db')[0]
        ruta_bd_a_importar = os.path.abspath(ruta_bd_a_importar)
        #print(ruta_bd_a_importar)
        ruta_de_bd = fr'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo'
        ruta_destino = fr"{ruta_de_bd}\\worker.db"

        if ruta_bd_a_importar == os.path.dirname(os.path.abspath(__file__)):# esto sucede cuando se presiona el boton cancelar en la ventana de seleccion de archivo
            pass

        else:

            #print(ruta_de_instalacio_prog)

            #print(comando)
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de importar la base de datos?. La base de datos '
                                                   'actual será sobre escrita y se perderan todos los datos. Luego de efectuada'
                                                   'la importación el programa se cerrará y usted deberá abrirlo nuevamente'
                                                   , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                try:
                    leew.backup_bd("importacionBD")

                    #shutil.copyfile(ruta_bd_a_importar, ruta_destino)
                    import subprocess as ss
                    ss.run(["copy", ruta_bd_a_importar, ruta_destino], shell=True)
                    QtWidgets.QMessageBox.warning(self, "Operación exitosa", "La importación se realizó correctamente, "
                                                                             "el programa se cerrará a continuación",
                                                  QtWidgets.QMessageBox.Ok)
                    self.ya_se_puede_cerrar = True
                    self.close()

                except:
                    QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)
    def exportar_base_datos(self):
        ruta_bd_a_exportar = \
        QtWidgets.QFileDialog.getSaveFileName(self, '', f'C:\\Users\\{os.environ.get("USERNAME")}', '*.db')[0]
        ruta_bd_a_exportar = os.path.abspath(ruta_bd_a_exportar)
        #print(ruta_bd_a_exportar)
        ruta_de_bd = f'C:\\Users\\{os.environ.get("USERNAME")}\\datosSNPdo'

        if ruta_bd_a_exportar == os.path.dirname(os.path.abspath(
                __file__)):  # esto sucede cuando se presiona el boton cancelar en la ventana de seleccion de archivo
            pass

        else:

            # print(ruta_de_instalacio_prog)
            comando = f'copy "{ruta_de_bd}\\worker.db" "{ruta_bd_a_exportar}" '
            #print(comando)
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de exportar la base de datos?'
                                                   , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                try:

                    os.system(comando)
                    QtWidgets.QMessageBox.warning(self, "Operación exitosa", "La exportación se realizó correctamente",
                                                  QtWidgets.QMessageBox.Ok)

                except:
                    QtWidgets.QMessageBox.warning(self, "Error fatal", "Error en operación",
                                                  QtWidgets.QMessageBox.Ok)

    def closeEvent(self, QCloseEvent):

        if self.ya_se_puede_cerrar == False:
            reply = QtWidgets.QMessageBox.question(self, 'Advertencia',
                                                   '¿Está usted seguro de cerrar la aplicación? Se perderán los datos '
                                                   'no guardados', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:

                QCloseEvent.accept()


            else:

                QCloseEvent.ignore()

        else:
            QCloseEvent.accept()


if __name__ == "__main__":
    from traceback import print_exc
    try:
        app = QtWidgets.QApplication([])
        window = MainWindowApp()
        window.show()
        app.exec_()
    except:
        with open("log.log", "a") as log:

            print_exc(file=log)
        from os import startfile

        startfile("log.log")  # comando para ejecutar un archivo con su aplicacion
