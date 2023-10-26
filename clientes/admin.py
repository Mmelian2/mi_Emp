from django.contrib import admin

from .models import cliente, empresa

# Register your models here. 
class cliente_admin(admin.ModelAdmin):
    list_display=('nombre','apellido','dni','rubro','foto')
    list_filter=('rubro',)
    search_fields=('dni','apellido')
    
admin.site.register(cliente,cliente_admin)

class empresa_admin(admin.ModelAdmin):
    list_display=('nombre','cuit','pais','foto')
    list_filter=('pais',)
    search_fields=('nombre','cuit')
    
admin.site.register(empresa,empresa_admin)