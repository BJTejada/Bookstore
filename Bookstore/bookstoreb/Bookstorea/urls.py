# myapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
     #path('LogIn', views.LogIn_View, name='LogIn'),
     path('Index', views.Index_View, name='Index'),
     path('Inventario', views.Inventario_View, name='Inventario'),
     path('InsertClient_View', views.InsertClient_View, name='InsertClient_View'),
     path('InsertVenta_View', views.InsertVenta_View, name='InsertVenta_View'),
     path('InsertDetVenta_View', views.InsertDetVenta_View, name='InsertDetVenta_View'),
     path('Productos', views.Productos_View, name='Productos'),
     path('generar_factura', views.generar_factura, name='generar_factura'),
     path('ProductoCRUD_View', views.ProductoCRUD_View, name='ProductoCRUD_View'),
     path('Entradas_View', views.Entradas_View, name='Entradas_View'),
    path('Registrar', views.Registrar_Usuario_View, name='Registrar'),
    path('LogIn',views.Iniciar_Sesion_View, name='LogIn'),
    path('LogOut', auth_views.LogoutView.as_view(next_page='LogIn'), name='logout'),
    path('InsertCompra_View', views.InsertCompra_View, name='InsertCompra_View'),
    path('InsertDetCompra_View', views.InsertDetCompra_View, name='InsertDetCompra_View'),
    path('Reportes_View', views.Reportes_View, name='Reportes_View'),
    
    
    

   # path('vistaindex/', views.index, name='index'),  # Para vistas basadas en función
    #path('hello-class/', views.HelloView.as_view(), name='hello_class'),  # Para vistas basadas en clase
   # path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]