import sys
import os
import subprocess
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("[X] Error: 'yt-dlp' no está instalado. Ejecuta: pip install yt-dlp")
    sys.exit(1)

def get_download_folder():
    """Crea y retorna la ruta de la carpeta 'Videos_Descargados'."""
    folder = Path.home() / "Videos" / "Videos_Descargados"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder)

def download_media(url):
    output_dir = get_download_folder()
    
    print("\n=== DESCARGADOR DE VIDEO UNIVERSAL ===")
    print(f"[+] Analizando URL: {url}")
    
    # Configuración limpia sin registros de depuración
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_dir, '%(title)s [%(id)s].%(ext)s'),
        'noplaylist': True,
        'quiet': True,               # Suprime los textos de depuración de yt-dlp
        'no_warnings': True,         # Desactiva advertencias secundarias
        'nocheckcertificate': True,
        'retries': 10,
        'fragment_retries': 10,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraer información del video
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video sin título')
            width = info.get('width')
            height = info.get('height')
            
            res_str = f"{width}x{height}" if width and height else "Máxima detectada"
            
            print(f"[+] Título: {title}")
            print(f"[+] Máxima resolución: {res_str}")
            print(f"[+] Carpeta de destino: {output_dir}")
            print("[+] Descargando...\n")
            
            # Ejecutar la descarga
            ydl.download([url])
            
            print("[✔] ¡Video descargado con éxito!")
            print("[+] Abriendo la carpeta de descargas...")
            
            # Abrir automáticamente la ubicación en el Explorador de archivos de Windows
            os.startfile(output_dir)
            
    except yt_dlp.utils.DownloadError:
        print("\n[X] Error al descargar el video: La URL no es compatible o el reproductor incrustado está protegido.")
        print("[i] En sitios de anime/películas, copia el enlace directo del reproductor interno o el flujo .m3u8 (F12).\n")
    except Exception as e:
        print(f"\n[X] Error inesperado: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUso correcto: videodl \"<URL_DEL_VIDEO>\"\n")
        sys.exit(1)
        
    target_url = sys.argv[1].strip()
    download_media(target_url)
