def cliente_es_receptor(remito_id: int, cliente_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cliente_receptor_id
        FROM remitos
        WHERE id = %s
    """, (remito_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result and result[0] == cliente_id