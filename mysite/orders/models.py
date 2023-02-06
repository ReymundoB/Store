import uuid
from django.db import models

from users.models import User
from carts.models import Cart

from enum import Enum

from django.db.models.signals import pre_save

class OrderStatus(Enum):
    CREATED ='CREATED'
    PAYED = 'PAYED'
    COMPLETED ='COMPLETED'
    CANCELED ='CANCELED'

choices =[(tag, tag.value) for tag in OrderStatus]


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True, null=False, blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE) # 1 user puede tener muchas ordenes de ccompra / para generar una roden debe estar un usuario
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE) # 1 carrito-> muchas ordenes / una orden puede tener varios estatus
    status = models.CharField(max_length=50, choices=choices,# se convierte en un menu
                              default=OrderStatus.CREATED) #Enum
    shipping_total = models.DecimalField(default=5,max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0,max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_total(self):
        return self.cart.total + self.shipping_total

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)#antes que un objeto de tipo order se guarde, se ejecutara el callback set_total