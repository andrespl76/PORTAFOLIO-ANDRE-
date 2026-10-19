from pathlib import Path
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from urllib.parse import urlsplit
import shutil
import sys

BASE = Path(__file__).resolve().parent

# ======================================================
# 1. INFORMACIÓN PERSONAL: EDITA ESTOS DATOS
# ======================================================

PERFIL = {
    "nombre": "Andre Pariona",
    "iniciales": "AP",
    "carrera": "Ingeniería de Sistemas",
    "universidad": "Universidad Nacional del Centro del Perú",
    "curso": "Desarrollo de Aplicaciones Web",
    "foto": "mi_foto.jpg",  # Coloca tu foto en assets/mi_foto.jpg
    "github": "https://github.com/andrespl76",
    "presentacion": (
        "Bienvenido a mi portafolio electrónico. "
        "Aquí comparto mis proyectos, mis prácticas y "
        "mi proceso de aprendizaje en el desarrollo web."
    ),
    "sobre_mi": (
        "Soy estudiante de Ingeniería de Sistemas y me interesa "
        "crear soluciones digitales útiles. Me gusta aprender "
        "mediante la práctica, resolver problemas y mejorar "
        "la experiencia de las personas a través de la tecnología."
    ),
    "estudios": (
        "Estudio Ingeniería de Sistemas en la Universidad Nacional "
        "del Centro del Perú. Este portafolio documenta mi aprendizaje "
        "en el curso de Desarrollo de Aplicaciones Web."
    ),
    "experiencia": (
        "Completa este espacio con tus proyectos académicos, "
        "prácticas preprofesionales y experiencia real."
    ),
}

# ======================================================
# 2. CUADERNO
#
# Los temas siguen la imagen de referencia.
# Completa las evidencias y reflexiones con tu trabajo real.
#
# repositorio: PEGA AQUÍ EL ENLACE DE CADA SEMANA.
# imagen: nombre de la captura guardada dentro de assets.
# practica: False para una semana sin laboratorio.
# ======================================================

