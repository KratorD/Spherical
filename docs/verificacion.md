# Estado de verificación del análisis de Spherical

Leyenda: **[S]** comprobado ejecutando el código en el simulador de SkoolKit; **[C]** comprobado contra la cinta/snapshots (datos); **[L]** leído en el código y consistente, sin ejecutar; **[?]** suposición.
Ninguna de estas comprobaciones sustituye a jugar el original en un emulador: lo marcado [S] es lo que hace EL CÓDIGO, que es lo que importa para reproducirlo 1:1.

## Mecánicas
| Mecánica | Estado | Prueba |
|---|---|---|
| Física de la esfera: caer 4 px/ciclo, rodar 1 unidad, rebote en paredes | [S] | `esfera`, `spherelog.py` |
| Salto del jugador: tabla `$D922` | [S] + [L] | `blocktest.py`, código `B5DD` |
| Colocar/quitar bloque (incl. agachado), animación 45-48 / 49-4C | [S] | `blocktest.py` |
| Bloque al SOLTAR la tecla | [S] | simulación |
| Poción con ENTER | [S] | `potiontest.py` |
| Orbe orbitando (poder 1) | [S] | `potiontest.py` |
| Lanzamiento del orbe: poder doble + mantener la tecla de bloque ≥16 ciclos (se lanza mientras se mantiene) | [S] | `orbtest.py` (1) |
| Reloj de arena `$34`: congela la esfera | [S] | `orbtest.py` (2) |
| Casilla `$3E`: impide crear bloques | [S] | `orbtest.py` (3) |
| Matraz verde `$35`: congela enemigos 0/1 | [S] | `orbtest.py` (4) |
| Frasco azul `$37`: bloques rojos aleatorios | [S] | `orbtest.py` (5) |
| Flechas de diamante `$58/$59/$5A` (acción de bloque sobre ellas) | [S] | `orbtest.py` (6) |
| Acción de bloque sobre `$2E` -> sala de bonus (`D39B=$42`) | [S] | `orbtest.py` (7) |
| Jefes de los mundos 1-8: vida inicial por mundo, animación de segmentos | [S] | `bosstest.py` |
| Daño del orbe al jefe (mundos 1, 2, 8) y vida $FF (mundos 3-5, inmunes al orbe) | [S] | `bosstest.py` |
| Fin del juego: vida del jefe 8 a 0 -> pantalla final `$AD45` | [S] | `finaltest.py` |
| Enemigos tipos 0,1,2,4,5,6,7,8,9,0A,0B,0D,0E | [S] | `enemytest.py` |
| Enemigos tipos 3, 0C (disparo del jefe), 0F-11 | [S] | `levtest.py` |
| Copa `$40` (D39B=$57) y pergamino `$3F` (muestra la clave en los niveles 12, 21, 41, 61, 75) | [S] | `casillatest.py` |
| Menú: teclas 1-7 (cada una llega a su rutina: `A96C, A971, A976, A983, AA02, AA57, AA5D`) | [S] | `menuteclas.py` |
| Claves: RADAGAST... -> niveles 9/19/39/59/75, 1P y 2P; ILLUMINATUS = invencible | [S] | `clavetest.py` |
| Carga de mundos por cinta | [C] | `CFB3` + TZX |
| Inserción en la tabla de mejores puntuaciones (5000,3000,1000,500,100 + 1234 -> 5000,3000,1234,1000,500) | [S] | `menuteclas.py` |
| Entrada de texto `AE6B`: teclear S K Y, borrar (tecla 0), F, ENTER -> `SKF` | [S] | `tecleotest.py` |
| Recogida de casillas `B38D` (puntos, energía, bits de +$15, temporizadores, poción doble, llaves y puertas, caducidad de escudo y poderes, peligros) | [S] | `recogetest.py` |
| Joystick Kempston: bit0 derecha, bit1 izquierda, bit2 abajo, bit3 arriba, bit4 disparo | [S] | `kempstontest.py` |
| Teclas especiales: M/N (con ILLUMINATUS) siguiente/anterior nivel, H pausa, T cancela el reloj de arena | [S] | `teclasjuego.py` |
| Paso de nivel `C524` -> carga `C563` -> carga de mundo `CFB3` (carga de cinta simulada), intercambio de casillas al entrar en el 70 y restauración al salir, 78 -> 80, 80 -> fin | [S] | `niveltest.py` |
| Pantalla final, tabla de puntuaciones y entrada del nombre tras acabar el juego | [S] | `niveltest.py final` |
| Orbe lanzado: trayectoria con rebotes en paredes/techo/suelo; orbe orbitando mata a un caminante | [S] | `orbebounce.py` |
| Cobertura de ejecución del código: 4675 de 4689 instrucciones (99,7 %) ejecutadas por alguna prueba; las 14 restantes (dos trozos de código muerto demostrable y cinco bordes de 1-3 instrucciones) están listadas y explicadas en `cobertura.md` | [S] | `cobertura.py`, `framesweep.py` |
| Carga de mundos por cinta con la ROM real: la señal EAR se genera desde el TZX; se rechaza un bloque de otro mundo, se detecta un error de paridad y se repite la carga ($D019 -> $CFB3), y al final `$6F00` coincide byte a byte con el bloque (11264 bytes) | [S] | `tapetest.py` (con y sin `CORRUPT=1`) |
| Menú: 2 -> D91D=2; 3 -> D39B=$54 (entrenamiento); 4 -> entrada de clave; 5 -> D39E 2->0; 6 -> mejores puntuaciones y vuelta; 7 -> F79B 1<->5; detección de Kempston en el arranque (D988=1) | [S] | `menuseguir.py`, `menuyfin.py` |
| Fin de partida en el nivel 70 restaura las casillas ($AD37); puntuación baja no entra en la tabla ($ADCA); fundidos con papel distinto de 0 | [S] | `menuyfin.py`, `puntuacionbaja.py`, `fundidotest.py` |
| Poción: mata tipos 0-3 y 5-8, no el 4 ni 9+; borra $41/$42 y no $43 | [S] | `pociontest2.py` |
| La esfera toca la salida $44 y pasa de nivel (`$B7BB`); 50 anillos acaban el nivel (`$B405`); pergamino con 2 jugadores | [S] | `salidatest.py`, `varios.py` |
| Recuperar el orbe lanzado (segunda pulsación larga); poder del jugador 2; jefe del nivel 60: sólo daña con fotograma $88-$9F | [S] | `varios.py`, `jefe60test.py` |
| Dibujado de nivel `C9F5`: atributos y píxeles del búfer = casillas del renderizador (20160 casillas, mundos 0-8, 1P y 2P, niveles no-jefe) | [S] | `colortest.py` |
| Velocidad de ciclo en el simulador (sin contención): ≈20 ciclos/s en 1P, ≈19 en 2P (un ciclo ≈ 2,5 interrupciones de 50 Hz) | [S] | `velocidad.py` |
| Velocidad CON un modelo de contención de memoria del 48K (accesos a $4000-$7FFF retrasados 6,5,4,3,2,1,0,0 T en las 192 líneas de pantalla): 1P ≈ 20,2 ciclos/s (173523 T por ciclo), 2P ≈ 18,7 ciclos/s (187421 T); la contención cuesta ≈ 0,7 % | [S] modelo | `velocidad_cont.py` (aproximado: no modela contención de puertos y usa el T del inicio de cada instrucción) |
| Velocidad medida en un Spectrum real | [?] no medida; sólo puede cerrarla hardware o un emulador de ciclo exacto | — |

