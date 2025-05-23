import os
from datetime import datetime

def log(mensaje, carpeta_path):
    print(mensaje)
    log_path = os.path.join(carpeta_path, "Documentos", "log.txt")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")