SEMANAS = [
    {
        "numero": 1,
        "titulo": "Fundamentos Web",
        "temas": (
            "Introducción a las tecnologías web, funcionamiento "
            "de DNS, protocolo HTTP y roles en el desarrollo "
            "(Frontend, Backend y Fullstack). Configuración de VS Code."
        ),
        "practica": False,
        "imagen": "",
        "repositorio": "",
        "laboratorio": "",
        "procedimiento": "",
        "resultados": "",
        "aprendi": "Escribe qué aprendiste sobre el funcionamiento de la web.",
        "como": "Explica qué actividades te ayudaron a comprender estos temas.",
    },
    {
        "numero": 2,
        "titulo": "HTML y CSS",
        "temas": (
            "Estructura HTML5, árbol DOM y optimización SEO. "
            "Diseño con CSS3, Flexbox, Grid Layout y diseño web responsivo."
        ),
        "practica": True,
        "imagen": "semana2.png",
        # PEGA TU ENLACE ENTRE LAS COMILLAS:
        "repositorio": "https://github.com/andrespl76/Portafolio-Andre.git",
        "laboratorio": "Describe el ejercicio de HTML y CSS que realizaste.",
        "procedimiento": "Explica los pasos que seguiste para desarrollar la página.",
        "resultados": "Describe el resultado y las pruebas realizadas.",
        "aprendi": "Escribe qué aprendiste sobre estructura y diseño de páginas.",
        "como": "Explica cómo la práctica te ayudó a comprender HTML y CSS.",
    },
    {
        "numero": 3,
        "titulo": "Bootstrap y Tailwind",
        "temas": (
            "Desarrollo de interfaces con librerías CSS. "
            "Uso de componentes, sistemas de cuadrícula "
            "y utilidades de Tailwind CSS."
        ),
        "practica": True,
        "imagen": "semana3.png",
        "repositorio": "https://github.com/THEDEMONS101/Practica01_DAW.git",
        "laboratorio": "Describe la interfaz que desarrollaste.",
        "procedimiento": "Explica cómo utilizaste las librerías CSS.",
        "resultados": "Indica qué componentes y diseños lograste implementar.",
        "aprendi": "Escribe qué aprendiste sobre Bootstrap y Tailwind.",
        "como": "Describe cómo comparaste sus herramientas y resolviste dificultades.",
    },
    {
        "numero": 4,
        "titulo": "JavaScript y TypeScript",
        "temas": (
            "Variables, operadores, estructuras de control, "
            "funciones y manejo del DOM. Introducción a TypeScript y Canvas."
        ),
        "practica": True,
        "imagen": "semana4.png",
        "repositorio": "https://github.com/saulPariona/PRACTICA-CALIFICADA_2_SUAZNABAR.git",
        "laboratorio": "Describe el ejercicio de programación realizado.",
        "procedimiento": "Explica cómo organizaste la lógica y los eventos.",
        "resultados": "Indica qué funcionalidades lograste implementar.",
        "aprendi": "Escribe qué aprendiste sobre interactividad y programación.",
        "como": "Explica cómo probaste tu código y corregiste los errores.",
    },
    {
        "numero": 5,
        "titulo": "Framework JS: React",
        "temas": (
            "Estructura de React, Client Side Rendering, "
            "componentes, JSX, Props y Children. Estilos en React."
        ),
        "practica": False,
        "imagen": "",
        "repositorio": "",
        "laboratorio": "",
        "procedimiento": "",
        "resultados": "",
        "aprendi": "Escribe qué comprendiste sobre los componentes de React.",
        "como": "Explica qué ejemplos o actividades facilitaron tu aprendizaje.",
    },
    {
        "numero": 6,
        "titulo": "Eventos y APIs",
        "temas": (
            "Manejo de eventos, renderizado condicional e iterativo. "
            "Consumo de APIs con Fetch y Axios."
        ),
        "practica": True,
        "imagen": "semana6.png",
        "repositorio": "https://github.com/Anthony-Valencia/daw-practica-02-semana-03.git",
        "laboratorio": "Describe la aplicación y la API utilizada.",
        "procedimiento": "Explica cómo solicitaste y mostraste los datos.",
        "resultados": "Indica qué información muestra tu aplicación.",
        "aprendi": "Escribe qué aprendiste sobre eventos y consumo de APIs.",
        "como": "Explica cómo verificaste las respuestas y manejaste los errores.",
    },
]

# ======================================================
# 3. REFLEXIÓN FINAL: COMPLETA CON TU EXPERIENCIA
# ======================================================

REFLEXION = {
    "aprendi": (
        "Explica los conocimientos y habilidades que desarrollaste "
        "durante el curso. Relaciónalos con los trabajos realizados."
    ),
    "como": (
        "Describe las estrategias que te ayudaron a aprender: práctica, "
        "documentación, revisión de errores o retroalimentación. "
        "Incluye una dificultad concreta y cómo la superaste."
    ),
    "mejorar": (
        "Identifica qué necesitas reforzar y qué acciones realizarás "
        "para continuar desarrollando tus habilidades."
    ),
}

# Fuentes sugeridas: conserva únicamente las que consultaste.
BIBLIOGRAFIA = [
    {
        "tipo": "Documentación",
        "titulo": "MDN Web Docs",
        "descripcion": "Referencia de HTML, CSS y JavaScript.",
        "url": "https://developer.mozilla.org/es/",
    },
    {
        "tipo": "Documentación",
        "titulo": "React",
        "descripcion": "Documentación y conceptos de React.",
        "url": "https://es.react.dev/",
    },
    {
        "tipo": "Documentación",
        "titulo": "Python",
        "descripcion": "Documentación oficial de Python.",
        "url": "https://docs.python.org/es/3/",
    },
    {
        "tipo": "Libro",
        "titulo": "Jon Duckett",
        "descripcion": (
            "HTML and CSS: Design and Build Websites. Wiley, 2011."
        ),
        "url": "",
    },
]

# ======================================================
# DISEÑO
# ======================================================

