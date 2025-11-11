# Bot de Entregas API

API para recibir pedidos por WhatsApp, guardarlos en MySQL y enviar mensajes salientes. Desarrollada con FastAPI, desplegada en Cloud Run, conectada a Cloud SQL y Twilio.

## Endpoints
- `GET /` → Estado del servicio
- `GET /ping-db` → Verifica conexión a MySQL
- `POST /whatsapp` → Webhook de recepción de pedidos
- `POST /enviar-mensaje` → Envío de mensajes salientes

## Estructura
- `main.py` → Rutas
- `repositories/` → Acceso a DB
- `services/` → Twilio
- `utils/` → Pool y logging
- `models/` → Validación
- `scripts/` → SQL