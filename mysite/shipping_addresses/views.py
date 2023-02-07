from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin #para evitar el acceso a un usuario no autenticado
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

from .models import ShippingAddress

from .forms import ShippingAddressForm

from django.views.generic import ListView, UpdateView, DeleteView


class ShippingAddresListView(LoginRequiredMixin,ListView):#caso especial por ser vista basada en una clase
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')
                                                    #enviar mensaje del server al cliente
class ShippingAddressUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Dirección actualizada de manera exitosa'

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):#permite hacer validaciones sobre la peticion
        if request.user.id != self.get_object().user.id:#si el usuario no le corresponde la direccion se manda a otra
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    login_url = 'login' #direccion para usuario no autenticado
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')#direccion despues de eliminar

    def dispatch(self, request, *args, **kwargs):#no eliminar la direccion default
        if self.get_object().default:#si es la direccion default entonces envia al listado de direcciones
            return redirect('shipping_addresses:shipping_addresses')

        if self.get_object().user.id!= self.request.user.id:#solo el ususario dueñoa de esa direccion puede eliminarla
            return redirect('carts:cart')

        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')#para usuarios autenticados
def create(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False) #no guarda la inof, genera una instancia
        shipping_address.user = request.user #asignamos el id del usuario logeado
        #shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()#si es la 1, la hace default
        shipping_address.default = not request.user.has_shipping_address()
        shipping_address.save()

        messages.success(request, 'Se ha creado la dirección de envío')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html',{
        'form':form
    })

@login_required(login_url='login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return  redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')