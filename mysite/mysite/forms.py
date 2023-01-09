from django import forms

#from django.contrib.auth.models import User
from users.models import User


#hereda de forms.Form
class RegisterForm(forms.Form):
    #cada atributo es un input en el formulario
    #para agregar clases a nuestros imput se utiliza el parametro widget
    #el parametro attrs es un diccionario para estblecer las clases
    username=forms.CharField(required=True, min_length=4,max_length=50,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'id':'username',
                             }))
    email=forms.EmailField(required=True,
                           widget=forms.EmailInput(attrs={
                               'class':'form-control',
                               'id':'email',
                               'placeholder':'example@correo.com'
                           }))
    password=forms.CharField(required=True,
                             widget=forms.PasswordInput(attrs={
                                 'class':'form-control'
                             }))
    password2=forms.CharField(label='Confirmar password:',
                              required=True,
                              widget=forms.PasswordInput(attrs={
                                  'class':'form-control'
                              }))

    def clean_username(self):
        username =self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')

        return email

    #Sobreescribimos el metodo clean porque necesitamos validar campos que dependen unos de otros
    #password2 depente del contenido del campo password
    def clean(self):
        #obtenemos todos los campos de formulario, ejecutamos metodo clean de nuestra clase padre
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2','El password no coincide')#campo al que enviamos el error, el mesaje error

    def save(self):
        #el metodo create_user retorna un objeto de tipo user
       return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )