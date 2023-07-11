from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from app1.forms import *
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
import string
import random
from django.core.mail import send_mail
import uuid
from app1.models import *
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import permission_required


def generar_usuario_aleatorio():
    
    usuario_aleatorio = "usuario" + str(uuid.uuid4())
    
    return str(usuario_aleatorio)

class HomeRegister(View):
    
    def get(self,request):
    
        request.session['carrito']=[] 
        formulario = SuscripcionEmail()
        lista = Producto.objects.all()
        context = {"formulario":formulario,'lista':lista}
        return render (request, 'home.html', context)
    def post(self,request):

        formulario = SuscripcionEmail(request.POST)
        
        email_formulario = formulario['email'].value()
   
        cantidad_usuarios = User.objects.filter(email=email_formulario).count()

        if cantidad_usuarios > 0:
                 return HttpResponse("EMAIL EXISTENTE")

        if formulario.is_valid():
            nombre_usuario = generar_usuario_aleatorio()
            clave = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            email = formulario.cleaned_data['email']
           
            usuario = User( email = email, username = nombre_usuario)
            usuario.password = make_password(clave)
            usuario.save()
            comuna= Comuna.objects.get(id=2)
            region= Region.objects.get(id=2)
            perfil_cliente=Cliente(user = usuario,
            telefono='',
            direccion='',
            rut='',
            comuna = comuna,
            region = region,
            correo=email


            )
            perfil_cliente.save()
            print("estoy enviando correo")
            asunto = 'CONFIRMACION SUSCRIPCION'
            cuerpo = 'USERNAME : '+ nombre_usuario+ '\nCORREO : '+ email + '\nTU CLAVE ES : ' + clave
            print(formulario['email'])
            print("estoy enviando correo")
            destinatarios=[email]
            #grupo = Group.objects.get(name='Cliente')
            send_mail(
            asunto,
            cuerpo,
            'talento@fabricadecodigo.dev',
            destinatarios,
            fail_silently=False,
        )


            return redirect('/login_view/')
        
class Login_View(View):
    template_name = 'login.html'

    def get(self,request):
        formulario = LoginUsuario()
        context={'formulario': formulario}
        #return HttpResponse('prueba')
        return render(request,self.template_name,context)
    
    def post(self,request):
            formulario =  LoginUsuario(request.POST)           
            if formulario.is_valid():
                usuario= formulario.cleaned_data['usuario']
                password = formulario.cleaned_data['clave']
                
                usuario_busqueda = User.objects.get(email=usuario)
                
                print(usuario_busqueda.username)
                print(password)
                user = authenticate(request, username=usuario_busqueda.username, password=password)
                print(user)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        cliente = Cliente.objects.filter(
                        user_id=user.id).count()
                        empleado = Empleado.objects.filter(
                        user_id=user.id).count()
                        if cliente ==1 and empleado == 0 :
                            return redirect('/perfil_cliente/')
                        if cliente ==0 and empleado == 1 :
                            return redirect('/perfil_empleado/')

                    else:
                        return redirect('/')
                else:
                    return redirect('/')
        

def perfil_cliente(request):
    cliente = Cliente.objects.get(user_id=request.user.id)
    carritos=Carrito.objects.filter(cliente_id = cliente.id)
    pedidos = []
    print(carritos)
    for x in carritos:
        pedido = Pedido.objects.get(carrito_id=x.id)
        pedidos.append(pedido)
        print(pedido.id)
    print(pedidos)
    context ={ 'lista':pedidos }
    
    return render(request, 'perfil_cliente.html',context)

def perfil_empleado(request):
    pedidos = Pedido.objects.all()
    context={'lista':pedidos}
    return render(request, 'perfil_empleado.html',context)

def logout_view(request):

    print('logout')
    logout(request)
    return redirect('/')


def registro_producto(request):

    if request.method == 'POST':
        
        form = RegistroProductoForm(request.POST, request.FILES)
        
        imagen = request.FILES['archivo']
        producto = Producto(nombre =form['nombre'].value(),  precio =form['precio'].value(), descripcion = form['descripcion'].value() )
        producto.imagen_b = imagen.read()
        producto.imagen_f = imagen
        producto.save()
        return redirect('/tomar_pedido_staff/')

    else:

        form = RegistroProductoForm()
      
        return render(request, 'registro_producto.html', {'form': form})


def listar_pedidos(request):
    template="lista_de_pedidos.html"
    pedidos = Pedido.objects.all()
    context={'lista':pedidos}
   
    return render(request,template,context)

