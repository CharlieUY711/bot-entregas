from services.db import get_connection

def entrega_asignada_a_usuario(entrega_id: int, usuario: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM entregas
        WHERE id = %s AND chofer_usuario = %s
    """, (entrega_id, usuario))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return bool(result)