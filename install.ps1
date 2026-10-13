Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 1. Verificar e instalar Python si falta
try {
    $pythonCheck = python --version 2>&1
    if ($pythonCheck -notlike "*Python 3*") { throw }
} catch {
    Write-Host "[!] Instalando Python..." -ForegroundColor Yellow
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 2. Verificar e instalar FFmpeg directamente si falta
if (!(Test-Path "$env:USERPROFILE\ffmpeg.exe") -and !(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Descargando e instalando FFmpeg..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "$env:TEMP\ffmpeg.zip"
    Expand-Archive -Path "$env:TEMP\ffmpeg.zip" -DestinationPath "$env:TEMP\ffmpeg" -Force
    $exe = Get-ChildItem -Path "$env:TEMP\ffmpeg" -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
    Copy-Item -Path $exe.FullName -Destination "$env:USERPROFILE\ffmpeg.exe" -Force
    Remove-Item "$env:TEMP\ffmpeg.zip" -Force
    Remove-Item "$env:TEMP\ffmpeg" -Recurse -Force
    [Environment]::SetEnvironmentVariable("Path", [System.Environment]::GetEnvironmentVariable("Path","User") + ";$env:USERPROFILE", "User")
    $env:Path += ";$env:USERPROFILE"
}

# 3. Instalar/Actualizar librerias requeridas
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
