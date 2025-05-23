import psycopg2
from config import DB_CONFIG

def obtener_datos_visita(consecutivo):
    """
    Consulta los datos del formulario para un consecutivo específico desde app.visita.

    Args:
        consecutivo (str): ID único del caso de visita.

    Returns:
        dict: Diccionario con los datos del formulario, o None si no se encuentra.
    """
    query = """
        SELECT *
        FROM app.visita
        WHERE consecutivo = %s
        LIMIT 1;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (consecutivo,))
            row = cur.fetchone()
            if not row:
                return None
            colnames = [desc[0] for desc in cur.description]
            return dict(zip(colnames, row))


def obtener_datos_espaciales(lat, lon):
    """
    Obtiene el nombre del barrio, localidad, sitios de interés cercanos y estrato
    a partir de una coordenada en EPSG:4686.

    Args:
        lat (float): Latitud del punto.
        lon (float): Longitud del punto.

    Returns:
        tuple: (barrio, localidad, sitios_cercanos, estrato)
    """
    query = """
        WITH punto AS (
            SELECT ST_SetSRID(ST_MakePoint(%s, %s), 4686) AS geom
        )
        SELECT
            b.scanombre,                    -- nombre del barrio (sector)
            l.locnombre,                   -- nombre de la localidad
            ARRAY_AGG(sdi.ngenombre),     -- sitios de interés cercanos
            e.estrato                      -- estrato
        FROM punto p
        LEFT JOIN app.barrios b ON ST_Contains(b.geom, p.geom)
        LEFT JOIN app.localidades l ON ST_Contains(l.geom, p.geom)
        LEFT JOIN app.sitios_de_interes sdi ON ST_Intersects(sdi.geom, ST_Buffer(p.geom, 0.0225))
        LEFT JOIN app.mz_estr e ON ST_Intersects(e.geom, p.geom)
        GROUP BY b.scanombre, l.locnombre, e.estrato;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (lon, lat))
            res = cur.fetchone()
            if res:
                barrio = res[0].title() if res[0] else "No encontrado"
                localidad = res[1].title() if res[1] else "No encontrado"
                sitios = ", ".join(res[2]) if res[2] else "No hay sitios cercanos relevantes"
                estrato = str(res[3]) if res[3] is not None else "No identificado"
                return barrio, localidad, sitios, estrato
            return "No encontrado", "No encontrado", "No hay sitios cercanos relevantes", "No identificado"