CSS = """
:root {
    --fondo: #0b1118;
    --panel: #131e29;
    --borde: #293746;
    --texto: #eef3f8;
    --gris: #a9b8c8;
    --verde: #c1f17a;
    --azul: #10365f;
}

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
    scroll-padding-top: 110px;
}

body {
    margin: 0;
    background: var(--fondo);
    color: var(--texto);
    font-family: "Segoe UI", Arial, sans-serif;
    line-height: 1.7;
}

a {
    color: inherit;
    text-decoration: none;
}

a:focus-visible,
summary:focus-visible {
    outline: 3px solid #e4a138;
    outline-offset: 5px;
}

.contenedor {
    width: min(1180px, 92%);
    margin: auto;
}

.navegacion {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(11, 17, 24, .97);
    border-bottom: 1px solid var(--borde);
}

.nav-interior {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 25px;
    padding: 18px 0;
}

.logo {
    font-size: 21px;
    font-weight: 800;
    white-space: nowrap;
}

.logo span {
    color: var(--verde);
}

.enlaces {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.enlaces a {
    font-size: 13px;
    color: var(--gris);
}

.enlaces a:hover {
    color: var(--verde);
}

.portada {
    display: grid;
    grid-template-columns: 1.25fr 1fr;
    gap: 65px;
    align-items: center;
    padding: 80px 0;
}

.etiqueta {
    display: block;
    color: var(--verde);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
}

h1 {
    font-size: clamp(48px, 6vw, 80px);
    line-height: 1.08;
    letter-spacing: -3px;
    margin: 22px 0;
}

h1 span {
    color: var(--verde);
}

h2 {
    font-size: clamp(30px, 4vw, 43px);
    line-height: 1.2;
    letter-spacing: -1.3px;
    margin: 12px 0 22px;
}

h3 {
    line-height: 1.4;
}

p {
    color: var(--gris);
}

.presentacion {
    max-width: 570px;
}

.acciones {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 28px;
}

.boton {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background: var(--verde);
    color: #17230c;
    border: 1px solid var(--verde);
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 700;
    transition: transform .2s, opacity .2s;
}

.boton:hover {
    transform: translateY(-2px);
    opacity: .9;
}

.boton-secundario {
    background: transparent;
    color: var(--texto);
    border-color: var(--borde);
}

.marco-foto {
    padding: 16px;
    border: 1px solid #3c5144;
    border-radius: 22px;
    background: linear-gradient(145deg, #304638, #131e29);
    transform: rotate(2deg);
}

.foto {
    width: 100%;
    height: 380px;
    object-fit: cover;
    border-radius: 12px;
    display: block;
}

.foto-pendiente {
    height: 380px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: 12px;
    background: radial-gradient(circle at top, #53684d, #17232c);
}

.foto-pendiente strong {
    font-size: 110px;
    color: var(--verde);
    letter-spacing: -8px;
}

.foto-pendiente span {
    font-size: 12px;
    letter-spacing: 3px;
}

.pie-foto {
    padding: 17px 5px 3px;
    font-size: 13px;
}

.punto {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--verde);
    margin-right: 8px;
}

.franja {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
    padding: 22px 0;
    border-top: 1px solid var(--borde);
    border-bottom: 1px solid var(--borde);
    color: var(--gris);
    font-size: 12px;
}

.seccion {
    padding: 70px 0;
}

.tres-columnas {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
}

.tarjeta-oscura {
    padding: 28px;
    background: var(--panel);
    border: 1px solid var(--borde);
    border-radius: 14px;
}

.tarjeta-oscura h3 {
    margin: 12px 0;
    font-size: 21px;
}

.tarjeta-oscura p {
    font-size: 14px;
    margin-bottom: 0;
}

.numero {
    color: var(--verde);
    font-family: monospace;
    font-size: 13px;
}

.proyecto {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 30px;
    padding: 38px;
    border: 1px solid #3e5542;
    border-radius: 16px;
    background: linear-gradient(110deg, #22362a, #131e29);
}

.proyecto p {
    max-width: 650px;
}

.proyecto .boton {
    flex-shrink: 0;
}

/* CUADERNO CON TARJETAS COMO LA REFERENCIA */

.cuaderno {
    background: #eef1f5;
    padding: 65px 0 75px;
}

.cuaderno .etiqueta {
    color: #536780;
}

.cuaderno h2 {
    color: var(--azul);
}

.intro-cuaderno {
    color: #596b80;
    max-width: 760px;
    margin-bottom: 30px;
}

.semanas {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 24px;
    align-items: stretch;
}

.tarjeta-semana {
    display: flex;
    flex-direction: column;
    background: white;
    border: 1px solid #dde3eb;
    border-radius: 13px;
    padding: 23px;
    min-height: 530px;
    box-shadow: 0 12px 24px rgba(21, 38, 62, .07);
}

.cabecera-semana {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid #eda948;
}

.cabecera-semana h3 {
    margin: 0;
    font-size: 17px;
    color: var(--azul);
    white-space: nowrap;
}

.titulo-tema {
    font-size: 13px;
    font-weight: 600;
    text-align: right;
    color: #142c49;
    line-height: 1.4;
}

.descripcion-semana {
    color: #53677f;
    font-size: 14px;
    line-height: 1.6;
    margin: 15px 0 20px;
}

.captura {
    display: block;
    width: 100%;
    height: 155px;
    object-fit: contain;
    background: #f2f4f8;
    border-radius: 8px;
}

.captura-pendiente {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 155px;
    background: #f2f4f8;
    border: 1px dashed #c5d0dd;
    border-radius: 8px;
    color: #61748d;
    font-size: 13px;
}

.captura-pendiente span {
    font-size: 31px;
    line-height: 1.4;
}

.enlace-repositorio {
    margin: 15px 0;
}

.boton-github {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 13px;
    background: var(--azul);
    color: white;
    border-radius: 5px;
    font-size: 13px;
    font-weight: 600;
}

.boton-github:hover {
    background: #204e7e;
}

.boton-github svg {
    width: 15px;
    height: 15px;
}

.pendiente {
    display: inline-block;
    padding: 6px 11px;
    border: 1px dashed #bdc9d7;
    border-radius: 5px;
    color: #65768b;
    font-size: 12px;
    background: #f7f9fb;
}

.teoria {
    color: #6a7687;
    font-style: italic;
    font-size: 14px;
    margin-top: 0;
}

.detalles-laboratorio {
    border: 1px solid #e1e7ee;
    border-radius: 6px;
    margin-bottom: 22px;
    background: #f8fafc;
}

.detalles-laboratorio summary {
    cursor: pointer;
    padding: 10px;
    color: #2a496c;
    font-size: 12px;
}

.contenido-laboratorio {
    padding: 0 12px 12px;
}

.contenido-laboratorio h4 {
    color: var(--azul);
    font-size: 12px;
    margin: 10px 0 3px;
}

.contenido-laboratorio p {
    color: #5b6d83;
    font-size: 12px;
    margin: 0;
    white-space: pre-line;
}

.reflexion-semana {
    margin-top: auto;
    border-top: 1px dashed #dce3eb;
    padding-top: 14px;
}

.reflexion-semana p {
    color: #5b6d83;
    font-size: 13px;
    line-height: 1.6;
    margin: 0 0 9px;
}

.reflexion-semana strong {
    color: var(--azul);
}

.bibliografia {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}

.fuente {
    border: 1px solid var(--borde);
    padding: 24px;
    border-radius: 12px;
}

.fuente h3 {
    margin: 10px 0;
}

.fuente p {
    font-size: 14px;
}

.fuente a {
    color: var(--verde);
    font-size: 13px;
    text-decoration: underline;
}

footer {
    border-top: 1px solid var(--borde);
    padding: 28px 0;
    color: var(--gris);
    font-size: 12px;
}

.pie-interior {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}

@media (max-width: 1000px) {
    .semanas {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .portada {
        gap: 30px;
    }

    .nav-interior {
        align-items: flex-start;
        flex-direction: column;
        gap: 10px;
    }
}

@media (max-width: 700px) {
    .portada,
    .tres-columnas,
    .bibliografia,
    .semanas {
        grid-template-columns: 1fr;
    }

    .portada {
        padding: 45px 0;
    }

    .marco-foto {
        max-width: 420px;
        transform: none;
    }

    .proyecto {
        align-items: flex-start;
        flex-direction: column;
        padding: 25px;
    }

    .tarjeta-semana {
        min-height: 440px;
    }

    .enlaces {
        gap: 8px 15px;
    }

    .enlaces a {
        font-size: 12px;
    }

    .pie-interior {
        flex-direction: column;
    }

    .seccion {
        padding: 50px 0;
    }
}

@media (prefers-reduced-motion: reduce) {
    html {
        scroll-behavior: auto;
    }

    * {
        transition: none !important;
    }
}
"""

