#!/bin/bash

gcloud builds submit --tag southamerica-east1-docker.pkg.dev/entregas-476319/bot-entregas-repo/bot-entregas

gcloud run deploy bot-entregas \
  --image southamerica-east1-docker.pkg.dev/entregas-476319/bot-entregas-repo/bot-entregas \
  --platform managed \
  --region southamerica-east1 \
  --set-env-vars DB_SOCKET=/cloudsql/entregas-476319:southamerica-east1:entregas-db,DB_USER=bot_entregas,DB_PASS=$DBPASS,DB_NAME=entregas-db,TWILIO_SID=ACeb8fc0ede5a0ddd674c616211ba82ec4,TWILIO_AUTH=f748f0b0801035cd4273f12b31da095c,TWILIO_NUMBER=whatsapp:+59899953871 \
  --add-cloudsql-instances entregas-476319:southamerica-east1:entregas-db \
  --allow-unauthenticated