from django.contrib.auth.models import User
from django.core.mail import send_mail
from sitio.forms import FormProducto,ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponse

from sitio.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages







def productos(request):
    
    
    productos = Producto.objects.all().order_by("-id")
    
    return render(request, "Productos.html", {
        'categorias' : Categoria.objects.all(),
        'productos_all' : productos[:6],
    })


""" 
    REGISTRO DE USUARIO
"""
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usuario_logeado = User.objects.last()
            #username = form.cleaned_data['username']
            messages.success(request, f"El usuario ha sido registrado exitosamente!")
            carrito = Carrito()
            carrito.usuario = usuario_logeado
            carrito.total = 0
            carrito.save()
            return redirect('SITIO:producto_index')
        else:
            messages.success(request, "No se pudo registrar el usuario, vuelva a intenarlo!")

    return render(request, 'sitio/register.html')

""" 
    PRODUCTOS
"""
def producto_index(request):
    productos = Producto.objects.all().order_by("-id")
    
    return render(request, "sitio/producto/index.html", {
        'categorias' : Categoria.objects.all(),
        'productos_top3' : productos[:3],
        'productos_all' : productos[:6],

        'productos' : productos[3:10]
    })


def producto_create(request):
    categorias = Categoria.objects.all()
    if request.method == "POST":
        categoria_del_producto = Categoria.objects.get(id=request.POST["categoria"])
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen'], categoria=categoria_del_producto))   
        if form.is_valid():
            form.save()
            return redirect("SITIO:producto_index")
            #return HttpResponse('Los campos fueron validados y aceptados!!! ' + str(categoria_del_producto))
        else:
            return render(request, 'sitio/producto/create.html', {
                'categorias' : categorias,
                'error_message' : 'Ingreso un campo incorrecto, vuelva a intentar'
            })
    else:
        return render(request, 'sitio/producto/create.html', {
            'categorias' : categorias
        })

def producto_show(request, producto_id):
    producto =  get_object_or_404(Producto, id=producto_id)

    return render(request, 'sitio/producto/show.html',{
        'categorias' : Categoria.objects.all(),
        'producto' : producto,

    })

def producto_edit(request, producto_id):
    categorias = Categoria.objects.all()
    producto = Producto.objects.get(id=producto_id)

    if request.method == "POST":
        categoria_del_producto = Categoria.objects.get(id=request.POST["categoria"])
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen'], categoria=categoria_del_producto))   
        if form.is_valid():
            producto.titulo = request.POST['titulo']
            producto.categoria = categoria_del_producto
            producto.descripcion = request.POST['descripcion']
            producto.imagen = request.FILES['imagen']
            producto.precio = request.POST['precio']
            producto.stock = request.POST['stock']
            peo = request.POST.get("txtStock")
            producto.save()
            return redirect("SITIO:producto_index")
        else:
            return render(request, 'sitio/producto/edit.html', {
                'categorias' : categorias,
                'error_message' : 'Ingreso un campo incorrecto, vuelva a intentar'
            })
    else:
        return render(request, 'sitio/producto/edit.html',{
            'categorias' : categorias,
            'producto' : producto
        })

