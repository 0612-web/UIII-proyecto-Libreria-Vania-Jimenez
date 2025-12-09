from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # Vistas Basadas en Clases
from django.urls import reverse_lazy, reverse # Importaciones para URLS
from django.db.models import F 
from decimal import Decimal # Cálculos financieros

# Modelos del Proyecto
from .models import Libro, Categoria, CarritoItem, Pedido, Proveedor, Inventario

# Componentes de autenticación y seguridad
from django.contrib.auth.models import User 
from .mixins import AdminRequiredMixin

# Función auxiliar para user_passes_test
def is_superuser_check(user):
    return user.is_superuser

# =======================================================
# 1. VISTAS DE AUTENTICACIÓN Y FRONT-END
# =======================================================

# 1. LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# 2. REGISTRO
def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

# 3. LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

# 4. DASHBOARD (Página Principal con Bienvenida)
@login_required(login_url='login') 
def dashboard(request):
    nombres_deseados = ['Poesía', 'Novela', 'Historia'] 
    categorias = Categoria.objects.filter(nombre__in=nombres_deseados)
    carrito_count = CarritoItem.objects.filter(usuario=request.user).count()
    
    return render(request, 'libreria/dashboard.html', {
        'categorias': categorias,
        'carrito_count': carrito_count
    })

# 5. VER LIBROS POR CATEGORÍA
@login_required(login_url='login')
def libros_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    libros = Libro.objects.filter(categoria=categoria)
    carrito_count = CarritoItem.objects.filter(usuario=request.user).count()
    return render(request, 'libreria/libros.html', {
        'categoria': categoria, 
        'libros': libros,
        'carrito_count': carrito_count
    })

# 6. AÑADIR AL CARRITO
@login_required(login_url='login')
def agregar_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    item, created = CarritoItem.objects.get_or_create(usuario=request.user, libro=libro)
    if not created:
        item.cantidad += 1
        item.save()
    messages.success(request, f'"{libro.titulo}" añadido al carrito.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

# 7. VER CARRITO Y SIMULACIÓN DE PAGO
@login_required(login_url='login')
def ver_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    subtotal = sum(item.subtotal() for item in items)
    iva = subtotal * Decimal('0.16') 
    total = subtotal + iva
    
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        
        Pedido.objects.create(usuario=request.user, direccion=direccion, total=total)
        
        items.delete()
        messages.success(request, '¡Compra realizada con éxito! Gracias por tu preferencia.')
        return redirect('dashboard')

    return render(request, 'libreria/carrito.html', {
        'items': items, 
        'subtotal': subtotal, 
        'iva': iva, 
        'total': total,
        'carrito_count': items.count()
    })

# ------------------ 🔑 VISTAS ADMINISTRATIVAS DE AUTENTICACIÓN (ACCESO FACILITADO) ------------------

def admin_login_view(request):
    # 1. Si el usuario ya está autenticado
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Si ya es Superusuario, redirigimos directamente al panel, respetando 'next'
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            messages.info(request, "Acceso al panel administrativo concedido.")
            return redirect('admin_dashboard') 
        else:
            # Si es usuario normal logueado, no lo dejamos pasar y lo redirigimos al dashboard normal
            messages.error(request, "Solo los administradores pueden acceder a esta sección.")
            return redirect('dashboard')

    # 2. Manejo del POST si no está logueado
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Verificación crucial: Solo si es Superusuario
            if user.is_superuser:
                login(request, user)
                
                next_url = request.GET.get('next')
                
                if next_url:
                    return redirect(next_url) 
                else:
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Acceso denegado. Solo las credenciales de administrador son válidas aquí.')
        
        messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'es_admin_login': True})


# ------------------ 🗑️ VISTA DE SEGURIDAD ELIMINADA ------------------
# Eliminamos la vista admin_security_gate para simplificar el acceso.
# Asegúrate de eliminar su ruta correspondiente en urls.py.
# ---------------------------------------------------------------------

# =======================================================
# 2. VISTAS CRUD DEL PANEL DE ADMINISTRACIÓN (CBV)
# =======================================================

# -------------------- DASHBOARD ADMINISTRATIVO --------------------

class AdminDashboardView(AdminRequiredMixin, ListView):
    model = Libro
    template_name = 'app_libreria/admin/admin_dashboard.html' 
    context_object_name = 'libros_recientes'
    queryset = Libro.objects.all().order_by('-id')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_libros'] = Libro.objects.count()
        context['total_proveedores'] = Proveedor.objects.count()
        context['total_pedidos'] = Pedido.objects.count()
        context['total_usuarios'] = User.objects.count()
        context['low_stock_items'] = Inventario.objects.filter(cantidad__lte=F('stock_minimo')).select_related('libro')
        return context

# ------------------ Gestión de Usuarios (Convertido a CBV) ------------------

class ListaUsuariosView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'libreria/usuarios.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_usuarios = []
        for u in context['users']:
            pedidos = Pedido.objects.filter(usuario=u).order_by('-fecha')
            data_usuarios.append({
                'user': u,
                'pedidos': pedidos
            })
        context['data_usuarios'] = data_usuarios
        return context

