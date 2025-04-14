# Magic Proxy

**¡Bienvenido a Magic Proxy!** 🎴

¿Te gustaría jugar a Magic: The Gathering, pero no tienes el dinero para comprar las cartas? ¡Este software es para ti!

## ¿Qué hace Magic Proxy?

Magic Proxy es una herramienta diseñada para ayudarte a crear proxies de cartas de Magic de manera rápida y sencilla. Con este software, podrás tomar un mazo de cartas en formato `.txt` y generar un archivo PDF listo para imprimir. ¡Así podrás tener tus cartas sin tener que gastar dinero!

### Funcionalidades principales:

1. **Generación automática de proxies**  
   Simplemente ingresa el nombre de las cartas en un archivo `.txt` y el software se encargará de descargarlas automáticamente desde Scryfall, el servicio que ofrece las imágenes oficiales de las cartas. Las cartas se agregarán a un PDF listo para ser impreso.

2. **Soporte para tokens**  
   Si una carta genera tokens adicionales, el programa te preguntará cuántas copias de esos tokens quieres generar. De esta manera, puedes asegurarte de tener suficientes tokens para jugar.

3. **Generación de la parte trasera de la carta**  
   Si deseas, puedes imprimir la parte de atrás de las cartas, que se agregará automáticamente en la primera página del PDF. Si no lo necesitas, simplemente puedes ignorarla.

4. **Guías de corte**  
   El PDF generado incluye líneas guía para que puedas cortar las cartas con precisión utilizando un cutter o tijeras. Esto facilita el proceso de cortar las cartas para que se adapten a las dimensiones correctas.

5. **Selección de versiones de cartas**  
   Cuando descargas cartas, si existen múltiples versiones o artes de la misma carta, el software elegirá una versión aleatoria de las primeras 100 variantes disponibles. Para esto debes agregar {r} luego del nombre de la carta.

---

## Archivos incluidos

En la carpeta del proyecto, encontrarás los siguientes archivos:

- **Código fuente**: Si deseas ver o modificar el código, puedes abrirlo y adaptarlo a tus necesidades.
- **Ejemplo**: Un archivo de ejemplo en formato `.txt` que contiene un mazo de cartas de ejemplo. Úsalo como referencia para crear tu propio mazo.
- **Ejecutable**: Si no quieres lidiar con el código, puedes usar el ejecutable directamente. Simplemente ejecuta el archivo y el software hará todo el trabajo por ti.

---

## Instrucciones de uso

1. **Prepara tu mazo**: Crea un archivo `.txt` con los nombres de las cartas que quieres agregar a tu mazo. Asegúrate de seguir la estructura correcta:\
  1 Lightning Bolt\
  2 Forest\
  3 Goblin Token

2. **Ejecuta el software**: Si estás usando el archivo ejecutable, solo haz doble clic en él. Si prefieres usar el código fuente, ejecuta el script de Python.

3. **Generación del PDF**: El programa descargará las imágenes de las cartas, las organizará y generará un archivo PDF listo para imprimir. ¡No olvides imprimir las guías de corte!

4. **¡A jugar!**: Una vez que tengas tus cartas impresas, puedes usarlas para jugar con tus amigos. Recuerda que, aunque las cartas son funcionales, el valor y la rareza de las cartas originales no se aplican a los proxies.

---

## Requisitos

Este software requiere tener Python y las siguientes bibliotecas instaladas:

- `requests`
- `Pillow`

Si estás usando el archivo ejecutable, no necesitas instalar nada adicional, ya que todo está incluido.

---

