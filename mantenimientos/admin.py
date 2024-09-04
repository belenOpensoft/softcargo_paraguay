from django.contrib import admin
from .models import Proyectos, Traficos, Actividades, Depositos, Empresa


class ProyectoAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = '-'
    list_display = ('codigo','nombre', 'status', 'fecha','observaciones')
    list_display_links = ['codigo','nombre']
    list_filter = ('fecha', 'status')
    search_fields = ('codigo','nombre', 'status', 'fecha','observaciones')
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # self.idusuario = 1
        super(ProyectoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Proyectos,ProyectoAdmin)


class TraficoAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = '-'
    list_display = ('codigo','nombre', 'diasim', 'diasia','diasit','diasem','diasea','diaset','observaciones')
    list_display_links = ['codigo','nombre']
    search_fields = ('codigo','nombre', 'diasim', 'diasia','diasit','diasem','diasea','diaset','observaciones')
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # self.idusuario = 1
        super(TraficoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Traficos,TraficoAdmin)

class ActividadAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = '-'
    list_display = ('numero','nombre', )
    list_display_links = ['numero','nombre']
    search_fields = ('numero','nombre', )
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # self.idusuario = 1
        super(ActividadAdmin, self).save_model(request, obj, form, change)

admin.site.register(Actividades,ActividadAdmin)


class DepositosAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = '-'
    list_display = ('codigo','empresa','telefono','direccion','localidad','ciudad','pais' )
    list_display_links = ['codigo','empresa','telefono','direccion','localidad','ciudad','pais']
    search_fields = ('codigo','empresa' )
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # self.idusuario = 1
        super(DepositosAdmin, self).save_model(request, obj, form, change)

admin.site.register(Depositos,DepositosAdmin)


class EmpresaAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = '-'
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # self.idusuario = 1
        super(EmpresaAdmin, self).save_model(request, obj, form, change)

admin.site.register(Empresa,EmpresaAdmin)

