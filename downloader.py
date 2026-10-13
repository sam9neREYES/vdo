import argparse
import os
import platform
import subprocess
import sys
import yt_dlp

# Habilitar soporte de colores ANSI en CMD / PowerShell de Windows
if platform.system() == "Windows":
    os.system('')

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def get_default_download_dir():
    """Obtiene la ruta estándar 'Videos/Videos_Descargados' del usuario actual."""
    user_videos = os.path.join(os.path.expanduser("~"), "Videos")
    target_dir = os.path.join(user_videos, "Videos_Descargados")
    return target_dir

def open_folder(path):
    """Abre la carpeta de destino en el Explorador de archivos nativo del sistema."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print(f"{YELLOW}[!] No se pudo abrir la carpeta automáticamente: {e}{RESET}")

def format_bytes(b):
    if not b:
        return "N/A"
    if b >= 1024**3:
        return f"{b / (1024**3):.2f} GB"
    elif b >= 1024**2:
        return f"{b / (1024**2):.2f} MB"
    elif b >= 1024:
        return f"{b / 1024:.2f} KB"
    return f"{b} B"

def format_seconds(s):
    if not s or s < 0:
        return "--:--"
    m, sec = divmod(int(s), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        speed = d.get('speed', 0) or 0
        eta = d.get('eta', 0) or 0

        percent = (downloaded / total * 100) if total > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * percent // 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        speed_str = f"{format_bytes(speed)}/s"
        eta_str = format_seconds(eta)
        downloaded_str = format_bytes(downloaded)
        total_str = format_bytes(total)

        msg = (
            f"\r{CYAN}[Progreso]{RESET} [{CYAN}{bar}{RESET}] "
            f"{BOLD}{percent:5.1f}%{RESET} | "
            f"{downloaded_str} / {total_str} | "
            f"{YELLOW}{speed_str}{RESET} | "
            f"ETA: {YELLOW}{eta_str}{RESET} "
        )
        sys.stdout.write(msg)
        sys.stdout.flush()

    elif d['status'] == 'finished':
        sys.stdout.write(f"\n{GREEN}[✔] Descarga finalizada. Procesando y unificando video/audio...{RESET}\n")
        sys.stdout.flush()

def download_video(url: str, output_dir: str = None):
    # Si no se especifica ruta personalizada, usará ~/Videos/Videos_Descargados
    if not output_dir:
        output_dir = get_default_download_dir()

    # Creación automática de la carpeta contenedora en la primera ejecución
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"{GREEN}[+] Se ha creado la carpeta contenedora por primera vez:{RESET} {output_dir}")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    print(f"\n{BOLD}{CYAN}=== DESCARGADOR DE VIDEO UNIVERSAL ==={RESET}")
    print(f"{YELLOW}[+] Analizando URL:{RESET} {url}")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video sin título')
            resolution = info.get('resolution') or f"{info.get('width')}x{info.get('height')}"
            
            print(f"{GREEN}[+] Título:{RESET} {title}")
            print(f"{GREEN}[+] Máxima resolución:{RESET} {resolution}")
            print(f"{GREEN}[+] Carpeta de destino:{RESET} {output_dir}")
            print(f"{YELLOW}[+] Descargando...{RESET}\n")
            
            ydl.download([url])
            print(f"\n{BOLD}{GREEN}[✔] ¡Video descargado con éxito!{RESET}")
            
            # Apertura automática de la carpeta
            print(f"{CYAN}[+] Abriendo la carpeta de descargas...{RESET}")
            open_folder(output_dir)

    except yt_dlp.utils.DownloadError as e:
        print(f"\n{RED}[✖] Error al descargar el video: {e}{RESET}", file=sys.stderr)
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Descarga cancelada por el usuario.{RESET}")
    except Exception as e:
        print(f"\n{RED}[✖] Error inesperado: {e}{RESET}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="CLI Universal para descargar videos en máxima resolución desde CMD, PowerShell o Terminal."
    )
    parser.add_argument("url", nargs="?", help="URL del video a descargar")
    parser.add_argument("-o", "--output", default=None, help="Ruta de destino personalizada (Opcional)")

    args = parser.parse_args()

    url = args.url
    if not url:
        url = input("Ingresa la URL del video: ").strip()

    if not url:
        print(f"{RED}[✖] Debes ingresar una URL válida.{RESET}")
        sys.exit(1)

    download_video(url, args.output)

if __name__ == "__main__":
    main()