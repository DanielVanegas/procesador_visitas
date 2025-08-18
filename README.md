# Real Estate Valuation Automation

This project automates the **organization, processing, and reporting** of real estate appraisal case files.  
It integrates PostgreSQL/PostGIS, Excel/Word/PDF handling, and static map generation.

---

## 📌 Workflow Overview

1. **File Organization**  
   - Extracts `.zip` case files.  
   - Creates a structured folder layout:  
     ```
     Case/
     ├── Documentos/
     ├── Fotos/
     └── parameters.xlsx
     ```
   - Moves and copies required files automatically.

2. **Database Queries**  
   - Retrieves visit information (location, property details, etc.) from the database.  
   - Runs spatial queries on PostGIS to obtain:  
     - Neighborhood  
     - Locality  
     - Nearby sites of interest  
     - Socioeconomic stratum.

3. **Report Generation**  
   - Creates `Observaciones.docx` with structured property description.  
   - Updates Excel parameter file with case data (dates, applicant, property value, coordinates, links).  
   - Extracts complementary data from PDF forms when available.

4. **Map Creation**  
   - Generates static maps (`3 contexto.png`, `4 contexto.png`) with Google-Maps-style markers.  
   - Maps are centered on property coordinates at zoom levels 13 and 15.

5. **Logging**  
   - Every step is logged to `Documentos/log.txt` for traceability.

---

## 📂 Project Structure
```
.
├── main.py           # Entry point: orchestrates the process
├── config.py         # Paths and DB configuration
├── datos.py          # Database and spatial queries
├── informe.py        # Report and Excel generation
├── mapas.py          # Map rendering
├── organizador.py    # File/folder organization
└── utils.py          # Logging utilities
```

---

## ⚙️ Requirements
- Python 3.9+
- PostgreSQL with PostGIS enabled
- Required Python libraries (see `requirements.txt`)

---

## ▶️ Running
Execute:

```bash
python main.py
```

The program will:
1. Organize case folders.  
2. Query data from PostgreSQL/PostGIS.  
3. Generate reports and update Excel files.  
4. Create contextual maps.  
5. Write logs for each case.  

---

## 🛠 Notes
- Database credentials are stored in `.env`.  
- Parameter Excel template is detected automatically from the configured path (`PARAM_FILE_PATH`).  
- Ensure spatial layers (`barrios`, `localidades`, `sitios_de_interes`, `mz_estr`) exist in the PostGIS database.  
