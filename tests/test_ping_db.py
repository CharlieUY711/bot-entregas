import requests

# Reemplazá esta URL por la real de tu servicio en Cloud Run
SERVICE_URL = "https://bot-entregas-xxxxxxxx-uc.a.run.app"

def test_ping_db():
    response = requests.get(f"{SERVICE_URL}/ping-db")
    assert response.status_code == 200
    data = response.json()
    assert data.get("ok") is True
    assert "Conexión MySQL ok" in data.get("mensaje", "")