def producto_delete(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('SITIO:producto_index')
    

def producto_search(request):
    texto_de_busqueda = request.GET['texto']
    productosPorTitulo = Producto.objects.filter(titulo__icontains = texto_de_busqueda).all()
    productosPorDescripcion = Producto.objects.filter(descripcion__icontains = texto_de_busqueda).all()
    productos = productosPorTitulo | productosPorDescripcion
    return render(request, 'sitio/producto/search.html',
    {
        'categorias' : Categoria.objects.all(),
        'productos' : productos,
        'texto_buscado' : texto_de_busqueda,
        'titulo_seccion' : 'Productos que contienen',
        'sin_productos' : 'No hay producto de la categoria ' + texto_de_busqueda
    })

def productos_por_categoria(request, categoria_id):
    
    #categoria = Categoria.objects.get(id=categoria_id)
    categoria = get_object_or_404(Categoria, id = categoria_id)
    productos = categoria.productos.all()
    return render(request, 'sitio/producto/search.html',
    {
        'categorias' : Categoria.objects.all(),
        'productos' : productos,
        'categoria' : categoria.descripcion,
        'titulo_seccion' : 'Productos de la categoria',
        'sin_productos' : 'No hay producto de la categoria ' + categoria.descripcion
    })

""" 

    CARRITO
"""
def carrito_index(request):
    categorias = Categoria.objects.all()
    usuario_logeado = User.objects.get(username=request.user)
    productos = Carrito.objects.get(usuario=usuario_logeado.id).items.all()
    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    lista = [carrito]
    nuevo_precio_Carrito = 0
    for item in carrito.items.all():
        nuevo_precio_Carrito += float(item.producto.precio) * item.stock
    carrito.total = nuevo_precio_Carrito
    carrito.save()

    return render(request, 'sitio/carrito/index.html', {
        'categorias' : categorias,
        'usuario' : usuario_logeado,
        'items_carrito' : productos,
        'carrito' : lista,

    })

def carrito_save(request):
    #tieneCarrito = Carrito.objects.filter(usuario=8).count()
    # Devuelve un 404 si no encuentra el carrito
    #arrito = get_object_or_404(Carrito, usuario=usuario_logeado.id)

    if request.method == 'POST':
        producto = Producto.objects.get(id=request.POST['producto_id'])
        usuario_logeado = User.objects.get(username=request.user)
        stock = request.POST.get('txtStock')
        print(stock)
        # Agrego producto al carrito
        carrito = Carrito.objects.get(usuario=usuario_logeado.id)
        item_carrito = Carrito_item()
        item_carrito.carrito = carrito
        item_carrito.producto = producto
        item_carrito.stock = stock
        precio = float(producto.precio)
        item_carrito.subtotal = float(stock) * precio
        item_carrito.total = item_carrito.subtotal 
        print(item_carrito.total) 
        item_carrito.save()
        producto.stock = producto.stock - int(stock)
        producto.save()

        # Sumo el precio del producto al carrito
        carrito.total = item_carrito.total
        carrito.save()
        messages.success(request, f"El producto {producto.titulo} fue agregado al carrito")
        #return HttpResponse(f"{usuario_logeado.id} | ITEM_CARRITO: {item_carrito} | CARRITO: {carrito}")
        return redirect("SITIO:producto_index")

    else:
        
 
        return redirect("SITIO:producto_index")

def carrito_clean(request):
    usuario_logeado = User.objects.get(username=request.user)
    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    carrito.items.all().delete()
    carrito.total = 0
    carrito.save()
    #return HttpResponse(f'Carrito: id({carrito.id}) ${carrito.total} | Usuario: id({usuario_logeado.id}) {usuario_logeado.username} | items_carrito: {carrito.items.all().count()}')
    return redirect('SITIO:carrito_index')

def item_carrito_delete(request, item_carrito_id):
    item_carrito = Carrito_item.objects.get(id=item_carrito_id)
    carrito = item_carrito.carrito
    
    # Vuelvo a calcular el precio del carrito
    nuevo_precio_Carrito = 0 - item_carrito.producto.precio
    for item in carrito.items.all():
        nuevo_precio_Carrito += item.producto.precio

    # Realizo los cambios en la base de datos
    carrito.total = nuevo_precio_Carrito
    item_carrito.delete()
    carrito.save()
    return redirect("SITIO:carrito_index")


"""
    PAGINAS
"""
def nosotros(request):
    return render(request, 'sitio/paginas/Nosotros.html',{
        'categorias' : Categoria.objects.all(),
    })


def detalle(request):
    categorias = Categoria.objects.all()
    usuario_logeado = User.objects.get(username=request.user)
    productos = Carrito.objects.get(usuario=usuario_logeado.id).items.all()
    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    lista = [carrito]
    iva = int(carrito.total) * 0.19
    descuento = int(carrito.total) * 0.10
    total = int(carrito.total) - descuento + iva 
    totaldescuento = int(carrito.total) - descuento


    return render(request, 'sitio/carrito/detalle.html', {
        'categorias' : categorias,
        'usuario' : usuario_logeado,
        'items_carrito' : productos,
        'carrito' : lista,
        'iva': iva,
        'total' : total,
        'descuento' : descuento,
        'totaldescuento' : totaldescuento,
    })

def contacto(request):
    return render(request, 'sitio/paginas/Contacto.html')

def servicios(request):
    msj = ""
    try:

        if tipo_servicio == "tass":
            tipo_servicio = "tass"
            nombre = request.POST["nombre"]
            apellido = request.POST["apellido"]
            numero = request.POST["numero"]
            email = request.POST["email"]
            mensaje = request.POST["mensaje"]
            
            try:

                Servicio.objects.create(tipo_servicio = tipo_servicio, nombre = nombre, apellido = apellido, numero = numero, email = email, mensaje = mensaje)
            
                msj="Se ha enviado su solicitud"
                return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})
            except:
                msj = "Ha ocurrido un error, intente nuevamente"

                return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})
        
        elif tipo_servicio == "sell_product":
            tipo_servicio = "sell_product"
            nombre = request.POST["nombre"]
            apellido = request.POST["apellido"]
            numero = request.POST["numero"]
            email = request.POST["email"]
            mensaje = request.POST["mensaje"]
            
            try:

                Servicio.objects.create(tipo_servicio = tipo_servicio, nombre = nombre, apellido = apellido, numero = numero, email = email, mensaje = mensaje)
            
                msj="Se ha enviado su solicitud"
                return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})
            except:
                msj = "Ha ocurrido un error, intente nuevamente"

                return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})

        elif tipo_servicio == "rest":
            tipo_servicio = "rest"
            nombre = request.POST["nombre"]
            apellido = request.POST["apellido"]
            numero = request.POST["numero"]
            email = request.POST["email"]
            mensaje = request.POST["mensaje"]
            
            try:

                Servicio.objects.create(tipo_servicio = tipo_servicio, nombre = nombre, apellido = apellido, numero = numero, email = email, mensaje = mensaje)
            
                msj="Se ha enviado su solicitud"
                return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})
            except:
                msj = "Ha ocurrido un error, intente nuevamente"

                return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})
        else:
            msj = "Ha ocurrido un error, intente nuevamente"

            return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})
    except:
        msj = ""

        return render(request, 'sitio/paginas/Contacto.html', {'msj':msj})