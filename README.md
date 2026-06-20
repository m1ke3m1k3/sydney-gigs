# Sydney Easy Money

Agregador de oportunidades para ganar dinero fácil en Sydney: focus groups, encuestas, product testing, estudios académicos y más.

## Estructura

```
sydney-gigs/
├── scraper/
│   ├── scraper.py          # Script principal de scraping
│   └── requirements.txt
├── web/
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── data/
│       └── opportunities.json   # Generado por el scraper
├── .github/workflows/
│   └── scraper.yml         # Automatización diaria
└── netlify.toml
```

## Setup inicial (tu máquina)

```bash
# 1. Clona o crea el repo en GitHub, luego:
cd scraper
pip install -r requirements.txt
playwright install chromium

# 2. Corre el scraper manualmente
python scraper.py

# 3. Abre web/index.html en el navegador para ver los resultados
```

## Deploy en Netlify

1. Sube el proyecto a GitHub
2. En Netlify → "Add new site" → "Import from Git" → selecciona el repo
3. Build settings:
   - Publish directory: `web`
   - Build command: (vacío)
4. Deploy

La web se actualiza automáticamente cuando GitHub Actions pushea nuevos datos al JSON.

## Automatización (GitHub Actions)

El archivo `.github/workflows/scraper.yml` corre el scraper todos los días a las 8:00 AM Sydney.

Para que funcione, el repo debe tener permisos de escritura para GitHub Actions:
- Settings → Actions → General → Workflow permissions → "Read and write permissions"

## Añadir nuevas fuentes

En `scraper/scraper.py`, añade una nueva función siguiendo el patrón de las existentes y agrégala al array `scrapers` en `run_all()`.

## Fuentes monitorizadas

| Fuente | URL | Tipo |
|--------|-----|------|
| Realtime Research | rtr.com.au | Focus groups, encuestas, taste tests |
| Research Connections | researchconnections.com.au | Focus groups presenciales |
| Sydney Focus Groups | sydneyfocusgroups.com.au | Focus groups Sydney |
| User Interviews | userinterviews.com | UX research online |
| Prolific | prolific.com | Estudios académicos |
| Gumtree AU | gumtree.com.au | Anuncios varios |
