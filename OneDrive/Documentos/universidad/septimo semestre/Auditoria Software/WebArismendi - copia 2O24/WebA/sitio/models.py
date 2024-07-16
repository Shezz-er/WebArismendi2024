from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    descripcion = models.CharField(max_length=200, null=False)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Descripcion: {self.descripcion}"


class Producto(models.Model):
    titulo = models.CharField(max_length=50, null=False)
    # Imagen
    imagen = models.FileField(upload_to='media/imagenes/productos/')
    descripcion = models.CharField(max_length=200, null=False)
    precio = models.IntegerField(null=False)
    stock = models.IntegerField()
    # FK
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name="productos")
    

    def __str__(self) -> str:
        return f"Id: {self.pk} | Titulo: {self.titulo} | Imagen: {self.imagen} | Descripcion: {self.descripcion} | Precio: {self.precio} || Categoria_id: {self.categoria.id} "


class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"


class Carrito_item(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    stock = models.IntegerField()
    subtotal = models.IntegerField()
    total = models.IntegerField()


    def __str__(self) -> str:
        return f"Id: {self.pk} | Producto: {self.producto.titulo} | Carrito_id: {self.carrito.id}"


class Servicio(models.Model):
    tipo_servicio = models.CharField(null=False, max_length=20)
    nombre = models.CharField(null=False, max_length=20)
    apellido = models.CharField(null=False, max_length=20)
    numero = models.IntegerField(null=False)
    email = models.CharField(null=False, max_length=50)
    mensaje = models.CharField(null=False, max_length=500)