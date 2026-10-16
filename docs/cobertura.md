# Cobertura de ejecución del código por las pruebas en el simulador

Instrucciones del programa: 4689 | ejecutadas por alguna prueba: **4689 (100 %)**: 4688 por juego o por estado forzado y 1 (`$B8A8`) con el PC forzado (`b8a8test.py`, ejecuta su `JP $BE70`). Ningún valor de entrada llega a ella (despachotest.py agota los 256 tipos), así que es código muerto.

Rutinas ejecutadas al 100 %: 82 de 82.

## Las últimas 14 instrucciones (antes sin ejecutar)

Se han resuelto en esta ronda con `herramientas/ultimos.py` y `energiatest.py`, que **fuerzan el estado** (se colocan los registros/variables y se llama a la rutina) y registran las direcciones ejecutadas. Se ejecuta el código real del juego; lo que es forzado es la situación, no el código. Por eso cada caso indica si es alcanzable jugando.

| Dirección | Qué hace | Cómo se ejecutó | ¿Alcanzable jugando? |
|---|---|---|---|
| `$B73A-$B73C` | Jugador subiendo en un salto (fase < 8) que choca con un techo: la fase pasa a 8 y empieza a caer | jugador en `y=$40`, fase 1, fila superior llena de bloques `$48`; `B6FE` | Sí (saltar bajo un techo). Mis barridos no lo provocaron. |
| `$BA88-$BA8C` | Proyectil del lanzador 5/6 que llega al borde derecho (`x + 8*recorrido >= $6A`): +7 = 0 (desaparece) | lanzador tipo 5 con +7 = 14, `BA25` | Sí (disparar con vía libre hasta el borde). Tras la rutina +7 = 0 ✔ |
| `$BEE5-$BEE8` | Bloque agachado fuera de la última fila: casilla destino una fila más abajo (`D += 16`) | jugador `x=24, y=$80`, frame `$0B`, +7 = 1, acción pulsada: se modifica la celda 130 del mapa (fila 9, columna 4) ✔ | Sí (agacharse en cualquier fila que no sea la última) |
| `$C272` | La esfera toca la salida `$44` situada ENCIMA, sólo si sube (D91F con el bit 7 = 1) | esfera `x=40, y=$50`, casilla `$44` encima: con D91F=`$FC` se obtiene D=1 y se ejecuta `$C272`; con D91F=`$04` D=0 | Sí (esfera ascendente tras una flecha de diamante) |
| `$CE12` | Energía: el resultado negativo se satura a 0 | `$CDF5` con energía 0 y C=`$FF` → 0 ✔ | Sí (un golpe más cuando la energía ya es 0) |
| `$CE03-$CE0A` | Energía: el resultado positivo se limita a 100 | `$CDF5` con energía 95 y C=`$0A` → 100 ✔ | **No**: los tres llamadores (`$AB1C`, `$AB55`, `$B3C8`) usan C=`$FF`; no hay forma de curar con esta rutina (la energía se restaura con la casilla `$31`, que escribe 100 directamente). Código sin uso real. |
| `$B8A8` (1 instrucción) | `JP $BE70` al final del despachador de tipos | no ejecutable | **Código muerto demostrado por ejecución exhaustiva** (`despachotest.py`: se entra en el despachador `$B836` con los 256 valores posibles del byte de tipo, con y sin congelación, 512 casos; todos salen a un manejador y ninguno ejecuta `$B8A8`) y además por lectura: tras `CP $0D / JC`, `JZ`, `CP $0E / JZ`, `CP $12 / JNC` y `CP $0F / JNC`, cualquier valor A cae en una de las ramas anteriores (A < $0D, $0D, $0E o >= $0F); no existe A que llegue a `$B8A8`. Tampoco hay referencias a esa dirección en ningún salto, llamada o tabla (búsqueda byte a byte de la dirección y de saltos relativos en toda la RAM). |

## Corrección de un comentario anterior

En `$C19C` el comentario decía que la salida por la casilla superior se activa "sólo si D91F tiene el bit 7 a 0". Es al revés: el código (`$C264-$C272`) salta el `LD D,1` cuando el bit 7 es 0; **sólo cuenta con D91F negativo (esfera subiendo)**. Verificado ejecutando la rutina con las dos velocidades. En la descripción anterior de `$CE03-$CE12` también se decía que limitaba a 100 hasta `$CE12`; en realidad `$CE12` es el `XOR A` de la saturación a 0, que sí es alcanzable.