## Datos
| Dato | Estado |
|---|---|
| Niveles 0-78 y 80 (mapas, fondos, cabeceras 1P/2P) | [C] coinciden con la memoria viva |
| Los niveles 79 y 81-89 NO EXISTEN: `C537` hace que el nivel 78 (`$4E`) pase al 80 (`$50`) y `C541` termina el juego al llegar a 81 (`$51`); los bytes que hay en esas posiciones son relleno/restos y no deben usarse (el JSON los marca `existe: false`) | [S] (`colortest.py` sólo coincide si se excluyen) |
| Colores por nivel: `C9F5` copia al búfer de atributos los 4 bytes de atributo de cada casilla (bit 7 borrado, `BFF6`); las casillas con máscara (0, 41-43, 4C) no tocan los atributos y dejan los del fondo. El renderizador reproduce exactamente atributos y píxeles. (Los colores de las casillas en memoria pueden cambiar en tiempo de ejecución con `F79B`/`C5F6`: el renderizador lee los atributos del snapshot cargado.) | [S] |
| Pantallas especiales (`$9550`, `$95DC`) | [C] renderizadas |
| Sprites: `sprites.json` es un volcado COMPLETO de toda la memoria de gráficos (112 fotogramas base + 184 por mundo = 1768 entradas, 933 con gráfico y 835 vacías) y además se comprobó que los 368 pares (mundo, fotograma) que el juego dibuja al recorrer todos los niveles existentes (1P y 2P, 9 mundos, con teclas inyectadas e invencibilidad) están en `sprites.json`; 17 de ellos son fotogramas en blanco a propósito (p. ej. el base `$46` y el `$70` de cada mundo). Los fotogramas que caen dentro de las imágenes grandes de jefe también se extraen (`en_imagen_grande: true`) | [S] `verificar_sprites.py`, `assets/verificacion_sprites.md` | **Ronda posterior** [S]: `manifiesto_sprites.json` clasifica TODAS las 1768 entradas: 370 sprites (con uso real por entidad), 533 fotogramas que son trozos de imágenes grandes de jefe (pares máscara/dato, NO sprites), 23 que son las casillas alternativas del nivel 70 (mundo 7), 7 que son la tabla de atributos del jefe 8 y 835 vacíos (huecos). Los 370 sprites se han comparado píxel a píxel con el resultado real de `$C384` (`verificar_mascara.py`): 370/370 coinciden. Fotogramas de la maga (`$0D-$19` = mago+`$0D`), orbes (`$3A/$3B/$3C`) y beber (`$38/$39`) comprobados con `rolesextra.py` y `pociontest2.py`. `$45` y `$FF` que aparecían como fotograma del orbe son valores residuales del registro antes de que `$B099` lo inicialice (`orbe45.py`).
| Casillas, fuente, HUD, imágenes de jefe, pantalla final | [C] reconocibles a la vista; las casillas además coinciden con el dibujado del juego (`colortest.py`) |
| Claves (codewords) | [S] |
| Tablas de datos `D99B`-`DC50`, `F79B` | [C] estructura verificada (este documento y `formatos_datos.md`) |

## Lo que sólo puede cerrar el juego real
Medir la velocidad en un Spectrum real (el modelo de contención da 20,2 ciclos/s en 1P y 18,7 en 2P) y si algún bug evidente del original (p. ej. `B38D` sólo examina la fila superior) es intencionado. No impiden reproducir el código.

**Completitud de sprites sin depender de las pruebas** [S]: `$C384` lee el fotograma de un byte (IX+2), así que sólo puede dibujar $00-$FF (dirección $6100+32·f). `completitud_sprites.py` comprueba que el manifiesto contiene los 112 fotogramas base y los 144 ($70-$FF) de cada uno de los 9 mundos (nada falta), y que los fotogramas de enemigos de las cabeceras de los 90 niveles en 1P y 2P están todos clasificados como sprite/vacío. Los fotogramas $100-$127 de la región por mundo no son alcanzables por `$C384`. Los otros orígenes (maga = +$0D, orbes $3A-$3C, beber $38/$39, tablas de animación, segmentos de jefe) están además observados en ejecución.
