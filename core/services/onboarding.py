from services.usuarios import entidad_registrada
from services.notificaciones import notificar_superior
from services.sesiones import activar_sesion
from services.correo import enviar_mail_contacto
from services.db_solicitudes import guardar_solicitud_entidad

def solicitar_datos_entidad(usuario: str) -> str:
    activar_sesion(usuario, estado="esperando_datos_entidad")
    return (
        "👋 Para continuar, necesitamos validar tu entidad.\n"
        "Por favor enviá los siguientes datos:\n"
        "1️⃣ Nombre de la entidad\n"
        "2️⃣ Tu cargo\n"
        "3️⃣ Celular del contacto administrativo\n"
        "4️⃣ Mail del contacto administrativo"
    )

def procesar_formulario_entidad(usuario: str, datos: dict) -> str:
    entidad = datos.get("entidad")
    cargo = datos.get("cargo")
    contacto_cel = datos.get("contacto_cel")
    contacto_mail = datos.get("contacto_mail")

    mensaje = (
        f"📥 Solicitud de acreditación:\n"
        f"Usuario: {usuario}\n"
        f"Entidad: {entidad}\n"
        f"Cargo: {cargo}\n"
        f"Contacto administrativo:\n"
        f"📞 {contacto_cel}\n"
        f"📧 {contacto_mail}"
    )

    notificar_superior("SuperEntregas", mensaje)
    enviar_mail_contacto(contacto_mail, entidad, usuario)
    guardar_solicitud_entidad(usuario, datos)
    activar_sesion(usuario, estado="formulario_enviado")

    return (
        "✅ Recibimos tu solicitud. SuperEntregas revisará la información y te acreditará en menos de 24 horas."
    )