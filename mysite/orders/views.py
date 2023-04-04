import threading

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect

from carts.utils import get_or_create_cart
from carts.utils import destroy_cart
from .models import Order

from .utils import get_or_create_order
from .utils import breadcrumb
from .utils import destroy_order

from .mails import Mail

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.db.models.query import EmptyQuerySet

from shipping_addresses.models import ShippingAddress


class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name='orders/orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()


@login_required(login_url='login') #se restringe vista para user autenticado
def order(request):
    cart = get_or_create_cart(request)
    order =get_or_create_order(cart,request)

    return render(request, 'orders/order.html',{
        'cart':cart,
        'order':order,
        'breadcrumb':breadcrumb()
    })

@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    shipping_address = order.get_ot_set_shipping_address()
    can_choose_address =request.user.has_shipping_addresses()

    return  render(request, 'orders/address.html',{
        'cart':cart,
        'order':order,
        'shipping_address' : shipping_address,
        'can_choose_address' : can_choose_address,
        'breadcrumb':breadcrumb(address=True)
    })
@login_required(login_url='login')
def select_address(request):#Nota: se movieron las consultas dentro del modelo (método, propiedad)
    shipping_addresses = request.user.addresses#obtenemos todas la direcciones
    return  render(request, 'orders/select_address.html',{
        'breadcrumb':breadcrumb(address=True),
        'shipping_addresses':shipping_addresses

    })
@login_required(login_url='login')
def check_address(request, pk):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)

    shipping_address = get_object_or_404(ShippingAddress,pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    order.update_shipping_address(shipping_address)

    return redirect('orders:address')

@login_required(login_url='login')
def confirm(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')

    return render(request, 'orders/confirm.html',{
        'cart':cart,
        'order': order,
        'shipping_address':shipping_address,
        'breadcrumb': breadcrumb(address=True, confirmation=True)
    })

@login_required(login_url='login')
def cancel(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    #seguridad
    if request.user.id != order.user.id: # en caso de no ser el usuario que creo la orden lo mandamos a otra vista
        return redirect('carts:cart')

    order.cancel()

    destroy_order(request)
    destroy_cart(request)


    messages.error(request, 'Orden cancelada')
    return redirect('index')

@login_required(login_url='login')
def complete(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    # seguridad
    if request.user.id != order.user_id:  # en caso de no ser el usuario que creo la orden lo mandamos a otra vista
        return redirect('carts:cart')

    order.complete()
    #Se envia el correo de manera asincrona mediante un hilo
    thread =threading.Thread(target=Mail.send_complete_order,args=(
        order, request.user
    ))
    thread.start()



    destroy_order(request)
    destroy_cart(request)

    messages.success(request, 'Compra completada exitosamente')
    return redirect('index')