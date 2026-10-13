Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 1. Verificar e instalar Python si falta
try {
    $pythonCheck = python --version 2>&1
    if ($pythonCheck -notlike "*Python 3*") { throw }
} catch {
    Write-Host "[!] Python no detectado. Instalando Python automaticamente..." -ForegroundColor Yellow
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 2. Verificar e instalar FFmpeg si falta
try {
    $ffmpegCheck = ffmpeg -version 2>&1
    if ($ffmpegCheck -notlike "*ffmpeg version*") { throw }
} catch {
    Write-Host "[!] FFmpeg no detectado. Instalando FFmpeg para unificacion de audio/video..." -ForegroundColor Yellow
    winget install Gyan.FFmpeg --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 3. Instalar/Actualizar librerias
python -m pip install yt-dlp --quiet --upgrade

# 4. Descargar script principal
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sam9neREYES/vdo/main/downloader.py" -OutFile "$env:USERPROFILE\downloader.py"

# 5. Registrar comando global
if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Type File -Force | Out-Null }
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($profileContent -notlike "*function videodl*") {
    Add-Content -Path $PROFILE -Value "`nfunction videodl { python `"$env:USERPROFILE\downloader.py`" `$args }"
}
function global:videodl { python "$env:USERPROFILE\downloader.py" $args }

Write-Host "`n[✔] Instalacion completada con exito. Ya puedes usar 'videodl' en tu terminal." -ForegroundColor Green
