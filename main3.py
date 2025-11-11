from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import logging
import uuid
import env  # carga .env si estás en local
from datetime import datetime
from mysql.connector import pooling
from twilio.rest import Client
from config import settings
import os
import uvicorn

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Pool diferido
def get_pool():
    try:
        return pooling.MySQLConnectionPool(pool_name="entregas_pool", pool_size=5, **settings.dbconfig())
    except Exception as e:
        logging.exception("Error inicializando pool MySQL")
        return None

# Cliente Twilio
try:
    twilio_client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH)
except Exception as e:
    logging.exception("Error inicializando cliente Twilio")
    twilio_client = None

# Guardar pedido
def guardar_pedido_en_ent_pedidos(body_text: str, from_number: str) -> str:
    codigo = f"ENT-{uuid.uuid4().hex[:8].upper()}"
    pool = get_pool()
    if not pool:
        raise Exception("Pool MySQL no disponible")
    conn = pool.get_connection()
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
            "",
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

# Endpoint raíz
@app.get("/")
def root():
    return {"status": "ok", "mensaje": "API Entregas operativa ✅"}

# Verificación de base
@app.get("/ping-db")
def ping_db():
    try:
        pool = get_pool()
        if not pool:
            raise Exception("Pool MySQL no disponible")
        conn = pool.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        return {"ok": True, "mensaje": "Conexión MySQL ok ✅"}
    except Exception as e:
        logging.exception("Error conexión MySQL")
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})

# Webhook WhatsApp
@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    body = form.get("Body", "").strip()
    from_number = form.get("From", "")
    logging.info(f"Mensaje recibido de {from_number}: {body}")
    try:
        codigo = guardar_pedido_en_ent_pedidos(body, from_number)
        respuesta = f"✅ Recibimos tu pedido. Código: {codigo}. Te avisamos cuando esté en proceso."
    except Exception as e:
        logging.exception("Error al guardar el pedido")
        respuesta = "⚠️ Tuvimos un problema registrando tu pedido. Probá de nuevo en unos minutos."
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response><Message>{respuesta}</Message></Response>'''
    return PlainTextResponse(content=twiml, media_type="application/xml")

# Envío de mensajes
@app.post("/enviar-mensaje")
async def enviar_mensaje(request: Request):
    data = await request.json()
    to = data.get("to")
    body = data.get("body")
    if not twilio_client:
        return JSONResponse(status_code=500, content={"status": "error", "detalle": "Twilio no disponible"})
    try:
        msg = twilio_client.messages.create(from_=settings.TWILIO_NUMBER, to=to, body=body)
        return {"status": "ok", "sid": msg.sid}
    except Exception as e:
        logging.exception("Error enviando mensaje por Twilio")
        return JSONResponse(status_code=500, content={"status": "error", "detalle": str(e)})

# Arranque para Cloud Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)