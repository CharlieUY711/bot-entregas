import os
import logging
from fastapi.responses import JSONResponse
from twilio.rest import Client

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

def enviar_twilio(to: str, body: str):
    try:
        msg = twilio_client.messages.create(from_=TWILIO_NUMBER, to=to, body=body)
        return {"status": "ok", "sid": msg.sid}
    except Exception as e:
        logging.exception("Error enviando mensaje por Twilio")
        return JSONResponse(status_code=500, content={"status": "error", "detalle": str(e)})