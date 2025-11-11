import os
import logging
from fastapi.responses import JSONResponse
from mysql.connector import pooling

cnxpool = None

def init_pool():
    global cnxpool
    if cnxpool is None:
        is_cloud_run = os.getenv("K_SERVICE") is not None
        dbconfig = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "database": os.getenv("DB_NAME"),
            "host": os.getenv("DB_HOST") if is_cloud_run else "127.0.0.1"
        }
        if not is_cloud_run:
            dbconfig["port"] = 3306
        cnxpool = pooling.MySQLConnectionPool(pool_name="entregas_pool", pool_size=5, **dbconfig)

def ping_db():
    try:
        init_pool()
        conn = cnxpool.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        return {"ok": True, "mensaje": "Conexión MySQL ok ✅"}
    except Exception as e:
        logging.exception("Error conexión MySQL")
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})