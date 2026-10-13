Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 1. Detectar si la sesion se ejecuta como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    $installDir = "C:\ProgramData\videodl"
    $targetScope = "Machine"
    Write-Host "[i] Modo de instalacion: Administrador (Global para el sistema)" -ForegroundColor Cyan
} else {
    $installDir = "$env:LOCALAPPDATA\videodl"
    $targetScope = "User"
    Write-Host "[i] Modo de instalacion: Usuario estandar" -ForegroundColor Cyan
}

# Crear la carpeta de instalacion si no existe
if (!(Test-Path $installDir)) {
    New-Item -Path $installDir -ItemType Directory -Force | Out-Null
}

# 2. Verificar e instalar Python si falta
try {
    $pythonCheck = python --version 2>&1
    if ($pythonCheck -notlike "*Python 3*") { throw }
} catch {
    Write-Host "[!] Python no detectado. Instalando Python..." -ForegroundColor Yellow
    if ($isAdmin) {
        winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    } else {
        winget install Python.Python.3.11 --scope user --silent --accept-package-agreements --accept-source-agreements
    }
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 3. Descargar e instalar FFmpeg directamente en la carpeta del programa
if (!(Test-Path "$installDir\ffmpeg.exe") -and !(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Descargando FFmpeg..." -ForegroundColor Yellow
    $zipPath = "$env:TEMP\ffmpeg.zip"
    $extractPath = "$env:TEMP\ffmpeg_extracted"
    
    Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    
    $ffmpegExe = Get-ChildItem -Path $extractPath -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
    if ($ffmpegExe) {
        Copy-Item -Path $ffmpegExe.FullName -Destination "$installDir\ffmpeg.exe" -Force
    }
    
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    Remove-Item $extractPath -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. Instalar o actualizar la libreria yt-dlp
python -m pip install yt-dlp --quiet --upgrade

# 5. Descargar el script principal downloader.py
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sam9neREYES/vdo/main/downloader.py" -OutFile "$installDir\downloader.py" -UseBasicParsing

# 6. Crear el ejecutable universal (.cmd) para CMD y PowerShell
$cmdContent = "@echo off`r`npython `"$installDir\downloader.py`" %*"
[System.IO.File]::WriteAllText("$installDir\videodl.cmd", $cmdContent)

# Crear copia de respaldo en WindowsApps para garantizar resolucion de comando
$winAppsDir = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
if (Test-Path $winAppsDir) {
    [System.IO.File]::WriteAllText("$winAppsDir\videodl.cmd", $cmdContent)
}

# 7. Registrar la carpeta en la variable de entorno PATH del sistema o usuario
$currentPath = [Environment]::GetEnvironmentVariable("Path", $targetScope)
if ($currentPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$installDir", $targetScope)
}

# Actualizar el PATH de la sesion actual de PowerShell
$env:Path += ";$installDir"

Write-Host "`n[✔] Instalacion completada con exito." -ForegroundColor Green
Write-Host "[✔] Ya puedes usar 'videodl' en CMD y PowerShell (como Usuario o Administrador)." -ForegroundColor Green
