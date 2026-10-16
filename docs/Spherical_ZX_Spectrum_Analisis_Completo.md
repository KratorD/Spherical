# Spherical (ZX Spectrum 48K, 1989) — Análisis completo del código

**Guía de ingeniería inversa para quien quiera entender, modificar o portar el juego sin repetir el trabajo.**

> Juego: *Spherical* — Rainbow Arts / Electronic Zoo, 1989 (diseño: Jörn Galka). Puzzle-plataformas de pantalla estática, parecido a *Solomon's Key*.
> Plataforma analizada: ZX Spectrum 48K (cinta TZX `Spherical_Erbe.tzx` + dos snapshots propios).
> Herramientas: SkoolKit 10.1 (desensamblado y simulador Z80 con la ROM real de 48K), scripts Python propios (incluidos en la carpeta `herramientas/`).
> Idioma: español. Todas las direcciones están en hexadecimal (`$XXXX`).

---

## 0. Aviso legal y de uso

*Spherical* (1989) fue publicado por Rainbow Arts / Electronic Zoo; según la investigación del autor de este repositorio, los derechos los tiene hoy **Ziggurat Interactive**. Este documento es un **análisis para fines educativos y de preservación**, hecho sobre una copia propia del juego. Contiene únicamente **descripciones** (direcciones, estructuras, algoritmos, comportamiento observado y herramientas propias). **No contiene** el código ni los datos del juego: ni binarios, ni cintas, ni snapshots, ni desensamblado con los bytes originales, ni sprites, ni mapas de niveles. Para seguir el análisis necesitas **tu propia copia legítima**. Si publicas un mod, distribúyelo como **parche** (IPS/BPS o diferencias binarias) y no como juego completo. Si el titular de los derechos solicita retirar algo de este material, se retirará.

## 0.1 Cómo leer este documento

Cada afirmación lleva, cuando importa, una etiqueta de certeza:

| Etiqueta | Significado |
|---|---|
| **[V]** | Verificado ejecutando el código real del juego en el simulador (con teclas inyectadas, estados forzados o la ROM real). |
| **[C]** | Comprobado contra los datos reales (cinta/snapshots), p. ej. que un renderizador reproduce píxeles y atributos del juego. |
| **[L]** | Leído en el desensamblado y coherente, pero sin ejecutar una prueba específica. |
| **[S]** | Suposición razonable; no demostrada. |

Importante: **[V] significa "lo que hace el código"**, que es lo que hay que reproducir. No sustituye a jugar el original en un emulador de ciclo exacto; por eso la única cosa que sigue sin medirse es la **velocidad real en hardware** (ver §13).

## 0.2 Resumen en diez líneas

1. El juego es un único bloque de código/datos de 38 656 bytes en `$6100-$F7FF` (cargado desde cinta) + 9 bloques de **mundo** de 11 264 bytes en `$6F00-$9AFF` que se cargan de cinta al cambiar de mundo (cada 10 niveles).
2. Punto de entrada: `$A7CC`. Modo de interrupciones **IM 2** con vector `$FDFD → JP $C4D5` (solo sirve para sonido).
3. **No hay sincronización por frame**: el bucle principal (`$AAC7`) corre libre; su velocidad depende solo de los T-estados que consume (≈ 20 ciclos/s en 1P, ≈ 18,7 en 2P).
4. El tablero es de **14 × 10 casillas de 16×16 px**; mapa de trabajo en `$DE5A` (140 bytes) sobre una capa de fondo en `$DEE6` (140 bytes).
5. Todo se dibuja en un **búfer en RAM** (`$DF72`, 160 líneas × 29 bytes) y se vuelca a pantalla con `LDI` (`$CD43`). Los sprites son 16×16 a 1 bit con **silueta calculada** por dos tablas de 256 bytes (`$5B00`, `$5C00`); el color lo ponen los atributos de las casillas.
6. Entidades: jugador (29 bytes, `$D3A7`), jugador 2 (`$D3C4`), orbes (`$D3E1`, `$D3E8`), esfera (8 bytes, `$D3F0`), hasta 14 enemigos de 22 bytes (`$D3F8`).
7. Hay **19 tipos de enemigo** (0–`$12`); los de tipo `$12`+ son segmentos de jefe. 8 jefes (mundos 1–8).
8. 91 casillas distintas (`$9B00 + 36·código`), 81 niveles reales (0–78 y 80) × 2 modos (1 jugador y 2 jugadores, **niveles distintos**).
9. El código fuente comentado de todo el programa se reensambla **byte a byte idéntico** a la memoria original (§2.3).
10. 4 689 instrucciones, 82 rutinas: **todas ejecutadas por alguna prueba** (una, `$B8A8`, solo con el PC forzado: es código muerto; §13).

## 0.3 Índice

