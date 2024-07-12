from django.contrib import admin
from .models import Medicos, Especialidades

class MedicosAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_first_name', 'matricula', 'crm', 'cns', 'celular', 'sisreg', 'especialidade')
    search_fields = ('user__username', 'user__first_name', 'matricula', 'crm', 'cns', 'celular')
    list_filter = ('especialidade',)

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.admin_order_field = 'user__first_name'  # Permite ordenação pelo primeiro nome
    get_first_name.short_description = 'Nome'  # Título da coluna

# Register your models here.
admin.site.register(Medicos, MedicosAdmin)
admin.site.register(Especialidades)

