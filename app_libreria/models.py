from django.db import models
from django.contrib.auth.models import User
from datetime import date

# --- MODELOS DE DATOS (CATÁLOGO) ---

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, default='#ff85a2') # Para el diseño rosa

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    
    # Campos nuevos del script
    editorial = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    paginas = models.IntegerField(default=0)
    isbn = models.CharField(max_length=20, blank=True)
    fecha_publicacion = models.DateField(default=date.today)
    
    # Mantenemos imagen_url con un default para que se vea bonito
    imagen_url = models.URLField(default="https://via.placeholder.com/300x400/ffb7b2/000000?text=Libro") 

    def __str__(self):
        return self.titulo

class Inventario(models.Model):
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    stock_minimo = models.PositiveIntegerField(default=5)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock de {self.libro.titulo}"

# --- MODELOS DE CARRITO Y VENTAS (FUNCIONALIDAD) ---

class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.libro.precio * self.cantidad

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)