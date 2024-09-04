from django.db import models


class VGrillaSeguimientos(models.Model):
    numero = models.IntegerField()
    modo = models.CharField(max_length=20, blank=True, null=True)
    cliente = models.CharField(max_length=500, blank=True, null=True)
    direccion_cliente = models.CharField(max_length=500, blank=True, null=True)
    telefono_cliente = models.CharField(max_length=500, blank=True, null=True)
    cliente_codigo = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    origen_text = models.CharField(max_length=50, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    destino_text = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    notas = models.CharField(max_length=1000, blank=True, null=True)
    consignatario = models.CharField(max_length=1000, blank=True, null=True)
    consignatario_codigo = models.IntegerField(blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    agente = models.CharField(max_length=1000, blank=True, null=True)
    agente_codigo = models.IntegerField(blank=True, null=True)
    embarcador = models.CharField(max_length=1000, blank=True, null=True)
    embarcador_codigo = models.IntegerField(blank=True, null=True)
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vencimiento = models.DateTimeField(blank=True, null=True)
    embarque = models.IntegerField(blank=True, null=True)
    vapor = models.CharField(max_length=200, blank=True, null=True)
    vapor_codigo = models.CharField(max_length=30, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=40, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    tarifaventa = models.FloatField(blank=True, null=True)
    tarifacompra = models.FloatField(blank=True, null=True)
    pago = models.CharField(max_length=10, blank=True, null=True)
    refcliente = models.CharField(max_length=1024, blank=True, null=True)
    transportista = models.CharField(max_length=1000, blank=True, null=True)
    transportista_codigo = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=30, blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotizacion1 = models.IntegerField(blank=True, null=True)
    vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vendedor = models.CharField(max_length=500,blank=True, null=True)
    vendedor_codigo = models.SmallIntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    agecompras = models.CharField(max_length=500,blank=True, null=True)
    agecompras_codigo = models.IntegerField(blank=True, null=True)
    ageventas = models.CharField(max_length=500,blank=True, null=True)
    ageventas_codigo = models.IntegerField(blank=True, null=True)
    deposito = models.CharField(max_length=500,blank=True, null=True)
    deposito_codigo = models.IntegerField(blank=True, null=True)
    recepcion = models.DateTimeField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    nrodespacho = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(max_length=20, blank=True, null=True)
    fecacepta = models.DateTimeField(blank=True, null=True)
    fecentrega = models.DateTimeField(blank=True, null=True)
    fecretiro = models.DateTimeField(blank=True, null=True)
    totalgiro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nroguiadesp = models.CharField(max_length=20, blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    refproveedor = models.CharField(max_length=250, blank=True, null=True)
    estimadorecepcion = models.DateTimeField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    etd = models.DateTimeField(blank=True, null=True)
    recepcionado = models.CharField(max_length=1, blank=True, null=True)
    lugar = models.CharField(max_length=30, blank=True, null=True)
    fecaduana = models.DateTimeField(db_column='Fecaduana', blank=True, null=True)  # Field name made lowercase.
    fecdocage = models.DateTimeField(db_column='Fecdocage', blank=True, null=True)  # Field name made lowercase.
    fecrecdoc = models.DateTimeField(blank=True, null=True)
    fecemision = models.DateTimeField(blank=True, null=True)
    fecseguro = models.DateTimeField(blank=True, null=True)
    nroseguro = models.CharField(max_length=10, blank=True, null=True)
    valor = models.CharField(max_length=20, blank=True, null=True)
    manifiesto = models.CharField(max_length=20, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    fecpagoder = models.DateTimeField(blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tomopeso = models.SmallIntegerField(blank=True, null=True)
    fecpresdi = models.DateTimeField(blank=True, null=True)
    prima = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    centro = models.CharField(max_length=25, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    transportelocal = models.IntegerField(blank=True, null=True)
    estimadopup = models.DateTimeField(blank=True, null=True)
    realpup = models.DateTimeField(blank=True, null=True)
    estimadodelivery = models.DateTimeField(blank=True, null=True)
    realdelivery = models.DateTimeField(blank=True, null=True)
    referencialocal = models.CharField(max_length=50, blank=True, null=True)
    modolocal = models.CharField(max_length=10, blank=True, null=True)
    fecguiadesp = models.DateTimeField(blank=True, null=True)
    tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    armador = models.CharField(max_length=1000, blank=True, null=True)
    armador_codigo = models.CharField(max_length=1000, blank=True, null=True)
    notificar = models.CharField(max_length=1000, blank=True, null=True)
    notificar_codigo = models.IntegerField(blank=True, null=True)
    fechaonhand = models.DateTimeField(db_column='FechaOnHand', blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=30, blank=True, null=True)
    propia = models.CharField(db_column='Propia', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
    trafico_codigo = models.SmallIntegerField(blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    proyecto_codigo = models.SmallIntegerField(blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    modificado = models.CharField(db_column='Modificado', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True,
                                                    null=True)  # Field name made lowercase.
    depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True,
                                                   null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True,
                                          null=True)  # Field name made lowercase.
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True,
                                          null=True)  # Field name made lowercase.
    retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
    arriboreal = models.DateTimeField(db_column='ArriboReal', blank=True, null=True)  # Field name made lowercase.
    pagoenfirme = models.DateTimeField(db_column='PagoenFirme', blank=True, null=True)  # Field name made lowercase.
    recepcionprealert = models.DateTimeField(db_column='RecepcionPrealert', blank=True,
                                             null=True)  # Field name made lowercase.
    bltipo = models.CharField(db_column='BLTipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    credito = models.CharField(db_column='Credito', max_length=50, blank=True, null=True)  # Field name made lowercase.
    revalidacion = models.DateTimeField(db_column='Revalidacion', blank=True, null=True)  # Field name made lowercase.
    almacenajelibrehasta = models.DateTimeField(db_column='AlmacenajeLibreHasta', blank=True,
                                                null=True)  # Field name made lowercase.
    demoraslibrehasta = models.DateTimeField(db_column='DemorasLibreHasta', blank=True,
                                             null=True)  # Field name made lowercase.
    entregavacio = models.DateTimeField(db_column='EntregaVacio', blank=True, null=True)  # Field name made lowercase.
    tipobonifcli = models.CharField(db_column='TipoBonifCli', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    bonifcli = models.FloatField(db_column='BonifCli', blank=True, null=True)  # Field name made lowercase.
    originales = models.CharField(db_column='Originales', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    consolidado = models.SmallIntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    rotulosincorrectos = models.CharField(db_column='RotulosIncorrectos', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    actividad_codigo = models.IntegerField(blank=True, null=True)
    entregadoa = models.CharField(db_column='EntregadoA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    loadingdate = models.DateTimeField(db_column='LoadingDate', blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True,
                                              null=True)  # Field name made lowercase.
    muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=19, decimal_places=4, blank=True,
                                       null=True)  # Field name made lowercase.
    choice_op = (("IMPORTACION","IMPORTACION"),
                 ("EXPORTACION","EXPORTACION"),
                 ("EXPORTACION FCL","EXPORTACION FCL"),
                 ("IMPORTACION LCL","IMPORTACION LCL"),
                 ("IMPORTACION FCL","IMPORTACION FCL"),
                 ("EXPORTACION CONSOLIDADA","EXPORTACION CONSOLIDADA"),
                 ("IMPORTACION PART CONT.","IMPORTACION PART CONT."),
                 ("TRANSITO FCL","TRANSITO FCL"),
                 ("IMPORTACION CONSOLIDADA","IMPORTACION CONSOLIDADA"),
                 ("REEMBARCO","REEMBARCO"),
                 ("COURIER","COURIER"),
                 ("TRANSITO","TRANSITO"),
                 ("EXPORTACION LCL","EXPORTACION LCL"),
                 ("EXPORTACION PART CONT.","EXPORTACION PART CONT."),
                 ("DUA","DUA"),
                 ("TRASLADO","TRASLADO"),
                 ("MUESTRA","MUESTRA"),
                 ("",""),
                 )
    operacion = models.CharField(db_column='Operacion', max_length=25, blank=True,null=True,choices=choice_op)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wwanumerobooking = models.IntegerField(db_column='WWANumeroBooking', blank=True,
                                           null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    fechastacking = models.DateTimeField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
    horastacking = models.CharField(db_column='HoraStacking', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True,
                                            null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    tieneseguro = models.CharField(db_column='TieneSeguro', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True,
                                          null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    nroreferedi = models.IntegerField(db_column='NroReferEDI', blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deaddocumentoshora = models.CharField(db_column='DeadDocumentosHora', max_length=10, blank=True,
                                          null=True)  # Field name made lowercase.
    emailem = models.CharField(db_column='emailEM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailea = models.CharField(db_column='emailEA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailet = models.CharField(db_column='emailET', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailim = models.CharField(db_column='emailIM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailia = models.CharField(db_column='emailIA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailit = models.CharField(db_column='emailIT', max_length=500, blank=True, null=True)  # Field name made lowercase.



    def __str__(self,):
        return self.modo + ' - ' + str(self.numero)

    class Meta:
        managed = False
        db_table = 'VGrillaSeguimientos'
