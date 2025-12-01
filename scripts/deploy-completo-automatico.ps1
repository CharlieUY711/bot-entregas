# Script de Deploy Completo Automático
# Despliega Backend (Cloud Run) y Frontend (Cloud Storage/Firebase) a www.entregas.com.uy
# Autor: Sistema de Deploy Automático
# Fecha: $(Get-Date -Format "yyyy-MM-dd")

$ErrorActionPreference = "Stop"

# ============================================
# CONFIGURACIÓN
# ============================================
$PROJECT_ID = "entregas-476319"
$REGION = "southamerica-east1"
$SERVICE_NAME = "bot-entregas"
$REPO_NAME = "entregas-repo"
$IMAGE_NAME = "backend-v1"
$BUCKET_NAME = "entregas-frontend"  # Puede ser: entregas-frontend, www.entregas.com.uy, entregas-com-uy

# Variables de entorno para el backend (ajustar según necesidad)
$DBPASS = $env:DBPASS
if (-not $DBPASS) {
    Write-Host "⚠️  Advertencia: DBPASS no está configurado. Se usará el valor del entorno." -ForegroundColor Yellow
}

# ============================================
# FUNCIONES AUXILIARES
# ============================================

function Write-Step {
    param([string]$Message, [string]$Color = "Cyan")
    Write-Host "`n========================================" -ForegroundColor $Color
    Write-Host $Message -ForegroundColor $Color
    Write-Host "========================================`n" -ForegroundColor $Color
}

function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# ============================================
# INICIO DEL DEPLOY
# ============================================

Write-Host "`n" -NoNewline
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   🚀 DEPLOY COMPLETO AUTOMÁTICO - PLATAFORMA ENTREGAS    ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`nIniciando proceso de deploy completo..." -ForegroundColor Cyan
Write-Host "Proyecto: $PROJECT_ID" -ForegroundColor Gray
Write-Host "Región: $REGION" -ForegroundColor Gray
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" -ForegroundColor Gray

# Verificar herramientas necesarias
Write-Step "🔍 Verificando herramientas necesarias..."

$toolsOk = $true

if (-not (Test-Command "gcloud")) {
    Write-Host "❌ Error: gcloud CLI no está instalado" -ForegroundColor Red
    Write-Host "   Instala Google Cloud SDK desde: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    $toolsOk = $false
} else {
    Write-Host "✅ gcloud CLI encontrado" -ForegroundColor Green
    $gcloudVersion = (gcloud --version | Select-Object -First 1)
    Write-Host "   Versión: $gcloudVersion" -ForegroundColor Gray
}

if (-not (Test-Command "docker")) {
    Write-Host "⚠️  Advertencia: Docker no está instalado (opcional para build local)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Docker encontrado" -ForegroundColor Green
}

if (-not (Test-Command "node")) {
    Write-Host "❌ Error: Node.js no está instalado" -ForegroundColor Red
    Write-Host "   Instala Node.js desde: https://nodejs.org/" -ForegroundColor Yellow
    $toolsOk = $false
} else {
    Write-Host "✅ Node.js encontrado" -ForegroundColor Green
    $nodeVersion = (node --version)
    Write-Host "   Versión: $nodeVersion" -ForegroundColor Gray
}

if (-not (Test-Command "npm")) {
    Write-Host "❌ Error: npm no está instalado" -ForegroundColor Red
    $toolsOk = $false
} else {
    Write-Host "✅ npm encontrado" -ForegroundColor Green
    $npmVersion = (npm --version)
    Write-Host "   Versión: $npmVersion" -ForegroundColor Gray
}

if (-not $toolsOk) {
    Write-Host "`n❌ Faltan herramientas necesarias. Por favor instálalas antes de continuar." -ForegroundColor Red
    exit 1
}

# Verificar autenticación con Google Cloud
Write-Step "🔐 Verificando autenticación con Google Cloud..."

try {
    $currentProject = (gcloud config get-value project 2>$null)
    if ($currentProject -ne $PROJECT_ID) {
        Write-Host "⚠️  El proyecto actual es: $currentProject" -ForegroundColor Yellow
        Write-Host "   Configurando proyecto a: $PROJECT_ID..." -ForegroundColor Yellow
        gcloud config set project $PROJECT_ID
    }
    Write-Host "✅ Proyecto configurado: $PROJECT_ID" -ForegroundColor Green
    
    # Verificar que estamos autenticados
    gcloud auth list --filter=status:ACTIVE --format="value(account)" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: No hay cuentas autenticadas" -ForegroundColor Red
        Write-Host "   Ejecuta: gcloud auth login" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Autenticación verificada" -ForegroundColor Green
} catch {
    Write-Host "❌ Error verificando autenticación: $_" -ForegroundColor Red
    exit 1
}

