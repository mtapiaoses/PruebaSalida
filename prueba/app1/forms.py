from django import forms
from app1.models import *

class SuscripcionEmail(forms.Form):
        email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su email','class':'form-control'}) )
        username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        rut = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))



class LoginUsuario(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su username','class':'form-control'}),max_length=50,required=True,label='Nombre de usuario')
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña','class':'form-control'}), max_length=20,label='Password',required=True,error_messages={'required':'La contraseña es obligatoria'})


class RegistroProductoForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    precio = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    archivo = forms.FileField(label='Selecciona un archivo')

class FormularioEstado(forms.Form):

        opciones_estado = EstadoPedido.objects.all().values_list('nombre', flat=True)

        OPCIONES_ESTADO = tuple([(opcion, opcion) for opcion in opciones_estado] )
        
        estado = forms.ChoiceField(
        choices=OPCIONES_ESTADO,
        widget=forms.Select( attrs={'class':'form-control'}))


class AgregarProductoFrom(forms.Form):
       producto_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese el precio','class':'form-control'}))
       cantidad_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese el precio','class':'form-control','style':'width:50%;'}))


class FormularioPedidoStaff(forms.Form):
        
        opciones_region = Region.objects.all().values_list('nombre', flat=True)
        opciones_comuna = Comuna.objects.all().values_list('nombre', flat=True)
        opciones_username = Cliente.objects.all()
        OPCIONES_REGION = tuple([(opcion, opcion) for opcion in opciones_region])
        OPCIONES_COMUNA = tuple([(opcion, opcion) for opcion in opciones_comuna] )
        OPCIONES_USERNAME = tuple([(opcion.user.username, opcion.user.username) for opcion in opciones_username] )
       


        direccion=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese la direccion del pedido','class':'form-control'}))
        fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
        cliente = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingrese el email para identificar el cliente','class':'form-control'}))



        region = forms.ChoiceField(
        choices=OPCIONES_REGION,
        widget=forms.Select(attrs={'class':'form-control'}))

        comuna = forms.ChoiceField(
        choices=OPCIONES_COMUNA,
        widget=forms.Select( attrs={'class':'form-control'}))

        cliente = forms.ChoiceField(
        choices=OPCIONES_USERNAME,
        widget=forms.Select(attrs={'class':'form-control'}))

class FormularioPedidoCliente(forms.Form):

        opciones_region = Region.objects.all().values_list('nombre', flat=True)
        opciones_comuna = Comuna.objects.all().values_list('nombre', flat=True)

        OPCIONES_REGION = tuple([(opcion, opcion) for opcion in opciones_region])
        OPCIONES_COMUNA = tuple([(opcion, opcion) for opcion in opciones_comuna] )
        


        direccion=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese la direccion del pedido','class':'form-control'}))
        fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))

        

        region = forms.ChoiceField(
        choices=OPCIONES_REGION,
        widget=forms.Select(attrs={'class':'form-control'}))

        comuna = forms.ChoiceField(
        choices=OPCIONES_COMUNA,
        widget=forms.Select( attrs={'class':'form-control'}))
