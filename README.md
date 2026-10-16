# Spherical (ZX Spectrum 48K, 1989) — ingeniería inversa documentada

Análisis completo del código Z80 de **Spherical** (Rainbow Arts / Electronic Zoo, 1989; puzzle-plataformas de pantalla estática al estilo *Solomon's Key*), pensado para quien quiera entenderlo, hacer mods o portarlo sin repetir el trabajo.

> Los derechos del juego pertenecen a sus titulares (según nuestra investigación, hoy **Ziggurat Interactive**). Este repositorio **no contiene el juego**: ni cintas, ni snapshots, ni código desensamblado con los bytes originales, ni gráficos ni niveles. Solo documentación propia, un archivo de control de SkoolKit y herramientas. Necesitas **tu propia copia legítima**. Si el titular pide retirar algo, se retirará.

## Qué hay aquí

| Ruta | Contenido |
|---|---|
| [`docs/Spherical_ZX_Spectrum_Analisis_Completo.md`](docs/Spherical_ZX_Spectrum_Analisis_Completo.md) | **El documento principal** (en español): cinta y carga, mapa de memoria, bucle principal, estructuras de datos, formato de niveles, gráficos y máscaras, todas las mecánicas (esfera, bloques, orbe, energía, 19 tipos de enemigo, 2 jugadores…), referencia de 81 rutinas, guía de modding con recetas probadas, y qué está verificado y qué no. |
| [`docs/verificacion.md`](docs/verificacion.md), [`docs/cobertura.md`](docs/cobertura.md) | Qué se comprobó y cómo; cobertura de instrucciones (4689/4689 ejecutadas por alguna prueba, con las salvedades que se explican). |
| [`control/spherical_anotado.ctl`](control/spherical_anotado.ctl) | Archivo de control de [SkoolKit](https://skoolkit.ca/) con la separación código/datos y **todos los comentarios** del análisis. No contiene bytes del juego. |
| [`herramientas/`](herramientas/) | Scripts Python (simulador con SkoolKit): inyección de teclas, cobertura, extracción, pruebas de cada mecánica, parcheador de cintas TZX. |

## Cómo reproducir el desensamblado comentado

1. Obtén un snapshot (`.sna`/`.z80`) de tu copia con el juego en ejecución (mundo 0 cargado).
2. Con SkoolKit ≥ 9:
   ```bash
   sna2skool.py -H -c control/spherical_anotado.ctl tu_snapshot.sna > spherical_anotado.skool
   ```
3. Obtendrás el `.skool` con el código comentado línea a línea (en el análisis reensambla idéntico byte a byte a la RAM `$5B00-$FFFF`). **No lo publiques.**

Las herramientas tienen algunas rutas fijas (`/home/claude/...`) de nuestro entorno; ajústalas a tu instalación.

## Resumen de lo que se sabe

- Código en `$A7CC–$D030`; bucle principal en `$AAC7` **sin sincronización con la interrupción** (la velocidad depende del contenido del nivel; hay un limitador probado en la guía de mods).
- 9 mundos de 10 niveles cargados de cinta (81 niveles reales, 1P y 2P distintos); sprites 16×16 con máscara calculada a partir de dos tablas de silueta.
- La energía es una barra compartida por ambos jugadores; a 0 → *Game Over*. El juego **no tiene vidas**: existe un contador de reintentos (tecla R).
- Todo lo no medido se marca como suposición; lo único sin medir es la **velocidad en hardware real**.

## Licencia

- Scripts de `herramientas/`: MIT (ver [`LICENSE`](LICENSE)).
- Documentación y archivo de control: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (propuesta; cámbiala si prefieres otra).
- Ninguna licencia aquí cubre el juego original ni sus datos.

---

