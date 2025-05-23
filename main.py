import os
from config import BASE_DIR
from organizador import organizar_archivos
from informe import generar_informe
from mapas import generar_mapa
from datos import obtener_datos_visita


def main():
    carpetas = organizar_archivos()

    if not carpetas:
        print("No se encontraron carpetas para procesar.")
        return

    for consecutivo in carpetas:
        carpeta_path = os.path.join(BASE_DIR, consecutivo)
        generar_informe(consecutivo, carpeta_path)
        datos = obtener_datos_visita(consecutivo)
        if datos and datos.get("latitud") and datos.get("longitud"):
            generar_mapa(consecutivo, carpeta_path, datos["latitud"], datos["longitud"])

    print("Proceso completo finalizado.")

if __name__ == "__main__":
    main()
