-- Crea la tabla 'pedidos' si no existe
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- ID único autoincremental
    direccion VARCHAR(255),                          -- Dirección de entrega (opcional)
    destinatario VARCHAR(255),                       -- Nombre del destinatario (opcional)
    fecha_deseada DATE,                              -- Fecha solicitada para la entrega (opcional)
    prioridad VARCHAR(50),                           -- Nivel de prioridad (alta, media, baja)
    observaciones TEXT,                              -- Texto libre con detalles del pedido
    codigo_pedido VARCHAR(20) UNIQUE,                -- Código único generado por el sistema
    numero_whatsapp VARCHAR(50),                     -- Número de WhatsApp del cliente
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Fecha y hora de creación del pedido
);