#!/bin/bash

# URL del servicio Cloud Run (ajustá si cambia)
SERVICE_URL="https://bot-entregas-xxxxxxxx-uc.a.run.app"

echo "🔍 Verificando / ..."
curl -s "$SERVICE_URL/" | jq

echo "🔍 Verificando /ping-db ..."
curl -s "$SERVICE_URL/ping-db" | jq