ICONO_GITHUB = """
<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58
    v-2.23c-3.34.73-4.04-1.42-4.04-1.42-.55-1.39-1.33-1.76-1.33-1.76
    -1.09-.75.08-.73.08-.73 1.2.08 1.84 1.23 1.84 1.23
    1.07 1.83 2.81 1.3 3.5.99.11-.78.42-1.3.76-1.6
    -2.67-.3-5.47-1.34-5.47-5.93 0-1.31.47-2.38 1.24-3.22
    -.12-.3-.54-1.52.12-3.17 0 0 1.01-.32 3.3 1.23
    a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23
    .66 1.65.24 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22
    0 4.6-2.81 5.63-5.49 5.93.43.37.82 1.1.82 2.22
    v3.3c0 .32.22.7.83.58A12 12 0 0 0 12 .5Z"/>
</svg>
"""


def texto(valor):
    """Protege los textos al insertarlos en HTML."""
    return escape(str(valor), quote=True)


def enlace_valido(url):
    partes = urlsplit(url.strip())
    return partes.scheme in ("https", "http") and bool(partes.netloc)


def copiar_imagen(nombre, destino):
    """Copia una imagen de assets a docs/assets si existe."""
    if not nombre:
        return ""

    archivo = BASE / "assets" / nombre

    if not archivo.is_file():
        return ""

    shutil.copy2(archivo, destino / "assets" / archivo.name)
    return f"assets/{archivo.name}"


