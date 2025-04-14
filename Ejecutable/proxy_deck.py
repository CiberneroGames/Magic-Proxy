import os
import requests
from urllib.parse import quote
from PIL import Image
from io import BytesIO
import shutil
import math
import random
import subprocess

# === 1. Detectar el archivo .txt ===
txt_files = [f for f in os.listdir() if f.endswith(".txt")]
if len(txt_files) != 1:
    print("❌ Se debe encontrar exactamente un archivo .txt en el directorio.")
    exit()

cartas_txt = txt_files[0]
nombre_base = os.path.splitext(cartas_txt)[0]  # Usar el nombre del archivo .txt para la carpeta y el PDF
output_folder = os.getcwd()
dorso_nombre = "Magic_card_back.jpg"
token_descargados = set()

# === 2. Leer archivo .txt ===
with open(cartas_txt, "r", encoding="utf-8") as f:
    lineas = [line.strip() for line in f if line.strip() and not line.strip().isdigit() and not line[0].isalpha()] 

# === 3. Descargar dorso de carta ===
if not os.path.exists(dorso_nombre):
    url_dorso = "https://static.wikia.nocookie.net/mtgsalvation_gamepedia/images/f/f8/Magic_card_back.jpg"
    response = requests.get(url_dorso)
    with open(dorso_nombre, "wb") as f:
        f.write(response.content)

# === 4. Descargar imágenes de cartas ===
# Carpeta actual (donde está el script)
output_folder = os.getcwd()
token_descargados = set()

def descargar_imagen(nombre_carta, numero, random_version=False):
    query = quote(nombre_carta)
    url = f"https://api.scryfall.com/cards/named?fuzzy={query}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Si la carta tiene múltiples versiones, seleccionamos una aleatoria si corresponde
        if random_version and "prints_search_uri" in data:
            url_variantes = data["prints_search_uri"]
            res_variantes = requests.get(url_variantes)
            res_variantes.raise_for_status()
            variantes = res_variantes.json()["data"]
            seleccion = random.choice(variantes[:100])
        else:
            seleccion = data

        # Obtención de la imagen
        if "image_uris" in seleccion:
            img_url = seleccion["image_uris"]["normal"]
        elif "card_faces" in seleccion and "image_uris" in seleccion["card_faces"][0]:
            img_url = seleccion["card_faces"][0]["image_uris"]["normal"]
        else:
            print(f"❌ No se encontró imagen para: {nombre_carta}")
            return

        # Descargar la imagen
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data)).convert("RGB")

        nombre_archivo = f"{numero}_{nombre_carta}.jpg"
        path = os.path.join(output_folder, nombre_archivo)
        img.save(path, "JPEG")
        print(f"✅ {nombre_carta} → {nombre_archivo}")

        # Verificar si la carta tiene tokens
        if "all_parts" in seleccion:
            token_parts = [p for p in seleccion["all_parts"] if p["component"] == "token"]
            for parte in token_parts:
                token_name = parte["name"]
                if token_name.lower() in token_descargados:
                    continue

                # Verificamos si es un token y descargamos la imagen correspondiente
                try:
                    token_data = requests.get(parte["uri"]).json()
                    if "type_line" in token_data and "Token" in token_data["type_line"]:
                        print(f"🪙 Esta carta genera el token: {token_name}")
                        try:
                            cantidad_token = int(input(f"¿Cuántas copias de '{token_name}' querés agregar? (0 para ignorar): "))
                        except:
                            cantidad_token = 0
                        if cantidad_token > 0:
                            token_descargados.add(token_name.lower())
                            # Obtener la URL de la imagen del token
                            imagen_token_url = token_data["image_uris"]["normal"]
                            descargar_token(imagen_token_url, token_name, cantidad_token)
                except Exception as e:
                    print(f"❌ Error con el token '{token_name}': {e}")
            
    except Exception as e:
        print(f"❌ Error con '{nombre_carta}': {e}")

def descargar_token(imagen_url, nombre_token, cantidad):
    try:
        nombre_archivo = f"{cantidad}_Token_{nombre_token.replace(' ', '_')}.jpg"
        path = os.path.join(output_folder, nombre_archivo)
        if not os.path.exists(path):
            img_data = requests.get(imagen_url).content
            img = Image.open(BytesIO(img_data)).convert("RGB")
            img.save(path, "JPEG")
            print(f"🎯 Token descargado: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error descargando token '{nombre_token}': {e}")

# === 6. Procesar líneas ===
for linea in lineas:
    try:
        cantidad, nombre = linea.split(" ", 1)
        cantidad = int(cantidad)
        if "{r}" in nombre:
            nombre = nombre.replace("{r}", "").strip()
            descargar_imagen(nombre, cantidad, random_version=True)
        else:
            descargar_imagen(nombre.strip(), cantidad)
    except ValueError:
        print(f"⚠️  Línea ignorada: {linea}")

