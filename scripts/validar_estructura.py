import os

estructura = {
    "main.py": "archivo",
    "requirements.txt": "archivo",
    "Dockerfile": "archivo",
    ".env": "archivo",
    "README.md": "archivo",
    "config": "carpeta",
    "config/env.py": "archivo",
    "repositories": "carpeta",
    "repositories/pedidos.py": "archivo",
    "services": "carpeta",
    "services/twilio_service.py": "archivo",
    "utils": "carpeta",
    "utils/db_pool.py": "archivo",
    "utils/logger.py": "archivo",
    "models": "carpeta",
    "models/mensaje.py": "archivo",
    "scripts": "carpeta",
    "scripts/init_db.sql": "archivo",
    "tests": "carpeta",
    "tests/test_ping.py": "archivo",
    "tests/test_whatsapp.py": "archivo",
    "tests/test_enviar_mensaje.py": "archivo",
}

validaciones_contenido = {
    "main.py": ["FastAPI", "app =", "def root", "def ping"],
    "Dockerfile": ["uvicorn", "EXPOSE 8080"],
    "requirements.txt": ["fastapi", "uvicorn", "mysql-connector-python", "twilio"],
    "utils/db_pool.py": ["pooling", "init_pool", "ping_db"],
    "services/twilio_service.py": ["twilio.rest", "Client", "enviar_twilio"],
    "repositories/pedidos.py": ["guardar_pedido_simple", "INSERT INTO pedidos"],
}

def validar_estructura(base_path="."):
    errores = []
    for ruta, tipo in estructura.items():
        full_path = os.path.join(base_path, ruta)
        if tipo == "archivo" and not os.path.isfile(full_path):
            errores.append(f"❌ Falta archivo: {ruta}")
        elif tipo == "carpeta" and not os.path.isdir(full_path):
            errores.append(f"❌ Falta carpeta: {ruta}")
    return errores

def validar_contenido(base_path="."):
    errores = []
    for ruta, claves in validaciones_contenido.items():
        full_path = os.path.join(base_path, ruta)
        if os.path.isfile(full_path):
            try:
                with open(full_path, encoding="utf-8") as f:
                    contenido = f.read().replace(" ", "").lower()
                    for clave in claves:
                        if clave.replace(" ", "").lower() not in contenido:
                            errores.append(f"⚠️ Falta '{clave}' en {ruta}")
            except Exception as e:
                errores.append(f"⚠️ No se pudo leer {ruta}: {e}")
    return errores

if __name__ == "__main__":
    print("📦 Validando estructura del proyecto Bot_Entregas...")
    errores_estructura = validar_estructura()
    errores_contenido = validar_contenido()

    if errores_estructura or errores_contenido:
        print("\n🔍 Validación incompleta:")
        for e in errores_estructura + errores_contenido:
            print(e)
    else:exit

        print("\n✅ Estructura y contenido mínimo verificados correctamente.")