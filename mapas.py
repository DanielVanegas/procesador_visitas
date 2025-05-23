import os
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw
from utils import log  # si usas logging centralizado

def generar_mapa(consecutivo, carpeta_path, lat, lon):
    def render(nombre_archivo, zoom):
        documentos_path = os.path.join(carpeta_path, "Documentos")

        output_path = os.path.join(documentos_path, f"{nombre_archivo}.png")
        if os.path.exists(output_path):
            log(f"{nombre_archivo}.png ya existe para {consecutivo}. Se omite.", carpeta_path)
            return
        
        width, height = 1200, 1200
        m = StaticMap(width, height)
        m.add_marker(CircleMarker((lon, lat), '#00000000', 0))  # marcador invisible
        image = m.render(zoom=zoom)

        center_x = width // 2
        center_y = height // 2
        draw = ImageDraw.Draw(image)

        # Ícono tipo Google Maps
        radius = 14
        top_y = center_y - 2 * radius
        bottom_y = center_y

        # 🔴 Círculo rojo
        draw.ellipse([
            (center_x - radius, top_y),
            (center_x + radius, top_y + 2 * radius)
        ], fill="#ff0033", outline="black")

        # ⚪ Círculo blanco al centro
        inner_radius = 8
        circle_center_y = top_y + radius
        draw.ellipse([
            (center_x - inner_radius, circle_center_y - inner_radius),
            (center_x + inner_radius, circle_center_y + inner_radius)
        ], fill="white", outline="black")

        image.save(output_path)
        log(f"Generado {nombre_archivo}.png para {consecutivo}.", carpeta_path)

    os.makedirs(carpeta_path, exist_ok=True)
    render("3 contexto", zoom=13)
    render("4 contexto", zoom=15)
