from django.shortcuts import render
from products.models import Product
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import CartProducts

from .models import Cart
from .utils import get_or_create_cart
# Create your views here.

#Validamos si la peticion tiene sesion carrito entonces obtenemos el carrito de la db y enviamos al cliente
# en caso contrario solo creamos un nuevo carrito y enviamos al cliente
def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html',{
        'cart':cart

    })

def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity =int( request.POST.get('quantity', 1))

    #agregamos los productos al carrito, recorda que tiene una relacion muchos a muchos, no permite actualizar
    #cart.products.add(product, through_defaults={
     #   'quantity': quantity
    #})

    cart_product=CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)

    return render(request,'carts/add.html',{
        'quantity':quantity,
        'cart_product':cart_product,
        'product':product
    })
def remove(request):

    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:cart')