# 9. ELIMINAR USUARIO (Mantiene Función para manejar la lógica directa)
@login_required(login_url='login')
def eliminar_usuario(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Acceso denegado. Se requiere ser administrador.")
        return redirect('dashboard')
        
    usuario_a_borrar = get_object_or_404(User, id=user_id)
    
    if usuario_a_borrar == request.user:
        messages.error(request, "No puedes eliminar tu propia cuenta desde aquí.")
    else:
        usuario_a_borrar.delete()
        messages.success(request, f"Usuario {usuario_a_borrar.username} eliminado.")
        
    return redirect('lista_usuarios')

# 10. CREAR USUARIO (Mantiene Función)
@login_required(login_url='login')
def crear_usuario_interno(request):
    if not request.user.is_superuser:
        messages.error(request, "Acceso denegado. Se requiere ser administrador.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo usuario creado exitosamente.")
            return redirect('lista_usuarios')
    else:
        form = UserCreationForm()
    
    return render(request, 'libreria/crear_usuario_interno.html', {'form': form})

# -------------------- VISTAS CRUD DE PROVEEDORES --------------------

class ProveedorListView(AdminRequiredMixin, ListView):
    model = Proveedor
    template_name = 'app_libreria/admin/proveedores_list.html'
    context_object_name = 'proveedores'

class ProveedorCreateView(AdminRequiredMixin, CreateView):
    model = Proveedor
    template_name = 'app_libreria/admin/proveedores_form.html'
    fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion']
    success_url = reverse_lazy('admin_proveedores_list')

class ProveedorUpdateView(AdminRequiredMixin, UpdateView):
    model = Proveedor
    template_name = 'app_libreria/admin/proveedores_form.html'
    fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion']
    success_url = reverse_lazy('admin_proveedores_list')

class ProveedorDeleteView(AdminRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'app_libreria/admin/proveedores_confirm_delete.html' 
    success_url = reverse_lazy('admin_proveedores_list')

# -------------------- VISTAS CRUD DE LIBROS --------------------

class LibroListView(AdminRequiredMixin, ListView):
    model = Libro
    template_name = 'app_libreria/admin/libros_list.html'
    context_object_name = 'libros'

class LibroCreateView(AdminRequiredMixin, CreateView):
    model = Libro
    template_name = 'app_libreria/admin/libros_form.html'
    fields = ['titulo', 'autor', 'categoria', 'proveedor', 'editorial', 'descripcion', 'precio', 'paginas', 'isbn', 'fecha_publicacion', 'imagen_url']
    success_url = reverse_lazy('admin_libros_list')

class LibroUpdateView(AdminRequiredMixin, UpdateView):
    model = Libro
    template_name = 'app_libreria/admin/libros_form.html'
    fields = ['titulo', 'autor', 'categoria', 'proveedor', 'editorial', 'descripcion', 'precio', 'paginas', 'isbn', 'fecha_publicacion', 'imagen_url']
    success_url = reverse_lazy('admin_libros_list')

class LibroDeleteView(AdminRequiredMixin, DeleteView):
    model = Libro
    template_name = 'app_libreria/admin/libros_confirm_delete.html' 
    success_url = reverse_lazy('admin_libros_list')

# -------------------- VISTAS CRUD DE PEDIDOS --------------------

class PedidoListView(AdminRequiredMixin, ListView):
    model = Pedido
    template_name = 'app_libreria/admin/pedidos_list.html'
    context_object_name = 'pedidos'

class PedidoCreateView(AdminRequiredMixin, CreateView):
    model = Pedido
    template_name = 'app_libreria/admin/pedidos_form.html'
    fields = ['usuario', 'direccion', 'total'] 
    success_url = reverse_lazy('admin_pedidos_list')

class PedidoUpdateView(AdminRequiredMixin, UpdateView):
    model = Pedido
    template_name = 'app_libreria/admin/pedidos_form.html'
    fields = ['usuario', 'direccion', 'total']
    success_url = reverse_lazy('admin_pedidos_list')

class PedidoDeleteView(AdminRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'app_libreria/admin/pedidos_confirm_delete.html' 
    success_url = reverse_lazy('admin_pedidos_list')

# -------------------- VISTAS CRUD DE CATEGORIAS --------------------

class CategoriaListView(AdminRequiredMixin, ListView):
    model = Categoria
    template_name = 'app_libreria/admin/categorias_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(AdminRequiredMixin, CreateView):
    model = Categoria
    template_name = 'app_libreria/admin/categorias_form.html'
    fields = ['nombre', 'descripcion', 'color']
    success_url = reverse_lazy('admin_categorias_list')

class CategoriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Categoria
    template_name = 'app_libreria/admin/categorias_form.html'
    fields = ['nombre', 'descripcion', 'color']
    success_url = reverse_lazy('admin_categorias_list')

class CategoriaDeleteView(AdminRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'app_libreria/admin/categorias_confirm_delete.html' 
    success_url = reverse_lazy('admin_categorias_list')

# -------------------- VISTAS CRUD DE INVENTARIO --------------------

class InventarioListView(AdminRequiredMixin, ListView):
    model = Inventario
    template_name = 'app_libreria/admin/inventario_list.html'
    context_object_name = 'inventarios'
    queryset = Inventario.objects.select_related('libro').all() 

class InventarioCreateView(AdminRequiredMixin, CreateView):
    model = Inventario
    template_name = 'app_libreria/admin/inventario_form.html'
    fields = ['libro', 'cantidad', 'stock_minimo']
    success_url = reverse_lazy('admin_inventario_list')

class InventarioUpdateView(AdminRequiredMixin, UpdateView):
    model = Inventario
    template_name = 'app_libreria/admin/inventario_form.html'
    fields = ['cantidad', 'stock_minimo'] 
    success_url = reverse_lazy('admin_inventario_list')

class InventarioDeleteView(AdminRequiredMixin, DeleteView):
    model = Inventario
    template_name = 'app_libreria/admin/inventario_confirm_delete.html' 
    success_url = reverse_lazy('admin_inventario_list')