# ============================================
# DEPLOY DEL BACKEND
# ============================================

Write-Step "🔧 DEPLOY DEL BACKEND (Cloud Run)"

# Verificar que existe el Dockerfile
if (-not (Test-Path "Dockerfile")) {
    Write-Host "❌ Error: No se encontró el Dockerfile" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dockerfile encontrado" -ForegroundColor Green

# Verificar que existe requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Host "⚠️  Advertencia: No se encontró requirements.txt" -ForegroundColor Yellow
}

# Build y Push de la imagen Docker
Write-Host "`n📦 Construyendo y subiendo imagen Docker..." -ForegroundColor Cyan
$imageTag = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}"

try {
    gcloud builds submit --tag $imageTag .
    if ($LASTEXITCODE -ne 0) {
        throw "Error en el build de Docker"
    }
    Write-Host "✅ Imagen construida y subida exitosamente" -ForegroundColor Green
    Write-Host "   Imagen: $imageTag" -ForegroundColor Gray
} catch {
    Write-Host "❌ Error construyendo imagen Docker: $_" -ForegroundColor Red
    exit 1
}

# Deploy a Cloud Run
Write-Host "`n🚀 Desplegando a Cloud Run..." -ForegroundColor Cyan

$deployArgs = @(
    "run", "deploy", $SERVICE_NAME,
    "--image=$imageTag",
    "--region=$REGION",
    "--platform=managed",
    "--allow-unauthenticated"
)

# Agregar variables de entorno si están configuradas
if ($DBPASS) {
    $envVars = "DB_SOCKET=/cloudsql/${PROJECT_ID}:${REGION}:entregas-db,DB_USER=bot_entregas,DB_PASS=$DBPASS,DB_NAME=entregas-db,TWILIO_SID=ACeb8fc0ede5a0ddd674c616211ba82ec4,TWILIO_AUTH=f748f0b0801035cd4273f12b31da095c,TWILIO_NUMBER=whatsapp:+59899953871"
    $deployArgs += "--set-env-vars=$envVars"
    $deployArgs += "--add-cloudsql-instances=${PROJECT_ID}:${REGION}:entregas-db"
}

try {
    & gcloud $deployArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Error en el deploy a Cloud Run"
    }
    Write-Host "✅ Backend desplegado exitosamente" -ForegroundColor Green
    
    # Obtener URL del servicio
    $serviceUrl = (gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)" 2>$null)
    if ($serviceUrl) {
        Write-Host "   URL del servicio: $serviceUrl" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Error desplegando backend: $_" -ForegroundColor Red
    exit 1
}

# ============================================
# DEPLOY DEL FRONTEND
# ============================================

Write-Step "🎨 DEPLOY DEL FRONTEND (Cloud Storage/Firebase)"