def crear_tarjeta_semana(semana, destino):
    numero = semana["numero"]

    if semana["practica"]:
        ruta = copiar_imagen(semana["imagen"], destino)

        if ruta:
            imagen = f"""
            <img
                class="captura"
                src="{texto(ruta)}"
                alt="Captura del laboratorio de la semana {numero}"
                loading="lazy"
            >
            """
        else:
            imagen = f"""
            <div class="captura-pendiente">
                <span aria-hidden="true">▧</span>
                <strong>Captura del laboratorio</strong>
                <small>Semana {numero}</small>
            </div>
            """

        repositorio = semana["repositorio"].strip()

        if enlace_valido(repositorio):
            boton = f"""
            <a
                class="boton-github"
                href="{texto(repositorio)}"
                target="_blank"
                rel="noopener noreferrer"
            >
                {ICONO_GITHUB}
                Ver en GitHub
            </a>
            """
        else:
            boton = '<span class="pendiente">Repositorio pendiente</span>'

        laboratorio = f"""
        {imagen}

        <div class="enlace-repositorio">
            {boton}
        </div>

        <details class="detalles-laboratorio">
            <summary>Ejercicio, procedimiento y resultados</summary>

            <div class="contenido-laboratorio">
                <h4>Ejercicio de laboratorio</h4>
                <p>{texto(semana["laboratorio"])}</p>

                <h4>Procedimiento</h4>
                <p>{texto(semana["procedimiento"])}</p>

                <h4>Resultados</h4>
                <p>{texto(semana["resultados"])}</p>
            </div>
        </details>
        """
    else:
        laboratorio = """
        <p class="teoria">
            (Semana teórica, sin laboratorio práctico)
        </p>
        """

    return f"""
    <article class="tarjeta-semana">
        <header class="cabecera-semana">
            <h3>Semana {numero}</h3>
            <span class="titulo-tema">{texto(semana["titulo"])}</span>
        </header>

        <p class="descripcion-semana">
            {texto(semana["temas"])}
        </p>

        {laboratorio}

        <div class="reflexion-semana">
            <p>
                <strong>Reflexión: ¿Qué aprendí?</strong>
                <em>{texto(semana["aprendi"])}</em>
            </p>

            <p>
                <strong>¿Cómo aprendí?</strong>
                <em>{texto(semana["como"])}</em>
            </p>
        </div>
    </article>
    """


