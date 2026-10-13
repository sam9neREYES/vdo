import sys
import os
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("[X] Error: 'yt-dlp' no está instalado. Ejecuta: pip install yt-dlp")
    sys.exit(1)

def get_download_folder():
    """Crea y retorna la ruta de la carpeta 'Videos_Descargados' en el usuario actual."""
    folder = Path.home() / "Videos" / "Videos_Descargados"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder)

def download_media(url):
    output_dir = get_download_folder()
    
    print("\n=== DESCARGADOR UNIVERSAL DE VIDEO (MÁXIMA CALIDAD) ===")
    print(f"[+] Carpeta de destino: {output_dir}")
    print(f"[+] Procesando enlace: {url}\n")
    
    # Configuración de alta fidelidad y máxima compatibilidad multiplataforma
    ydl_opts = {
        # Seleccionar la máxima resolución de video y mejor pista de audio disponibles
        'format': 'bestvideo+bestaudio/best',
        
        # Unificar automáticamente el stream de video y audio en un archivo MP4 con FFmpeg
        'merge_output_format': 'mp4',
        
        # Estructura del nombre de archivo: Título [ID_Plataforma].ext
        'outtmpl': os.path.join(output_dir, '%(title)s [%(id)s].%(ext)s'),
        
        # Evitar descargar listas completas si el enlace pertenece a una playlist
        'noplaylist': True,
        
        # Reintentos y tolerancia a fallos de red en plataformas con protección anti-bot
        'retries': 10,
        'fragment_retries': 10,
        'nocheckcertificate': True,
        'no_warnings': True,
        
        # User-Agent actualizado para evitar bloqueos en Instagram, TikTok y Twitter/X
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraer información sin descargar primero para mostrar datos
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video sin título')
            extractor = info.get('extractor_key', 'Plataforma desconocida')
            width = info.get('width', 'N/A')
            height = info.get('height', 'N/A')
            
            res_str = f"{width}x{height}" if width and height else "Máxima detectada"
            
            print(f"[+] Plataforma: {extractor}")
            print(f"[+] Título: {title}")
            print(f"[+] Resolución objetivo: {res_str}")
            print("[+] Iniciando descarga...")
            
            # Realizar la descarga y fusión
            ydl.download([url])
            
            print(f"\n[✔] ¡Descarga completada con éxito!")
            print(f"[✔] Archivo guardado en: {output_dir}\n")
            
    except yt_dlp.utils.DownloadError as e:
        print(f"\n[X] Error de descarga: El enlace es privado, requiere inicio de sesión o no contiene video soportado.")
    except Exception as e:
        print(f"\n[X] Error inesperado: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUso correcto: videodl \"<URL_DEL_VIDEO>\"")
        print("Ejemplo: videodl \"https://www.tiktok.com/@usuario/video/123456789\"\n")
        sys.exit(1)
        
    target_url = sys.argv[1].strip()
    download_media(target_url)
