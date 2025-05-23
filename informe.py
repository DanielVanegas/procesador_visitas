import os
from docx import Document
from openpyxl import load_workbook
from datos import obtener_datos_visita, obtener_datos_espaciales
from config import PARAM_FILE_PATH
from utils import log

def generar_informe(consecutivo, carpeta_path):
    documentos_path = os.path.join(carpeta_path, 'Documentos')
    observaciones_path = os.path.join(documentos_path, "Observaciones.docx")

    if os.path.exists(observaciones_path):
        log(f"La carpeta {consecutivo} ya tiene informe generado. Se omite.", carpeta_path)
        return

    datos = obtener_datos_visita(consecutivo)
    if not datos:
        log(f"No hay datos para el consecutivo {consecutivo}.", carpeta_path)
        return

    lat = datos.get("latitud")
    lon = datos.get("longitud")

    if lat is None or lon is None:
        log(f"Coordenadas faltantes para {consecutivo}.", carpeta_path)
        return

    barrio, localidad, sitios, estrato = obtener_datos_espaciales(lat, lon)
    
    if barrio == "No encontrado" or localidad == "No encontrado":
        log(f"Datos espaciales no encontrados para {consecutivo}. No se genera Observaciones.docx.", carpeta_path)
    else:
        texto = f"""
Inmueble ubicado en la localidad de {localidad}, barrio {barrio}, al sur {datos['al_sur']}, norte {datos['al_norte']}, oriente {datos['al_oriente']}, occidente {datos['al_occidente']}. Tiene cercanía a {sitios}.

Sector {datos['sector']}

{datos['edificio']} ubicado en un lote {datos['lote']} de forma irregular, tipología {datos['tipologia']}, topografía {datos['topografia']}, construcción de {datos['construccion']} pisos, {datos['sotanos']} sótano(s), zonas comunes {datos['zonas_comunes']}.

Apartamento ubicado en {datos['piso']} piso, vista {datos['vista']}, diseño funcional, iluminación y ventilación natural, acabados normales.

Garajes No. 39 y 40 (2 unidades), sencillos, cubiertos, en servidumbre propia. Depósito No. 206 (1 unidad). Los garajes y del depósito son de uso privado, según Escritura Pública suministrada. Área construida total de 91.05 m², área privada de 85.82 m², cuenta con el derecho de uso exclusivo sobre una zona común destinada a terraza con un área de 31.69 m², aproximadamente 28.61 m² medidos in situ.

Fecha de la visita: {datos['fecha_formulario']}.
"""

        os.makedirs(documentos_path, exist_ok=True)
        doc = Document()
        doc.add_paragraph(texto.strip())
        doc.save(observaciones_path)
        log(f"Generado Observaciones.docx para {consecutivo}.", carpeta_path)

    param_dest_path = os.path.join(carpeta_path, os.path.basename(PARAM_FILE_PATH))
    if not os.path.exists(param_dest_path):
        log(f"No se encontró el archivo de parámetros en {consecutivo}.", carpeta_path)
        return

    wb = load_workbook(param_dest_path)
    ws = wb.active

    ws['C2'] = datos['fecha_formulario']
    ws['D2'] = datos['fecha_formulario']
    ws['H2'] = f"{consecutivo}-DVF"
    ws['C8'] = barrio.upper() if barrio != "No encontrado" else ""
    ws['E8'] = estrato if estrato != "No identificado" else ""
    ws['E9'] = localidad.upper() if localidad != "No encontrado" else ""
    ws['K105'] = f"{lat}, {lon}"
    ws['K103'] = f"https://www.google.com/maps?q={lat},{lon}"

    wb.save(param_dest_path)

    log(f"Generado informe y Excel para {consecutivo}.", carpeta_path)
