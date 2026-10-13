Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
python -m pip install yt-dlp --quiet
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sam9neREYES/vdo/main/downloader.py" -OutFile "$env:USERPROFILE\downloader.py"
if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Type File -Force | Out-Null }
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($profileContent -notlike "*function videodl*") {
    Add-Content -Path $PROFILE -Value "`nfunction videodl { python `"$env:USERPROFILE\downloader.py`" `$args }"
}
. $PROFILE
Write-Host "`n[✔] Instalacion completada con exito. Ya puedes usar 'videodl' en tu terminal." -ForegroundColor Green
