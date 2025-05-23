import os
import zipfile
import shutil
from config import BASE_DIR, PARAM_FILE_PATH
from utils import log

def organizar_archivos():
    if not os.listdir(BASE_DIR):
        print("La carpeta raíz está vacía.")  # Log general, no pertenece a una carpeta específica
        return []

    zip_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.zip')]
    if not zip_files:
        print("No se encontraron archivos ZIP para descomprimir.")
    else:
        for zip_file in zip_files:
            zip_path = os.path.join(BASE_DIR, zip_file)
            extract_folder = os.path.join(BASE_DIR, os.path.splitext(zip_file)[0])
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            os.remove(zip_path)

    carpetas = []
    for carpeta in os.listdir(BASE_DIR):
        carpeta_path = os.path.join(BASE_DIR, carpeta)
        if not os.path.isdir(carpeta_path):
            continue

        documentos_path = os.path.join(carpeta_path, 'Documentos')
        fotos_path = os.path.join(carpeta_path, 'Fotos')
        param_dest_path = os.path.join(carpeta_path, os.path.basename(PARAM_FILE_PATH))
        archivos_originales = [
            f for f in os.listdir(carpeta_path)
            if os.path.isfile(os.path.join(carpeta_path, f)) and not f.endswith('.zip') and f != os.path.basename(PARAM_FILE_PATH)
        ]

        if os.path.exists(documentos_path) and os.path.exists(fotos_path) and not archivos_originales and os.path.exists(param_dest_path):
            log(f"La carpeta {carpeta} ya estaba organizada.", carpeta_path)
            carpetas.append(carpeta)
            continue

        os.makedirs(documentos_path, exist_ok=True)
        os.makedirs(fotos_path, exist_ok=True)

        archivos_movidos = 0
        for archivo in archivos_originales:
            shutil.move(os.path.join(carpeta_path, archivo), os.path.join(documentos_path, archivo))
            archivos_movidos += 1

        if not os.path.exists(param_dest_path) and os.path.exists(PARAM_FILE_PATH):
            shutil.copy(PARAM_FILE_PATH, param_dest_path)
            log(f"Archivo de parámetros copiado en {carpeta}.", carpeta_path)
        elif os.path.exists(param_dest_path):
            log(f"El archivo de parámetros ya se encuentra en {carpeta}.", carpeta_path)

        log(f"Procesada carpeta: {carpeta} - Archivos originales: {len(archivos_originales)}, Archivos movidos: {archivos_movidos}.", carpeta_path)
        carpetas.append(carpeta)

    return carpetas