# permission_required('permiso_cliente')
def visualizar_pedidos(request,id):
    template="pedido.html"
    pedido = Pedido.objects.get(id=id)
    carrito = Carrito.objects.get(id=pedido.carrito_id)
    detalles = DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id)
    suma_precio=0
    for x in detalles:
        suma_precio = suma_precio + (x.producto.precio * x.cantidad)
        

    suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))
   
  
    context={'pedido':pedido,
              'carrito':carrito,
              'detalles':detalles,
                'suma_precio':suma_precio,
                'suma_cantidad':suma_cantidad['total'] 
             }
    return render(request,template,context)


    
permission_required('permiso_empleado')
def visualizar_pedidos_e(request,id):
    template="estado_pedido.html"
    pedido = Pedido.objects.get(id=id)
    carrito = Carrito.objects.get(id=pedido.carrito_id)
    detalles = DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id)
    suma_precio=0
    for x in detalles:
        suma_precio = suma_precio + (x.producto.precio * x.cantidad)
        

    suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))
   
    formulario_estado = FormularioEstado()
    context={'pedido':pedido,
             'carrito':carrito,
             'detalles':detalles,
             'suma_precio':suma_precio,
             'suma_cantidad':suma_cantidad['total'] ,
             'formulario':formulario_estado    
             }
    return render(request,template,context)






def visualizacion_producto(request, id_pr):
    template="producto.html"
    producto = Producto.objects.get(id=id_pr)
    context={'producto': producto}
    return render(request,template,context)

permission_required('permiso_empleado')
class TomarPedidoStaff(View):
   
    id_carrito = None
    def get(self,request):
   
        carrito = Carrito(precio_total=0,cantidad_total=0)
        carrito.save()
        self.id_carrito = carrito.id
       
        lista = Producto.objects.all()
        carrito = request.session.get("carrito")     
        template="tomar_pedido_staff.html"
       
        return render(request,template,context={'lista':lista, 'carrito': carrito})
        #return HttpResponse(lista)
    def post(self,request):
        pass




def imprimir_producto(request,id):

    producto = Producto.objects.get(id=id)
    
    return HttpResponse(producto.imagen_b,content_type='image/jpeg')


def lista_producto(request):
          template= 'lista_de_productos.html'
          context={'lista': Producto.objects.all()}
          return render(request,template,context)

class TomarPedidoCliente(View):
   
    id_carrito = None
    def get(self,request):
   
        carrito = Carrito(precio_total=0,cantidad_total=0)
        carrito.save()
        self.id_carrito = carrito.id
       
        lista = Producto.objects.all()
        carrito = request.session.get("carrito")     
        template="tomar_pedido_cliente.html"
       
        return render(request,template,context={'lista':lista, 'carrito': carrito})
        #return HttpResponse(lista)
    def post(self,request):
        pass


def funcion_para_guardar_cliente(request):
    if request.method=="POST":
        formulario = AgregarProductoFrom(request.POST)

        if request.session.get('carrito') == None:
        
            request.session['carrito']=[]
        
        carrito = request.session.get('carrito')
        producto = Producto.objects.get(id=formulario['producto_id'].value())
        carrito.append({"producto":formulario['producto_id'].value(),"cantidad":formulario['cantidad_id'].value(),'nombre':producto.nombre})
        
        request.session['carrito'] = carrito
        return redirect('/tomar_pedido_cliente/')


# permission_required('permiso_empleado')
def funcion_para_guardar_staff(request):
    if request.method=="POST":
        formulario = AgregarProductoFrom(request.POST)

        if request.session.get('carrito') == None:
        
            request.session['carrito']=[]
        
        carrito = request.session.get('carrito')
        
        producto = Producto.objects.get(id=formulario['producto_id'].value())

        carrito.append({"producto":formulario['producto_id'].value(),"cantidad":formulario['cantidad_id'].value(),'nombre':producto.nombre})
        
        request.session['carrito'] = carrito
        return redirect('/tomar_pedido_staff/')


# permission_required('permiso_empleado')

