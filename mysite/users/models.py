from django.db import models

# proxymodel: es un modelo que hereda de otro pero este no genera una nueva tabla
from django.contrib.auth.models import User

#3. la forma de sobreescribir el modelo user es usando AbstractUser o AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from orders.common import OrderStatus


class User(AbstractUser):
#se configuró la constante AUTH_USER_MODEL en settings
    def get_full_name(self):
        return  '{} {} '.format(self.firts_name, self.last_name)
    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None

    def orders_completed(self):#obtenemos las ordenes y las ordenamos en forma descendente
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')

    def has_shipping_addresses(self):
        return self.shippingaddress_set.exists()

    @property
    def addresses(self):
        return self.shippingaddress_set.all()


# 1. esto hace que el nuevo modelo no genere la nueva tabla
class Customer(User):
    class Meta:
        proxy = True

#hecho lo anterior podemos definir los nuevos metodos que deseamos extender a la clase padre.

        #retorna todos los productos adquiridos por el ciente
    def get_products(self):
        return []

class Profile(models.Model):
    # 2. usamos la opcion 1 a 1 para extender nuevos atributos a nuestro modelo
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    biografia = models.TextField()