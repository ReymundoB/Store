from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages

#from django.contrib.auth.models import User
from users.models import User
from .forms import RegisterForm

from products.models import Product

def index(request):
    products = Product.objects.all().order_by('-id')

    return render(request,'index.html',{
        'message':'Listado de productos',
        'title':'Producto',
        'products':products,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method =='POST':
        username = request.POST.get('username')#diccionario
        password = request.POST.get('password')
        print(username)
        print(password)
        user=authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request,'Bienvenido {}'.format(user.username))
            if request.GET.get('next'):#para redireccionar a la orden
                return HttpResponseRedirect(request.GET['next'])

            return  redirect('index')#recibe de argumento un string debe ser la direccion a dirigir
        else:
            messages.error(request,'Usuario o contraseña no validos')


    return  render(request,'users/login.html',{
        #diccionario
    })

def logout_view(request):
    logout(request)
    messages.success(request,'Sesión cerrada exitosamente')
    return redirect('login')#usa el nombre del url y no la ruta

def register(request):

    if request.user.is_authenticated:
        return  redirect('index')

    #si la peticion es por POST se crea el formulario con los datos que envia
    #de lo contrario crea el formulario con los datos vacios
    form= RegisterForm(request.POST or None)

    #para extraer la info del formulario que esta por clase
    if request.method == 'POST' and form.is_valid():
        #username = form.cleaned_data.get('username')#diccionario
        #email = form.cleaned_data.get('email')
        #password = form.cleaned_data.get('password')
    #creamos el ususario y el metodo encripta el password
    #    user = User.objects.create_user(username,email,password)
        user=form.save() #el codigo anterio de los apellidos lo trasladamos al metodo save
        if user:
            login(request,user)
            messages.success(request,'Usuario creado exitosamente')
            return redirect('index')

    return render (request,'users/register.html',{
        'form':form
    })
