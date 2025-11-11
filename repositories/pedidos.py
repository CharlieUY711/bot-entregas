from utils.db_pool import init_pool, cnxpool
import uuid
from datetime import datetime

def guardar_pedido_en_ent_pedidos(body_text: str, from_number: str) -> str:
    init_pool()
    codigo = f"ENT-{uuid.uuid4().hex[:8].upper()}"
    conn = cnxpool.get_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        INSERT INTO ent_pedidos (
            codigo_pedido, cliente_nombre, cliente_telefono,
            fecha_pedido, prioridad, observaciones, estado, bot_type
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (
            codigo,
            "",  # cliente_nombre opcional
            from_number,
            datetime.now(),
            "media",
            body_text,
            "pendiente",
            "oddy"
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return codigo