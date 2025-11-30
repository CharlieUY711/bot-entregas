"""
Script para crear los 3 perfiles de Carlos Varalla:
1. Carlos Varalla / Independiente - Permisos básicos
2. Carlos Varalla / entregas - Permisos Máximo
3. Carlos Varalla / Wesco - Anixter - Permisos Máximos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.identity_service import IdentityService
from services.db import get_connection
import logging

logging.basicConfig(level=logging.INFO)

def crear_perfiles_carlos():
    """Crea los 3 perfiles de Carlos Varalla"""
    
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if not conn:
            print("ERROR: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        # Paso 1: Verificar/crear entidades necesarias
        print(" Verificando/Creando entidades...")
        
        # Entidad "Independiente" (id = -1 o NULL)
        cursor.execute("SELECT id_entidad FROM entidades WHERE nombre = 'Independiente' OR id_entidad = -1 LIMIT 1")
        entidad_independiente = cursor.fetchone()
        if not entidad_independiente:
            try:
                cursor.execute("""
                    INSERT INTO entidades (id_entidad, nombre, rubro, razon_social, activo) 
                    VALUES (-1, 'Independiente', 'Independiente', 'Usuario Independiente', TRUE)
                """)
                entidad_independiente_id = -1
                print(f"[OK] Entidad 'Independiente' creada (ID: -1)")
            except Exception as e:
                # Si falla por el ID -1, crear sin especificar ID
                cursor.execute("""
                    INSERT INTO entidades (nombre, rubro, razon_social, activo) 
                    VALUES ('Independiente', 'Independiente', 'Usuario Independiente', TRUE)
                """)
                entidad_independiente_id = cursor.lastrowid
                print(f"[OK] Entidad 'Independiente' creada (ID: {entidad_independiente_id})")
        else:
            entidad_independiente_id = entidad_independiente['id_entidad']
            print(f"[OK] Entidad 'Independiente' encontrada (ID: {entidad_independiente_id})")
        
        # Entidad "Entregas"
        cursor.execute("SELECT id_entidad FROM entidades WHERE nombre = 'Entregas' LIMIT 1")
        entidad_entregas = cursor.fetchone()
        if not entidad_entregas:
            cursor.execute("""
                INSERT INTO entidades (nombre, rubro, razon_social, activo) 
                VALUES ('Entregas', 'Plataforma', 'Entregas', TRUE)
            """)
            entidad_entregas_id = cursor.lastrowid
            print(f"[OK] Entidad 'Entregas' creada (ID: {entidad_entregas_id})")
        else:
            entidad_entregas_id = entidad_entregas['id_entidad']
            print(f"[OK] Entidad 'Entregas' encontrada (ID: {entidad_entregas_id})")
        
        # Entidad "Wesco - Anixter"
        cursor.execute("SELECT id_entidad FROM entidades WHERE nombre LIKE '%Wesco%' OR nombre LIKE '%Anixter%' LIMIT 1")
        entidad_wesco = cursor.fetchone()
        if not entidad_wesco:
            cursor.execute("""
                INSERT INTO entidades (nombre, rubro, razon_social, activo) 
                VALUES ('Wesco - Anixter', 'Distribución', 'Wesco - Anixter', TRUE)
            """)
            entidad_wesco_id = cursor.lastrowid
            print(f"[OK] Entidad 'Wesco - Anixter' creada (ID: {entidad_wesco_id})")
        else:
            entidad_wesco_id = entidad_wesco['id_entidad']
            print(f"[OK] Entidad 'Wesco - Anixter' encontrada (ID: {entidad_wesco_id})")
        
        # Paso 2: Verificar/crear usuario principal
        print("\n Verificando/Creando usuario...")
        cursor.execute("SELECT id_user FROM users WHERE email = 'cvaralla@gmail.com' LIMIT 1")
        usuario_existente = cursor.fetchone()
        
        if usuario_existente:
            user_id = usuario_existente['id_user']
            print(f"[WARN]  Usuario ya existe (ID: {user_id}). Actualizando datos...")
            
            # Actualizar contraseña y datos
            password_hash = IdentityService.hash_password('Carlos123')
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, 
                    nombre = 'Carlos Varalla',
                    telefono = '+59896800037',
                    celular = '+59896800037',
                    email_verificado = TRUE,
                    activo = TRUE
                WHERE id_user = %s
            """, (password_hash, user_id))
            print("[OK] Usuario actualizado")
        else:
            # Crear nuevo usuario usando IdentityService
            print("📝 Creando nuevo usuario...")
            try:
                user_data = IdentityService.register_user(
                    email='cvaralla@gmail.com',
                    telefono='+59896800037',
                    password='Carlos123',
                    nombre='Carlos Varalla',
                    app_origen='entregas'
                )
                user_id = user_data['id_user']
                print(f"[OK] Usuario creado (ID: {user_id})")
            except Exception as e:
                # Si falla IdentityService, crear directamente
                print(f"[WARN]  IdentityService falló, creando usuario directamente: {e}")
                password_hash = IdentityService.hash_password('Carlos123')
                cursor.execute("""
                    INSERT INTO users (
                        email, 
                        nombre, 
                        password_hash, 
                        activo, 
                        email_verificado,
                        telefono,
                        celular
                    ) VALUES (
                        'cvaralla@gmail.com',
                        'Carlos Varalla',
                        %s,
                        TRUE,
                        TRUE,
                        '+59896800037',
                        '+59896800037'
                    )
                """, (password_hash,))
                user_id = cursor.lastrowid
                print(f"[OK] Usuario creado directamente (ID: {user_id})")
        
        # Paso 3: Crear/actualizar relaciones usuario-entidad
        print("\n Creando/Actualizando relaciones usuario-entidad...")
        
        # 3.1 Independiente - Permisos básicos (operador)
        cursor.execute("""
            INSERT INTO user_entidades (id_user, id_entidad, es_principal, activo, rol)
            VALUES (%s, %s, TRUE, TRUE, 'operador')
            ON DUPLICATE KEY UPDATE 
                activo = TRUE, 
                es_principal = TRUE,
                rol = 'operador'
        """, (user_id, entidad_independiente_id))
        print("[OK] Relación 'Independiente' creada/actualizada (Permisos básicos - operador)")
        
        # 3.2 Entregas - Permisos Máximo (superusuario)
        cursor.execute("""
            INSERT INTO user_entidades (id_user, id_entidad, es_principal, activo, rol)
            VALUES (%s, %s, FALSE, TRUE, 'superusuario')
            ON DUPLICATE KEY UPDATE 
                activo = TRUE, 
                rol = 'superusuario'
        """, (user_id, entidad_entregas_id))
        print("[OK] Relación 'Entregas' creada/actualizada (Permisos Máximo - superusuario)")
        
        # 3.3 Wesco - Anixter - Permisos Máximos (superusuario)
        cursor.execute("""
            INSERT INTO user_entidades (id_user, id_entidad, es_principal, activo, rol)
            VALUES (%s, %s, FALSE, TRUE, 'superusuario')
            ON DUPLICATE KEY UPDATE 
                activo = TRUE, 
                rol = 'superusuario'
        """, (user_id, entidad_wesco_id))
        print("[OK] Relación 'Wesco - Anixter' creada/actualizada (Permisos Máximos - superusuario)")
        
        # Paso 4: Crear/actualizar direcciones
        print("\n Creando/Actualizando direcciones...")
        
        # Dirección para Independiente y Entregas
        cursor.execute("""
            SELECT id_direccion FROM direcciones 
            WHERE id_user = %s AND nombre = 'Convención 1259 Apto.101'
            LIMIT 1
        """, (user_id,))
        dir_independiente = cursor.fetchone()
        
        if not dir_independiente:
            # Verificar si existe tabla direcciones
            cursor.execute("""
                SELECT COUNT(*) as existe FROM information_schema.tables 
                WHERE table_schema = DATABASE() AND table_name = 'direcciones'
            """)
            tabla_existe = cursor.fetchone()
            
            if tabla_existe and tabla_existe['existe'] > 0:
                cursor.execute("""
                    INSERT INTO direcciones (
                        id_user, nombre, calle, numero, apartamento, 
                        ciudad, departamento, pais, es_principal, activo
                    ) VALUES (
                        %s, 'Convención 1259 Apto.101', 'Convención', '1259', 'Apto.101',
                        'Montevideo', 'Montevideo', 'Uruguay', TRUE, TRUE
                    )
                """, (user_id,))
                print("[OK] Dirección 'Convención 1259 Apto.101' creada")
            else:
                print("[WARN]  Tabla 'direcciones' no existe, omitiendo creación de dirección")
        else:
            print("[OK] Dirección 'Convención 1259 Apto.101' ya existe")
        
        # Dirección para Wesco - Anixter
        cursor.execute("""
            SELECT id_direccion FROM direcciones 
            WHERE id_user = %s AND nombre = 'Sarandí 675 piso 5'
            LIMIT 1
        """, (user_id,))
        dir_wesco = cursor.fetchone()
        
        if not dir_wesco:
            cursor.execute("""
                SELECT COUNT(*) as existe FROM information_schema.tables 
                WHERE table_schema = DATABASE() AND table_name = 'direcciones'
            """)
            tabla_existe = cursor.fetchone()
            
            if tabla_existe and tabla_existe['existe'] > 0:
                cursor.execute("""
                    INSERT INTO direcciones (
                        id_user, nombre, calle, numero, apartamento, 
                        ciudad, departamento, pais, es_principal, activo
                    ) VALUES (
                        %s, 'Sarandí 675 piso 5', 'Sarandí', '675', 'piso 5',
                        'Montevideo', 'Montevideo', 'Uruguay', FALSE, TRUE
                    )
                """, (user_id,))
                print("[OK] Dirección 'Sarandí 675 piso 5' creada")
            else:
                print("[WARN]  Tabla 'direcciones' no existe, omitiendo creación de dirección")
        else:
            print("[OK] Dirección 'Sarandí 675 piso 5' ya existe")
        
        # Paso 5: Establecer entidad activa por defecto (Independiente)
        cursor.execute("""
            UPDATE users 
            SET entidad_activa = %s
            WHERE id_user = %s
        """, (entidad_independiente_id, user_id))
        print(f"[OK] Entidad activa establecida como 'Independiente' (ID: {entidad_independiente_id})")
        
        # Commit cambios
        conn.commit()
        
        # Verificar resultado
        print("\n" + "="*70)
        print(" VERIFICANDO RESULTADO")
        print("="*70)
        
        cursor.execute("""
            SELECT 
                u.id_user,
                u.email,
                u.nombre,
                u.telefono,
                u.activo as usuario_activo,
                u.entidad_activa,
                ue.id_entidad,
                COALESCE(e.nombre, 'Independiente') as entidad_nombre,
                ue.rol,
                ue.es_principal,
                CASE 
                    WHEN ue.rol = 'superusuario' THEN 5
                    WHEN ue.rol = 'admin' THEN 4
                    WHEN ue.rol = 'operador' THEN 3
                    WHEN ue.rol = 'lector' THEN 2
                    ELSE 1
                END as nivel_acceso
            FROM users u
            LEFT JOIN user_entidades ue ON u.id_user = ue.id_user AND ue.activo = TRUE
            LEFT JOIN entidades e ON ue.id_entidad = e.id_entidad
            WHERE u.email = 'cvaralla@gmail.com'
            ORDER BY ue.es_principal DESC, e.nombre ASC
        """)
        
        resultados = cursor.fetchall()
        
        print("\n[OK] PERFILES CREADOS EXITOSAMENTE")
        print("="*70)
        print(f"\n Usuario: Carlos Varalla")
        print(f" Email: cvaralla@gmail.com")
        print(f" Teléfono: +59896800037")
        print(f" Contraseña: Carlos123")
        print(f"\n Perfiles asociados:")
        
        for row in resultados:
            nivel_texto = {
                5: 'Super Admin (Máximo)',
                4: 'Admin',
                3: 'Operador (Básico)',
                2: 'Lector',
                1: 'Básico'
            }.get(row['nivel_acceso'], 'Básico')
            
            principal = "[*] (Principal)" if row['es_principal'] else ""
            activa = "[>] (Activa)" if row['entidad_activa'] == row['id_entidad'] or (row['entidad_activa'] is None and row['id_entidad'] == entidad_independiente_id) else ""
            
            print(f"\n  • {row['entidad_nombre']}")
            print(f"    - Rol: {row['rol']} ({nivel_texto}) {principal} {activa}")
            print(f"    - ID Entidad: {row['id_entidad']}")
        
        print("\n" + "="*70)
        print("[OK] PROCESO COMPLETADO")
        print("="*70)
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logging.error(f"Error creando perfiles: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            try:
                conn.rollback()
            except:
                pass
        print(f"\n[ERROR] Error: {str(e)}")
        return False
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass

if __name__ == "__main__":
    crear_perfiles_carlos()