class FinalizarPedidoStaff(View):
    permission_required('permiso_empleado')
    def get(self,request):
        
        print("STAFF")
        carrito = request.session.get('carrito')
        print("STAFF2")
        formulario = FormularioPedidoStaff()
        template = 'finalizar_pedido_staff.html'
        context = {'formulario':formulario,'carrito':carrito}
        
        return render(request,template,context)
        
        
    # permission_required('permiso_empleado')  
    
    def post(self,request):
        formulario = FormularioPedidoStaff(request.POST)
   
        if formulario.is_valid():
            username = formulario.cleaned_data['cliente']
            try:
                usuario_cliente =  User.objects.get(username=username)
            except User.DoesNotExist:
                
                
                return redirect("/finalizar_pedido_staff/")
            
            
            print(usuario_cliente)
            cliente = Cliente.objects.get(user_id= usuario_cliente.id)
            usuario_empleado =  User.objects.get(id=request.user.id)
           
            empleado = Empleado.objects.get(user_id=request.user.id)
            
            carrito= Carrito(
                cantidad_total= 0,
                precio_total=0,
                cliente = cliente,
                empleado = empleado 
                 )
            carrito.save()
            carrito_session = request.session.get('carrito')
            suma_precio=0
            for x in carrito_session:
                producto = Producto.objects.get(id=x['producto'])
                cantidad = x['cantidad']
                detalle = DetalleProductoSocilicitado(
                    producto =producto,
                    cantidad= cantidad,
                    valor_producto = producto.precio,
                    carrito = carrito
                 )
                detalle.save()
                suma_precio = suma_precio + (int(producto.precio) *int(cantidad))
            suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))

           
            carrito.cantidad_total = suma_cantidad['total']
            carrito.precio_total = suma_precio
            carrito.save()

            estado = EstadoPedido.objects.get(id=1)
            comuna = Comuna.objects.get(nombre=formulario.cleaned_data['comuna'])
            region = Region.objects.get(nombre=formulario.cleaned_data['region'])
            pedido = Pedido( 
                    fecha = formulario.cleaned_data['fecha_entrega'],
                    estado=estado,
                    calle_entrega=formulario.cleaned_data['direccion'],
                    comuna=comuna,
                    region=region,
                    carrito = carrito         
                    
                )        

            pedido.save()
            return redirect('/perfil_empleado')


class FinalizarPedidoCliente(View):
    # permission_required('permiso_cliente')
    def get(self,request):
        carrito = request.session.get('carrito')
        formulario = FormularioPedidoCliente()
        template = 'finalizar_pedido_cliente.html'
        context = {'formulario':formulario,'carrito':carrito}
        return render(request,template,context)
        
    # permission_required('permiso_cliente')
    def post(self,request):
        formulario = FormularioPedidoCliente(request.POST)
       
        if formulario.is_valid():
          
            usuario_cliente =  User.objects.get(email=request.user.email)

            cliente = Cliente.objects.get(user_id= usuario_cliente.id)
        
            
            carrito= Carrito(
                cantidad_total= 0,
                precio_total=0,
                cliente = cliente
      
                 )
            carrito.save()
            carrito_session = request.session.get('carrito')
            suma_precio=0
            for x in carrito_session:
                producto = Producto.objects.get(id=x['producto'])
                cantidad = x['cantidad']
                detalle = DetalleProductoSocilicitado(
                    producto =producto,
                    cantidad= cantidad,
                    valor_producto = producto.precio,
                    carrito = carrito
                 )
                detalle.save()
                suma_precio = suma_precio + (int(producto.precio) * int(cantidad))
            suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))
            carrito.cantidad_total = suma_cantidad['total']
            carrito.precio_total = suma_precio
            carrito.save()
            estado = EstadoPedido.objects.get(id=1)
            comuna = Comuna.objects.get(nombre=formulario.cleaned_data['comuna'])
            region = Region.objects.get(nombre=formulario.cleaned_data['region'])
            pedido = Pedido( 
                    fecha = formulario.cleaned_data['fecha_entrega'],
                    estado=estado,
                    calle_entrega=formulario.cleaned_data['direccion'],
                    comuna=comuna,
                    region=region,
                    carrito = carrito         
                    
                )        

            pedido.save()
            return redirect('/perfil_cliente')


def lista_producto(request):
          template= 'lista_productos.html'
          context={'lista': Producto.objects.all()}
          return render(request,template,context)


def limpiar_carrito_staff(request):
    request.session['carrito']=[]
    return redirect('/tomar_pedido_staff/')

# permission_required('permiso_cliente')
def limpiar_carrito_cliente(request):
    request.session['carrito']=[]
    return redirect('/tomar_pedido_cliente/')


# permission_required('permiso_empleado')
def modificar_estado_pedido(request,id_pedido):
    
    formulario = FormularioEstado(request.POST)

    if formulario.is_valid():
        nombre_estado = formulario.cleaned_data['estado']
        estado = EstadoPedido.objects.get(nombre=nombre_estado)
        pedido=Pedido.objects.get(id=id_pedido)
        pedido.estado = estado
        pedido.save()
        
        email = pedido.carrito.cliente.user.email
        print(email)
        destinatarios=[email]
        asunto = 'ESTADO DE TU PEDIDO'
        cuerpo = 'TU PEDIDO ESTA ' + nombre_estado
               
        send_mail(
            asunto,
            cuerpo,
            'talento@fabricadecodigo.dev',
            destinatarios,
            fail_silently=False,
        )
        direccion='/pedido_e/'+ str(id_pedido)
        return redirect(direccion)