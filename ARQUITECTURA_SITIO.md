# 📐 Arquitectura del Sitio - www.entregas.com.uy

## 🌐 Resumen General

El sitio está completamente alojado en **Google Cloud Platform** con la siguiente estructura:

---

## 📍 FRONTEND (Sitio Web Público)

### **Ubicación:**
- **URL Pública**: https://www.entregas.com.uy
- **Alojamiento**: Google Cloud Storage
- **Bucket**: `gs://www.entregas.com.uy`
- **Alternativa**: Firebase Hosting (configurado en `firebase.json`)

### **Código Fuente:**
- **Directorio**: `frontend/src/`
- **Build Compilado**: `frontend/dist/`
- **Framework**: React + Vite + TypeScript
- **Estilos**: Tailwind CSS

### **Estructura del Frontend:**

#### 1. **Landing/Login** (Página Inicial)
- **Archivo**: `frontend/src/pages/Login.tsx`
- **Descripción**: Primera página que ve el usuario al entrar al sitio
- **Contenido**: 
  - Título "Plataforma de Entregas"
  - Botón "Aceptar" para acceder al dashboard
- **Ruta**: Se muestra cuando `isAuthenticated = false`

#### 2. **Dashboard** (Página Principal)
- **Archivo**: `frontend/src/App.tsx` (líneas 16-57)
- **Descripción**: Panel principal después del login
- **Contenido**:
  - Header con título y botón "Cerrar Sesión"
  - Menú de navegación:
    - Dashboard (activo)
    - Entregas Perdidos
    - Perfil
  - Área de contenido principal
- **Ruta**: Se muestra cuando `isAuthenticated = true`

### **Flujo de Navegación:**
```
Usuario entra a www.entregas.com.uy
    ↓
Ve Login.tsx (página de bienvenida)
    ↓
Hace clic en "Aceptar"
    ↓
Ve Dashboard (App.tsx con menú)
```

---

## 🔧 BACKEND (API)

### **Ubicación:**
- **Servicio**: Google Cloud Run
- **Nombre del Servicio**: `bot-entregas`
- **Región**: `southamerica-east1`
- **URL**: `https://bot-entregas-vqbx52hmoq-rj.a.run.app`

### **Código Fuente:**
- **Archivo Principal**: `main.py`
- **Framework**: FastAPI (Python)
- **Base de Datos**: MySQL (Cloud SQL)
- **Endpoints Principales**:
  - `/check-email` - Verificar email de usuario

---

## 📦 Despliegue

### **Frontend:**
```powershell
# Construir
cd frontend
npm run build

# Desplegar
gsutil -m rsync -r -d frontend/dist/ gs://www.entregas.com.uy/
```

### **Backend:**
```powershell
# Desplegar a Cloud Run
gcloud run deploy bot-entregas --source .
```

---

## 🔄 Configuración Actual

### **Estado del Código:**
- ✅ **Login.tsx**: Funcional con botón "Aceptar"
- ✅ **App.tsx**: Dashboard básico con menú
- ❌ **Perfil.tsx**: Eliminado (estaba causando problemas)
- ⚠️ **Entregas Perdidos**: Menú existe pero sin componente

### **Problemas Conocidos:**
- El dashboard muestra un menú básico
- Las páginas "Entregas Perdidos" y "Perfil" del menú no tienen componentes implementados
- Necesita crear los componentes faltantes o restaurar el código original

---

## 📝 Notas Importantes

1. **El sitio está en Cloud Storage**, no en Firebase Hosting activo
2. **Todo el frontend es una SPA (Single Page Application)** - React maneja el routing
3. **No hay routing real** - Todo está en `App.tsx` con estado `isAuthenticated`
4. **El backend está separado** en Cloud Run y se comunica vía API REST

---

## 🎯 Próximos Pasos Sugeridos

1. Crear componentes para "Entregas Perdidos" y "Perfil"
2. Implementar routing con React Router si se necesita navegación real
3. Conectar el dashboard con el backend para obtener datos reales
4. Restaurar el código original del dashboard si existe en otro lugar
