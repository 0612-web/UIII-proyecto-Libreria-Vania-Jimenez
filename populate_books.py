import os
import django
import random

# CONFIGURACIÓN
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_libreria.settings') 
django.setup()

from app_libreria.models import Categoria, Proveedor, Libro, Inventario

def reiniciar_biblioteca():
    print("⚠️  ATENCIÓN: BORRANDO LIBROS ANTIGUOS...")
    # Borramos todo para empezar limpio y que salgan los 10 exactos
    Libro.objects.all().delete()
    print("✅ Base de datos de libros limpia.")

    print("\n--- CREANDO NUEVOS LIBROS (10 por categoría) ---")
    
    # Obtener categorías
    try:
        cat_poesia = Categoria.objects.get(nombre='Poesía')
        cat_novela = Categoria.objects.get(nombre='Novela')
        cat_historia = Categoria.objects.get(nombre='Historia')
    except Categoria.DoesNotExist:
        print("❌ Error: Categorías no encontradas. Ejecuta el script anterior para crearlas o créalas en el admin.")
        return

    # Proveedores (creamos uno genérico si no hay)
    prov, _ = Proveedor.objects.get_or_create(
        nombre="Editorial General", 
        defaults={'contacto': 'Admin', 'telefono': '000', 'email': 'x@x.com', 'direccion': 'CDMX'}
    )

    # --- LISTAS DE 10 LIBROS EXACTOS ---

    lista_poesia = [
        ('Veinte poemas de amor', 'Pablo Neruda', 280),
        ('Poeta en Nueva York', 'Federico García Lorca', 320),
        ('Rimas y Leyendas', 'Gustavo Adolfo Bécquer', 250),
        ('La voz a ti debida', 'Pedro Salinas', 290),
        ('Los heraldos negros', 'César Vallejo', 310),
        ('Piedra de sol', 'Octavio Paz', 340),
        ('La rosa separada', 'Pablo Neruda', 300),
        ('Antología poética', 'Mario Benedetti', 260),
        ('Cántico', 'Jorge Guillén', 270),
        ('Los versos del capitán', 'Pablo Neruda', 295),
    ]

    lista_novela = [
        ('Cien años de soledad', 'Gabriel García Márquez', 450),
        ('Don Quijote de la Mancha', 'Miguel de Cervantes', 520),
        ('Orgullo y prejuicio', 'Jane Austen', 380),
        ('1984', 'George Orwell', 420),
        ('Crimen y castigo', 'Fiódor Dostoyevski', 490),
        ('Rayuela', 'Julio Cortázar', 510),
        ('La sombra del viento', 'Carlos Ruiz Zafón', 390),
        ('El amor en los tiempos del cólera', 'Gabo', 430),
        ('Los miserables', 'Víctor Hugo', 580),
        ('El nombre de la rosa', 'Umberto Eco', 470),
    ]

    lista_historia = [
        ('Sapiens', 'Yuval Noah Harari', 550),
        ('Breve historia del mundo', 'Ernst H. Gombrich', 480),
        ('Historia mínima de México', 'Daniel Cosío Villegas', 350),
        ('Los cañones de agosto', 'Barbara W. Tuchman', 520),
        ('Historia de Roma', 'Indro Montanelli', 420),
        ('Armas, gérmenes y acero', 'Jared Diamond', 590),
        ('La guerra del Peloponeso', 'Tucídides', 380),
        ('El siglo XX', 'Eric Hobsbawm', 610),
        ('Historia de las mujeres', 'Michelle Perrot', 680),
        ('Vida privada', 'Philippe Ariès', 540),
    ]

    # --- PROCESO DE CREACIÓN ---

    crear_lote(lista_poesia, cat_poesia, "p", prov)
    crear_lote(lista_novela, cat_novela, "n", prov)
    crear_lote(lista_historia, cat_historia, "h", prov)

def crear_lote(lista, categoria, prefijo, proveedor):
    count = 1
    for titulo, autor, precio in lista:
        # Ruta exacta: /static/images/p1.jpg
        ruta_img = f"/static/images/{prefijo}{count}.jpg"
        
        libro = Libro.objects.create(
            titulo=titulo,
            autor=autor,
            categoria=categoria,
            proveedor=proveedor,
            precio=precio,
            descripcion=f"Edición especial de {titulo}. Una obra imprescindible.",
            imagen_url=ruta_img, # Guardamos la ruta estática
            isbn=f"978-{random.randint(100000, 999999)}"
        )
        
        # Inventario
        Inventario.objects.create(libro=libro, cantidad=20)
        
        print(f"  [{count}/10] {categoria.nombre}: {titulo} -> {ruta_img}")
        count += 1

if __name__ == '__main__':
    reiniciar_biblioteca()
    print("\n🎉 ¡LISTO! 30 Libros creados (10 por categoría).")