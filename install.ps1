Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Verificar e instalar Python si no existe
try {
    $pythonCheck = python --version 2>&1
    if ($pythonCheck -notlike "*Python 3*") { throw }
} catch {
    Write-Host "[!] Python no detectado. Instalando Python automaticamente..." -ForegroundColor Yellow
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Instalar librerias requeridas
python -m pip install yt-dlp --quiet

# Descargar script principal
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sam9neREYES/vdo/main/downloader.py" -OutFile "$env:USERPROFILE\downloader.py"

# Registrar comando global
if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Type File -Force | Out-Null }
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($profileContent -notlike "*function videodl*") {
    Add-Content -Path $PROFILE -Value "`nfunction videodl { python `"$env:USERPROFILE\downloader.py`" `$args }"
}
function global:videodl { python "$env:USERPROFILE\downloader.py" $args }

Write-Host "`n[✔] Instalacion completada con exito. Ya puedes usar 'videodl' en tu terminal." -ForegroundColor Green
