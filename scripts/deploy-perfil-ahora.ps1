# Script rápido para desplegar el componente Perfil a www.entregas.com.uy
# Ejecutar desde la raíz del proyecto

$ErrorActionPreference = "Stop"

Write-Host "🚀 Desplegando componente Perfil a www.entregas.com.uy..." -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "frontend\src\pages\Perfil.tsx")) {
    Write-Host "❌ Error: Ejecuta este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

# Opción 1: Si está en Firebase Hosting
if (Test-Path "firebase.json") {
    Write-Host "📦 Detectado Firebase Hosting" -ForegroundColor Yellow
    
    Set-Location frontend
    Write-Host "🔨 Construyendo frontend..." -ForegroundColor Cyan
    npm run build
    
    Set-Location ..
    Write-Host "📤 Desplegando a Firebase..." -ForegroundColor Cyan
    firebase deploy --only hosting
    
    Write-Host "✅ Despliegue completado!" -ForegroundColor Green
    exit 0
}

# Opción 2: Si está en Cloud Storage
Write-Host "📦 Intentando desplegar a Google Cloud Storage..." -ForegroundColor Yellow

# Verificar gcloud
$gcloud = Get-Command gcloud -ErrorAction SilentlyContinue
if (-not $gcloud) {
    Write-Host "❌ gcloud CLI no está instalado" -ForegroundColor Red
    exit 1
}

# Construir frontend
Set-Location frontend
Write-Host "🔨 Construyendo frontend..." -ForegroundColor Cyan
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al construir" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Set-Location ..

# Buscar carpeta de build
$buildDirs = @("frontend\dist", "frontend\build")
$buildDir = $null

foreach ($dir in $buildDirs) {
    if (Test-Path $dir) {
        $buildDir = $dir
        break
    }
}

if (-not $buildDir) {
    Write-Host "❌ No se encontró la carpeta de build" -ForegroundColor Red
    exit 1
}

# Intentar buckets comunes
$buckets = @("entregas-frontend", "www.entregas.com.uy", "entregas-com-uy", "gs://entregas-frontend")

foreach ($bucket in $buckets) {
    Write-Host "🔍 Verificando bucket: $bucket..." -ForegroundColor Cyan
    $result = gsutil ls "$bucket" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Bucket encontrado: $bucket" -ForegroundColor Green
        Write-Host "📤 Subiendo archivos..." -ForegroundColor Cyan
        gsutil -m rsync -r -d "$buildDir" "$bucket"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Despliegue completado exitosamente!" -ForegroundColor Green
            Write-Host "🌐 Verifica en: https://www.entregas.com.uy" -ForegroundColor Cyan
            exit 0
        }
    }
}

Write-Host "⚠️  No se pudo encontrar el bucket de despliegue" -ForegroundColor Yellow
Write-Host "Por favor, configura Firebase Hosting o Cloud Storage manualmente" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Yellow
Write-Host "Para Firebase:" -ForegroundColor Cyan
Write-Host "  1. firebase init hosting" -ForegroundColor White
Write-Host "  2. firebase deploy --only hosting" -ForegroundColor White
Write-Host "" -ForegroundColor Yellow
Write-Host "Para Cloud Storage:" -ForegroundColor Cyan
Write-Host "  1. Crear bucket: gsutil mb gs://entregas-frontend" -ForegroundColor White
Write-Host "  2. Configurar como sitio web: gsutil web set -m index.html -e 404.html gs://entregas-frontend" -ForegroundColor White
Write-Host "  3. Ejecutar este script nuevamente" -ForegroundColor White
