# Portafolio electrónico — Andre Pariona

Proyecto en Python 3.9 o superior, sin dependencias externas. Python genera el HTML y CSS y sirve una vista local. La carpeta docs contiene la versión estática para GitHub Pages.

## 1. Ejecutar en Visual Studio Code / Windows

Extrae el ZIP, abre la carpeta portafolio en VS Code y abre Terminal > Nueva terminal:

```powershell
python app.py
```

Si Windows usa el lanzador py, ejecuta `py app.py`.
Abre http://localhost:8000 en el navegador. Para detenerlo, pulsa Ctrl+C.
Si el puerto está ocupado: `python app.py --port 8001`.
Después de editar el código, detén el servidor, ejecútalo otra vez y recarga la página.
También puedes abrir docs/index.html directamente para ver la versión ya generada.

## 2. Dónde poner tu foto

Copia tu fotografía a la carpeta assets y renómbrala mi_foto.jpg. La ruta es:

assets/mi_foto.jpg

Debe ser una imagen JPG real. Si usas PNG, guarda assets/mi_foto.png y cambia el campo foto de PERFIL en app.py a 'mi_foto.png'. Se recomienda una foto vertical, con tu rostro centrado. No hace falta subirla a otro servicio. Al generar la página, Python la copia a docs/assets para publicarla junto con el sitio.
Mientras no exista la foto, se muestran tus iniciales.

## 3. Dónde poner los enlaces de GitHub del cuaderno

Abre app.py y busca SEMANAS. En cada semana reemplaza el valor vacío de repositorio:

```python
'repositorio': 'https://github.com/andrespl76/nombre-de-tu-repositorio',
```

Cada semana tiene su propio enlace. Sin enlace aparece «Repositorio pendiente», sin botón roto. Puedes enlazar también una carpeta de un repositorio usando su URL completa de GitHub. Para añadir semanas, duplica un diccionario de SEMANAS y cambia numero, titulo y contenido.

## 4. Qué debes personalizar

- PERFIL: nombre, estudios, experiencia, presentación y fotografía.
- SEMANAS: temas con tus palabras, definiciones, procedimientos, laboratorio, resultados, qué aprendiste, cómo aprendiste y repositorio.
- REFLEXION: reflexión metacognitiva final y próximos pasos.
- BIBLIOGRAFIA: libros y URLs realmente consultados, sin videos.

Los contenidos de las semanas son ejemplos, no afirman lo que hiciste. La experiencia y reflexión final contienen indicaciones para completar. Los proyectos concluidos tienen el botón solicitado a https://github.com/andrespl76; no se inventan proyectos terminados.

## 5. Publicar en GitHub Pages

GitHub Pages aloja archivos estáticos: no ejecuta este servidor Python. Por eso generamos docs/index.html con Python antes de publicar.

1. Termina tus cambios y ejecuta `python app.py --build`.
2. Crea un repositorio de GitHub para el portafolio, por ejemplo portafolio-web.
3. Sube app.py, README.md y las carpetas assets y docs, conservando su estructura. No subas solamente el ZIP. Si subes desde el navegador, usa Add file > Upload files y arrastra los archivos/carpetas extraídos.
4. En el repositorio abre Settings > Pages. Selecciona Deploy from a branch y la rama main con la carpeta /docs. Guarda.
5. Cuando termine la publicación, GitHub mostrará el enlace de tu sitio. Para el repositorio portafolio-web de tu cuenta, normalmente será https://andrespl76.github.io/portafolio-web/.
6. Cada vez que cambies el contenido o la foto, vuelve a ejecutar `python app.py --build` y sube los archivos actualizados, incluyendo docs.

Documentación: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

## Estructura

- app.py: datos editables, diseño y generador/servidor Python.
- assets/: coloca aquí la fotografía original.
- docs/index.html: página generada lista para publicar.
- docs/assets/: copia de la foto para el sitio publicado.

El diseño usa HTML semántico, CSS responsive y desplegables nativos: no necesita JavaScript ni servicios externos para funcionar.
