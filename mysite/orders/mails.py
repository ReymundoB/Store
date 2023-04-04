from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse #retorna un string

class Mail:

    @staticmethod
    def get_absolute_url(url):
        if settings.DEBUG:
            return 'http://127.0.0.1:8000{}'.format(
                reverse(url)#permite obtener la direccion a partir del nombre de una ruta
            )
    @staticmethod
    def send_complete_order(order,user):
        subject= 'Tú pedido ha sido enviado'
        template = get_template('orders/mails/complete.html')
        content = template.render({
            'user': user,
            'next_url':Mail.get_absolute_url('orders:completeds')
        })
        message = EmailMultiAlternatives(subject, 'Mensaje importante', settings.EMAIL_HOST_USER,[user.email])

        message.attach_alternative(content,'text/html')
        message.send()
