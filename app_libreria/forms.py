# Elimina el archivo actual


# Crea el archivo correcto

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from .models import Libro, Resena, Categoria, Proveedor

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'autocomplete': 'email'
        }),
        validators=[EmailValidator(message='Ingresa un correo válido')]
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'username'
        }),
        validators=[MinLengthValidator(3, 'El usuario debe tener al menos 3 caracteres')]
    )
    
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña segura',
            'autocomplete': 'new-password'
        })
    )
    
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este usuario ya existe')
        return username

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o correo',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )

class CheckoutForm(forms.Form):
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Calle, número, colonia, ciudad, código postal'
        }),
        max_length=500,
        label='Dirección de envío'
    )
    
    metodo_pago = forms.ChoiceField(
        choices=[
            ('tarjeta', 'Tarjeta de crédito/débito'),
            ('paypal', 'PayPal'),
            ('transferencia', 'Transferencia bancaria'),
            ('efectivo', 'Efectivo al entregar'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Método de pago'
    )
    
    tarjeta_numero = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'autocomplete': 'cc-number'
        }),
        label='Número de tarjeta'
    )
    
    tarjeta_expiracion = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/AA',
            'autocomplete': 'cc-exp'
        }),
        label='Expiración (MM/AA)'
    )
    
    tarjeta_cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'autocomplete': 'cc-csc'
        }),
        label='CVV'
    )
    
    notas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Instrucciones especiales para la entrega...'
        }),
        label='Notas adicionales'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        metodo_pago = cleaned_data.get('metodo_pago')
        
        if metodo_pago == 'tarjeta':
            if not cleaned_data.get('tarjeta_numero'):
                self.add_error('tarjeta_numero', 'Este campo es requerido para pago con tarjeta')
            if not cleaned_data.get('tarjeta_expiracion'):
                self.add_error('tarjeta_expiracion', 'Este campo es requerido para pago con tarjeta')
            if not cleaned_data.get('tarjeta_cvv'):
                self.add_error('tarjeta_cvv', 'Este campo es requerido para pago con tarjeta')
        
        return cleaned_data

class ReviewForm(forms.ModelForm):
    calificacion = forms.ChoiceField(
        choices=[(i, '★' * i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Calificación'
    )
    
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Comparte tu experiencia con este libro...'
        }),
        label='Tu reseña'
    )
    
    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']

class LibroForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    
    precio = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )
    
    imagen = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'descripcion', 'precio', 'categoria', 'proveedor', 'imagen']
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar libros, autores...',
            'aria-label': 'Buscar'
        })
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label='Todas las categorías',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo',
            'step': '0.01'
        })
    )
