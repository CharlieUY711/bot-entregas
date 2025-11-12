from services.db import get_connection

def registrar_interaccion(usuario: str, estado: str, mensaje: str, entrega_id: int | None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interacciones_bot (usuario, estado, mensaje, entrega_id)
        VALUES (%s, %s, %s, %s)
    """, (usuario, estado, mensaje, entrega_id))
    conn.commit()
    cursor.close()
    conn.close()