1. [Qué se entrega y cómo reproducirlo](#1-qué-se-entrega-y-cómo-reproducirlo)
2. [Metodología y herramientas](#2-metodología-y-herramientas)
3. [La cinta y la carga](#3-la-cinta-y-la-carga)
4. [Mapa de memoria](#4-mapa-de-memoria)
5. [Arranque, interrupciones, pantalla y sonido](#5-arranque-interrupciones-pantalla-y-sonido)
6. [Flujo del programa y bucle principal](#6-flujo-del-programa-y-bucle-principal)
7. [Estructuras de datos y variables](#7-estructuras-de-datos-y-variables)
8. [Niveles](#8-niveles)
9. [Gráficos](#9-gráficos)
10. [Mecánicas del juego](#10-mecánicas-del-juego)
11. [Referencia de rutinas (81)](#11-referencia-de-rutinas-81)
12. [Guía de modificación (mods)](#12-guía-de-modificación-mods)
13. [Verificación, correcciones e incógnitas](#13-verificación-correcciones-e-incógnitas)
14. [Apéndices](#14-apéndices)

---

## 1. Qué contiene el repositorio y cómo reproducirlo

```
README.md
docs/Spherical_ZX_Spectrum_Analisis_Completo.md   Este documento
docs/verificacion.md, docs/cobertura.md           Qué se probó y cómo (cobertura de instrucciones)
control/spherical_anotado.ctl                     Archivo de control de SkoolKit: separa código/datos y lleva todos los comentarios (sin bytes del juego)
herramientas/                                     Scripts Python de extracción, prueba y verificación
```

El **desensamblado comentado completo** (`.skool`) y los recursos extraídos (sprites, casillas, niveles) **no se publican** por ser material con copyright; se regeneran localmente a partir de tu propia copia con el `.ctl` y las herramientas.

Para **regenerar el desensamblado** desde un snapshot (SkoolKit ≥ 9):

```bash
python3 sna2skool.py -H -c spherical_anotado.ctl 2jugadores.sna > spherical_anotado.skool
```

El `.sna` debe ser una captura del juego en ejecución (el mundo 0 cargado). Los snapshots que se usaron arrancan con `PC=$FDFD` (dentro de la rutina de interrupción), `SP=$FFFA` e interrupciones desactivadas; el simulador de SkoolKit incluye la ROM real de 48K.

---

## 2. Metodología y herramientas

### 2.1 Flujo de trabajo (el de SkoolKit, ampliado)

1. **Snapshot** `.sna` del juego en marcha (FUSE/ZEsarUX).
2. **Perfilado** de ejecución → mapa de código (se usó también el propio simulador de SkoolKit con `COVER=` para registrar cada instrucción ejecutada).
3. **Archivo de control** `.ctl` con `sna2skool.py`; se refinó a mano: código (`c`), bytes (`b`), palabras (`w`), texto (`t`), cadenas… y comentarios de rutina.
4. **Iteración**: leer → formular hipótesis → **comprobarla ejecutando** (ver 2.2) → anotar con etiqueta de certeza.
5. **Cobertura**: medir qué instrucciones no ha ejecutado ninguna prueba y atacarlas hasta llegar al 100 % (§13).

### 2.2 El método que más ha valido: simular, no solo leer

SkoolKit trae un **simulador Z80 en Python** (`skoolkit.simulator.Simulator`) con la ROM de 48K. Se cargó el snapshot y se inyectaron teclas interceptando las lecturas de puertos (`IN A,(C)`/`IN A,($FE)`) con un "tracer". Con eso se pudo ejecutar el juego **sin emulador gráfico**, avanzar frames a mano y leer la memoria. Notas prácticas (te ahorrarán horas):

* **Registros del simulador** (lista `sim.registers`): `0 A, 1 F, 2 B, 3 C, 4 D, 5 E, 6 H, 7 L, 8 IXh, 9 IXl, 10 IYh, 11 IYl, 12 SP, 13 SP', 14 I, 15 R, 24 PC, 25 T-estados, 26 IFF, 27 IM`. (El `23` es L', no SP: error fácil de cometer.)
* Ejecutar una instrucción: `sim.opcodes[mem[pc]]()`. Aceptar la interrupción: `sim.accept_interrupt(reg, mem, pc)`.
* Bucle de frames: cada `sim.frame_duration` T-estados hay una interrupción; hay que **avanzar el tiempo aunque se rechace la interrupción** (IFF = 0 en los menús), o el bucle se atasca.
* Los `.sna` de esta captura empiezan dentro del manejador IM 2. Hay que esperar ≈150 interrupciones antes de pulsar una tecla en el menú, y mantenerla pulsada.
* Para forzar el estado de una rutina concreta: se coloca `PC`, `SP` (con una dirección de retorno centinela en la pila) y las variables y se ejecuta hasta el centinela. Es lo que hacen `ultimos.py`, `energiatest.py`, `despachotest.py`…
* Cobertura: se envuelve cada opcode (`ops[i] = wrap(ops[i])`) y se guarda el `PC` de inicio de cada instrucción. La variable `COVER=fichero` de `keytrace.py` lo activa.

### 2.3 El código fuente se reensambla idéntico (prueba para modders)

El `.skool` anotado se reensambla con `skool2bin.py` y el resultado es **idéntico byte a byte** a la memoria del snapshot en `$5B00-$FFFF` (42 240 bytes, 0 diferencias):

```bash
python3 skool2bin.py spherical_anotado.skool juego.bin     # origen $5B00, 42 240 bytes
```

Las advertencias que emite ("Address $CD93 replaced … in unsubbed LD operation") son esperables: son los puntos de **código automodificable** (§12.4). Si tu instalación de SkoolKit se queja de que faltan `128-0.rom`/`128-1.rom` (pasa con copias montadas a mano), basta con copiar `48.rom` con esos nombres a `skoolkit/resources/`: no se usan.

Esto significa que puedes **editar el `.skool`, reensamblar y volcar el resultado sobre un snapshot o sobre el bloque `smc` de la cinta** y obtener un juego modificado. (Los bytes de `$5B00-$5CFF` son tablas generadas en ejecución y `$5D00-$60FF` restos del cargador BASIC; el bloque de cinta `smc` empieza en `$6100`.)

### 2.4 Lista de herramientas (`herramientas/`)

| Script | Para qué |
|---|---|
| `keytrace.py` | Base de casi todo: carga un snapshot, inyecta teclas (mapa `KEYS`), joystick Kempston (`.kemp`), señal EAR de cinta (`.tape`), y con `COVER=`/`ROLES=`/`CALLERS=` registra cobertura, fotogramas dibujados y llamadores. |
| `framesweep.py` | Recorre los 90 niveles de un mundo (1P o 2P) con teclas y registra los sprites dibujados. |
| `cobertura.py` | Cruza un `.skool` con las direcciones ejecutadas y genera el informe de cobertura. |
| `extraer_assets.py`, `extraer_cinta.py`, `extraer_niveles.py`, `extraer_jefes_animados.py` | Extracción de sprites, mundos de la cinta, niveles (JSON + PNG) y animaciones de jefe. |
| `manifiesto_sprites.py`, `verificar_mascara.py`, `completitud_sprites.py`, `rolesextra.py`, `orbe45.py` | Manifiesto y atlas de sprites, y su verificación contra `$C384`. |
| `blocktest.py`, `orbtest.py`, `potiontest.py`, `pociontest2.py`, `enemytest.py`, `levtest.py`, `bosstest.py`, `finaltest.py`, `recogetest.py`, `salidatest.py`, `niveltest.py`, `tapetest.py`, `kempstontest.py`, `teclasjuego.py`, `menuteclas.py`, `menuseguir.py`, `menuyfin.py`, `clavetest.py`, `tecleotest.py`, `fundidotest.py`, `jefe60test.py`, `varios.py`, `orbebounce.py`, `puntuacionbaja.py`, `colortest.py` | Pruebas de cada mecánica (véase §13). |
| `ultimos.py`, `energiatest.py`, `despachotest.py`, `b8a8test.py` | Las últimas ramas del código y la prueba de código muerto. |
| `velocidad.py`, `velocidad_cont.py` | Velocidad del ciclo (sin y con modelo de contención). |
| `modtest.py` | Comprueba recetas de modificación (§12). |
| `parchear_tzx.py` | Parchea bytes de un bloque CODE de la cinta TZX y recalcula la paridad (§12.1). |

---

## 3. La cinta y la carga

`Spherical_Erbe.tzx` contiene solo **bloques estándar** (sin turbo; paridad correcta):

| Bloque | Tipo | Contenido |
|---|---|---|
| `Spherical` | BASIC, 441 B | Cargador (restos en `$5D00`). |
| `fadscr` | CODE 6 912 B en `$8000` | Pantalla de carga (SCREEN$). |
| `smc` | CODE 38 656 B en `$6100` | **El juego**: sprites base, tablas, gráficos de casillas, código y datos hasta `$F7FF`. |
| `border` | CODE 6 912 B en `$8000` | Pantalla con el marco. |
| `0` … `8` | CODE 11 264 B en `$6F00` | **9 mundos** (niveles 0–89; el último jugable es el 80). |

**Carga de mundos** (`$CFB3`, [V] con la ROM real y la señal EAR generada desde el TZX): muestra "SEARCHING FOR n", llama a `LD-BYTES` de la ROM (`$0562`, vía `$D01F`) para leer primero una cabecera de 17 bytes (`$D031`: tipo, nombre de 10 caracteres, longitud, inicio) y, **si el nombre coincide con `D98B+'0'`**, el bloque de datos en la dirección de la cabecera. Si el bloque es de otro mundo lo rechaza y sigue buscando; con error de paridad (`$D019`) repite la carga. El bloque de un mundo ocupa **`$6F00-$9AFF`**:

| Zona del bloque | Contenido |
|---|---|
| `$6F00-$85FF` | Sprites propios del mundo (frames `$70+`), **imágenes grandes de jefe** (pares máscara/dato), y en el mundo 7 las casillas alternativas del nivel 70 |
| `$8600-$8A5F` | 8 capas de fondo de 140 bytes |
| `$8A60-$8FD7` | 10 mapas de 1 jugador (140 B c/u) |
| `$8FD8-$954F` | 10 mapas de 2 jugadores |
| `$9550-$9667` | 2 mapas especiales (`$9550`, `$95DC`) |
| `$9668-$98A9` | Cabeceras de nivel (enemigos y posiciones) |
| `$98AA-$9AFF` | Sin uso identificado. (En el mundo 8 la pantalla final "The End" está en `$9064`, dentro de la zona de mapas 2P.) |

El mundo 0 es el que está residente en los snapshots; **el bloque `0` de la cinta coincide byte a byte con la RAM** de los snapshots.

---

## 4. Mapa de memoria

| Zona | Contenido |
|---|---|
| `$4000-$57FF` / `$5800-$5AFF` | Pantalla / atributos |
| `$5B00-$5CFF` | Tablas de **silueta** A y B (256 B cada una), generadas al arrancar por `$A84B` (en zona de variables de sistema, sin uso) |
| `$5D00-$60FF` | Restos del cargador BASIC |
| `$6100-$6EFF` | **112 sprites 16×16** (frames `$00-$6F`, 32 B cada uno) |
| `$6F00-$9AFF` | **Bloque del mundo cargado** (ver §3) |
| `$9B00-$A7CB` | **91 gráficos de casilla** (36 B: 32 de bitmap + 4 de atributos) |
| `$A7CC-$D030` | **Código** |
| `$D031-$D3A6` | Textos (con descriptores de posición), cabecera de cinta, tablas de teclas/claves (`$D2E8` reintentos, `$D2E9`/`$D2FD` claves) |
| `$D3A7-$D52C` | **Registros de entidades** (jugadores, orbes, esfera, enemigos) y contador de enemigos `$D52C` |
| `$D52D-$D91C` | Búferes de fondo de sprites (48 B por entidad) y temporal de dibujo |
| `$D91D-$DE59` | Variables de juego y **tablas** (salto `$D922`, órbita `$D948`, trayectorias `$D968`, rutas `$D99B…`, jefes `$DABA…`, sonido…) |
| `$DE5A-$DEE5` | **Mapa de trabajo** 14×10 |
| `$DEE6-$DF71` | **Capa de fondo** 14×10 |
| `$DF72-$F191` | **Búfer de pantalla** (160 líneas × 29 B) |
| `$F192-$F491` | Copia de atributos (768 B) |
| `$F1D4` | (dentro del búfer de atributos) origen del tablero: stride 32 por fila de caracteres, 64 por fila de casillas, +2 por casilla |
| `$F492-$F591` | Iconos del HUD (8 × 32 B) |
| `$F592-$F791` | Fuente 8×8 (`$F592 + 8·(ASCII−$20)`) |
| `$F79B/$F79C` | Recoloreado de casillas (papel claro/oscuro) |
| `$FE00-$FF00` | Tabla IM 2 (257 bytes con `$FD`); `$FDFD: JP $C4D5` |

Pila en `$FFFE` al arrancar (el juego reinicia la pila al salir de nivel/partida).

---

## 5. Arranque, interrupciones, pantalla y sonido

### 5.1 `$A7CC` — inicio
Desactiva interrupciones, pila en `$FFFE`, configura **IM 2**: llena `$FE00-$FF00` con `$FD` (cualquier vector apunta a `$FDFD`) y escribe allí `JP $C4D5`. Construye la tabla de direcciones de línea de pantalla (`$DD1A`, 160 entradas: las líneas del tablero), asigna a cada entidad su búfer de fondo, **detecta Kempston** (lee el puerto `$1F`; si el valor es ≥ `$20` no hay joystick → `D988=0`) y genera las tablas de silueta `$5B00/$5C00`. Termina en el menú (`$A8D1`).

### 5.2 Interrupción IM 2 (`$C4D5`): solo sonido
Si hay un **descriptor de sonido** activo (`$D076 ≠ 0`, puntero al descriptor), toca un tramo de onda cuadrada por el altavoz (`OUT ($FE)`, bit 4) por interrupción. Descriptor de 6 bytes: `+0` periodo, `+1` nº de ciclos del tramo, `+2` incremento del periodo por interrupción, `+3` interrupciones restantes, `+4` periodo de reinicio, `+5` cuenta de reinicio. Al acabar pone `$D076=0`. Efectos: rebote `$DCA2`, energía `$DC8A` (tono según energía), explosión `$DCAE`, paso `$DC90`, disparo/aparición `$DCA8`, bloque `$DC9C`. **El bucle principal no espera a la interrupción**: la interrupción interrumpe el cálculo y sigue.

### 5.3 Tubería de dibujo
1. **Fondo**: `C9F5` dibuja la **capa de fondo** (`$DEE6`) con `BFF6` (sin máscara) y encima el **mapa** (`$DE5A`) con `CB2D`. Los códigos 0, `$41-$43` y `$4C` se dibujan con máscara (`CB40`), el resto sobrescribe. Se hace al cargar el nivel y por casilla cuando cambia.
2. **Entidades** (`C2DC`): para cada una, `C384` guarda el fondo bajo el sprite (búfer de la entidad), calcula la silueta y mezcla (`fondo AND máscara OR dibujo`), con 4 posiciones de subpíxel (x AND 3).
3. **Partículas** (`B296`, `B2F3`): píxeles sueltos con máscara según x AND 3.
4. **Volcado** (`CD43`): copia las 160 líneas del búfer (28 `LDI` por línea) a la pantalla y los atributos de `$F192` a `$5800` (se desactiva durante los fundidos parcheando `$CD93`).
5. **Borrado** (`C338`): restaura el fondo de cada entidad **en orden inverso** (para que se deshagan bien los solapes).

Orden de dibujo (el último queda encima): enemigos 0…n−1, esfera, jugador 1, orbe 1 (si `D3BC AND $18`), jugador 2 (frame **+`$0D`**: la maga es el mismo conjunto de frames desplazado), orbe 2.

Coordenadas: **x en unidades de 2 px** (0…`$69`; pantalla = 16 + 2·x), **y en píxeles** (0…`$90`; pantalla = 16 + y). El tablero es de 14×10 casillas con origen en (16,16). La casilla de una posición se calcula con `C037`: `índice = (y>>4)·14 + (x>>3)`.

### 5.4 Entrada
`CCB5` construye en `D98A` el byte de entrada del jugador en curso: bit 0 arriba, 1 derecha, 2 abajo, 3 izquierda, 4 acción de bloque. Las 5 teclas de cada jugador están en su registro (`+$0F…+$13`). **Código de tecla** = `8·(4−bit) + (7−semifila)`, probado con `CDD3` (devuelve Z si pulsada). Semifilas: 0 `$FE` (CAPS-V), 1 `$FD` (A-G), 2 `$FB` (Q-T), 3 `$F7` (1-5), 4 `$EF` (0-6), 5 `$DF` (P-Y), 6 `$BF` (ENTER-H), 7 `$7F` (ESPACIO-B). Esquemas (tecla 5 del menú, `D39E`): 0 Sinclair-Sinclair, 1 Kempston-Sinclair, 2 Teclado-Sinclair, 3 Kempston-Teclado (los esquemas Kempston solo si `D988≠0`). Teclado J1 = **Q P A O ESPACIO**; Sinclair 2 = 9 7 8 6 0; Sinclair 1 = 4 2 3 1 5. Kempston (solo J1): bit 0 derecha, 1 izquierda, 2 abajo, 3 arriba, 4 disparo [V].

**La tecla de bloque actúa al SOLTAR**: mientras está pulsada, el contador `+$14` sube hasta `$40`; al soltarla, si es > 0, se activa el bit 4 de `D98A` y el contador vuelve a 0. El mismo contador distingue pulsación corta (colocar/quitar bloque) de larga (lanzar el orbe; §10.5).

---

## 6. Flujo del programa y bucle principal

### 6.1 Menú (`$A8D1`)
Teclas: **1** una persona (`$A96C` → `$AA85` con A=1), **2** dos (A=2), **3** entrenamiento (`D39B=$54`), **4** clave (`$A983`; compara con las tablas `$D2E9` y `$D2FD`), **5** mandos (`$AA02`), **6** mejores puntuaciones (`$AA57`), **7** alterna fondo claro/oscuro (`F79B`: 1 ↔ 5; `$AA5D`). [V] cada tecla alcanza su rutina.

### 6.2 Inicio de partida (`$AA85`/`$AA8C`)
Pone `D91D` (nº de jugadores), nivel `D39A=0`, y a cero: pociones `D98C`, banderas `D3BC`/`D3D9`, temporizadores, puntuaciones; **reintentos `D2E8=4`** (`LD A,$04` en `$AAA5`: el operando está en `$AAA6`), **energía `D3EF=100`** (`$AAAA`: operando en `$AAAB`), y dibuja los indicadores de poder de ambos jugadores (`CE5C`). Entra en el bucle principal.

### 6.3 Bucle principal (`$AAC7`)
```
AAC7  carga el nivel (C563) con transición (fundido a negro CB7D / blanco CC0A) y reaparición
AAF4  jugador 1 (IY=$D3A7, D91E=1):  B38D casillas -> CCB5 teclas -> B5DD movimiento
                                     -> BFD7 choque con enemigo -> CDF5(C=$FF) daño
                                     -> BE7B bloques -> AEF7 poderes/puertas
AB25  si D91D<>1: lo mismo para el jugador 2 (IY=$D3C4, D91E=2)
AB5E  esfera B767 (salvo D39B=$54), enemigos B82C
      dibujo: C2DC -> B2F3 -> CD43 (volcado) -> B296 -> C338 (borrado)
AB78  D989 = (D989+1) AND 3          (reloj de 4 fases para ralentizar animaciones)
AB81  teclas globales: R, F, T, ENTER, H (+ M/N con ILLUMINATUS)
```
* **R** (código `$0D`, `$AB81`): si quedan reintentos (`D2E8`) resta una y **reinicia el nivel** (`JP $AAC7`); con 0 reintentos se ignora. **Los reintentos solo se gastan con R.**
* **F** (`$0E`, `$AB97`): abandona la partida (`$AD2F`, vuelve al menú; restaura los gráficos del nivel 70 si procede).
* **Energía = 0** (`$AB9F-$ABA3`): **Game Over directo** (`$ACEE`), sin gastar reintentos.
* **T** (`$05`): si `D920≠0` lo reinicia a `$0101` → **cancela el reloj de arena**.
* **ENTER** (`$21`): **poción** (`$ABBB`; §10.7).
* **H** (`$ACB3`): pausa (atributos a azul oscuro; vuelve al pulsar otra vez).
* Con `D079≠0` (clave ILLUMINATUS): **invencible**, y **M/N** avanzan/retroceden de nivel.

**Velocidad.** No hay `HALT` en el bucle: es un bucle libre. Con el simulador (sin contención) un ciclo = 173 523 T-estados en 1P (≈ 2,47 interrupciones; ≈ 20,2 ciclos/s) y 187 421 T en 2P (≈ 18,7 ciclos/s); el modelo de contención de memoria del 48K (accesos a `$4000-$7FFF` retrasados 6,5,4,3,2,1,0,0 T durante las 192 líneas) añade ≈ 0,7 %. Al ser un bucle libre, **la velocidad en hardware real debería coincidir con esa cifra**, pero **no está medida** [S].

### 6.4 Fin de nivel (`$C524`)
Se llega al **tocar la esfera la salida `$44`**, al recoger la casilla `$3A` o con **50 anillos** (`D07B`). No suma puntos. Avanza `D39A` (con `$4E`=78 salta a `$50`=80: **no existen** los niveles 79 ni 81–89), restaura el intercambio de casillas del mundo 7 si el nivel era `$46`, pone `D39B=0` y vuelve al bucle (que carga el nivel). Si el nuevo nivel pertenece a otro mundo (`D98B ≠ D39A/10`), `C563` llama a `CFB3` y pide el bloque a la cinta. Con `D39A=$51` salta a `$AD45` (juego completado). Con `D39B=$57` avanza dos niveles y con `$42` uno [V].

### 6.5 Fin de partida (`$ACEE`) y pantalla final (`$AD45`)
Game Over: fundido, textos (`$D2AE`, `$D282`), espera de 100 ciclos, inserta la puntuación del jugador 1 (y la del 2) con `ADAC` en la tabla de mejores (`$D109`, 5 entradas de 15 B: 2 de puntos + 13 de nombre; pide el nombre con `AE6B` si entra), muestra "BEST PLAYERS" (`AE09`), restaura casillas si el nivel era `$46` y vuelve al menú. Juego completado (`$AD45`): pantalla "The End" (128×64 px en `$9064` del bloque del mundo 8), espera acción y va a las puntuaciones.

### 6.6 Modos especiales (`D39B`)
`0` normal · `$42` sala de bonus (se activa con la acción de bloque sobre una casilla `$2E`; mapa `$9550`, cabecera n.º 20) · `$54` entrenamiento del menú (sin esfera) · `$57` tras la copa `$40` (mapa `$95DC`, cabecera n.º 21; al terminar avanza dos niveles). El mundo 8 no tiene salas especiales (sus bytes son la pantalla final).

---

## 7. Estructuras de datos y variables

### 7.1 Registro de jugador (29 bytes: `$D3A7` J1, `$D3C4` J2) — `IY`

| Offset | Campo |
|---|---|
| `+0` | x (unidades de 2 px) |
| `+1` | y (px) |
| `+2` | fotograma (sprite = `$6100 + 32·f`; la maga se dibuja con `f+$0D`) |
| `+3/+4` | puntero al búfer donde se guarda el fondo |
| `+5/+6` | dirección del sprite en el búfer de pantalla (la calcula el dibujo) |
| `+7` | dirección: `+1` derecha, `$FF` izquierda |
| `+8` | fotograma guardado |
| `+9` | fase vertical (0 = en suelo; si no, índice en la tabla de salto `$D922`) |
| `+$0A` | fase de la animación de bloque (≠0 = ocupado) |
| `+$0B/$0C` | dirección en el mapa de la casilla afectada |
| `+$0D/$0E` | dirección en el búfer de pantalla de esa casilla |
| `+$0F…+$13` | teclas: arriba, derecha, abajo, izquierda, bloque |
| `+$14` | contador de pulsación de la tecla de bloque (0–`$40`) |
| `+$15` | **banderas**: bit0 mover más rápido en el aire (casilla `$32`) · bit1 escudo · bit2 matraz verde (congela enemigos 0/1) · bit3 poder del orbe · bit4 poder doble · bit5 matraz azul (bloques rojos aleatorios) · bit6 orbe lanzado · bit7 bloqueo de bloques (casilla `$3E`) |
| `+$16/$17` | puntuación (16 bits) |
| `+$18` | temporizador del escudo (`$96` = 150 ciclos; se resta cada 4 ciclos) |
| `+$19` | temporizador del poder mágico (≈ `$C0`) |
| `+$1A` | índice de órbita del orbe (0–15) / dirección del orbe lanzado |
| `+$1B/$1C` | puntero de atributos |

### 7.2 Esfera (8 B, `$D3F0`), orbes (7 B, `$D3E1` y `$D3E8`)
Esfera: `+0` x (`$FF` = inactiva), `+1` y, `+2` fotograma (`$1A-$23`), `+7` dirección (`+1/$FF`). **Velocidad vertical global `D91F`** (+4 cae, −4 sube). Orbe: frame `$3A` (poder simple), `$3B` (doble), `$3C` (nivel `$50`).

### 7.3 Registro de enemigo (22 B desde `$D3F8`, hasta 14; contador `$D52C`) — `IY`

| Offset | Uso |
|---|---|
| `+0` | x (`$FF` = inactivo) |
| `+1` | y |
| `+2` | fotograma |
| `+3/+4` | puntero al búfer de fondo (48 B) |
| `+5/+6` | dirección del sprite en el búfer |
| `+7` | dirección / estado según tipo |
| `+8` | **tipo** |
| `+9/+A` | índice y/o puntero a tabla de ruta; en tipos 4 y 9–`$0E`, `+A` = y de origen |
| `+B` | x de origen (tipos 9–`$0E`) |
| `+D` | nº de segmentos (jefes) / contador de giros (tipo 8) |

### 7.4 Variables globales importantes

| Dirección | Contenido |
|---|---|
| `$D079` | invencibilidad (≠0 con ILLUMINATUS) |
| `$D07B` | anillos recogidos (50 → fin de nivel) |
| `$D076/$D087…` | puntero al descriptor de sonido activo y parámetros de texto/atributos |
| `$D085` | semilla del generador aleatorio (`CD9F`: A = máximo → 0…A−1) |
| `$D0C0` | dígito del texto "PLAYER n" |
| `$D2E8` | **reintentos** (se gasta solo con la tecla R; 4 al empezar). El juego **no tiene vidas**: tiene barra de energía y, a 0, Game Over. El nombre «reintentos» es interpretación del contador [S]; su comportamiento sí es [V] |
| `$D39A` | nivel actual (0-based) |
| `$D39B` | modo especial (0, `$42`, `$54`, `$57`) |
| `$D39E` | esquema de mandos (0–3) |
| `$D3EF` | **energía compartida** (0–100) |
| `$D52C` | nº de enemigos |
| `$D91D` | nº de jugadores · `$D91E` jugador en curso · `$D91F` velocidad vertical de la esfera |
| `$D920` | contador del reloj de arena (`$0100`; al recoger `$34` = `$14`) |
| `$D988` | Kempston presente · `$D989` reloj de ciclo (0–3) · `$D98A` entrada del jugador en curso |
| `$D98B` | **mundo cargado** (= `D39A/10`) · `$D98C` pociones |
| `$DC3A` | vida actual del jefe (`$DC3B+mundo` = vida inicial: **0, 24, 32, $FF, $FF, $FF, 48, 0, 64**; `$FF` = inmune al orbe) |
| `$DC44` | texto tecleado (clave/nombre, terminado en `$FF`) |
| `$F79B` | modo claro/oscuro de las casillas |

---

## 8. Niveles

### 8.1 Estructura general
* **81 niveles reales**: 0–78 y 80 (`$00-$4E` y `$50`), en **9 mundos** de 10 niveles (mundo = nivel/10). `C524` salta del 78 (`$4E`) al 80 (`$50`) y `C541` termina el juego al llegar a 81 (`$51`): **el 79 y el 81–89 no existen** (los bytes de esas posiciones son relleno y no deben usarse) [V].
* **Los niveles de 1 jugador y de 2 jugadores son distintos** (tablas separadas).
* El primer nivel de cada mundo 1–8 (10, 20, …, 80) es un **nivel de jefe/guardián**. El nivel 80 (`$50`) es el final.
* `C563` (cargar nivel) copia el mapa de 140 bytes a `$DE5A` desde `$8A60 + 140·n` (1P) o `$8FD8 + 140·n` (2P), con `n = D39A − 10·D98B`, copia la capa de fondo a `$DEE6` e interpreta la cabecera (`C65B`).

### 8.2 El tablero
**14 columnas × 10 filas** de casillas de 16×16 px (140 bytes, fila a fila, stride 14); origen en pantalla (16,16); la casilla (col, fila) está en x = 16+16·col, y = 16+16·fila. Los 140 bytes siguientes (`$DEE6`) son la **capa de fondo** (papel pintado) que se dibuja debajo, sin máscara. *(Notas antiguas hablaban de 12 filas: es falso.)*

### 8.3 Cabeceras (`$9668`)
Tabla de registros de longitud variable: 10 registros de 1P, 10 de 2P y 2 especiales; `C64E` salta N registros (`9 + 4·n` bytes cada uno):

```
fondo(2)  esfera(x,y)  J1(x,y)  J2(x,y)  nEnemigos(1)  nEnemigos × [x, y, tipo, frame]
```
* `fondo` = desplazamiento que se suma a `$4B00` para obtener la dirección de la capa de fondo (`$8600 + 140·k`).
* `J2 = $FFFF` en 1P. Un enemigo con `x=$FF` está inactivo.
* En los enemigos de tipo 5, 6 y 8 el `frame` se ignora; en los **jefes** es el número de segmentos −1 del primer registro.
* Los niveles 10, 20 y 50 rellenan la capa de fondo con una casilla (`$11`, `$00`, `$00`) en lugar de leerla del bloque (`C682-C6A3`).
* **Mundo 7, nivel 70 (`$46`)**: al entrar se **intercambian 20 casillas gráficas** (`$18-$2B`; `$2D0` bytes) entre `$9E60` y una copia de seguridad en `$71D0`, y se copian a `$9E60` los gráficos alternativos de `$6F00`. `C524` y `AD37` los restauran al salir o al terminar la partida [V]. Esto explica los "sprites" `$70-$86` del mundo 7: **son casillas, no sprites**.
* **Nivel 80 (`$50`)**: antes de dibujar desplaza la fila de fondo; con `D39B=0` pone los reintentos a 0 (`C563`); el orbe usa el frame `$3C`.

### 8.4 Códigos de casilla (el byte del mapa)

| Código | Efecto | Cert. |
|---|---|---|
| `00` | vacío | V |
| `01-2C` | piezas de fondo (papel pintado) | V |
| `2D` | gema: +30 puntos | V |
| `2E` | gema +1 punto; **con la acción de bloque encima abre la sala de bonus** (`D39B=$42`) | V |
| `2F` | anillo +10; `D07B`+1; con 50 → fin de nivel | V |
| `30` | anillo magenta +10 | V |
| `31` | energía a 100 | V |
| `32` | bit 0 de `+$15`: mover más rápido en el aire | V |
| `33` | varita: 1.ª vez **orbe mágico** (bit 3, temporizador `+$19≈$C0`); 2.ª vez **poder doble** (bit 4) | V |
| `34` | reloj de arena: `D920=$13/$14` → **congela la esfera** (la tecla T lo cancela) | V |
| `35` | matraz verde: bit 2 → **congela a los enemigos 0 y 1** | V |
| `36` | **poción**: `D98C`+1 (se gasta con ENTER) | V |
| `37` | matraz azul: bit 5 → aparecen **bloques rojos aleatorios** | V |
| `38` | escudo: bit 1, `+$18=$96` | V |
| `39` | +40 puntos | V |
| `3A` | fin de nivel | V |
| `3B,3C,3D` | llaves: eliminan las puertas `$55/$56/$57` (de una en una, con chispas) | V |
| `3E` | frasco rosa: bit 7 → **impide crear bloques** | V |
| `3F` | pergamino: muestra la clave en los niveles 12, 21, 41, 61, 75 (también con 2 jugadores) | V |
| `40` | copa: `D39B=$57` (sala especial; avanza dos niveles) | V |
| `41,42,43` | **peligros**: −1 de energía por ciclo mientras se pisan. `$41`/`$42` son además los **proyectiles** de los lanzadores 5/6 (viajan a derecha/izquierda) | V |
| `44` | **salida**: si la esfera la toca → fin de nivel. Bloquea al jugador. También se activa desde arriba si la esfera **sube** | V |
| `45-48` | bloque del jugador en **creación** (`45→46→47→48`); `48` = **bloque rojo** (el único que se puede destruir) | V |
| `49-4C` | bloque en **destrucción** (`49→4A→4B→4C→00`) | V |
| `4D-4F` | bloque amarillo fijo (3 variantes de dibujo) | V |
| `50-54` | estalactitas | V |
| `55-57` | puertas de colores (se abren con las llaves `3B-3D`) | V |
| `58,59,5A` | **rombos de flecha**: usar la acción de bloque sobre ellos cambia `D91F` de la esfera: `58` → −4 (sube), `5A` → +4 (cae), `59` → invierte el signo | V |

Colisión: el **jugador** es bloqueado por casillas **≥ `$44`**; la **esfera** por las **≥ `$2D` excepto `$43`**. Los enemigos usan la misma consulta que la esfera (`C19C`). **Rojo = bloque que coloca el jugador; amarillo = bloque fijo** (confirmado jugando).

**Rareza del original [L/V]**: `B38D` (recogida de casillas) recorre `B` filas, pero `B` se queda siempre en 1 (el `JP Z` de `$B3AB` salta a la instrucción siguiente y nunca se incrementa), así que **solo se examina la fila superior** bajo el jugador (`y>>4`) y 1 o 2 columnas (según `x AND 7`). Parece un bug del original; hay que respetarlo para reproducirlo 1:1.

---

## 9. Gráficos

### 9.1 Sprites 16×16 (`$6100 + 32·frame`)
16 filas × 2 bytes, **1 bit por píxel**, bit 7 = píxel de la izquierda, sin color propio (el color lo da el **atributo de la casilla** donde se dibuja). El juego no guarda máscara: la **calcula** al dibujar con dos tablas de 256 bytes generadas en `$A84B`:

```
silueta (16 bits por fila) = ( ~TablaA[byte_izquierdo] << 8 ) | ~TablaB[byte_derecho]      (1 = opaco)
píxel final = (fondo AND NOT silueta) OR gráfico
```
* `TablaA[b]` (en `$5B00`): AND que borra el fondo **desde un píxel a la izquierda del primer píxel activo hasta el borde derecho del byte** (p. ej. `A[$01]=$FC`, `A[$80]=$00`).
* `TablaB[b]` (en `$5C00`): borra **desde el borde izquierdo hasta un píxel a la derecha del último píxel activo** (p. ej. `B[$80]=$3F`, `B[$04]=$01`).
* Resultado: un **contorno relleno** (silueta) con 1 píxel de margen, con una asimetría entre bytes que es comportamiento real. Se ha comprobado que esta fórmula reproduce **píxel a píxel** lo que dibuja `$C384` para los **370 sprites** (`verificar_mascara.py`).
* `C384` no dibuja si `x ≥ $6A` o `y ≥ $91`. Se desplaza el sprite `x AND 3` posiciones de 2 px (cuatro subpíxeles dentro del byte).

El dominio de fotogramas posible es `$00-$FF` (el frame es un byte): **`$00-$6F` son del bloque base** (siempre residentes) y **`$70-$FF` son de cada mundo** (cambian con el bloque cargado). Las posiciones `$100-$127` de la región no pueden dibujarse como sprite.

### 9.2 Quién usa cada fotograma (medido ejecutando los 90 huecos de nivel posibles (81 reales) en 1P y 2P)

| Entidad | Fotogramas | Mundos |
|---|---|---|
| Mago (J1) | `$00-$03` andar izq., `$04-$06` giro, `$07-$0A` andar der., `$0B/$0C` agachado (izq./der.), `$38/$39` beber poción | 0-8 |
| Maga (J2) | los del mago **+`$0D`**: `$0D-$19` (agachada `$18/$19`) | 0-8 |
| Esfera | `$1A-$23` (giro) | 0-8 |
| Orbe | `$3A` (simple), `$3B` (doble), `$3C` (nivel 80) | 1-8 |
| Tipo 0 | `$24-$27` | 0-8 |
| Tipo 1 | `$28-$2F` | 0-7 |
| Tipos 2, 3 | `$30,$31` | 1-4, 7 |
| Tipo 4 | `$32-$37`, `$46` (oculta) | 0-7 |
| Tipo 5 | `$3D-$46` | 3-7 |
| Tipo 6 | `$46`, `$4F-$57` | 1,3-7 |
| Tipo 7 | `$47-$49` | 2-7 |
| Tipo 8 | `$4A-$4E` | 1-7 |
| Tipos 9, `$0A`, `$0B`, `$0C` | `$58` (y `$59` el `$0B` en los mundos 3, 5) | 1,2,3/5,6 |
| Tipo `$0D` | `$3A` | 7 |
| Tipo `$0E` | `$5A` | 8 |
| Tipos `$0F-$11` | `$5B-$6F` (tres partes de una criatura) | 5-7 |
| Tipo `$12` (jefes) | frames `$70-$B7` propios del mundo | 1,2,3,4,6,8 |

`$46` es el **fotograma invisible** (reposo de lanzadores y de la gota). Hay 835 de las 1 768 posiciones del volcado que son ceros (huecos de las regiones) y 533 que son **trozos de imágenes grandes** (no sprites); el manifiesto se genera con `manifiesto_sprites.py` a partir de tu propia copia. El `$45` que a veces aparece como "frame del orbe" es un valor residual del registro antes de que `B099` lo inicialice.

### 9.3 Imágenes grandes con máscara (jefes y escenarios)
Tabla `$DABA`, 8 bytes por mundo 1–8: **ancho (bytes), alto (filas), dirección de los datos, dirección de destino en el búfer `$DF72`, y el puntero (`+6/+7`) a la tabla de animación del jefe**. Datos = pares (máscara, dato) por byte, fila a fila (`C488`: `píxel = fondo AND máscara OR dato`).

| Mundo | Tamaño (B × filas) | Datos | Destino | Animación del jefe |
|---|---|---|---|---|
| 1 | 8 × 85 | `$7300` | `$E3B5` | `$DAFA` |
| 2 | 14 × 128 | `$7100` | `$E150` | `$DB17` |
| 3 | 12 × 69 (×2) | `$7400`, `$7A78` | `$E9C1`, `$E9D1` | `$DB2C` |
| 4 | 6 × 46 | `$7800` | `$DF88` | `$DB4F` |
| 5 | 19 × 121 | `$6F00` | `$DF76` | — |
| 6 | 4 × 32 | `$7800` | `$E6CA` | `$DBA5` |
| 7 | — | — | — | — |
| 8 | 16 × 104 | `$7380` | `$E5D4` | `$DC19` |

Extras: el mundo 4 pinta atributos blancos (`$CA8F`), el 8 copia atributos desde `$8080` (`$CAEA`; ocupan los "frames" `$FC-$102`), y el 3 tiene un parche (`$CA83`).

**Segmentos de jefe (tipo `$12`)**: el registro "cabeza" gobierna a `+$0D` registros siguientes; cada 2 ciclos toma el fotograma de su tabla de animación (`+$09/$0A`, índice `+$07`) y asigna al segmento *k* el fotograma `cabeza + k`; su posición (x,y) es **fija** (la de la cabecera). Geometría: mundo 1 → 4 segmentos (2×2), 2 → 4, 3 → 8 (dos bloques 2×2 = las mandíbulas), 4 → 9 (3×3), 6 → 6 (3×2), 8 → 9 (3×3). En el mundo 4 desplaza además 9 registros en vertical con la tabla de ondas `$DB7A`. Las secuencias de animación están en `assets/jefes_animacion.json`.

### 9.4 Casillas (`$9B00 + 36·código`)
32 bytes de bitmap (16 filas × 2) + **4 bytes de atributo** (2×2 caracteres; el bit 7 se borra al volcar a los atributos). 91 casillas (`$00-$5A`). El color puede cambiar en ejecución (`F79B/F79C`: tema claro/oscuro). Las casillas con máscara (0, `$41-$43`, `$4C`) no tocan los atributos.

### 9.5 Otros recursos gráficos
* **Fuente**: `$F592 + 8·(ASCII−$20)`, 8×8 a 1 bpp. El carácter `$21` (`!`) está sustituido por un icono de poción.
* **HUD**: `$F492-$F591` = 8 iconos de 16×16 (reintentos llenos/vacíos, barras de energía `CE2D` y de poder `CE5C`: `$F4B2`, `$F516+`, `$F57A/$F586`).
* **Pantalla final "The End"**: 128×64 px (64 líneas × 16 B) en `$9064` del bloque del mundo 8, seguida de 8×16 atributos; se copia a `$E400` y `$F27A`.
* **Textos**: cadenas con **descriptores** (`CF0C`): `$00 x y` posición (columna = (x−8)/2, fila = y), `$01 a` atributo, `$FF` fin, otro = carácter.

---

## 10. Mecánicas del juego

### 10.1 La esfera (`B767`) [V]
1. Si `x = $FF`, no hace nada. Consulta `C19C` → `E` (bits de **casilla libre**: 0 arriba, 1 derecha, 2 abajo, 3 izquierda) y `D=1` si toca la salida `$44` (a los lados siempre; encima solo si sube).
2. Si `D=1` → `C524` (nivel completado).
3. **Vertical**: `D91F` es la velocidad vertical con signo (normalmente +4). Si es ≥ 0 y hay hueco debajo, `y += D91F` y termina el paso; si es negativa, igual pero con "arriba".
4. **Horizontal** (solo si no se movió en vertical): dirección `+7` = ±1; si el lado está libre, `x += dir` (1 unidad = 2 px); si no, **invierte la dirección** y suena el rebote (`DCA2`). Los límites del campo (`x=0` y `x=$69`) cuentan como pared. **El rebote no pierde velocidad.**
5. La esfera avanza 1 unidad por ciclo (≈ 20 unidades/s) y cae 4 px por ciclo.
6. Está **congelada** mientras `D920 ≠ 0` (reloj de arena) y, en modo entrenamiento (`D39B=$54`), no se ejecuta.

### 10.2 El jugador: movimiento y salto (`B5DD`) [V]
* En suelo se mueve **2 unidades (4 px) por ciclo**; en el aire 1 unidad (algo más con el bit 0 de `+$15`). Usa `C092` (colisión: bloquean las casillas ≥ `$44`).
* Fotogramas: andar izq. `0-3` (cambian solo en ciclos pares de `D989`), giro `4-6`, andar der. `7-$0A` (al llegar a `$0B` vuelve a `7`), agachado `$0B/$0C`.
* **Salto**: tabla `$D922` (`dy` por ciclo): **−4, −2×6, +2×6, +4×9, +8…** (38 entradas); `+9` es la fase (0 = en el suelo). Sube 16 px (una casilla) en 7 ciclos y luego cae acelerando hasta 8 px/ciclo. En suelo, si hay hueco debajo la fase pasa a 8 (empieza a caer); si pulsa arriba, no está agachado y `y≠0`: fase 1 (o 7 si hay techo: salto casi sin altura). **Si choca con un techo mientras sube (fase < 8) la fase pasa a 8 y cae** (`$B73A`) [V]. Al tocar suelo `y &= $F8`, fase 0.
* **Agacharse** (A): fotograma `$0B/$0C`; vuelve al soltar.

### 10.3 Colocar y quitar bloques (`BE7B`) [V]
Se ejecuta **al soltar** la tecla de bloque (bit 4 de `D98A`). Se ignora si `D39A=$50` y `D39B=0`, si `+$0A≠0` (animación en curso: se sigue con `BF71`) o si el bit 7 de `+$15` está activo (frasco rosa).
1. Casilla destino: `E = x AND $F8`, `D = y AND $F0`.
   * Mirando a la **derecha**: se rechaza si `x ≥ $62`; `E += 8` y, si `x AND 7 ≥ 2`, otro `+8`.
   * Mirando a la **izquierda**: se rechaza si `x < 8`; `E −= 8`.
   * **Agachado** (`frame ≥ $0B`): la fila destino es la **inferior** (`D += 16`); se rechaza si `y = $90`. Se ejecuta con `y=$80` modificando la celda de la fila de abajo [V].
2. Se rechaza si el bloque solaparía con **la esfera** (`BFBA`), **el otro jugador** o **cualquier enemigo** (`BFD7`).
3. Casilla **vacía** → `$45` y animación de creación `45→46→47→48` (un paso cada ≈ 3 interrupciones); **`$48`** → `$49` y destrucción `49→4A→4B→4C→00`; las demás no se cambian, salvo `$2E` (sala de bonus) y `$58-$5A` (flechas).
4. Guarda en el registro del jugador la dirección del mapa (`+$0B/$0C`), la del búfer (`+$0D/$0E`) y los atributos (`+$1B/$1C`); suena `DC9C`.

### 10.4 Recogida de casillas (`B38D`)
Véase §8.4. Las recogibles **desaparecen del mapa** (se redibujan con la casilla de la capa de fondo en esa posición, `BFF6`). Las puntuaciones se suman en `+$16/$17` y se actualiza el marcador (`CEC1`; columna `$0E` para J1, `$38` para J2). Los peligros (`$41-$43`) llaman a `CDF5` con `C=$FF` y **no** se recogen.

### 10.5 Poderes: orbe mágico y poder doble [V]
* Al recoger `$33`: bit 3, **temporizador `+$19`** (≈ `$C0` = 192 ciclos). Un **orbe** (sprite `$3A`; `$3B` con poder doble; `$3C` en el nivel 80) **gira alrededor del jugador**: posición = jugador + par `(dx,dy)` de la tabla `$D948` (16 pares, radio 16 px), índice `+$1A`, uno por ciclo. Mata (con explosión de partículas) a los enemigos tipos 0, 1 y 9–`$11`; a los jefes les quita 1 de `DC3A` por contacto (en el nivel 60 solo si su fotograma está entre `$88` y `$9F`).
* **Poder doble** (2.ª `$33`, bit 4): permite **lanzar el orbe** manteniendo la tecla de bloque ≥ 16 ciclos; vuela mientras se mantiene (bit 6) y **rebota** contra paredes, techo y suelo (cambia la dirección con `XOR $05/$0A` sobre `+$1A`). Una segunda pulsación larga (10–13 ciclos) lo **recupera**.
* Los dos jugadores tienen su propio orbe (`$D3E1` J1, `$D3E8` J2).

### 10.6 Escudo, reloj, matraces
* **Escudo** (`$38`): bit 1; mientras está activo, `CDF5` no resta energía. Dura 150 ciclos (`+$18`, cuenta atrás cada 4). Al acabar se apaga el bit y se muestra el mensaje `$D2A0`.
* **Reloj de arena** (`$34`): `D920 = $13/$14`; mientras sea ≠ 0 la esfera no se mueve; **T** lo cancela.
* **Matraz verde** (`$35`): bit 2 → los enemigos tipo 0 y 1 dejan de moverse (`B82C`; se calcula con el OR de ambos jugadores).
* **Matraz azul** (`$37`): bit 5 → aparecen bloques rojos aleatorios.
* **Frasco rosa** (`$3E`): bit 7 → no se pueden crear bloques.

### 10.7 Poción (ENTER) [V]
Requiere `D98C > 0`. Resta una, borra su icono del marcador, reproduce la **animación de beber** (frames `$05,$05,$38,$38,$39,$39,$39` desde `$D98D`, y `$39,$38,$38,$05,$05` desde `$D995`; siempre sobre el registro del **jugador 1**) y **elimina** los enemigos de tipos **0–3 y 5–8** (no el 4 ni los 9+) y las casillas `$41/$42` (no la `$43`).

### 10.8 Energía y daño (`CDF5`) [V]
* **Energía compartida** `D3EF` (0–100) entre los dos jugadores. `CDF5(C)`: suma `C` con saturación a 0 y 100 (en la práctica solo se usa `C=$FF`; la rama positiva `$CE03-$CE0A` no tiene llamadores). Sin efecto si el escudo está activo. Actualiza el tono `DC8A` y la barra de 50 segmentos (energía/2, `CE2D`).
* **Contacto con un enemigo** (`BFBA`: caja de 8 unidades × 16 px): **−1 de energía por ciclo** mientras dure, salvo si su fotograma es `$46` (oculto) o hay escudo. Son los tres `LD C,$FF` de `$AB1A` (J1), `$AB53` (J2) y `$B3C6` (casillas peligro).
* Energía 0 → **Game Over** directo (no consume reintentos).
* **Reintentos** (`D2E8`, 4 al empezar): solo las consume la tecla **R**.

### 10.9 Enemigos (despachador `B82C`, 19 tipos)
Cada ciclo `B82C` recorre los `D52C` enemigos (IY = registro) y salta según el tipo (`+8`); los tipos `$0C` y `$0D` se procesan aunque `x=$FF`, los demás se saltan si `x=$FF`. Tabla de saltos: 0 `$B8AB`, 1 `$B90D`, 2 `$B984`, 3 `$B9A9`, 4 `$B9CE`, 5-6 `$BA25`, 7 `$BAE6`, 8 `$BB37`, 9 `$BBCD`, `$0A` `$BC0F`, `$0B` `$BC69`, `$0C` `$BCCF`, `$0D` `$BCFC`, `$0E` `$BD99`, `$0F-$11` `$BDD2`, ≥ `$12` `$BDFA`. Todas terminan en `$BE70` (IY += 22, siguiente). Se ha demostrado exhaustivamente (los 256 valores del byte de tipo) que no hay ningún tipo que quede sin manejador.

| Tipo | Comportamiento |
|---|---|
| 0 | **Caminante en el suelo**: 1 unidad/ciclo, gira al chocar con pared, no cae. Animación cada 4 ciclos (`D989=0`): der. `$24-$25`, izq. `$26-$27`. |
| 1 | **Caminante con gravedad**: igual, pero cae 4 px/ciclo si no hay suelo. Der. `$28-$2B`, izq. `$2C-$2F`. |
| 2 | **Burbuja** que oscila en vertical: tabla `$D99B` de pares (frame, dy): −4,−4,−4,−2,−2,+2,+2,+4,+4,(+4). |
| 3 | Igual con la tabla `$D9B0` (12 pasos, mayor amplitud). |
| 4 | **Gota** (máquina de estados por frame): `$46` oculta (10 %/ciclo de empezar) → `$32-$34` formándose (cada 4 ciclos) → `$35` cayendo 4 px/ciclo → `$36` salpicadura → `$37` reinicio en su y original. Inofensiva si está oculta. |
| 5, 6 | **Lanzadores** de proyectiles: boca animada con la tabla `$D9C9` (40 pasos; el 6 suma `$12` al frame); en el paso 12 **disparan**: el proyectil es una **casilla del mapa** (`$3C+tipo`: `$41` viaja a la derecha, `$42` a la izquierda), 1 casilla/ciclo, borra la anterior, y se detiene al salir (`x ≥ $6A`) o chocar con una casilla no vacía. |
| 7 | **Disco** que rebota en vertical, 4 px/ciclo; frames `$47,$48,$49,$48` (`$D9F1`). |
| 8 | **Sigue paredes**: rumbo `+7` (0 arriba, 1 der., 2 abajo, 3 izq.); si se bloquea gira `±1`; el sentido de giro (operando **autoparcheado** en `$BBBE`) se invierte cada 8 giros (`+$0D`). Frames de `$D9F5/$DA03`. |
| 9 | Proyectil que cruza hacia la izquierda a 8 px/ciclo con 7 pendientes cíclicas; al salir reaparece en el origen (`+$0B,+$0A`). |
| `$0A` | **Torbellino**: tabla circular `$D968` (16 pares) con deriva a la izquierda. |
| `$0B` | **Pelota que bota**: arco `$DA14` (`$90→$32→$90`), `x ±2`; en el nivel 50 deja anillos `$2F` con un 6 %/ciclo. |
| `$0C` | **Disparo del jefe** (mundo 6): sale cuando el fotograma del enemigo 0 está en `$9A-$9F`. |
| `$0D` | Proyectil en espiral de **8 direcciones** (contador compartido `D07A`). |
| `$0E` | Proyectil diagonal (`y += 4·D078`, `x −= 2`). |
| `$0F-$11` | Criatura de **3 sprites** (cabeza, torso, pies) animados por tablas `$DA3F/$DA68/$DA91` (12 pasos de reposo con `$46` + 28 de animación). |
| `$12+` | **Jefes y serpientes** (§9.3). |

**Vida de los jefes** (`DC3B`): mundo 1 → 24, 2 → 32, 3/4/5 → `$FF` (inmunes al orbe), 6 → 48, 8 → 64. Con la vida del jefe 8 a 0 se ejecuta `AD45` (fin del juego) [V]. Los enemigos con `x=$FF` están muertos; la poción los deja con `x=$FF` (y lanza partículas).

### 10.10 Dos jugadores
* **Comparten**: energía (`D3EF`), reintentos (`D2E8`), nivel, esfera y enemigos. **Tienen propios**: registro (`+$15` banderas, puntuación, escudo, poder), orbe (las pociones `D98C` son globales).
* **Secuencial en el mismo ciclo**: el bucle ejecuta primero todo el turno del J1 y luego, si `D91D=2`, el del J2, con `IY=$D3C4` y `D91E=2` (no hay turnos por pantalla). La maga se dibuja con `frame+$0D`.
* El J2 usa los mandos del esquema elegido (Sinclair/Kempston/teclado); **Kempston solo lo usa el J1**. Los niveles 2P son distintos de los 1P.

### 10.11 Partículas
`B23C` crea hasta B partículas alrededor de (L,H) en la tabla `$DCB6` (5 B: x, y, vx, vy, fondo guardado); `B296` las mueve (la vertical se aplica dos veces, simula gravedad) y escribe un byte de color en el búfer; `B2F3` guarda el fondo y pinta con máscara según `x AND 3` (`$C0,$30,$0C,$03`).

### 10.12 Claves, puntuaciones y texto
* **Claves** (tabla `$D2E9` 1P ×5, `$D2FD` 2P ×6; cada entrada de 4 B: nivel del pergamino `$3F` que la muestra, nivel de inicio, puntero al texto): 1P → **RADAGAST** 9, **YARMAK** 19, **ORCSLAYER** 39, **SKYFIRE** 59, **MIRGAL** 75; 2P → **GHANIMA** 9, **GLIEP** 19, **MOURNBLADE** 39, **JADAWIN** 59, **GUMBACHACHMAL** 75; **ILLUMINATUS** → invencibilidad (`D079`).
* **Mejores puntuaciones**: `$D109`, 5 entradas de 15 B. `ADAC` inserta con desplazamiento; una puntuación baja no entra. `AE6B` es la **entrada de texto** (teclas por semifila, borrar con `0`, `ENTER` termina).
* **Efectos de pantalla**: `CB7D` (fundido a negro, 7 pasos, resta 1 a tinta y papel), `CBBA` (aparecer), `CC0A` (fundido rápido a blanco con borde; al morir un jefe y al terminar el nivel), `CC5A` (aparición con borde). Parchean `$CD93` (`RET`) para que `CD43` no copie atributos mientras dura el efecto.
## 11. Referencia de rutinas (81)

Tabla generada del archivo de control anotado (`spherical_anotado.ctl`). **V** = además de leída, comprobada ejecutando el juego en el simulador. Sin marca = leída en el desensamblado (y ejecutada por alguna prueba: ver `cobertura.md`, 4689/4689 instrucciones). Los comentarios línea a línea están en `spherical_anotado.skool`.

| Dirección | Rutina | Descripción |
|---|---|---|
| `$A7CC` | Inicio: preparación del sistema, tablas y menú principal **V** | Punto de entrada del juego (tras el cargador BASIC). Desactiva interrupciones, coloca la pila en $FFFE y configura el modo de interrupción 2 (IM 2): se rellena la tabla $FE00-$FF00 con el valor $FD, de modo que cualquier interrupción salta a la dirección $FDFD, donde se escribe un `JP $C4D5` (la rutina de sonido, ver `$C4D5`). Después construye la tabla de direcciones de línea de pantalla ($DD1A), asigna a cada entidad su búfer de fondo, detecta si hay interfaz Kempston (lee el puerto $1F; un valor >= $20 indica que no hay joystick) y genera las tablas de silueta $5B00/$5C00. |
| `$AAC7` | Bucle principal del juego **V** | Carga el nivel actual (`$C563`) con un efecto de transición y ejecuta indefinidamente el ciclo del juego. Cada vuelta (aprox. 2,5 interrupciones = unos 20 ciclos/s) hace, en orden: |
| `$AD45` | Fin de partida / juego completado **V** | Se llega aquí con la pila reiniciada al terminar los niveles (D39A=$51) o al jugar el nivel final. Muestra el mensaje y la lista de puntuaciones. |
| `$AD8F` | Esperar una tecla del jugador **V** | Espera a que se pulse (y se suelte) la tecla de disparo de cada jugador (códigos $D3BA / $D3D7). Utilidad de pantallas de texto. |
| `$ADAC` | Insertar puntuación en la tabla de mejores jugadores **V** | Entrada: HL = puntuación; $D0C0 = '1' o '2' (jugador). Si la puntuación entra en el top 5 ($D109, 5 entradas de 15 bytes: 2 de posición + 13 caracteres) pide el nombre con `$AE6B` y desplaza el resto. |
| `$AE09` | Pantalla de mejores puntuaciones **V** | Dibuja "BEST PLAYERS" ($D0C5) y las 5 entradas de $D109 con nombre y puntos; espera una tecla. |
| `$AE6B` | Entrada de texto (nombre o clave) **V** | Edición de texto con el teclado: lee las teclas (códigos de letra por semifila), borra con la tecla de código $21... y termina con $23 ($21 = ENTER). Deja el texto en $DC44 (terminado en $FF). Se usa para claves y para el nombre en la tabla de récords. |
| `$AEF7` | Puertas de colores y estado de poderes del jugador **V** | Tres veces (tabla $D07C, 3 entradas de 3 bytes: código de casilla de puerta $55/$56/$57, x, y de barrido): cuando el jugador recoge una llave (casillas $3B-$3D, ver `$B38D`) la entrada correspondiente se activa y, mientras no haya partículas en marcha (DCB4=0), se barre el mapa casilla a casilla (x+8, y+16 al final de cada fila) hasta encontrar una casilla de puerta de ese color: se pone a 0, se redibuja con la casilla de la CAPA DE FONDO situada en la misma posición (dirección +$8C = $DEE6) y se lanza una chispa (`$B23C`). Así la puerta se deshace de una en una. Después gestiona el temporizador del escudo (bit 1 de +$15, +$18 cuenta atrás cada 4 ciclos; al acabar muestra `$D2A0`) y el poder mágico (bits 3-4, temporizador +$19): el orbe mágico (D3E1 / D3E8) gira alrededor del jugador en 16 posiciones de la tabla $D948 y mata a los enemigos que toca (`$B099`). |
| `$B038` | Auxiliar: avanza el orbe un paso de la tabla de órbita **V** |  |
| `$B060` | Auxiliar del orbe (continuación) **V** |  |
| `$B06E` | Auxiliar del orbe (continuación) **V** |  |
| `$B079` | Auxiliar del orbe (continuación) **V** |  |
| `$B087` | Auxiliar del orbe (continuación) **V** |  |
| `$B099` | Orbe mágico: órbita, daño a enemigos y disparo **V** | Posición del orbe = posición del jugador + desplazamiento de la tabla $D948 (16 pares dx,dy que describen una circunferencia de radio 16 px; el índice está en +$1A y avanza uno por ciclo). El sprite del orbe es el frame $3A ($3B con bit 4 = poder doble, $3C en el nivel $50). Si el orbe solapa un enemigo (`$BFD7`): tipos 0-1 y 9-$11 se destruyen con una explosión de partículas (`$B23C`); otros tipos (jefes, >= $12) reducen el contador $DC3A (puntos de vida del jefe) y al llegar a 0 comienza la secuencia de victoria (`$C524` / `$AD45`). |
| `$B23C` | Generar explosión de partículas | Crea hasta B partículas alrededor de (L,H) en la tabla $DCB6 (5 bytes cada una: x, y, vx, vy, byte de fondo guardado). A = duración en ciclos, C = dispersión. Inicia además el sonido DCAE. |
| `$B296` | Partículas: mover | Cada ciclo avanza cada partícula con su velocidad (la vertical se aplica dos veces, simulando gravedad) y escribe un byte de color en el búfer de pantalla ($DF72). |
| `$B2F3` | Partículas: guardar fondo y dibujar | Guarda el byte de fondo del búfer bajo cada partícula (antes de dibujarla) y después pinta los píxeles con una máscara que depende de x AND 3 ($C0,$30,$0C,$03). |
| `$B38D` | Jugador: interacción con casillas **V** | Examina las casillas que ocupa el jugador (IY) y aplica el efecto de la que toca (ver tabla de casillas en el documento de formatos). Códigos: $2D gema +30, $2E gema +1, $2F anillo +10 (cuenta D07B; con 50 anillos se completa el nivel), $30 anillo +10, $39 +40, $31 energía al 100, $32 bit 0 (+$15), $33 poder mágico (1ª vez orbe, 2ª poder doble), $34 reloj de arena (D920=$14), $35 bit 2, $36 poción (D98C+1), $37 bit 5 (bloques aleatorios), $38 escudo ($96 ciclos), $3A fin de nivel (`$C524`), $3B-$3D llaves, $41-$43 peligros (-1 energía por ciclo), $3E bit 7. Las casillas se vacían al recogerlas (`$BFF6` redibuja). [VERIFICADO con recogetest.py, una casilla bajo el jugador 1: $2D +30 puntos, $2E +1, $2F +10 y D07B+1, $30 +10, $31 energía a 100, $32 +15 bit 0, $33 +15 bit 3 y temporizador +$19≈$C0 (la segunda poción $33 activa además el bit 4 = poder doble), $34 D920=$13, $35 +15 bit 2, $36 D98C+1, $37 +15 bit 5, $38 +15 bit 1 y +$18≈$96, $39 +40, $3A fin de nivel, $3E +15 bit 7; $41-$43 restan energía cada ciclo; todas las recogibles desaparecen del mapa; las llaves $3B/$3C/$3D eliminan la puerta $55/$56/$57; al caducar +$18/+$19 se apagan los bits del escudo/poderes.] |
| `$B5DD` | Jugador: movimiento, salto y animación **V** | Interpreta D98A (bit0 arriba/salto, bit1 derecha, bit2 abajo/agachar, bit3 izquierda, bit4 acción de bloque). En suelo: 2 unidades (4 px) por ciclo, en el aire 1 unidad (algo más con el bit 0 de +$15). Usa `$C092` para saber qué lados están libres. El salto sigue la tabla $D922 (-4, -2x6, +2x6, +4x9, +8 terminal) con +$09 como fase (0 = en el suelo). Frames: 0-3 caminar izq., 4-6 giro, 7-$0A caminar der., $0B/$0C agachado. |
| `$B767` | Esfera: física **V** | Mueve la esfera (registro $D3F0). Consulta `$C19C`: E = bits de casillas libres (bit0 arriba, bit1 derecha, bit2 abajo, bit3 izquierda); D=1 si toca la salida ($44) -> `$C524`. Algoritmo: si hay vacío debajo cae 4 px por ciclo (D91F = velocidad vertical); si no, avanza 1 unidad en horizontal en la dirección +$07 (+1/-1); al chocar con una pared invierte la dirección y suena el rebote (descriptor $DCA2). Frames de giro $1A-$23. [VERIFICADO con salidatest.py: al tocar la esfera la casilla $44 se ejecuta $B7BB y el nivel pasa al siguiente.] |
| `$B82C` | Enemigos: despachador por tipo | Recorre los D52C enemigos (registros de 22 bytes desde $D3F8, IY = registro actual, B = contador) y salta a la rutina del tipo (+$08). Los tipos $0C y $0D se procesan aunque x=$FF; el resto se ignora si x=$FF (enemigo inactivo). Si algún jugador tiene el bit 2 de +$15 (matraz verde, casilla $35) los tipos 0 y 1 (caminantes) quedan congelados [L]. Tabla de saltos: 0 $B8AB, 1 $B90D, 2 $B984, 3 $B9A9, 4 $B9CE, 5 y 6 $BA25, 7 $BAE6, 8 $BB37, 9 $BBCD, $0A $BC0F, $0B $BC69, $0C $BCCF, $0D $BCFC, $0E $BD99, $0F-$11 $BDD2, >= $12 $BDFA. Todas terminan en $BE70 (IY += 22 y siguiente enemigo). |
| `$B8AB` | Enemigo tipo 0: caminante en el suelo | Se mueve 1 unidad (2 px) por ciclo en la dirección +$07 (+1 derecha, $FF izquierda) mientras haya casilla libre a ese lado (`$C19C`, bit 1 = derecha, bit 3 = izquierda). No comprueba el suelo: no cae. Al chocar invierte la dirección. Animación cada 4 ciclos (D989=0): derecha frames $24-$25, izquierda $26-$27. VERIFICADO. |
| `$B90D` | Enemigo tipo 1: caminante con gravedad | Si hay vacío debajo (bit 2 de E) cae 4 px por ciclo. Si no, camina como el tipo 0 (1 unidad por ciclo, animación cada 2 ciclos): derecha frames $28-$2B, izquierda $2C-$2F. Al chocar invierte la dirección (el código siempre pone el frame $2C tras girar; el siguiente paso de animación lo corrige). VERIFICADO (cae por el borde de una plataforma). |
| `$B984` | Enemigo tipo 2: burbuja que oscila verticalmente | (+$09,+$0A) = puntero a la tabla de ruta $D99B (pares frame, dy terminados en $FF). Cada ciclo pone el frame y suma dy a y: -4,-4,-4,-2,-2,+2,+2,+4,+4,(+4) = ida y vuelta de 16 px. Al llegar a $FF vuelve a $D99B. VERIFICADO. |
| `$B9A9` | Enemigo tipo 3: burbuja que oscila (amplitud mayor) **V** | Igual que el tipo 2 pero con la tabla $D9B0: pares (frame,dy) en x fijo: dy -4,-4,-4,-2,-2,-2,+2,+2,+2,+4,+4,+4 (12 pasos, frames $30-$31). Es una lectura determinista de la tabla. [VERIFICADO en el simulador (levtest.py, nivel 5): frames $30/$31 y la y oscila entre 112 y 94] |
| `$B9CE` | Enemigo tipo 4: gota | Máquina de estados por frame (+$02): $46 = oculta (cada ciclo 10% de probabilidad de pasar a $32); $32-$34 = formándose (frame+1 cada 4 ciclos); $35 = cayendo (y += 4 por ciclo hasta que no haya vacío debajo, entonces $36); $36 = salpicadura; $37 = reinicio: y = (+$0A) (y original), frame $46. Es inofensiva mientras está oculta ($46). VERIFICADO. |
| `$BA25` | Enemigos tipos 5 y 6: lanzadores de proyectiles | Anima la boca con la tabla $D9C9 (40 entradas, índice +$09; el tipo 6 suma $12 al frame) y, cuando el índice es $0C, dispara: +$07 pasa a ser el número de casillas recorridas por el proyectil. El proyectil es una casilla del mapa ($3C + tipo = $41 para el tipo 5 que viaja a la derecha y $42 para el 6 que viaja a la izquierda): cada ciclo borra la casilla anterior (redibujando el fondo), avanza 8 unidades (1 casilla), y se detiene al salir de pantalla (x >= $6A) o chocar con una casilla no vacía. Las casillas $41/$42 quitan 1 de energía por ciclo al jugador. VERIFICADO el ciclo de animación y el disparo. |
| `$BAE6` | Enemigo tipo 7: disco que rebota en vertical | Frames $47,$48,$49,$48 (tabla $D9F1) cada 2 ciclos. Se mueve 4 px por ciclo: +$07 con bit 7 activo = sube, en caso contrario baja; al toparse con una casilla ocupada invierte. VERIFICADO. |
| `$BB37` | Enemigo tipo 8: criatura que sigue las paredes | Frames de las tablas $D9F5/$DA03 (se elige una al azar al llegar a $FF). Rumbo +$07 (0 arriba, 1 derecha, 2 abajo, 3 izquierda): avanza 1 unidad (horizontal) o 2 px (vertical) por ciclo mientras la casilla esté libre. Si se bloquea gira: +$07 = (+$07 +/-1) AND 3; el sentido de giro (operando autoparcheado en $BBBE) se invierte cada 8 giros (+$0D). VERIFICADO. |
| `$BBCD` | Enemigo tipo 9: proyectil que cruza la pantalla hacia la izquierda | Avanza 4 unidades (8 px) por ciclo a la izquierda y varía y en 4*(+$07)-12 px. Al salir (x<0 o y >= $91) reaparece en el punto de origen (+$0B,+$0A), incrementa +$07 (0-6, abanico de 7 pendientes) y suena $DCA8. VERIFICADO. |
| `$BC0F` | Enemigo tipo $0A: torbellino | Cada ciclo suma a x (-2 + dx) e y (+$07 + dy) un par de la tabla circular $D968 (16 pares, índice +$09 AND $0F): deriva hacia la izquierda describiendo círculos. Al salir de pantalla reaparece en (+$0B,+$0A) con +$07 = aleatorio(11)-5 e índice 5, con sonido. VERIFICADO. |
| `$BC69` | Enemigo tipo $0B: pelota que bota (y generador de anillos en el nivel 50) | Llama a `$BC99` (movimiento). En el nivel D39A=$32 (50) la llama dos veces y, con un 6% de probabilidad por ciclo, deja una casilla de anillo $2F en su posición si está vacía. VERIFICADO el movimiento. |
| `$BC99` | Movimiento de la pelota (tipo $0B) | x += +$07 (rebota en x >= $6A cambiando de signo); y = tabla $DA14[+$09] (arco parabólico $90 -> $32 -> $90 terminado en $FF), +$09 avanza cada ciclo. |
| `$BCCF` | Enemigo tipo $0C: disparo del jefe **V** | Si x < $6A vuela hacia la izquierda 2 unidades por ciclo. En espera (x >= $6A) dispara solo cuando el frame del enemigo 0 ($D3FA, primer segmento del jefe) está en $9A-$9F y ese enemigo está activo (x <> $FF): x = $48-2 = $46, suena $DCA8. Al salir por la izquierda x pasa de 0 a $FE (>= $6A) y vuelve a quedar en espera; la y es la de la cabecera del nivel. [VERIFICADO en el simulador (levtest.py, nivel 60, mundo 6): el disparo aparece en x=$46 justo cuando el primer segmento del jefe llega al frame $9A, avanza 2 unidades por ciclo y al salir queda en espera con x=$FE] |
| `$BCFC` | Enemigo tipo $0D: proyectil en espiral de 8 direcciones | Si sale de pantalla reaparece en (+$0B,+$0A). Cada ciclo se mueve según el contador compartido D07A (0-7): arriba, arriba-derecha, derecha, abajo-derecha, abajo, abajo-izquierda, izquierda, arriba-izquierda (pasos de 4 en x y 8 en y). El contador D07A lo comparten todos los enemigos de este tipo. VERIFICADO. |
| `$BD99` | Enemigo tipo $0E: proyectil diagonal | x -= 2 por ciclo; y += 4*D078 (D078 = 0..3 compartido). Si sale (x<0 o y >= $91) reaparece en (+$0B,+$0A) con sonido. VERIFICADO. |
| `$BDD2` | Enemigos tipos $0F-$11: partes animadas de una criatura de 3 sprites **V** | Cada 2 ciclos toma el frame de la tabla apuntada por (+$09,+$0A) con índice +$07 ($DA3F, $DA68 o $DA91, terminadas en $FF): las tres partes usan frames $5B-$6F; las tres tablas ($DA3F, $DA68, $DA91) tienen 12 pasos de reposo (frame $46 = invisible) y después una secuencia de animación de 28 pasos (p. ej. $5B,$5E,$5E,$5E,$61...). Lectura determinista de tabla. [VERIFICADO en el simulador (levtest.py, nivel 52): las tres partes siguen $5E,$61,$6A,$6D... y el segundo trío espera en $46 (invisible) como indica la tabla] |
| `$BDFA` | Jefes y serpientes (tipos >= $12) **V** | Un registro "cabeza" gobierna a (+$0D) registros siguientes: toma el frame de una tabla de animación (+$09,+$0A / índice +$07, cada 2 ciclos) y asigna a los segmentos consecutivos los frames f+1, f+2, ... (escribiendo en +$18 de los registros siguientes) y descuenta esos registros del contador del bucle (no se despachan por separado). En el mundo 4 (D98B=4) ademas desplaza 9 registros en vertical con la tabla de ondas $DB7A. Las tablas de animación de cada jefe (por mundo, apuntadas por los bytes +6/+7 de $DABA: $DAFA, $DB17, $DB2C, $DB4F, -, $DBA5, -, $DC19) contienen el frame de la cabeza (valores $70-$AF = sprites propios del mundo, en grupos de 9 consecutivos, uno por segmento); el segmento k usa el frame cabeza+k y su posición (x,y) es fija, la de la cabecera del nivel. En el mundo 3 los 8 segmentos forman dos bloques 2x2 de 32x32 px (las mandíbulas) superpuestos a la imagen grande. [VERIFICADO en el simulador (bosstest.py, mundos 1-8): todos los jefes cargan con la vida de $DC3B (24, 32, $FF, $FF, $FF, 48, 0, 64), animan sus segmentos según su tabla; el orbe baja la vida en los mundos 1, 2 y 8; en los mundos 3-5 ($FF) no se les puede dañar. Con la vida del jefe del mundo 8 a 0 se ejecuta `$AD45` (finaltest.py). Ensamblado en assets/jefes_animados] |
| `$BE7B` | Poner / quitar bloque **V** | Se ejecuta cuando el bit 4 de D98A está activo (el jugador SOLTÓ la tecla de bloque; ver `$CCB5`). Casilla destino: x AND $F8, y AND $F0. Mirando a la derecha (+$07=1): se rechaza si x >= $62, destino +8 (otro +8 si x AND 7 >= 2); a la izquierda: se rechaza si x < 8, destino -8. Con frame >= $0B (agachado) la fila destino es la inferior (y+16; se rechaza si y=$90). Se rechaza si el bloque solaparía con la esfera, con el otro jugador o con un enemigo. Casilla vacía -> $45 (animación de creación $45,$46,$47,$48 cada ~3 interrupciones; $48 = bloque rojo del jugador). Casilla $48 -> $49 (animación de destrucción $49-$4C, luego $00). Casillas especiales $2E y $58-$5A tienen efectos propios. |
| `$BFBA` | Prueba de solapamiento **V** | Entradas: HL = (x,y) de una entidad, DE = (x,y) de otra. Z=0 (NZ) si /dx/ < 8 unidades (16 px) y /dy/ < 16 px. |
| `$BFD7` | Solapamiento con enemigos | Compara (E,D) con todos los enemigos activos (x <> $FF). Devuelve Z=0 si hay solapamiento, con IX apuntando al enemigo. |
| `$BFF6` | Redibujar una casilla | Redibuja la casilla de la dirección de mapa DE con el código A en el búfer de pantalla ($DF72) y los atributos ($F1D4). |
| `$C037` | Dirección de mapa de una posición **V** | Convierte (x,y) de la entidad en la dirección dentro del mapa $DE5A: índice = (y>>4)*14 + (x>>3). |
| `$C092` | Colisión del jugador con las casillas | Como `$C19C` pero para el jugador: las casillas >= $44 le bloquean, mientras que la esfera es bloqueada por todas las >= $2D excepto la $43. |
| `$C19C` | Colisión de la esfera/enemigos con las casillas **V** | Devuelve en E los bits de casillas libres (0 arriba, 1 derecha, 2 abajo, 3 izquierda) y D=1 si toca la salida $44: a los lados siempre; encima sólo si la esfera SUBE (D91F negativo) **V** (`ultimos.py`). |
| `$C2DC` | Dibujar entidades (guardar fondo y pintar sprites) | Para cada entidad (enemigos, esfera, J1, orbe 1, J2 con frames +13, orbe 2) llama a `$C384`. |
| `$C338` | Borrar entidades (restaurar fondo) | Restaura el fondo guardado de cada entidad (en orden inverso) mediante `$C45D`. |
| `$C384` | Dibujar un sprite 16x16 con máscara | Entrada: IX = registro de entidad. Si x >= $6A o y >= $91 no se dibuja. Sprite = $6100 + frame*32. Genera la máscara con las tablas $5B00/$5C00, desplaza el sprite según x AND 3 (cuatro posiciones de subpíxel dentro del byte), calcula la dirección en el búfer ($DF72, 29 bytes por línea) y la guarda en +5/+6, y mezcla con AND/OR. El fondo original se guarda en el búfer de la entidad (+3/+4). |
| `$C45D` | Restaurar el fondo de una entidad |  |
| `$C488` | Mezclar un bloque con máscara en el búfer | Rutina genérica: C=ancho en bytes, B=alto, DE=datos (máscara,dato alternados), HL=destino. |
| `$C49F` | Limpiar el área de juego | Pone a 0 las 160 líneas del búfer y atributos $47 (blanco sobre negro). |
| `$C4D5` | Interrupción: sonido **V** | Rutina de interrupción (IM 2, vía $FDFD). Si hay un descriptor de sonido activo ($D076 <> 0) toca un tramo de onda cuadrada con el altavoz (OUT ($FE), bit 4). Descriptor de 6 bytes: +0 periodo, +1 número de ciclos, +2 incremento del periodo por interrupción, +3 interrupciones restantes, +4 periodo de reinicio, +5 cuenta de reinicio. Al terminar pone $D076=0. |
| `$C524` | Nivel completado **V** | Se llega al tocar la esfera la salida $44, al recoger la casilla $3A o al conseguir 50 anillos. NO suma bonus (corrección: no hay puntuación aquí): restaura el intercambio de casillas del mundo 7 si el nivel es $46, avanza D39A (con $4E salta el $4F: $4E+2=$50; en consecuencia el nivel 79 NO EXISTE, ni tampoco el 81-89: los datos de esas posiciones son relleno; verificado con colortest.py), y con D39A=$51 va a `$AD45` (fin del juego). Pone D39B a 0 y vuelve al bucle principal `$AAC7` (que carga el nivel). [VERIFICADO con niveltest.py (la carga de cinta se simula en $D01F): 3->4; 9->10 carga el mundo 1 de cinta; 69->70 carga el mundo 7 y hace el intercambio de las casillas $18-$2B (bitmaps de $6F00, atributos = F79B); 70->71 restaura las casillas originales; 78->80 (carga el mundo 8); 80->81 llega a $AD45; con D39B=$57 avanza 2 niveles y con $42 uno.] |
| `$C563` | Cargar nivel **V** | Copia el mapa del nivel (140 bytes = 14x10 casillas) al mapa de trabajo $DE5A: mapas de 1 jugador en $8A60+140*n y de 2 jugadores en $8FD8+140*n (n = D39A - 10*D98B). Los niveles de 1 y 2 jugadores son DISTINTOS. Si el nivel pertenece a otro mundo (D98B <> D39A/10) llama a `$CFB3` para cargarlo de la cinta. Copia 140 bytes de capa de fondo ($4B00 + desplazamiento leído de la cabecera) a $DEE6. Después interpreta la cabecera del nivel (`$C65B`). Niveles especiales: D39B=$42 y otros usan los mapas de $9550 y $95DC y las cabeceras 20 y 21 de la tabla. |
| `$C64E` | Saltar cabeceras de nivel | Avanza HL por B registros de cabecera (8 + 1 + 4*enemigos bytes cada uno). |
| `$C65B` | Interpretar la cabecera del nivel **V** | En los mundos 1-8 el primer nivel (D39A múltiplo de 10) es un nivel de jefe/guardián (ver `$C9F5`). Registro: fondo (2 bytes), esfera (x,y), J1 (x,y), J2 (x,y, $FFFF si 1 jugador), nº de enemigos y, por enemigo, x,y,tipo,frame. Inicializa los registros de esfera ($D3F0), jugadores ($D3A7/$D3C4) y enemigos ($D3F8, 22 bytes) con sus estados iniciales y rutas. Dibuja el marcador (reintentos, energía, nivel, puntuación). |
| `$C9D7` | Pintar un icono de 2 columnas | Copia filas de 2 bytes del icono HL a la pantalla DE, bajando de línea correctamente (cálculo de dirección de pantalla del Spectrum). |
| `$C9F5` | Dibujar el nivel completo | Dibuja el nivel completo: primero la CAPA DE FONDO ($DEE6, papel pintado 14x10 con `$BFF6`) y encima el MAPA ($DE5A, con `$CB2D`) mediante `$CAFE`; en el nivel $50 desplaza antes la fila de fondo. Al final, si hay jefe activo ($DC3A<>0) dibuja el jefe del mundo (tabla $DABA, 8 bytes por mundo) y decoraciones propias de los mundos 3, 4 y 8. |
| `$CAED` | Copiar filas de gráfico |  |
| `$CAFE` | Dibujar el mapa de casillas | Recorre IX (10 filas x 14 columnas = 140 bytes) y para cada código llama a la rutina cuyo puntero está parcheado en $CB13 (`$BFF6` para la capa de fondo, `$CB2D` para el mapa del nivel). |
| `$CB2D` | Dibujar una casilla 16x16 | A = código de casilla del mapa. Los códigos 0, $41-$43 y $4C se dibujan con máscara en `$CB40` (el resto se delega en `$BFF6`, sin máscara, que sobrescribe todo). Gráfico de casilla = $9B00 + 36*código (32 bytes de bitmap, 16 filas x 2 bytes, + 4 bytes de atributos). |
| `$CB7D` | Efecto de pantalla: fundido a negro | Copia los atributos actuales ($5800, 768 bytes) a $F192 y durante 7 pasos (una interrupción por paso con `$CCB2`) resta 1 al color de tinta y 1 al de papel de cada atributo hasta llegar a 0: la pantalla se apaga a negro. Parchea el byte $CD93 con $C9 (RET) para que `$CD43` deje de copiar atributos mientras dura el efecto (en $CC04/$CCAE se restaura a $01). |
| `$CBBA` | Efecto de pantalla: aparecer | Inverso de `$CB7D`: durante 8 pasos acerca cada atributo de la pantalla al guardado en $F192 (primero la tinta/papel poco a poco: +1 en brillo de cada componente hasta igualar). Al terminar restaura $CD93 a $01. |
| `$CC0A` | Efecto de pantalla: fundido rápido | Fundido rápido a blanco: silencia el sonido ($D076=0), parchea $CD93 y sube 7 pasos tinta y papel hasta 7 (blanco), cambiando el borde con OUT ($FE) en cada paso. Se usa al morir un jefe y al terminar el nivel. |
| `$CC5A` | Efecto de pantalla: aparición con borde | Aparición desde blanco a los atributos guardados en $F192, con borde decreciente (OUT ($FE) con el contador); restaura $CD93=$01. |
| `$CCB2` | Esperar una interrupción (EI + HALT) |  |
| `$CCB5` | Leer los controles del jugador en curso **V** | Construye en E el byte de entrada y lo guarda en D98A. Bits: 0 arriba, 1 derecha, 2 abajo, 3 izquierda, 4 acción de bloque. Las 5 teclas de cada jugador están en su registro (+$0F..+$13). Con Kempston (D39E bit 0 y J1) se lee el puerto $1F. La tecla de bloque (+$13) funciona por flanco de bajada: mientras está pulsada el contador +$14 sube hasta $40; al soltarla, si el contador es > 0, se activa el bit 4 y el contador vuelve a 0. [VERIFICADO con kempstontest.py: Kempston bit0 = derecha, bit1 = izquierda, bit2 = abajo, bit3 = arriba, bit4 = disparo (acción de bloque); sólo lo usa el jugador 1.] |
| `$CD43` | Volcar el búfer a pantalla | Copia las 160 líneas del búfer ($DF72, 28 bytes por línea) a la pantalla con 28 LDI por línea y copia los atributos de $F192 a $5800 (ver CD93). |
| `$CD9F` | Número aleatorio | Entrada A = máximo; salida A = valor 0..A-1 con un generador congruencial con semilla $D085. |
| `$CDC9` | Auxiliar del generador aleatorio |  |
| `$CDD3` | Probar una tecla **V** | Entrada A = código de tecla = 8*(4-bit) + (7-semifila). Devuelve Z (A=0) si la tecla está pulsada. Semifilas: 0 $FE (CAPS..V), 1 $FD (A..G), 2 $FB (Q..T), 3 $F7 (1..5), 4 $EF (0..6), 5 $DF (P..Y), 6 $BF (ENTER..H), 7 $7F (ESPACIO..B). |
| `$CDF5` | Cambiar la energía **V** | Entrada C = incremento con signo. Sin efecto si el escudo está activo (bit 1 de +$15). Energía D3EF limitada entre 0 y 100; actualiza el tono del sonido de energía ($DC8A) y el marcador (`$CE2D`). |
| `$CE5C` | Marcador de poder mágico | Dibuja la barra de temporizador del poder mágico (+$19) del jugador en curso en $4080 (J1) o $40C0 (J2). |
| `$CE98` | Imprimir el número de nivel (2 dígitos) |  |
| `$CEC1` | Imprimir la puntuación (5 dígitos) |  |
| `$CEFB` | Dividir DE y escribir un dígito ASCII |  |
| `$CF0C` | Imprimir un texto descriptor | Interpreta una cadena en IX: $00 x y = posición (columna = (x-8)/2, fila = y); $01 a = atributo; $FF = fin; otro = carácter a pintar con `$CF82`. |
| `$CF6F` | Pintar atributo en la posición actual |  |
| `$CF82` | Dibujar un carácter 8x8 | Fuente en $F592 (ASCII-32 * 8 bytes). |
| `$CFB3` | Cargar un mundo desde cinta **V** | Muestra SEARCHING FOR n, carga con la rutina de la ROM $0562 (LD-BYTES) primero una cabecera de 17 bytes ($D031: tipo, nombre de 10 caracteres, longitud, dirección de inicio) y, si el nombre es el del mundo esperado (D98B+'0'), el bloque de datos en la dirección de la cabecera. VERIFICADO con la cinta TZX: cada mundo ('0'..'8') es un bloque estándar de 11264 bytes que se carga en $6F00-$9AFF; los nombres son un carácter ASCII (D98B+$30). [VERIFICADO con tapetest.py usando la ROM real: la señal EAR se genera desde el TZX; con una cinta que empieza por un bloque de otro mundo, el juego lo rechaza (compara el nombre de la cabecera con D98B+$30) y carga el mundo pedido; el contenido de $6F00 coincide byte a byte con el bloque de la cinta (11264 bytes).] |
| `$D01F` | Llamar a LD-BYTES de la ROM |  |

---

## 12. Guía de modificación (mods)

Todo lo que sigue se refiere a la versión analizada (cinta `Spherical_Erbe.tzx`). Cada receta lleva su grado de certeza: **[V]** = probada aplicando el parche y ejecutando el juego en el simulador; **[L]** = deducida de leer el código, **sin probar** (pruébala antes de fiarte).

### 12.1 Tres formas de aplicar un cambio

| Vía | Cuándo | Cómo |
|---|---|---|
| **A. Poke en un snapshot** | Experimentar rápido | Escribe el byte en la RAM del `.sna`/`.z80` con tu emulador (ZEsarUX, Fuse…). No requiere herramientas. |
| **B. Parchear la cinta TZX** | Obtener un juego modificado que cargue desde cinta | `python3 -I parchear_tzx.py entrada.tzx salida.tzx NOMBRE DIRECCION_HEX BYTES_HEX`. `NOMBRE` es el del bloque CODE (`smc` para el juego en `$6100-$F7FF`; `0`…`8` para los mundos en `$6F00-$9AFF`); `DIRECCION` es la dirección de memoria del juego, no el desplazamiento; el script recalcula el byte de paridad del bloque. Ejemplo: `parchear_tzx.py in.tzx out.tzx smc AAA6 02`. [V] (comprobado cargando la cinta parcheada con la ROM real, `tapetest.py`). |
| **C. Editar el `.skool` y reensamblar** | Cambios grandes (código nuevo, reubicar datos) | Edita `spherical_anotado.skool`, ejecuta `skool2bin.py` (§2.3; el original reensambla idéntico byte a byte) y vuelca el resultado a `$5B00` de un snapshot o sobre el bloque `smc`. |

Advertencia sobre la cinta: el cargador carga los 9 mundos con `LD-BYTES` y comprueba la paridad; si editas con un editor hexadecimal tienes que recalcularla (XOR de todos los bytes del bloque incluida la bandera). Hay que parchear **el mundo correcto**: el bloque `0` es el residente, el bloque `N` se carga al llegar al nivel `10·N`.

### 12.2 Recetas probadas [V]

Resultados obtenidos con `modtest.py` sobre el snapshot del menú (pulsando `1` para empezar):

| Qué | Dirección (byte a cambiar) | Valor original | Resultado medido |
|---|---|---|---|
| **Reintentos iniciales** | `$AAA6` (operando de `LD A,$04` en `$AAA5`) | `$04` | 2 → 2 reintentos; 3 → 3 reintentos. **Rango válido 1–4** (ver gotcha 12.5). |
| **Energía inicial** | `$AAAB` (operando de `LD A,$64` en `$AAAA`) | `$64` (100) | `$32` → energía 50 al empezar. Máximo útil: 100 (la barra tiene 50 segmentos = energía/2). |
| **Duración del escudo** | `$B44A` (operando de `LD (IY+$18),$96` en `$B447`) | `$96` (150) | `$FF` → el contador `+$18` del jugador queda a `$FF` al recoger la casilla `$38`. |
| **Duración del poder del orbe** | `$B4DD` (operando de `LD (IY+$19),$C0` en `$B4DA`) | `$C0` (192) | `$FF` → contador `+$19` = `$FF` al recoger la casilla `$33`. |
| **Limitador de velocidad** | trampolín en `$AB78` + `$F7C0` (abajo) | — | 24,1 → 18,0 (1 espera) → 13,2 ciclos/s (2 esperas). |
| **Editar un nivel** | 1P: `$8A60 + 140·n`; 2P: `$8FD8 + 140·n` (n = 0…9 dentro del mundo) | — | Parche de un byte en el mundo 5 cargado desde cinta: la casilla cambia (`tapetest.py`). Códigos de casilla en §8.4. |

#### Limitador de velocidad (la receta más útil)

El bucle principal **no se sincroniza con la interrupción** (§6.3): la velocidad depende de los T-estados de cada ciclo y del contenido del nivel, así que en un emulador a velocidad real puede ir demasiado rápido o variar entre niveles. La solución es meter una espera `EI; HALT` por ciclo. Sitio libre: `$F7BC-$F7FF` (dentro del bloque `smc`, sin usar).

```
; en $AB78 (9 bytes originales: 3A 89 D9 3C E6 03 32 89 D9 = LD A,($D989) / INC A / AND 3 / LD ($D989),A)
AB78  C3 C0 F7 00 00 00 00 00 00        ; JP $F7C0 + 6 NOP

; en $F7C0
F7C0  CD B2 CC                          ; CALL $CCB2  (EI + HALT; repetir 1, 2... veces)
F7C3  3A 89 D9 3C E6 03 32 89 D9        ; las 9 instrucciones originales
F7CC  C3 81 AB                          ; JP $AB81  (continúa donde seguía el código)
```

Cada `CALL $CCB2` extra baja el ritmo en una interrupción (20 ms). Se midió: sin parche 24,1 ciclos/s en el primer nivel; una espera 18,0; dos esperas 13,2. **La velocidad de la máquina real no se ha podido medir** (§13.4): ajusta el número de esperas a ojo.

### 12.3 Recetas por lectura del código [L]

* **Daño por contacto.** Los tres puntos que llaman a `CDF5` (restar energía) cargan `C=$FF` (= −1 con signo): `$AB1A` (J1 toca enemigo), `$AB53` (J2) y `$B3C6` (casilla peligrosa). El operando está en `$AB1B`, `$AB54`, `$B3C7`. `$FE` sería −2, etc. `CDF5` satura a 0 y a 100. Los tres son aplicados **cada ciclo** mientras dura el contacto, así que −1 es poco por ciclo pero mucho por segundo.
* **Daño con el escudo o con el fotograma `$46`**: se evita saltándose el `CALL CDF5` (`JP Z,$AB1F`/`$AB58`); es la lógica de "inmunidad", no un valor.
* **Nivel de inicio.** Las claves (§10.12) llevan en la tabla `$D2E9` (1P, 5 entradas) y `$D2FD` (2P, 6 entradas) entradas de 4 bytes; el segundo byte es el nivel al que lleva la clave. Cambiarlo hace que, p. ej., RADAGAST salte a otro nivel. El primer byte es el nivel del pergamino que muestra la clave. No se ha probado a cambiar ninguno.
* **Reloj de arena.** El valor `$14` cargado en `$B461` (`LD A,$14`) es el valor del contador `D920` al recoger la casilla `$34`.
* **Salto.** La tabla `$D922` (desplazamientos verticales por fase: −4, −2×6, +2×6, +4×9, +8) fija la altura y forma del salto. Cambiar valores cambia la altura; la longitud de la tabla la marca su terminador (compruébalo en el `.skool` antes de alargarla).
* **Controles.** Las tablas `$D1EF`, `$D210`, `$D231`, `$D252` (una por esquema; `D39E` elige) se copian a los registros de jugador `$D3B6`/`$D3D3`. Código de tecla = `8·(4−bit) + (7−semifila)` (§5.4). Puedes reasignar teclas cambiando esos bytes.
* **Vida de los jefes.** `$DC3B+mundo`: 0, 24, 32, `$FF`, `$FF`, `$FF`, 48, 0, 64 (`$FF` = inmune al orbe, §10.9).

### 12.4 Código automodificable (cuidado al reubicar)

El juego se reescribe a sí mismo en cinco sitios más el dígito de un texto. Si cambias esas instrucciones o mueves el código, estas escrituras acabarán en otra parte:

| Dirección | Qué se sobrescribe |
|---|---|
| `$CD93` | primer byte de `LD BC,$0300` en `CD43` (copia de atributos): `CB7F`/`CC06` lo cambian a `$C9` (`RET`) durante los fundidos y luego lo restauran a `$01` |
| `$CEBE` | opcode del `JP $CF0C`: se escribe desde `$C995` y `$C9A0` |
| `$CB13` | puntero (2 B) de un `CALL` en el dibujo de capas; `CA29`/`CA36` lo apuntan a la rutina gráfica que toque (p. ej. `BFF6` para la capa de fondo) |
| `$BBBE` | operando de `LD A,$FF` en la IA del enemigo tipo 8 (sigue paredes): `BBB5-BBBA` lo niega con `NEG` para invertir el sentido de giro |
| `$CA83` | `LD BC,$450C` de la carga del escenario del mundo 3; el `.skool` lo anota como "parche" (mira `CA78-CA86` antes de tocarlo) |
| `$D0C0` | dígito del texto "PLAYER n" (`AD13`/`AD26` escriben `1` o `2`) |

(Las advertencias de `skool2bin` "Address … replaced in unsubbed LD operation" señalan estos sitios. La interpretación exacta de cada operando está en los comentarios del `.skool`.)

### 12.5 Límites y trampas conocidas

* **Reintentos > 4 rompen el juego** [V]: el dibujo de los reintentos en el marcador (`$C96E`, repite `4−reintentos` con signo) desborda y el programa salta a la ROM (`NEW`). Con 5 y 9 se obtuvo reintentos = 0, energía = 0. Si quieres más de 4 reintentos hay que reescribir esa rutina.
* **Máximo 14 enemigos** por nivel: los registros de 22 B empiezan en `$D3F8` y `$D52C` (contador) está justo después.
* **Casillas: 91 tipos** (`$9B00 + 36·código`, hasta `$A7CB`; el código empieza en `$A7CC`). No hay hueco para añadir más sin reubicar.
* **Espacio libre**: `$F7BC-$F7FF` (68 B) dentro del bloque de cinta. Para más, hay que alargar la cinta o reubicar.
* **Bug de recogida** (`$B38D`): `B` queda a 1, así que solo se examina la fila de casillas bajo el jugador, no las dos. Es un fallo del original; arreglarlo cambia el comportamiento (y puede romper niveles diseñados con él).
* **Numeración de niveles**: tras el 78 se pasa al 80 y al llegar al 81 termina el juego; el 79 y el 81-89 no existen (§6.4).

### 12.6 Ideas de mods realistas (sin tocar la arquitectura)

* Reducir o ampliar la energía o los reintentos iniciales ([V]).
* Limitar la velocidad con el trampolín ([V]).
* Alargar el escudo o el orbe poniendo su duración a `$FF` (el contador se carga con `$FF` [V]; cuánto tarda en agotarse en juego no se ha medido).
* Rediseñar niveles editando los mapas de 140 B del mundo ([V] la vía de parcheo; el contenido de cada código de casilla en §8.4).
* Cambiar los sprites: están en `$6100 + 32·frame` (bloque `smc`) y en el principio de cada mundo; **atención a la silueta**: la máscara se calcula a partir de las tablas `$5B00/$5C00` del propio gráfico (§9.1), así que basta con editar el gráfico; no hay máscara aparte (salvo en las imágenes grandes de jefe, que van en pares máscara/dato).

---

## 13. Verificación, correcciones e incógnitas

### 13.1 Qué está verificado y cómo

| Afirmación | Método | Certeza |
|---|---|---|
| Todo el código (4689 instrucciones) | Ejecutado por alguna prueba en el simulador (`cobertura.md`). Salvedades: estados forzados en algunas ramas y `$B8A8` forzado por PC | **V** con salvedades |
| El `.skool` reensambla idéntico | `skool2bin` vs RAM `$5B00-$FFFF`: 42 240 B, 0 diferencias | **V** |
| Fórmula de máscara | `verificar_mascara.py`: 370/370 sprites contra `$C384` | **V** |
| Sprites completos | Dominio de frames alcanzables + cierre de cabeceras + comparación de píxeles (`completitud_sprites.py`) | **V** |
| Carga de mundos desde cinta | ROM real + señal EAR del TZX (`tapetest.py`) | **V** |
| Física de la esfera, bloques, orbes, poción, energía, enemigos | `blocktest`, `orbtest`, `potiontest`, `enemytest`… (§2.4) | **V** |
| Tabla de salto `$D922`, velocidades | Lectura + medida | **L**/**V** |
| Velocidad en máquina real | **No medida** | **S** |

### 13.2 Código muerto

* `$B8A8` es **inalcanzable**: se probó la cadena de despacho con los 256 valores del tipo de enemigo.
* `$CE03-$CE0A` (rama positiva de `CDF5`: sumar energía) no tiene llamadores reales: los tres llamadores usan `C=$FF`. `$CE12` (saturar a 0) sí se alcanza.

### 13.3 Correcciones de análisis (para no repetir los errores)

* Se llegó a afirmar que `$CE03-$CE12` era código muerto completo; solo lo es `$CE03-$CE0A`.
* `$C19C`: la salida `$44` se activa **desde arriba solo si la esfera sube** (bit 7 de `D91F` = 1); un comentario anterior tenía la polaridad al revés.
* Los fotogramas `$45` y `$FF` del orbe son valores residuales del registro, no gráficos (`orbe45.py`).
* Los roles de enemigo medidos con estados sintéticos (`pociontest2`) contaminaron el análisis de los tipos 04/09; se filtraron.
* **Nombre de `$D2E8`**: en las primeras versiones de este análisis se llamó «vidas», porque el HUD dibuja iconos y el contador empieza en 4. Es un error de nombre: el juego no tiene vidas (solo la barra de energía; a 0, Game Over). El contador solo baja al pulsar R (Retry), así que se renombró «reintentos». Lo que hace el código no cambia; lo que representan exactamente los iconos del HUD no se ha contrastado visualmente [S].
* La **energía 0** lleva a Game Over directo; los reintentos solo los gasta la tecla `R`. 

### 13.4 Incógnitas y límites

* **Velocidad en hardware real.** El bucle principal no tiene `HALT`; la velocidad se estimó con un modelo de T-estados y contención (≈20 ciclos/s en 1P, ≈19 en 2P, contención ≈0,7 %). Es un modelo, no una medición. Medir de verdad exige hardware real o un emulador con precisión de ciclo y contención de memoria completa.
* `$B8A8` y `$CE03` son restos de código no alcanzable: no se pueden "observar" en juego.
* **Datos no identificados**: `$98AA-$9AFF` de cada mundo.
* Comportamientos exactos de algunos enemigos con estados raros (se probaron con estados forzados para cubrir las ramas, no con partidas reales).

---

## 14. Apéndices

### A. Mapa de la cinta
Ver §3. Bloques: `Spherical` (BASIC), `fadscr` (SCREEN$), `smc` (`$6100`, 38 656 B), `border` (SCREEN$), `0`…`8` (`$6F00`, 11 264 B cada uno).

### B. Cómo empezar a analizar desde cero con estas herramientas

1. Obtén tu propia copia (cinta o snapshot) y haz un snapshot en el menú.
2. `sna2skool.py -H -c spherical_anotado.ctl tu.sna > juego.skool` (§1) para obtener el código comentado.
3. Abre `indice_rutinas.md`/§11 y los mapas de §4 y §7 y lee primero `$AAC7` (bucle principal), después `$B767` (esfera) y `$BE7B` (bloques).
4. Para probar una hipótesis, carga el snapshot en el simulador de SkoolKit con `keytrace.py` (inyecta teclas, cobertura, fotogramas dibujados).
5. Para cambiar algo, §12.

### C. Glosario rápido de convenciones
* `IX`/`IY` apuntan a registros (jugador: `IY`; enemigo: `IY` en el despachador, `IX` en colisiones). Registro de jugador de 29 B (§7.1); enemigo de 22 B (§7.3).
* `D91D` número de jugadores; `D91E` jugador en curso (1P usa solo J1; en 2P los dos se procesan cada ciclo).
* Mapa de 140 B por nivel (14 columnas × 10 filas; índice = (y>>4)·14 + x/8, §8).
* `$FF` en x = enemigo inactivo.

### D. Aviso final
Este documento describe el funcionamiento del código; **no contiene el código, ni los gráficos, ni los niveles originales**. Quien lo use debe partir de su propia copia legítima. Los derechos de *Spherical* pertenecen a sus autores (Rainbow Arts / Electronic Zoo). Los datos extraídos (sprites, mapas) no deben redistribuirse; las direcciones, estructuras y descripciones sí se pueden compartir como documentación.
