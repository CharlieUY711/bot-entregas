from services.db import get_connection

def obtener_rol(usuario: str) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE usuario = %s", (usuario,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def obtener_cliente(usuario: str) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cliente_id FROM usuarios WHERE usuario = %s", (usuario,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None