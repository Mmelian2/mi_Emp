from django import views
from django.urls import include, path
from . import views
from .views import create_pdfView
urlpatterns = [
    path('',views.index, name='index'),
    path('lista_clientes/',views.list_cliente, name='lista_clientes'),
    path('lista_emp/',views.list_emp, name='lista_emp'),
    path('cliente_nuevo/',views.nuevo_cliente,name='cliente_nuevo'),
    path('emp_nueva/',views.nueva_emp,name='emp_nueva'),
    path('editt_emp/<int:id>',views.editar_emp,name='editt_emp'),
    path('editar_cliente/<int:id>',views.editar_cliente,name='editar_cliente'),
    path('eliminar_cliente/<int:id>',views.eliminar_cliente,name='eliminar_cliente'),
    path('eliminar_emp/<int:id>',views.eliminar_emp,name='eliminar_emp'),
    path('cliente_info/<int:id>',views.cliente_info,name='cliente_info'),
    path('emp_info/<int:id>',views.info_emp,name='emp_info'),
    path('cliente_lista/',views.clien_listado,name='cliente_lista'),
    path('contacto/',views.contacto, name='contacto'),
    path('crear_pdf/<int:id>',create_pdfView.as_view(),name='crear_pdf'),
    path('generar_lista/', views.generar_lista.as_view(),name='generar_lista'),
    path('clientes_list/',views.clientes_list, name='clientes_list'),
    path('Emp_list/',views.Emp_list, name='Emp_list'),
]