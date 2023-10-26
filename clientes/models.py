from typing import Self
from django.db import models

# Create your models here
          
class cliente (models.Model):
    nombre=models.CharField(max_length=50,verbose_name='Nombre')
    apellido=models.CharField(max_length=50,verbose_name='Apellido')
    dni=models.CharField(max_length=8,verbose_name='DNI')
    email=models.EmailField(max_length=250,default='ejemplo@gmail.com',unique=True,null=False,blank=False)
    rubro=models.CharField(max_length=50,verbose_name='Rubro')
    calle=models.CharField(max_length=25,verbose_name='Calle',default=' ')
    numero=models.CharField(max_length=20,verbose_name='Número',default=' ')
    foto=models.ImageField(upload_to='media/imagenes/', verbose_name='Foto 4x4', null=True,blank=True, max_length=254)
    
    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
        
    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()
        
    def __str__(self):
        return f'{self.nombre, self.apellido, self.dni,self.email,self.rubro,self.calle,self.numero,self.foto}'
    
class empresa(models.Model):
    
    nombre=models.CharField(max_length=50,verbose_name='Nombre')
    cuit=models.CharField(max_length=11,verbose_name='cuit')
    email=models.EmailField(max_length=250,default='ejemplo@gmail.com', unique=True, null=False,blank=False)
    pais=models.CharField(max_length=20,verbose_name='País',default=' ')
    prov=models.CharField(max_length=50,verbose_name='Provincia',default=' ')
    foto=models.ImageField(upload_to='media/imagenes/', verbose_name='Logo', null=True,blank=True, max_length=254)
    
    class Meta:
        verbose_name='Empresa'
        verbose_name_plural='Empresas'
    
    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()
        
    def __str__(self):
        return f'{self.nombre, self.cuit, self.pais}'
    
    
class contacto(models.Model):
    nombre=models.CharField(max_length=50)
    email=models.EmailField(max_length=250)
    mensaje=models.TextField(max_length=250)
    

    