def generar_portafolio():
    destino = BASE / "docs"
    destino.mkdir(exist_ok=True)
    (destino / "assets").mkdir(exist_ok=True)
    (BASE / "assets").mkdir(exist_ok=True)

    foto = copiar_imagen(PERFIL["foto"], destino)

    if foto:
        retrato = f"""
        <img
            class="foto"
            src="{texto(foto)}"
            alt="Fotografía de {texto(PERFIL['nombre'])}"
        >
        """
    else:
        retrato = f"""
        <div class="foto-pendiente">
            <strong>{texto(PERFIL["iniciales"])}</strong>
            <span>MI PORTAFOLIO DIGITAL</span>
        </div>
        """

    tarjetas = "".join(
        crear_tarjeta_semana(semana, destino)
        for semana in SEMANAS
    )

    fuentes = ""

    for fuente in BIBLIOGRAFIA:
        enlace = ""

        if enlace_valido(fuente["url"]):
            enlace = f"""
            <a
                href="{texto(fuente['url'])}"
                target="_blank"
                rel="noopener noreferrer"
            >
                Consultar fuente ↗
            </a>
            """

        fuentes += f"""
        <article class="fuente">
            <span class="etiqueta">{texto(fuente["tipo"])}</span>
            <h3>{texto(fuente["titulo"])}</h3>
            <p>{texto(fuente["descripcion"])}</p>
            {enlace}
        </article>
        """

    pagina = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta
        name="description"
        content="Portafolio académico de {texto(PERFIL['nombre'])}.
        Proyectos y cuaderno de aprendizaje de desarrollo web."
    >
    <title>{texto(PERFIL["nombre"])} | Portafolio</title>

    <style>
        {CSS}
    </style>
</head>

