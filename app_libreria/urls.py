from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

# =======================================================
# 1. RUTAS DE LA APLICACIÓN (FRONTEND & AUTENTICACIÓN)
# =======================================================

urlpatterns = [
    # ------------------ Autenticación y Home ------------------
    path('admin/', admin.site.urls), # Mantiene el panel de Django por defecto
    
    # Rutas de Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 💡 PUERTA DE ACCESO ADMINISTRACIÓN EXCLUSIVA (ACCESO FACILITADO)
    path('admin-login/', views.admin_login_view, name='admin_login'),
    
    # 🛡️ RUTA 'admin-gate' ELIMINADA PARA EVITAR EL ERROR
    
    # ------------------ Carrito y Libros ------------------
    path('categoria/<int:categoria_id>/', views.libros_por_categoria, name='libros_por_categoria'),
    path('agregar/<int:libro_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),

    # ------------------ Home (Raíz del sitio) ------------------
    # 'inicio' apunta a dashboard, que es la vista principal para los usuarios
    path('', views.dashboard, name='inicio'), 

    # =======================================================
    # 2. RUTAS CRUD DEL PANEL DE ADMINISTRACIÓN
    # =======================================================
    
    # ------------------ Dashboard Principal ------------------
    path('admin-panel/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # ------------------ Gestión de Usuarios (desde Admin Panel) ------------------
    # ✅ CORRECCIÓN FINAL: Usa la clase ListaUsuariosView.as_view()
    path('admin-panel/usuarios/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('admin-panel/usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('admin-panel/usuarios/crear/', views.crear_usuario_interno, name='crear_usuario_interno'),

    # ------------------ CRUD de Libros ------------------
    path('admin-panel/libros/', views.LibroListView.as_view(), name='admin_libros_list'),
    path('admin-panel/libros/crear/', views.LibroCreateView.as_view(), name='admin_libros_create'),
    path('admin-panel/libros/editar/<int:pk>/', views.LibroUpdateView.as_view(), name='admin_libros_edit'),
    path('admin-panel/libros/eliminar/<int:pk>/', views.LibroDeleteView.as_view(), name='admin_libros_delete'),
    
    # ------------------ CRUD de Proveedores ------------------
    path('admin-panel/proveedores/', views.ProveedorListView.as_view(), name='admin_proveedores_list'),
    path('admin-panel/proveedores/crear/', views.ProveedorCreateView.as_view(), name='admin_proveedores_create'),
    path('admin-panel/proveedores/editar/<int:pk>/', views.ProveedorUpdateView.as_view(), name='admin_proveedores_edit'), 
    path('admin-panel/proveedores/eliminar/<int:pk>/', views.ProveedorDeleteView.as_view(), name='admin_proveedores_delete'),

    # ------------------ CRUD de Pedidos ------------------
    path('admin-panel/pedidos/', views.PedidoListView.as_view(), name='admin_pedidos_list'),
    path('admin-panel/pedidos/crear/', views.PedidoCreateView.as_view(), name='admin_pedidos_create'),
    path('admin-panel/pedidos/editar/<int:pk>/', views.PedidoUpdateView.as_view(), name='admin_pedidos_edit'), 
    path('admin-panel/pedidos/eliminar/<int:pk>/', views.PedidoDeleteView.as_view(), name='admin_pedidos_delete'),

    # ------------------ CRUD de Categorías ------------------
    path('admin-panel/categorias/', views.CategoriaListView.as_view(), name='admin_categorias_list'),
    path('admin-panel/categorias/crear/', views.CategoriaCreateView.as_view(), name='admin_categorias_create'),
    path('admin-panel/categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='admin_categorias_edit'), 
    path('admin-panel/categorias/eliminar/<int:pk>/', views.CategoriaDeleteView.as_view(), name='admin_categorias_delete'),

    # ------------------ CRUD de Inventario ------------------
    path('admin-panel/inventario/', views.InventarioListView.as_view(), name='admin_inventario_list'),
    path('admin-panel/inventario/crear/', views.InventarioCreateView.as_view(), name='admin_inventario_create'),
    path('admin-panel/inventario/editar/<int:pk>/', views.InventarioUpdateView.as_view(), name='admin_inventario_edit'), 
    path('admin-panel/inventario/eliminar/<int:pk>/', views.InventarioDeleteView.as_view(), name='admin_inventario_delete'),
]

# =======================================================
# 3. MANEJO DE ARCHIVOS ESTÁTICOS Y MEDIOS (IMÁGENES)
# =======================================================

if settings.DEBUG:
    # 1. Manejo de archivos estáticos (CSS/JS)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # 2. Manejo de archivos de Media (Imágenes subidas de libros)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)