# === 7. Clasificar imágenes ===
imagenes = [f for f in os.listdir() if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
imagenes_con_numero = []
for imagen in imagenes:
    if imagen == dorso_nombre:
        continue
    nombre, _ = os.path.splitext(imagen)
    if "_" in nombre and nombre.split("_")[0].isdigit():
        imagenes_con_numero.append(imagen)

# === 8. Construir lista de cartas ===
lista_cartas = [dorso_nombre] * 9  # Agregar 9 dorsos como primera página
for imagen in sorted(imagenes_con_numero):
    cantidad = int(imagen.split("_")[0])
    lista_cartas.extend([imagen] * cantidad)

total_cartas = len(lista_cartas)
paginas = math.ceil(total_cartas / 9)
nombre_base_pdf = f"{nombre_base}_{total_cartas - 9}_cartas"

# === 9. Generar archivo LaTeX ===
contenido = r"""\documentclass{article}
\usepackage[paperwidth=210mm, paperheight=297mm, margin=0mm]{geometry}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{eso-pic}
\pagestyle{empty}

\begin{document}
"""

margen_izquierdo = 9.75
margen_superior = 15.15

for pagina in range(paginas):
    contenido += r"""
\AddToShipoutPictureBG*{
  \begin{tikzpicture}[remember picture, overlay]
    \def\cardwidth{63.5}
    \def\cardheight{88.9}
"""
    for row in range(1, 3):
        y = margen_superior + row * 88.9
        contenido += (
            f"    \\draw[black, line width=0.5pt] "
            f"([yshift={-y}mm] current page.north west) -- "
            f"([xshift=210mm, yshift={-y}mm] current page.north west);\n"
        )
    for col in range(1, 3):
        x = margen_izquierdo + col * 63.5
        contenido += (
            f"    \\draw[black, line width=0.5pt] "
            f"([xshift={x}mm] current page.north west) -- "
            f"([xshift={x}mm, yshift=-297mm] current page.north west);\n"
        )
    contenido += (
        f"    \\draw[black, line width=0.5pt] "
        f"([xshift={margen_izquierdo}mm, yshift={-margen_superior}mm] current page.north west) "
        f"to ([xshift={margen_izquierdo}mm, yshift={-297}mm] current page.north west);\n"
    )
    contenido += (
        f"    \\draw[black, line width=0.5pt] "
        f"([xshift={margen_izquierdo + 3 * 63.5}mm, yshift={-margen_superior}mm] current page.north west) "
        f"to ([xshift={margen_izquierdo + 3 * 63.5}mm, yshift={-297}mm] current page.north west);\n"
    )
    contenido += (
        f"    \\draw[black, line width=0.5pt] "
        f"([xshift={margen_izquierdo}mm, yshift={-margen_superior}mm] current page.north west) "
        f"to ([xshift={margen_izquierdo + 3 * 63.5}mm, yshift={-margen_superior}mm] current page.north west);\n"
    )
    contenido += (
        f"    \\draw[black, line width=0.5pt] "
        f"([xshift={margen_izquierdo}mm, yshift={-(margen_superior + 3 * 88.9)}mm] current page.north west) "
        f"to ([xshift={margen_izquierdo + 3 * 63.5}mm, yshift={-(margen_superior + 3 * 88.9)}mm] current page.north west);\n"
    )

    for i in range(9):
        idx = pagina * 9 + i
        if idx >= total_cartas:
            break
        imagen = lista_cartas[idx]
        row = i // 3
        col = i % 3
        xshift = margen_izquierdo + col * 63.5
        yshift = margen_superior + row * 88.9
        contenido += (
            f"    \\node[anchor=north west, inner sep=0pt] at "
            f"([xshift={xshift}mm, yshift={-yshift}mm] current page.north west) "
            f"{{\\includegraphics[width=63.5mm,height=88.9mm]{{{imagen}}}}};\n"
        )
    contenido += r"""
  \end{tikzpicture}
}
\mbox{}
\newpage
"""

contenido += r"\end{document}"

with open(f"{nombre_base_pdf}.tex", "w", encoding="utf-8") as f:
    f.write(contenido)

print(f"📄 Archivo LaTeX generado: {nombre_base_pdf}.tex")

# === 10. Compilar PDF ===
print("🛠️ Compilando PDF...")
try:
    subprocess.run(["pdflatex", f"{nombre_base_pdf}.tex"], check=True)
    print(f"✅ PDF generado: {nombre_base_pdf}.pdf")
except subprocess.CalledProcessError as e:
    print(f"❌ Error al compilar PDF: {e}")

# === 11. Organizar todo ===
os.makedirs(nombre_base, exist_ok=True)
shutil.move(f"{nombre_base_pdf}.pdf", os.path.join(nombre_base, f"{nombre_base_pdf}.pdf"))
shutil.move(f"{nombre_base_pdf}.tex", os.path.join(nombre_base, f"{nombre_base_pdf}.tex"))

for archivo in lista_cartas:
    if os.path.exists(archivo):
        shutil.move(archivo, os.path.join(nombre_base, archivo))

shutil.move(cartas_txt, os.path.join(nombre_base, cartas_txt))

for ext in [".log", ".aux"]:
    aux_file = f"{nombre_base_pdf}{ext}"
    if os.path.exists(aux_file):
        os.remove(aux_file)

# === 12. Script de limpieza ===
script_limpieza = '''import os

extensiones = ['.jpg', '.jpeg', '.png', '.webp', '.tex', '.log', '.aux']
eliminados = 0

for archivo in os.listdir():
    if any(archivo.lower().endswith(ext) for ext in extensiones):
        os.remove(archivo)
        print(f"🗑️ Borrado: {archivo}")
        eliminados += 1

if eliminados == 0:
    print("✨ No había archivos para borrar.")
else:
    print(f"✅ {eliminados} archivos eliminados.")

try:
    os.remove(__file__)
    print("🧼 Script de limpieza eliminado.")
except Exception as e:
    print(f"⚠️ No se pudo eliminar el script: {e}")
'''
with open(os.path.join(nombre_base, "limpiar_archivos.py"), "w", encoding="utf-8") as f:
    f.write(script_limpieza)

print(f"📂 Todo guardado en la carpeta: {nombre_base}")
