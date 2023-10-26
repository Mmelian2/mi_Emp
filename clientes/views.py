import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ContactoForm, FormCliente, FormEmpresa 
from .models import cliente, empresa
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import Context
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import cliente
# Create your views here.

def index(request):
    return render(request,'clientes/index.html')

def list_cliente(request):
    clien=cliente.objects.all()
    return render (request,'clientes/lista_clientes.html',{'cliente':clien})

def list_emp(request):
    empr=empresa.objects.all()
    return render(request,'clientes/lista_emp.html',{'empresa':empr})

def nuevo_cliente(request):
    if request.method=='POST':
        formCliente=FormCliente(request.POST,request.FILES)
        if formCliente.is_valid():
            formCliente.save()
            return redirect('lista_clientes')
    else:
        formCliente=FormCliente()
    return render(request,'clientes/cliente_nuevo.html',{'formCliente':formCliente})

def nueva_emp(request):
    if request.method=='POST':
        formEmpresa=FormEmpresa(request.POST,request.FILES)
        if formEmpresa.is_valid():
            formEmpresa.save()
            return redirect('lista_emp')
    else:
        formEmpresa=FormEmpresa()
    return render(request,'clientes/emp_nueva.html',{'formEmpresa':formEmpresa})

def editar_emp(request,id):
    emp=get_object_or_404(empresa,pk=id)
    if request.method=='POST':
        formEmpresa=FormEmpresa(request.POST,request.FILES,instance=emp)
        if formEmpresa.is_valid():
            formEmpresa.save()
            return redirect('lista_emp')
    else:
        formEmpresa=FormEmpresa(instance=emp)
        return render(request,'clientes/editt_emp.html',{'formEmpresa':formEmpresa})
 
def eliminar_emp(request,id):
    borrar_emp=get_object_or_404(empresa,pk=id)
    borrar_emp.delete()
    return redirect('lista_emp')
    
def editar_cliente(request,id):
    clien=get_object_or_404(cliente,pk=id)
    if request.method=='POST':
        formCliente=FormCliente(request.POST,request.FILES,instance=clien)
        if formCliente.is_valid():
            formCliente.save()
            return redirect('lista_clientes')
    else:
        formCliente=FormCliente(instance=clien)
        return render(request,'clientes/editar.html',{'formCliente':formCliente})

def eliminar_cliente(reuqest,id):
    borrar_clien=get_object_or_404(cliente,pk=id)
    borrar_clien.delete()
    return redirect('lista_clientes')

def cliente_info(request,id):
    clien=get_object_or_404(cliente,pk=id)
    clien=cliente.objects.get(pk=id)
    return render(request,'clientes/cliente_info.html',{'clien':clien})

def info_emp(request,id):
    empr=get_object_or_404(empresa,pk=id)
    empr=empresa.objects.get(pk=id)
    return render (request,'clientes/emp_info.html',{'empr':empr})

def clien_listado(request):
    busqueda=request.POST.get('buscar')
    clientes=cliente.objects.all().order_by('apellido','nombre')
    cantidad=len(clientes)
    encontrados=cantidad
    if busqueda:
        clientes=cliente.objects.filter(
                Q(dni_icontains=busqueda)|
                Q(apellido_icontains=busqueda)|
                Q(nombre_icontains=busqueda)|
                Q(email_icontains=busqueda)
            ).distinct().order_by('apellido','nombre')
        encontrados=len(clientes)
        return render(request,'clientes/cliente_lista.html',{"clientes":clientes,"cantidad":cantidad,"encontrados":encontrados})
    
def contacto(request):
    form_contacto= ContactoForm()
    if request.method == 'POST':
        form_contacto = ContactoForm(request.POST)
        if form_contacto.is_valid():
            nombre = request.POST['nombre']
            email = request.POST['email']
            mensaje = request.POST['mensaje']
            send_mail(
                'Contacto - Empresa',
                f'Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}',
                'tu_email@dominio.com', # Dirección de correo electrónico del remitente
                ['correo_destino@dominio.com'], # Lista de destinatarios o solo 1
                fail_silently=False,)
            messages.success(request, 'Correo enviado con éxito')
        else:
            messages.error('Error. Por favor verifica que los datos esten correctos')
    return render(request,'clientes/contacto.html',{'form_contacto':form_contacto})
    
class create_pdfView(View):
    def get(self,request,*args,**kwargs):
        template=get_template('clientes/pdf.html')
        context={'title':'PDF'}
        html=template.render(context)
        response=HttpResponse(content_type='pdf')
        response['Content-Disposition']='attachment; filename="report.pdf"'
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
        return response
    
class generar_lista(View):
    def link_callback(self,uri,rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri
        
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' %(sUrl, mUrl)
            )
        return path

    def get(self, request, *args,**kwrags):
        template = get_template('clientes/reporte_clien.html')
        context= {
            'reporte': cliente.objects.all(),
            'logo': '{}{}'.format(settings.MEDIA_URL, 'avatar.png')
            }
        html = template.render(context)
        response = HttpResponse(content_type='pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"' #para que el archivo se descargue automaticante
        pisaStatus = pisa.CreatePDF(
            html, dest=response,
            link_callback=self.link_callback
            )
        if pisaStatus.err:
            return HttpResponse ('Ocurrió un error <pre>' + html + '</pre>')   
        return response


def clientes_list(request):
    clientes = cliente.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(clientes, 5)  #  paginate_by 5
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(1)
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)
    return render(request, "clientes/lista.html", {"clientes": clientes})

def Emp_list(request):
    Emp= empresa.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(Emp, 5)  #  paginate_by 5
    try:
        Emp = paginator.page(page)
    except PageNotAnInteger:
        Emp= paginator.page(1)
    except EmptyPage:
        Emp = paginator.page(paginator.num_pages)
    return render(request, "clientes/Emp_list.html", {"Emp": Emp})