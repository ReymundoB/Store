from django.urls import path

from . import views

#lo defines para indicar que las rutas de abajo son para esta app y evitar
#entrar en conflicto con otras apps
#debes indicar tus archivos de app la ruta por ejemplo products:search
app_name = 'products'

urlpatterns =[
    path('search', views.ProductSearchListView.as_view(),name='search'),
    path('<slug:slug>', views.ProductDetailView.as_view(),name='product'),#id -> llave primaria /:id

]