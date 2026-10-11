# AranChasingTheWorld · web rediseñada

## Subir a GitHub Pages
1. Borra del repositorio los archivos antiguos (index.html, index-en.html, styles.css, carpeta img/, sitemap.xml, robots.txt, CNAME.txt).
2. Sube TODO el contenido de la carpeta `site/` (incluidos `CNAME` y `.nojekyll`).
3. En Google Search Console, envía https://aranchasingworld.com/sitemap.xml

## Antes de publicar
- `tools/content.py` → OWNER: rellena nombre, NIF, domicilio y email (páginas legales). Mientras estén vacíos salen resaltados en amarillo.
- `tools/content.py` → PRACTICAL: duración y punto de encuentro de cada tour (si están vacíos pone "te lo confirmo al reservar").
- Fotos propias: guarda `seda.jpg`, `esencial.jpg`, `modernista.jpg`, `bici.jpg`, `altea.jpg`, `islandia.jpg` en `photos/` y ejecuta `python3 tools/build.py`. Sustituyen a las ilustraciones.
- Revisa las traducciones al italiano y el número de WhatsApp (+354).

## Regenerar la web
`python3 tools/assets.py` (logos, fotos, fuentes) y `python3 tools/build.py` (páginas). Necesita Python 3 con Pillow y fontTools.
