from services.entregas import entrega_asignada_a_usuario

def requiere_entrega_asignada(func):
    def wrapper(usuario, mensaje, estado, entrega_id):
        if not entrega_id or not entrega_asignada_a_usuario(entrega_id, usuario):
            return "❌ No tienes acceso a esta entrega."
        return func(usuario, mensaje, estado, entrega_id)
    return wrapper