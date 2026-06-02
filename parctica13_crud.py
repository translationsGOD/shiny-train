import mysql.connector
#=================================
# CONFIGURACIÓN DE LA CONEXIÓN
#=================================
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mexico",
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci",
)

#=================================
# CRUD DE LA BASE DE DATOS
#=================================

def agregar_estado():
    nombre = input("Ingrese el nombre del estado: ")
    abrev = input("Ingrese la abreviatura del estado: ")
    area_km2 = int(input("Ingrese el área en KM²: "))
    
    sql = """
    INSERT INTO estados (nombre, abrev, area_km2)
    VALUES (%s, %s, %s)
    """
    
    cursor = conexion.cursor()
    cursor.execute(sql, (nombre, abrev, area_km2))
    conexion.commit()
    cursor.close()
    print("Estado agregado exitosamente.")

def consultar_estados():
    print("--- LISTA DE ESTADOS ---")
    
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre, abrev, area_km2
        FROM estados
        ORDER BY nombre
    """)
    
    registros = cursor.fetchall()
    cursor.close()
    
    if len(registros) == 0:
        print("No se encontraron estados.")
        return

    print("-" * 60)
    print(f"{'ID':<5} {'Nombre':<20} {'Abrev':<10} {'Área (KM²)':<15}")
    print("-" * 60)
    
    for estados in registros:
        print(f"{estados[0]:<5} {estados[1]:<20} {estados[2]:<10} {estados[3]:<15}")

        
def modificar_estado():
    id_estado = int(input("Ingrese el ID del estado a modificar: "))
    
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT nombre, abrev, area_km2 FROM estados WHERE id = %s",
        (id_estado,)
    )
    estado = cursor.fetchone()
    
    if estado is None:
        print("No se encontró un estado con ese ID.")
        cursor.close()
        return
    
    print("Datos actuales del estado:")
    print(f"Nombre: {estado[0]}")
    print(f"Abreviatura: {estado[1]}")
    print(f"Área (KM²): {estado[2]}")

    nuevo_nombre = input("Ingrese el nuevo nombre del estado: ")
    nueva_abrev = input("Ingrese la nueva abreviatura del estado: ")
    nueva_area_km2 = int(input("Ingrese la nueva área en KM²: "))
    
    sql = """
    UPDATE estados
    SET nombre = %s, abrev = %s, area_km2 = %s
    WHERE id = %s
    """
    
    cursor.execute(sql, (nuevo_nombre, nueva_abrev, nueva_area_km2, id_estado))
    conexion.commit()
    cursor.close()
    print("Estado modificado exitosamente.")
    
def eliminar_estado():
    id_estado = int(input("Ingrese el ID del estado a eliminar: "))
    
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT nombre FROM estados WHERE id = %s",
        (id_estado,)
    )
    estado = cursor.fetchone()
    
    if estado is None:
        print("No se encontró un estado con ese ID.")
        cursor.close()
        return
    
    confirmacion = input(f"¿Está seguro que desea eliminar el estado '{estado[0]}'? (s/n): ")
    
    if confirmacion.lower() == 's':
        cursor.execute("DELETE FROM estados WHERE id = %s", (id_estado,))
        conexion.commit()
        print("Estado eliminado exitosamente.")
    else:
        print("Eliminación cancelada.")
    
    cursor.close()

def buscar_estado():
    nombre_busqueda = input("Ingrese el nombre del estado a buscar: ")
    
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, abrev, area_km2 FROM estados WHERE nombre LIKE %s",
        (f"%{nombre_busqueda}%",)
    )
    
    registros = cursor.fetchall()
    cursor.close()
    
    if len(registros) == 0:
        print("No se encontraron estados con ese nombre.")
        return

    print("-" * 60)
    print(f"{'ID':<5} {'Nombre':<20} {'Abrev':<10} {'Área (KM²)':<15}")
    print("-" * 60)
    
    for estado in registros:
        print(f"{estado[0]:<5} {estado[1]:<20} {estado[2]:<10} {estado[3]:<15}")
        
#=================================
# MENÚ PRINCIPAL
#=================================

while True:
    print("\n--- MENÚ DE ESTADOS DE MÉXICO ---")
    print("1. Agregar estado")
    print("2. Consultar estados")
    print("3. Modificar estado")
    print("4. Eliminar estado")
    print("5. Buscar estado por nombre")
    print("6. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        agregar_estado()
    elif opcion == '2':
        consultar_estados()
    elif opcion == '3':
        modificar_estado()
    elif opcion == '4':
        eliminar_estado()
    elif opcion == '5':
        buscar_estado()
    elif opcion == '6':
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")
        
conexion.close()
print("Conexión cerrada. ¡Hasta luego!")