<body>
    <nav class="navegacion" aria-label="Navegación principal">
        <div class="contenedor nav-interior">
            <a href="#inicio" class="logo">
                {texto(PERFIL["iniciales"])}<span>.</span> / portafolio
            </a>

            <div class="enlaces">
                <a href="#inicio">Inicio</a>
                <a href="#sobre-mi">Sobre mí</a>
                <a href="#proyectos">Proyectos</a>
                <a href="#cuaderno">Cuaderno</a>
                <a href="#reflexion">Reflexión final</a>
                <a href="#bibliografia">Bibliografía</a>
            </div>
        </div>
    </nav>

    <main>
        <div class="contenedor">
            <section class="portada" id="inicio">
                <div>
                    <span class="etiqueta">
                        Portafolio electrónico · Desarrollo web
                    </span>

                    <h1>
                        Aprender.<br>
                        Construir.<br>
                        <span>Evolucionar.</span>
                    </h1>

                    <h3>Hola, soy {texto(PERFIL["nombre"])}.</h3>

                    <p class="presentacion">
                        {texto(PERFIL["presentacion"])}
                    </p>

                    <div class="acciones">
                        <a href="#cuaderno" class="boton">
                            Explorar mi cuaderno ↓
                        </a>

                        <a href="#proyectos" class="boton boton-secundario">
                            Ver proyectos ↗
                        </a>
                    </div>
                </div>

                <div class="marco-foto">
                    {retrato}

                    <div class="pie-foto">
                        <span class="punto"></span>
                        {texto(PERFIL["carrera"])}
                    </div>
                </div>
            </section>

            <div class="franja">
                <span>{texto(PERFIL["universidad"])}</span>
                <span>TEORÍA + PRÁCTICA + REFLEXIÓN</span>
            </div>

            <section class="seccion" id="sobre-mi">
                <span class="etiqueta">01 / Mi perfil</span>
                <h2>La persona detrás del código.</h2>

                <div class="tres-columnas">
                    <article class="tarjeta-oscura">
                        <span class="numero">01</span>
                        <h3>Sobre mí</h3>
                        <p>{texto(PERFIL["sobre_mi"])}</p>
                    </article>

                    <article class="tarjeta-oscura">
                        <span class="numero">02</span>
                        <h3>Mis estudios</h3>
                        <p>{texto(PERFIL["estudios"])}</p>
                    </article>

                    <article class="tarjeta-oscura">
                        <span class="numero">03</span>
                        <h3>Mi experiencia</h3>
                        <p>{texto(PERFIL["experiencia"])}</p>
                    </article>
                </div>
            </section>

            <section class="seccion" id="proyectos">
                <span class="etiqueta">02 / Mi trabajo</span>
                <h2>Proyectos concluidos.</h2>

                <div class="proyecto">
                    <div>
                        <h3>De una idea a una solución.</h3>
                        <p>
                            Explora mis repositorios para conocer el código,
                            la documentación y el desarrollo de mis proyectos.
                        </p>
                    </div>

                    <a
                        href="{texto(PERFIL["github"])}"
                        class="boton"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Ver proyectos en GitHub ↗
                    </a>
                </div>
            </section>
        </div>

        <section class="cuaderno" id="cuaderno">
            <div class="contenedor">
                <span class="etiqueta">03 / Cuaderno de aprendizaje</span>
                <h2>Mi aprendizaje, semana a semana.</h2>

                <p class="intro-cuaderno">
                    Conceptos, ejercicios de laboratorio, resultados y
                    reflexiones de mi recorrido en el curso.
                </p>

                <div class="semanas">
                    {tarjetas}
                </div>
            </div>
        </section>

        <div class="contenedor">
            <section class="seccion" id="reflexion">
                <span class="etiqueta">04 / Reflexión final</span>
                <h2>Mirar atrás para seguir creciendo.</h2>

                <div class="tres-columnas">
                    <article class="tarjeta-oscura">
                        <span class="numero">01 / CONOCIMIENTO</span>
                        <h3>¿Qué aprendí?</h3>
                        <p>{texto(REFLEXION["aprendi"])}</p>
                    </article>

                    <article class="tarjeta-oscura">
                        <span class="numero">02 / PROCESO</span>
                        <h3>¿Cómo aprendí?</h3>
                        <p>{texto(REFLEXION["como"])}</p>
                    </article>

                    <article class="tarjeta-oscura">
                        <span class="numero">03 / MEJORA</span>
                        <h3>Mi siguiente paso</h3>
                        <p>{texto(REFLEXION["mejorar"])}</p>
                    </article>
                </div>
            </section>

            <section class="seccion" id="bibliografia">
                <span class="etiqueta">05 / Bibliografía</span>
                <h2>Las bases de mi aprendizaje.</h2>

                <p>Libros y recursos web de consulta.</p>

                <div class="bibliografia">
                    {fuentes}
                </div>
            </section>
        </div>
    </main>

    <footer>
        <div class="contenedor pie-interior">
            <span>
                {texto(PERFIL["nombre"])} ·
                {texto(PERFIL["curso"])}
            </span>

            <a href="#inicio">Volver al inicio ↑</a>
        </div>
    </footer>
</body>
</html>
"""

    (destino / "index.html").write_text(pagina, encoding="utf-8")
    (destino / ".nojekyll").touch()

    return destino


if __name__ == "__main__":
    carpeta = generar_portafolio()

    if "--build" in sys.argv:
        print(f"Página generada en: {carpeta / 'index.html'}")
    else:
        puerto = 8000
        manejador = partial(
            SimpleHTTPRequestHandler,
            directory=str(carpeta),
        )

        try:
            servidor = ThreadingHTTPServer(
                ("127.0.0.1", puerto),
                manejador,
            )
        except OSError:
            print(
                "No se pudo iniciar el servidor. "
                "Comprueba si ya tienes otro app.py ejecutándose."
            )
            raise SystemExit(1)

        print(f"Abre en tu navegador: http://localhost:{puerto}")
        print("Para detener el servidor, presiona Ctrl+C.")
        print("Después de editar el código, reinicia el servidor.")

        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
        finally:
            servidor.server_close()