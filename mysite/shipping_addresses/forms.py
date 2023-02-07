from django.forms import ModelForm
from .models import ShippingAddress

class ShippingAddressForm(ModelForm): # genera un formulario a partir del modelo ShippingAddress
    class Meta:
        model = ShippingAddress
        fields = [ #indicamos los campos del modelo que interesan
            'line1','line2','city','state','country','postal_code','reference'
        ]
        labels = {
            'line1': 'Calle',
            'line2' : 'Colonia',
            'city' : 'Ciudad',
            'state' : 'Estado',
            'country' : 'País',
            'postal_code' : 'Código Postal',
            'reference' : 'Referencias'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['line1'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['line2'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['state'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['postal_code'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '00000'
        })
        self.fields['reference'].widget.attrs.update({
            'class': 'form-control'
        })
