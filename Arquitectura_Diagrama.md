# 📊 Diagrama de Arquitectura - Plataforma de Entregas

## 🎯 Punto de Reconstrucción del Sistema

Este documento contiene el diagrama visual completo de la arquitectura del sistema para facilitar la reconstrucción y comprensión del proyecto.

---

## 🏗️ Arquitectura Completa del Sistema

```mermaid
graph TB
    subgraph "🌐 Internet"
        Usuario[👤 Usuario]
        WhatsApp[📱 WhatsApp/Twilio]
    end

    subgraph "☁️ Google Cloud Platform"
        subgraph "Frontend"
            GCS[📦 Google Cloud Storage<br/>Bucket: www.entregas.com.uy<br/>URL: https://www.entregas.com.uy]
            FrontendCode[⚛️ React + Vite + TypeScript<br/>frontend/src/]
        end

        subgraph "Backend"
            CloudRun[🚀 Cloud Run<br/>bot-entregas<br/>southamerica-east1<br/>URL: https://bot-entregas-vqbx52hmoq-rj.a.run.app]
            BackendCode[🐍 FastAPI Python<br/>main.py]
        end

        subgraph "Base de Datos"
            CloudSQL[(🗄️ Cloud SQL MySQL<br/>Base de Datos)]
        end

        subgraph "CI/CD"
            GitHub[📦 GitHub Repository<br/>CharlieUY711/bot-entregas]
            GitHubActions[⚙️ GitHub Actions<br/>Workflows de Deploy]
        end
    end

    subgraph "💻 Desarrollo Local"
        LocalFrontend[⚛️ Frontend Local<br/>localhost:5173<br/>npm run dev]
        LocalBackend[🐍 Backend Local<br/>localhost:8000<br/>uvicorn main:app]
    end

    %% Flujos de Usuario
    Usuario -->|HTTPS| GCS
    Usuario -->|API Calls| CloudRun
    
    %% Flujos de WhatsApp
    WhatsApp -->|Webhook| CloudRun
    CloudRun -->|Enviar Mensajes| WhatsApp
    
    %% Flujos Backend-DB
    CloudRun -->|Queries| CloudSQL
    BackendCode -->|Pool de Conexiones| CloudSQL
    
    %% Flujos de Deploy
    GitHub -->|Push| GitHubActions
    GitHubActions -->|Deploy| CloudRun
    GitHubActions -->|Deploy| GCS
    
    %% Flujos de Desarrollo
    LocalFrontend -->|Proxy| LocalBackend
    LocalBackend -->|Conexión| CloudSQL
    
    %% Estilos
    classDef frontend fill:#61dafb,stroke:#20232a,stroke-width:2px,color:#000
    classDef backend fill:#009688,stroke:#004d40,stroke-width:2px,color:#fff
    classDef database fill:#f29111,stroke:#d68910,stroke-width:2px,color:#000
    classDef cloud fill:#4285f4,stroke:#1a73e8,stroke-width:2px,color:#fff
    classDef local fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    
    class GCS,FrontendCode,LocalFrontend frontend
    class CloudRun,BackendCode,LocalBackend backend
    class CloudSQL database
    class GitHub,GitHubActions cloud
    class LocalFrontend,LocalBackend local
```

---

## 🔄 Flujo de Datos - Proceso de Entrega

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend<br/>(React)
    participant B as Backend<br/>(FastAPI)
    participant DB as MySQL<br/>(Cloud SQL)
    participant W as WhatsApp<br/>(Twilio)

    Note over U,W: Flujo de Autenticación
    U->>F: Accede a www.entregas.com.uy
    F->>F: Muestra Login.tsx
    U->>F: Clic en "Aceptar"
    F->>B: POST /check-email
    B->>DB: Verificar usuario
    DB-->>B: Datos del usuario
    B-->>F: Token/Auth
    F->>F: Muestra Dashboard

    Note over U,W: Flujo de Recepción de Pedido
    W->>B: POST /whatsapp (Webhook)
    B->>DB: Guardar pedido
    B->>DB: Actualizar estado
    B-->>W: Confirmación

    Note over U,W: Flujo de Envío de Mensaje
    U->>F: Acción en Dashboard
    F->>B: POST /enviar-mensaje
    B->>DB: Consultar datos
    B->>W: Enviar mensaje
    W-->>B: Confirmación
    B-->>F: Respuesta
    F-->>U: Notificación
