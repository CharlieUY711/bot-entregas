# Script para desplegar solo el componente Perfil a www.entregas.com.uy
# Este script asume que el frontend está en Firebase Hosting o Cloud Storage

$ErrorActionPreference = "Stop"

Write-Host "🚀 Iniciando despliegue del componente Perfil..." -ForegroundColor Cyan

# Verificar que el archivo existe
$perfilPath = "frontend\src\pages\Perfil.tsx"
if (-not (Test-Path $perfilPath)) {
    Write-Host "❌ Error: No se encontró el archivo Perfil.tsx" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Archivo Perfil.tsx encontrado" -ForegroundColor Green

# Verificar si está en Firebase Hosting
$firebaseJson = "firebase.json"
$firebaseRc = ".firebaserc"

if (Test-Path $firebaseJson) {
    Write-Host "📦 Detectado Firebase Hosting" -ForegroundColor Yellow
    
    # Verificar si firebase-tools está instalado
    $firebaseInstalled = Get-Command firebase -ErrorAction SilentlyContinue
    if (-not $firebaseInstalled) {
        Write-Host "⚠️  Firebase CLI no está instalado. Instalando..." -ForegroundColor Yellow
        npm install -g firebase-tools
    }
    
    Write-Host "🔨 Construyendo el frontend..." -ForegroundColor Cyan
    Set-Location frontend
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al construir el frontend" -ForegroundColor Red
        Set-Location ..
        exit 1
    }
    Set-Location ..
    
    Write-Host "📤 Desplegando a Firebase Hosting..." -ForegroundColor Cyan
    firebase deploy --only hosting
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al desplegar a Firebase" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Despliegue completado exitosamente!" -ForegroundColor Green
    exit 0
}

# Verificar si está en Cloud Storage (bucket estático)
$bucketName = "entregas-frontend"
$projectId = "entregas-476319"

Write-Host "📦 Intentando desplegar a Google Cloud Storage..." -ForegroundColor Yellow

# Verificar si gcloud está instalado
$gcloudInstalled = Get-Command gcloud -ErrorAction SilentlyContinue
if (-not $gcloudInstalled) {
    Write-Host "❌ Error: gcloud CLI no está instalado" -ForegroundColor Red
    Write-Host "Por favor instala Google Cloud SDK desde: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

Write-Host "🔨 Construyendo el frontend..." -ForegroundColor Cyan
Set-Location frontend
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al construir el frontend" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Set-Location ..

# Obtener la carpeta de build (puede ser dist, build, o public)
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
    Write-Host "Carpetas buscadas: $($buildDirs -join ', ')" -ForegroundColor Yellow
    exit 1
}

Write-Host "📤 Subiendo archivos a Cloud Storage bucket: gs://$bucketName" -ForegroundColor Cyan
gsutil -m rsync -r -d "$buildDir" "gs://$bucketName"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al subir archivos a Cloud Storage" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Despliegue completado exitosamente!" -ForegroundColor Green
Write-Host "🌐 El sitio debería estar disponible en: https://www.entregas.com.uy" -ForegroundColor Cyan