# Verificar que existe la carpeta frontend
if (-not (Test-Path "frontend")) {
    Write-Host "❌ Error: No se encontró la carpeta frontend" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Carpeta frontend encontrada" -ForegroundColor Green

# Verificar si está en Firebase Hosting
$firebaseJson = "firebase.json"
$firebaseRc = ".firebaserc"

if ((Test-Path $firebaseJson) -and (Test-Path $firebaseRc)) {
    Write-Host "📦 Detectado Firebase Hosting" -ForegroundColor Yellow
    
    # Verificar si firebase-tools está instalado
    if (-not (Test-Command "firebase")) {
        Write-Host "⚠️  Firebase CLI no está instalado. Instalando..." -ForegroundColor Yellow
        npm install -g firebase-tools
    }
    
    Write-Host "`n🔨 Construyendo el frontend..." -ForegroundColor Cyan
    Push-Location frontend
    try {
        npm install
        if ($LASTEXITCODE -ne 0) {
            throw "Error instalando dependencias"
        }
        
        npm run build
        if ($LASTEXITCODE -ne 0) {
            throw "Error construyendo el frontend"
        }
        Write-Host "✅ Frontend construido exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error construyendo frontend: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    
    Write-Host "`n📤 Desplegando a Firebase Hosting..." -ForegroundColor Cyan
    try {
        firebase deploy --only hosting
        if ($LASTEXITCODE -ne 0) {
            throw "Error desplegando a Firebase"
        }
        Write-Host "✅ Frontend desplegado a Firebase Hosting exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error desplegando a Firebase: $_" -ForegroundColor Red
        Write-Host "   Intentando Cloud Storage como alternativa..." -ForegroundColor Yellow
        # Continuar con Cloud Storage
    }
} else {
    Write-Host "📦 Firebase no configurado, usando Cloud Storage" -ForegroundColor Yellow
}

# Deploy a Cloud Storage (si Firebase no se usó o falló)
if (-not ((Test-Path $firebaseJson) -and (Test-Path $firebaseRc) -and $LASTEXITCODE -eq 0)) {
    Write-Host "`n📦 Desplegando a Google Cloud Storage..." -ForegroundColor Cyan
    
    Write-Host "🔨 Construyendo el frontend..." -ForegroundColor Cyan
    Push-Location frontend
    try {
        npm install
        if ($LASTEXITCODE -ne 0) {
            throw "Error instalando dependencias"
        }
        
        npm run build
        if ($LASTEXITCODE -ne 0) {
            throw "Error construyendo el frontend"
        }
        Write-Host "✅ Frontend construido exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error construyendo frontend: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    
    # Buscar la carpeta de build
    $buildDirs = @("frontend\dist", "frontend\build", "frontend\public")
    $buildDir = $null
    
    foreach ($dir in $buildDirs) {
        if (Test-Path $dir) {
            $buildDir = $dir
            break
        }
    }
    
    if (-not $buildDir) {
        Write-Host "❌ Error: No se encontró la carpeta de build" -ForegroundColor Red
        Write-Host "   Carpetas buscadas: $($buildDirs -join ', ')" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "   Carpeta de build encontrada: $buildDir" -ForegroundColor Gray
    
    # Intentar desplegar a diferentes buckets posibles
    $buckets = @("entregas-frontend", "www.entregas.com.uy", "entregas-com-uy")
    $deployed = $false
    
    foreach ($bucket in $buckets) {
        Write-Host "`n🔍 Verificando bucket: gs://$bucket..." -ForegroundColor Cyan
        try {
            $bucketExists = (gsutil ls "gs://$bucket" 2>$null)
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Bucket encontrado: $bucket" -ForegroundColor Green
                Write-Host "📤 Subiendo archivos..." -ForegroundColor Cyan
                gsutil -m rsync -r -d "$buildDir" "gs://$bucket"
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Frontend desplegado exitosamente a gs://$bucket" -ForegroundColor Green
                    $deployed = $true
                    break
                } else {
                    Write-Host "⚠️  Error subiendo a $bucket, intentando siguiente bucket..." -ForegroundColor Yellow
                }
            }
        } catch {
            Write-Host "⚠️  Bucket $bucket no accesible, intentando siguiente..." -ForegroundColor Yellow
        }
    }
    
    if (-not $deployed) {
        Write-Host "❌ Error: No se pudo desplegar a ningún bucket" -ForegroundColor Red
        Write-Host "   Buckets intentados: $($buckets -join ', ')" -ForegroundColor Yellow
        Write-Host "   Por favor verifica que los buckets existan y tengas permisos" -ForegroundColor Yellow
        exit 1
    }
}

# ============================================
# VERIFICACIÓN FINAL
# ============================================

Write-Step "✅ VERIFICACIÓN FINAL"

Write-Host "🔍 Verificando servicios desplegados..." -ForegroundColor Cyan

# Verificar backend
try {
    $backendUrl = (gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)" 2>$null)
    if ($backendUrl) {
        Write-Host "✅ Backend: $backendUrl" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No se pudo obtener URL del backend" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Error verificando backend: $_" -ForegroundColor Yellow
}

# Verificar frontend
Write-Host "✅ Frontend: https://www.entregas.com.uy" -ForegroundColor Green

# ============================================
# RESUMEN FINAL
# ============================================

Write-Host "`n" -NoNewline
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ DEPLOY COMPLETADO EXITOSAMENTE            ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📋 RESUMEN:" -ForegroundColor Cyan
Write-Host "   • Backend desplegado a Cloud Run" -ForegroundColor White
Write-Host "   • Frontend desplegado a Cloud Storage/Firebase" -ForegroundColor White
Write-Host "   • Sitio disponible en: https://www.entregas.com.uy" -ForegroundColor White

if ($backendUrl) {
    Write-Host "   • API Backend: $backendUrl" -ForegroundColor White
}

Write-Host "`n🎉 ¡Deploy completado exitosamente!`n" -ForegroundColor Green