```

---

## 📁 Estructura de Directorios

```mermaid
graph LR
    subgraph "Proyecto Root"
        A[09_Bot_Entregas/]
        A --> B[frontend/]
        A --> C[core/]
        A --> D[config/]
        A --> E[utils/]
        A --> F[scripts/]
        A --> G[.github/]
        A --> H[main.py]
    end

    subgraph "Frontend"
        B --> B1[src/]
        B --> B2[dist/]
        B --> B3[package.json]
        B1 --> B1a[pages/]
        B1 --> B1b[App.tsx]
        B1 --> B1c[main.tsx]
        B1a --> B1a1[Login.tsx]
        B1a --> B1a2[Perfil.tsx]
    end

    subgraph "Backend"
        C --> C1[services/]
        C --> C2[tests/]
        C1 --> C1a[onboarding.py]
        C1 --> C1b[parser.py]
        C1 --> C1c[remitos.py]
        C1 --> C1d[twilio_service.py]
    end

    subgraph "Scripts"
        F --> F1[deploy-completo-automatico.ps1]
        F --> F2[verificar-bucket.ps1]
        F --> F3[validar_estructura.py]
    end

    subgraph "GitHub Actions"
        G --> G1[workflows/]
        G1 --> G1a[deploy.yaml]
        G1 --> G1b[deploy-frontend.yaml]
    end
```

---

## 🔐 Componentes y Tecnologías

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS
- **Hosting**: Google Cloud Storage
- **URL**: https://www.entregas.com.uy

### Backend
- **Framework**: FastAPI (Python)
- **Servidor**: Uvicorn
- **Hosting**: Google Cloud Run
- **Región**: southamerica-east1
- **URL**: https://bot-entregas-vqbx52hmoq-rj.a.run.app

### Base de Datos
- **Tipo**: MySQL
- **Hosting**: Google Cloud SQL
- **Pool de Conexiones**: MySQL Connector Pool

### Integraciones
- **WhatsApp**: Twilio API
- **CI/CD**: GitHub Actions
- **Storage**: Google Cloud Storage

---

## 🚀 Procesos de Deploy

```mermaid
graph TB
    Start[Inicio] --> Check{¿Cambio en<br/>frontend/src?}
    Check -->|Sí| BuildFrontend[Build Frontend<br/>npm run build]
    Check -->|No| CheckBackend{¿Cambio en<br/>Backend?}
    
    BuildFrontend --> DeployFrontend[Deploy a GCS<br/>gsutil rsync]
    DeployFrontend --> End[Fin]
    
    CheckBackend -->|Sí| BuildBackend[Build Backend<br/>Docker]
    CheckBackend -->|No| End
    
    BuildBackend --> DeployBackend[Deploy a Cloud Run<br/>gcloud run deploy]
    DeployBackend --> End
    
    style BuildFrontend fill:#61dafb
    style BuildBackend fill:#009688
    style DeployFrontend fill:#4285f4
    style DeployBackend fill:#4285f4
```

---

## 📋 Endpoints Principales

### Backend API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado del servicio |
| GET | `/ping-db` | Verificación de conexión MySQL |
| POST | `/whatsapp` | Webhook de recepción de pedidos |
| POST | `/enviar-mensaje` | Envío de mensajes salientes |
| POST | `/check-email` | Verificar email de usuario |

---

## 🔧 Variables de Entorno

### Backend (.env)
- `DB_HOST`: Host de Cloud SQL
- `DB_USER`: Usuario de MySQL
- `DB_PASSWORD`: Contraseña de MySQL
- `DB_NAME`: Nombre de la base de datos
- `TWILIO_ACCOUNT_SID`: Account SID de Twilio
- `TWILIO_AUTH_TOKEN`: Auth Token de Twilio
- `TWILIO_PHONE_NUMBER`: Número de teléfono de Twilio

### Frontend
- `VITE_API_URL`: URL del backend (producción o local)

---

## 📝 Notas de Reconstrucción

1. **Frontend**: El código fuente está en `frontend/src/`, el build compilado en `frontend/dist/`
2. **Backend**: El código principal está en `main.py` y los servicios en `core/services/`
3. **Base de Datos**: La conexión se configura en `config/env.py` y `config.py`
4. **Deploy**: Los scripts automatizados están en `scripts/`
5. **CI/CD**: Los workflows están en `.github/workflows/`

---

## 🎯 Estado Actual del Sistema

- ✅ Frontend desplegado en GCS
- ✅ Backend desplegado en Cloud Run
- ✅ Base de datos en Cloud SQL
- ✅ GitHub Actions configurado
- ✅ Integración con Twilio funcionando
- ⚠️ Algunos componentes del frontend pendientes (Perfil, Entregas Perdidos)

---

*Última actualización: $(Get-Date -Format "yyyy-MM-dd")*
