
from django.contrib import admin
from django.urls import path
from app1.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [    path('admin/', admin.site.urls),
  
    path('',HomeRegister.as_view(), name='home'),
    path('login_view/', Login_View.as_view(),name='login_view'),
    path('perfil_cliente/', login_required(perfil_cliente),name='perfil_cliente'),
    path('perfil_empleado/', login_required(perfil_empleado),name='perfil_staff'),
    path('logout_view/', logout_view,name='logout_view'),
    path('lista/', listar_pedidos,name='lista'),
    path('pedido/<int:id>', visualizar_pedidos, name='PEDIDO'),
    path('pedido_e/<int:id>', visualizar_pedidos_e, name='PEDIDO_CON_ESTADO'),
    path('registro_producto/', registro_producto,name='registro_producto'),
    path('productos/', lista_producto,name='lista'),
    path('producto/<int:id_pr>', visualizacion_producto,name='VISTA_PRODUCTO'),
    path('tomar_pedido_staff/', TomarPedidoStaff.as_view(),name='TOMAR_PEDIDO_STAFF'),
    path('tomar_pedido_cliente/', TomarPedidoCliente.as_view(),name='TOMAR_PEDIDO_CLIENTE'),
    path('ag_pro_cliente/', funcion_para_guardar_cliente,name='AGREGAR_PRO_CLIENTE'),
    path('ag_pro_staff/', funcion_para_guardar_staff,name='AGREGAR_PRO_STAFF'),
    path('finalizar_pedido_staff/',FinalizarPedidoStaff.as_view(),name='FINALIZAR_PEDIDO'),
    path('finalizar_pedido_cliente/',FinalizarPedidoCliente.as_view(),name='FINALIZAR_PEDIDO'),
    path('limpiar_carrito_staff/', limpiar_carrito_staff,name="LIMPIAR_CARRITO_STAFF"),
    path('limpiar_carrito_cliente/', limpiar_carrito_cliente,name="LIMPIAR_CARRITO_CLIENTE"),
    path('modificar_estado/<int:id_pedido>', modificar_estado_pedido,name="LIMPIAR_CARRITO"),


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

