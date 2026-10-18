# AranChasingTheWorld · web

Todo el proyecto está en la raíz: `index.html` junto a `CNAME` y `.nojekyll`.

## Subir a GitHub Pages
1. Borra del repositorio los archivos antiguos.
2. Sube TODO el contenido de esta carpeta a la RAÍZ del repositorio.
3. Settings → Pages → Deploy from a branch → rama `main`, carpeta `/ (root)`.
4. En Google Search Console, envía https://aranchasingworld.com/sitemap.xml

## Antes de publicar
- `tools/content.py` → OWNER (nombre, NIF, domicilio, email) y PRACTICAL (duración y punto de encuentro de cada tour).
- Fotos propias en `photos/` (`seda.jpg`, `esencial.jpg`, `modernista.jpg`, `bici.jpg`, `altea.jpg`, `islandia.jpg`) y ejecutar `python3 tools/build.py`.

## Regenerar la web
`python3 tools/assets.py` y `python3 tools/build.py` (Python 3 con Pillow y fontTools). Escriben directamente en la raíz.
