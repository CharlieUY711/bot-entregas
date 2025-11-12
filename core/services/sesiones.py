import redis, json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def tiene_sesion(usuario: str) -> bool:
    return r.exists(usuario)

def activar_sesion(usuario: str, estado: str, entrega_id: int | None = None):
    r.set(usuario, json.dumps({"estado": estado, "entrega_id": entrega_id}), ex=3600)

def obtener_estado(usuario: str) -> str:
    data = r.get(usuario)
    if not data:
        return "menu_principal"
    return json.loads(data).get("estado", "menu_principal")

def obtener_entrega(usuario: str) -> int | None:
    data = r.get(usuario)
    if not data:
        return None
    return json.loads(data).get("entrega_id")