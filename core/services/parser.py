import re

def parsear_formulario(texto: str) -> dict:
    entidad = extraer(texto, r"(?:Entidad|Empresa):?\s*(.+)")
    cargo = extraer(texto, r"(?:Cargo|Rol):?\s*(.+)")
    contacto_cel = extraer(texto, r"(?:Contacto|Celular):?\s*(\+?\d{6,})")
    contacto_mail = extraer(texto, r"(?:Mail|Correo):?\s*([\w\.-]+@[\w\.-]+)")

    return {
        "entidad": entidad,
        "cargo": cargo,
        "contacto_cel": contacto_cel,
        "contacto_mail": contacto_mail
    }

def extraer(texto: str, patron: str) -> str | None:
    match = re.search(patron, texto, re.IGNORECASE)
    return match.group(1).strip() if match else None