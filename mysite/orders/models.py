import uuid
import decimal
from django.db import models

from users.models import User
from carts.models import Cart

from .common import OrderStatus
from .common import choices

from promo_codes.models import PromoCode

from django.db.models.signals import pre_save

from shipping_addresses.models import ShippingAddress


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True, null=False, blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE) # 1 user puede tener muchas ordenes de ccompra / para generar una roden debe estar un usuario
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE) # 1 carrito-> muchas ordenes / una orden puede tener varios estatus
    status = models.CharField(max_length=50, choices=choices,# se convierte en un menu
                              default=OrderStatus.CREATED) #Enum
    shipping_total = models.DecimalField(default=5,max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0,max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress,null=True,blank=True,on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

    def apply_promo_code(self, promo_code):
        if self.promo_code is None:
            self.promo_code = promo_code
            self.save()

            self.update_total()
            promo_code.use()

    def get_ot_set_shipping_address(self):
        if self.shipping_address: # obtenemos la direccion de envio que tiene la orden
            return self.shipping_address
        shipping_address = self.user.shipping_address #Buscamos traes la del usuario
        if shipping_address: #actualizamos la orden con es direccion
           self.update_shipping_address(shipping_address)
        return shipping_address

    def update_shipping_address(self, shipping_address ):
        self.shipping_address = shipping_address
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()


    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_discount(self):
        if self.promo_code:
            return self.promo_code.discount

        return 0

    def get_total(self):
        return self.cart.total + self.shipping_total - decimal.Decimal( self.get_discount())

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)#antes que un objeto de tipo order se guarde, se ejecutara el callback set_total
