@ $5B00 start
@ $5B00 org
b $5B00 Tabla de silueta A (máscara por byte gráfico)
D $5B00 256 bytes generados en #R$A84B. Para un byte gráfico b da la máscara AND que borra el fondo desde el primer píxel activo hacia la derecha. Se usa en #R$C384 y #R$CB40. Esta zona coincide con las variables del sistema del Spectrum (no se usan: el juego no emplea la ROM salvo LD-BYTES).
B $5B00,256,16
b $5C00 Tabla de silueta B
D $5C00 256 bytes generados en #R$A89x; máscara para el byte derecho del sprite.
B $5C00,256,16
b $5D00 Restos del cargador BASIC (no usado por el juego)
D $5D00 Programa BASIC que hace RANDOMIZE USR 24800 ($60E0) y carga el bloque de código.
B $5D00,1024,16
b $6100 Sprites 16x16 (112 fotogramas de 32 bytes)
D $6100 Cada fotograma = 16 filas x 2 bytes, 1 bit por píxel, sin máscara (la máscara se calcula con las tablas $5B00/$5C00). Dirección = $6100 + 32*fotograma. Ver atlas_sprites.png. 00-03 mago camina izq., 04-06 giro, 07-0A camina der., 0B-0C agachado, 0D-19 maga (los mismos +$0D), 1A-23 esfera girando, 24-27 caminante tipo 0, 28-2F caminante tipo 1, 30-31 burbujas, 32-37 gotas (tipo 4), 38-39 mago bebiendo la poción, 3A-3C orbe mágico, 46 vacío (oculto), 47-49 y 4A-4E, 4F-... resto: enemigos y jefes por identificar.
B $6100,32,2 Fotograma $00 - mago camina izq. 1
B $6120,32,2 Fotograma $01
B $6140,32,2 Fotograma $02
B $6160,32,2 Fotograma $03
B $6180,32,2 Fotograma $04 - mago giro
B $61A0,32,2 Fotograma $05
B $61C0,32,2 Fotograma $06
B $61E0,32,2 Fotograma $07 - mago camina der. 1
B $6200,32,2 Fotograma $08
B $6220,32,2 Fotograma $09
B $6240,32,2 Fotograma $0A
B $6260,32,2 Fotograma $0B - mago agachado izq.
B $6280,32,2 Fotograma $0C - mago agachado der.
B $62A0,32,2 Fotograma $0D - maga camina izq. 1
B $62C0,32,2 Fotograma $0E
B $62E0,32,2 Fotograma $0F
B $6300,32,2 Fotograma $10
B $6320,32,2 Fotograma $11
B $6340,32,2 Fotograma $12
B $6360,32,2 Fotograma $13
B $6380,32,2 Fotograma $14
B $63A0,32,2 Fotograma $15
B $63C0,32,2 Fotograma $16
B $63E0,32,2 Fotograma $17
B $6400,32,2 Fotograma $18
B $6420,32,2 Fotograma $19
B $6440,32,2 Fotograma $1A - esfera girando 1
B $6460,32,2 Fotograma $1B
B $6480,32,2 Fotograma $1C
B $64A0,32,2 Fotograma $1D
B $64C0,32,2 Fotograma $1E
B $64E0,32,2 Fotograma $1F
B $6500,32,2 Fotograma $20
B $6520,32,2 Fotograma $21
B $6540,32,2 Fotograma $22
B $6560,32,2 Fotograma $23
B $6580,32,2 Fotograma $24 - enemigo tipo 0 (1)
B $65A0,32,2 Fotograma $25
B $65C0,32,2 Fotograma $26
B $65E0,32,2 Fotograma $27
B $6600,32,2 Fotograma $28 - enemigo tipo 1 (1)
B $6620,32,2 Fotograma $29
B $6640,32,2 Fotograma $2A
B $6660,32,2 Fotograma $2B
B $6680,32,2 Fotograma $2C
B $66A0,32,2 Fotograma $2D
B $66C0,32,2 Fotograma $2E
B $66E0,32,2 Fotograma $2F
B $6700,32,2 Fotograma $30 - burbuja
B $6720,32,2 Fotograma $31
B $6740,32,2 Fotograma $32 - gota (tipo 4)
B $6760,32,2 Fotograma $33
B $6780,32,2 Fotograma $34
B $67A0,32,2 Fotograma $35
B $67C0,32,2 Fotograma $36
B $67E0,32,2 Fotograma $37
B $6800,32,2 Fotograma $38 - mago bebiendo
B $6820,32,2 Fotograma $39
B $6840,32,2 Fotograma $3A - orbe mágico
B $6860,32,2 Fotograma $3B
B $6880,32,2 Fotograma $3C
B $68A0,32,2 Fotograma $3D
B $68C0,32,2 Fotograma $3E
B $68E0,32,2 Fotograma $3F
B $6900,32,2 Fotograma $40
B $6920,32,2 Fotograma $41
B $6940,32,2 Fotograma $42
B $6960,32,2 Fotograma $43
B $6980,32,2 Fotograma $44
B $69A0,32,2 Fotograma $45
B $69C0,32,2 Fotograma $46 - vacío
B $69E0,32,2 Fotograma $47
B $6A00,32,2 Fotograma $48
B $6A20,32,2 Fotograma $49
B $6A40,32,2 Fotograma $4A
B $6A60,32,2 Fotograma $4B
B $6A80,32,2 Fotograma $4C
B $6AA0,32,2 Fotograma $4D
B $6AC0,32,2 Fotograma $4E
B $6AE0,32,2 Fotograma $4F
B $6B00,32,2 Fotograma $50
B $6B20,32,2 Fotograma $51
B $6B40,32,2 Fotograma $52
B $6B60,32,2 Fotograma $53
B $6B80,32,2 Fotograma $54
B $6BA0,32,2 Fotograma $55
B $6BC0,32,2 Fotograma $56
B $6BE0,32,2 Fotograma $57
B $6C00,32,2 Fotograma $58
B $6C20,32,2 Fotograma $59
B $6C40,32,2 Fotograma $5A
B $6C60,32,2 Fotograma $5B
B $6C80,32,2 Fotograma $5C
B $6CA0,32,2 Fotograma $5D
B $6CC0,32,2 Fotograma $5E
B $6CE0,32,2 Fotograma $5F
B $6D00,32,2 Fotograma $60
B $6D20,32,2 Fotograma $61
B $6D40,32,2 Fotograma $62
B $6D60,32,2 Fotograma $63
B $6D80,32,2 Fotograma $64
B $6DA0,32,2 Fotograma $65
B $6DC0,32,2 Fotograma $66
B $6DE0,32,2 Fotograma $67
B $6E00,32,2 Fotograma $68
B $6E20,32,2 Fotograma $69
B $6E40,32,2 Fotograma $6A
B $6E60,32,2 Fotograma $6B
B $6E80,32,2 Fotograma $6C
B $6EA0,32,2 Fotograma $6D
B $6EC0,32,2 Fotograma $6E
B $6EE0,32,2 Fotograma $6F
s $6F00 Gráficos propios del mundo (sprites a partir del frame $70); vacío en el mundo 0
D $6F00 Cada bloque de mundo de la cinta (nombres "0"-"8", 11264 bytes) se carga en $6F00-$9AFF: esta zona (sprites extra de enemigos y jefes), los fondos, los mapas y las cabeceras. VERIFICADO con el TZX: el bloque "0" coincide byte a byte con la RAM del snapshot. En el nivel 70 (D39A=$46) se copian 720 bytes ($2D0, 20 casillas) de $9E60 a $71D0 (copia de seguridad) y de $6F00 a $9E60 (juego alternativo de casillas), ver #R$C5DB.
S $6F00,5632
b $8600 Capas de fondo (papel pintado): 8 juegos de 140 bytes (14x10 casillas)
D $8600 La cabecera de cada nivel indica el desplazamiento (+$4B00) del fondo que usa. Se copia a $DEE6.
B $8600,140,14 Fondo 0
B $868C,140,14 Fondo 1
B $8718,140,14 Fondo 2
B $87A4,140,14 Fondo 3
B $8830,140,14 Fondo 4
B $88BC,140,14 Fondo 5
B $8948,140,14 Fondo 6
B $89D4,140,14 Fondo 7
b $8A60 Mapas de nivel de 1 JUGADOR (mundo cargado): 10 mapas de 140 bytes (14x10)
D $8A60 Códigos de casilla en el documento de formatos. Se copian a $DE5A. Los niveles de 1 y 2 jugadores son distintos.
B $8A60,140,14 Mapa 1P, nivel local 0
B $8AEC,140,14 Mapa 1P, nivel local 1
B $8B78,140,14 Mapa 1P, nivel local 2
B $8C04,140,14 Mapa 1P, nivel local 3
B $8C90,140,14 Mapa 1P, nivel local 4
B $8D1C,140,14 Mapa 1P, nivel local 5
B $8DA8,140,14 Mapa 1P, nivel local 6
B $8E34,140,14 Mapa 1P, nivel local 7
B $8EC0,140,14 Mapa 1P, nivel local 8
B $8F4C,140,14 Mapa 1P, nivel local 9
b $8FD8 Mapas de nivel de 2 JUGADORES (mundo cargado): 10 mapas de 140 bytes
B $8FD8,140,14 Mapa 2P, nivel local 0
B $9064,140,14 Mapa 2P, nivel local 1
B $90F0,140,14 Mapa 2P, nivel local 2
B $917C,140,14 Mapa 2P, nivel local 3
B $9208,140,14 Mapa 2P, nivel local 4
B $9294,140,14 Mapa 2P, nivel local 5
B $9320,140,14 Mapa 2P, nivel local 6
B $93AC,140,14 Mapa 2P, nivel local 7
B $9438,140,14 Mapa 2P, nivel local 8
B $94C4,140,14 Mapa 2P, nivel local 9
b $9550 Mapa especial A (D39B=$42)
B $9550,140,14
b $95DC Mapa especial B (otros niveles especiales)
B $95DC,140,14
b $9668 Cabeceras de nivel (10 de 1P, 10 de 2P, 2 especiales)
D $9668 Registro: fondo(2), esfera x,y, J1 x,y, J2 x,y ($FFFF en 1P), nº enemigos(1), nº*[x, y, tipo, frame]. Ver #R$C65B.
B $9668,8,2 Cabecera 1P 0: fondo, esfera, J1, J2
B $9670,1 Número de enemigos
B $9671,4,4 Enemigos (x,y,tipo,frame)
B $9675,8,2 Cabecera 1P 1: fondo, esfera, J1, J2
B $967D,1 Número de enemigos
B $967E,8,4 Enemigos (x,y,tipo,frame)
B $9686,8,2 Cabecera 1P 2: fondo, esfera, J1, J2
B $968E,1 Número de enemigos
B $968F,16,4 Enemigos (x,y,tipo,frame)
B $969F,8,2 Cabecera 1P 3: fondo, esfera, J1, J2
B $96A7,1 Número de enemigos
B $96A8,12,4 Enemigos (x,y,tipo,frame)
B $96B4,8,2 Cabecera 1P 4: fondo, esfera, J1, J2
B $96BC,1 Número de enemigos
B $96BD,16,4 Enemigos (x,y,tipo,frame)
B $96CD,8,2 Cabecera 1P 5: fondo, esfera, J1, J2
B $96D5,1 Número de enemigos
B $96D6,32,4 Enemigos (x,y,tipo,frame)
B $96F6,8,2 Cabecera 1P 6: fondo, esfera, J1, J2
B $96FE,1 Número de enemigos
B $96FF,16,4 Enemigos (x,y,tipo,frame)
B $970F,8,2 Cabecera 1P 7: fondo, esfera, J1, J2
B $9717,1 Número de enemigos
B $9718,20,4 Enemigos (x,y,tipo,frame)
B $972C,8,2 Cabecera 1P 8: fondo, esfera, J1, J2
B $9734,1 Número de enemigos
B $9735,24,4 Enemigos (x,y,tipo,frame)
B $974D,8,2 Cabecera 1P 9: fondo, esfera, J1, J2
B $9755,1 Número de enemigos
B $9756,28,4 Enemigos (x,y,tipo,frame)
B $9772,8,2 Cabecera 2P 0: fondo, esfera, J1, J2
B $977A,1 Número de enemigos
B $977B,8,4 Enemigos (x,y,tipo,frame)
B $9783,8,2 Cabecera 2P 1: fondo, esfera, J1, J2
B $978B,1 Número de enemigos
B $978C,8,4 Enemigos (x,y,tipo,frame)
B $9794,8,2 Cabecera 2P 2: fondo, esfera, J1, J2
B $979C,1 Número de enemigos
B $979D,8,4 Enemigos (x,y,tipo,frame)
B $97A5,8,2 Cabecera 2P 3: fondo, esfera, J1, J2
B $97AD,1 Número de enemigos
B $97AE,8,4 Enemigos (x,y,tipo,frame)
B $97B6,8,2 Cabecera 2P 4: fondo, esfera, J1, J2
B $97BE,1 Número de enemigos
B $97BF,16,4 Enemigos (x,y,tipo,frame)
B $97CF,8,2 Cabecera 2P 5: fondo, esfera, J1, J2
B $97D7,1 Número de enemigos
B $97D8,16,4 Enemigos (x,y,tipo,frame)
B $97E8,8,2 Cabecera 2P 6: fondo, esfera, J1, J2
B $97F0,1 Número de enemigos
B $97F1,20,4 Enemigos (x,y,tipo,frame)
B $9805,8,2 Cabecera 2P 7: fondo, esfera, J1, J2
B $980D,1 Número de enemigos
B $980E,32,4 Enemigos (x,y,tipo,frame)
B $982E,8,2 Cabecera 2P 8: fondo, esfera, J1, J2
B $9836,1 Número de enemigos
B $9837,24,4 Enemigos (x,y,tipo,frame)
B $984F,8,2 Cabecera 2P 9: fondo, esfera, J1, J2
B $9857,1 Número de enemigos
B $9858,16,4 Enemigos (x,y,tipo,frame)
B $9868,8,2 Cabecera especial 20: fondo, esfera, J1, J2
B $9870,1 Número de enemigos
B $9871,8,2 Cabecera especial 21: fondo, esfera, J1, J2
B $9879,1 Número de enemigos
B $987A,48,4 Enemigos (x,y,tipo,frame)
s $98AA Libre
S $98AA,598
b $9B00 Gráficos de casillas (91 casillas de 36 bytes)
D $9B00 32 bytes de bitmap (16 filas x 2 bytes) + 4 bytes de atributos (2x2). Ver atlas_casillas.png.
B $9B00,32,2 Casilla $00 bitmap
B $9B20,4,2 Casilla $00 atributos
B $9B24,32,2 Casilla $01 bitmap
B $9B44,4,2 Casilla $01 atributos
B $9B48,32,2 Casilla $02 bitmap
B $9B68,4,2 Casilla $02 atributos
B $9B6C,32,2 Casilla $03 bitmap
B $9B8C,4,2 Casilla $03 atributos
B $9B90,32,2 Casilla $04 bitmap
B $9BB0,4,2 Casilla $04 atributos
B $9BB4,32,2 Casilla $05 bitmap
B $9BD4,4,2 Casilla $05 atributos
B $9BD8,32,2 Casilla $06 bitmap
B $9BF8,4,2 Casilla $06 atributos
B $9BFC,32,2 Casilla $07 bitmap
B $9C1C,4,2 Casilla $07 atributos
B $9C20,32,2 Casilla $08 bitmap
B $9C40,4,2 Casilla $08 atributos
B $9C44,32,2 Casilla $09 bitmap
B $9C64,4,2 Casilla $09 atributos
B $9C68,32,2 Casilla $0A bitmap
B $9C88,4,2 Casilla $0A atributos
B $9C8C,32,2 Casilla $0B bitmap
B $9CAC,4,2 Casilla $0B atributos
B $9CB0,32,2 Casilla $0C bitmap
B $9CD0,4,2 Casilla $0C atributos
B $9CD4,32,2 Casilla $0D bitmap
B $9CF4,4,2 Casilla $0D atributos
B $9CF8,32,2 Casilla $0E bitmap
B $9D18,4,2 Casilla $0E atributos
B $9D1C,32,2 Casilla $0F bitmap
B $9D3C,4,2 Casilla $0F atributos
B $9D40,32,2 Casilla $10 bitmap
B $9D60,4,2 Casilla $10 atributos
B $9D64,32,2 Casilla $11 bitmap
B $9D84,4,2 Casilla $11 atributos
B $9D88,32,2 Casilla $12 bitmap
B $9DA8,4,2 Casilla $12 atributos
B $9DAC,32,2 Casilla $13 bitmap
B $9DCC,4,2 Casilla $13 atributos
B $9DD0,32,2 Casilla $14 bitmap
B $9DF0,4,2 Casilla $14 atributos
B $9DF4,32,2 Casilla $15 bitmap
B $9E14,4,2 Casilla $15 atributos
B $9E18,32,2 Casilla $16 bitmap
B $9E38,4,2 Casilla $16 atributos
B $9E3C,32,2 Casilla $17 bitmap
B $9E5C,4,2 Casilla $17 atributos
B $9E60,32,2 Casilla $18 bitmap
B $9E80,4,2 Casilla $18 atributos
B $9E84,32,2 Casilla $19 bitmap
B $9EA4,4,2 Casilla $19 atributos
B $9EA8,32,2 Casilla $1A bitmap
B $9EC8,4,2 Casilla $1A atributos
B $9ECC,32,2 Casilla $1B bitmap
B $9EEC,4,2 Casilla $1B atributos
B $9EF0,32,2 Casilla $1C bitmap
B $9F10,4,2 Casilla $1C atributos
B $9F14,32,2 Casilla $1D bitmap
B $9F34,4,2 Casilla $1D atributos
B $9F38,32,2 Casilla $1E bitmap
B $9F58,4,2 Casilla $1E atributos
B $9F5C,32,2 Casilla $1F bitmap
B $9F7C,4,2 Casilla $1F atributos
B $9F80,32,2 Casilla $20 bitmap
B $9FA0,4,2 Casilla $20 atributos
B $9FA4,32,2 Casilla $21 bitmap
B $9FC4,4,2 Casilla $21 atributos
B $9FC8,32,2 Casilla $22 bitmap
B $9FE8,4,2 Casilla $22 atributos
B $9FEC,32,2 Casilla $23 bitmap
B $A00C,4,2 Casilla $23 atributos
B $A010,32,2 Casilla $24 bitmap
B $A030,4,2 Casilla $24 atributos
B $A034,32,2 Casilla $25 bitmap
B $A054,4,2 Casilla $25 atributos
B $A058,32,2 Casilla $26 bitmap
B $A078,4,2 Casilla $26 atributos
B $A07C,32,2 Casilla $27 bitmap
B $A09C,4,2 Casilla $27 atributos
B $A0A0,32,2 Casilla $28 bitmap
B $A0C0,4,2 Casilla $28 atributos
B $A0C4,32,2 Casilla $29 bitmap
B $A0E4,4,2 Casilla $29 atributos
B $A0E8,32,2 Casilla $2A bitmap
B $A108,4,2 Casilla $2A atributos
B $A10C,32,2 Casilla $2B bitmap
B $A12C,4,2 Casilla $2B atributos
B $A130,32,2 Casilla $2C bitmap
B $A150,4,2 Casilla $2C atributos
B $A154,32,2 Casilla $2D bitmap
B $A174,4,2 Casilla $2D atributos
B $A178,32,2 Casilla $2E bitmap
B $A198,4,2 Casilla $2E atributos
B $A19C,32,2 Casilla $2F bitmap
B $A1BC,4,2 Casilla $2F atributos
B $A1C0,32,2 Casilla $30 bitmap
B $A1E0,4,2 Casilla $30 atributos
B $A1E4,32,2 Casilla $31 bitmap
B $A204,4,2 Casilla $31 atributos
B $A208,32,2 Casilla $32 bitmap
B $A228,4,2 Casilla $32 atributos
B $A22C,32,2 Casilla $33 bitmap
B $A24C,4,2 Casilla $33 atributos
B $A250,32,2 Casilla $34 bitmap
B $A270,4,2 Casilla $34 atributos
B $A274,32,2 Casilla $35 bitmap
B $A294,4,2 Casilla $35 atributos
B $A298,32,2 Casilla $36 bitmap
B $A2B8,4,2 Casilla $36 atributos
B $A2BC,32,2 Casilla $37 bitmap
B $A2DC,4,2 Casilla $37 atributos
B $A2E0,32,2 Casilla $38 bitmap
B $A300,4,2 Casilla $38 atributos
B $A304,32,2 Casilla $39 bitmap
B $A324,4,2 Casilla $39 atributos
B $A328,32,2 Casilla $3A bitmap
B $A348,4,2 Casilla $3A atributos
B $A34C,32,2 Casilla $3B bitmap
B $A36C,4,2 Casilla $3B atributos
B $A370,32,2 Casilla $3C bitmap
B $A390,4,2 Casilla $3C atributos
B $A394,32,2 Casilla $3D bitmap
B $A3B4,4,2 Casilla $3D atributos
B $A3B8,32,2 Casilla $3E bitmap
B $A3D8,4,2 Casilla $3E atributos
B $A3DC,32,2 Casilla $3F bitmap
B $A3FC,4,2 Casilla $3F atributos
B $A400,32,2 Casilla $40 bitmap
B $A420,4,2 Casilla $40 atributos
B $A424,32,2 Casilla $41 bitmap
B $A444,4,2 Casilla $41 atributos
B $A448,32,2 Casilla $42 bitmap
B $A468,4,2 Casilla $42 atributos
B $A46C,32,2 Casilla $43 bitmap
B $A48C,4,2 Casilla $43 atributos
B $A490,32,2 Casilla $44 bitmap
B $A4B0,4,2 Casilla $44 atributos
B $A4B4,32,2 Casilla $45 bitmap
B $A4D4,4,2 Casilla $45 atributos
B $A4D8,32,2 Casilla $46 bitmap
B $A4F8,4,2 Casilla $46 atributos
B $A4FC,32,2 Casilla $47 bitmap
B $A51C,4,2 Casilla $47 atributos
B $A520,32,2 Casilla $48 bitmap
B $A540,4,2 Casilla $48 atributos
B $A544,32,2 Casilla $49 bitmap
B $A564,4,2 Casilla $49 atributos
B $A568,32,2 Casilla $4A bitmap
B $A588,4,2 Casilla $4A atributos
B $A58C,32,2 Casilla $4B bitmap
B $A5AC,4,2 Casilla $4B atributos
B $A5B0,32,2 Casilla $4C bitmap
B $A5D0,4,2 Casilla $4C atributos
B $A5D4,32,2 Casilla $4D bitmap
B $A5F4,4,2 Casilla $4D atributos
B $A5F8,32,2 Casilla $4E bitmap
B $A618,4,2 Casilla $4E atributos
B $A61C,32,2 Casilla $4F bitmap
B $A63C,4,2 Casilla $4F atributos
B $A640,32,2 Casilla $50 bitmap
B $A660,4,2 Casilla $50 atributos
B $A664,32,2 Casilla $51 bitmap
B $A684,4,2 Casilla $51 atributos
B $A688,32,2 Casilla $52 bitmap
B $A6A8,4,2 Casilla $52 atributos
B $A6AC,32,2 Casilla $53 bitmap
B $A6CC,4,2 Casilla $53 atributos
B $A6D0,32,2 Casilla $54 bitmap
B $A6F0,4,2 Casilla $54 atributos
B $A6F4,32,2 Casilla $55 bitmap
B $A714,4,2 Casilla $55 atributos
B $A718,32,2 Casilla $56 bitmap
B $A738,4,2 Casilla $56 atributos
B $A73C,32,2 Casilla $57 bitmap
B $A75C,4,2 Casilla $57 atributos
B $A760,32,2 Casilla $58 bitmap
B $A780,4,2 Casilla $58 atributos
B $A784,32,2 Casilla $59 bitmap
B $A7A4,4,2 Casilla $59 atributos
B $A7A8,32,2 Casilla $5A bitmap
B $A7C8,4,2 Casilla $5A atributos
c $A7CC Inicio: preparación del sistema, tablas y menú principal
@ $A7CC label=INICIO
D $A7CC Punto de entrada del juego (tras el cargador BASIC). Desactiva interrupciones, coloca la pila en $FFFE y configura el modo de interrupción 2 (IM 2): se rellena la tabla $FE00-$FF00 con el valor $FD, de modo que cualquier interrupción salta a la dirección $FDFD, donde se escribe un `JP $C4D5` (la rutina de sonido, ver #R$C4D5). Después construye la tabla de direcciones de línea de pantalla ($DD1A), asigna a cada entidad su búfer de fondo, detecta si hay interfaz Kempston (lee el puerto $1F; un valor >= $20 indica que no hay joystick) y genera las tablas de silueta $5B00/$5C00.
D $A7CC **Concepto Z80 - IM 2:** en el modo 2 el Spectrum, al producirse la interrupción (50 veces por segundo), lee un byte del bus, lo combina con el registro I ($FE) y salta a la dirección guardada en esa posición de la tabla. Como el bus suele devolver $FF, el programador rellena toda la tabla con el mismo valor ($FD) para que la dirección sea siempre $FDFD.
N $A7D0 Rellena $FE00..$FF00 (257 bytes) con $FD usando LDIR (LDIR copia (HL)->(DE) y avanza ambos BC veces: aquí copia cada byte sobre el siguiente, propagando $FD).
N $A7F3 Tabla de 160 direcciones de línea de pantalla (una por cada línea de píxeles del área de juego, empezando en $4042 = columna 2, línea 0). Cada entrada son 2 bytes (little endian).
N $A819 A cada una de las 14 entidades enemigas se le asigna su búfer de 48 bytes ($30) donde guardar el fondo, empezando en $D67D (campos +3/+4 del registro).
N $A834 Detección de Kempston: se lee $1F 10.000 veces; si alguna lectura da >= $20 (bits altos activos = no hay interfaz) D988 queda a 0; si todas son < $20 D988=1 (hay Kempston).
N $A84B Generación de la tabla de silueta $5B00 (256 entradas). Para cada valor gráfico C la máscara pone a 0 todos los bits desde el primer píxel activo hacia la derecha (+1) - sirve para borrar el fondo bajo el sprite.
N $A8D1 Pantalla de menú: pinta los colores, el texto del menú ($D154), el texto de la configuración de mandos actual ($D1EF/$D210/$D231/$D252 según D39E) y entra en el bucle de lectura de teclas $A931.
N $A931 Bucle de teclas del menú: 1=1 jugador, 2=2 jugadores, 3=entrenamiento de movimiento, 4=introducir clave, 5=cambiar mandos, 6=ver mejores puntuaciones, 7=fondos claros/oscuros. Cada tecla se prueba con #R$CDD3 (código de tecla en A). [VERIFICADO con menuseguir.py manteniendo la tecla: 2 -> D91D=2; 3 -> D39B=$54 (entrenamiento, pasa por $C8FB); 4 -> entrada de texto $AE6B; 5 -> D39E pasa de 2 a 0 (cambia el esquema de mandos); 7 -> F79B pasa de 1 a 5 (color de tinta de las casillas de fondo claro/oscuro).]
N $A96C 1 jugador: A=1, salta a $AA85. 2 jugadores: A=2.
N $A976 Entrenamiento de movimiento: D39B=$54 (nivel especial), un jugador.
N $A983 Clave (codeword): pide el texto con #R$AE6B y lo compara con las tablas $D2E9 (5 claves de 1 jugador) y $D2FD (6 de 2 jugadores). Cada entrada: nivel del pergamino $3F que la muestra, nivel de inicio, puntero al texto. Si el nivel es $FF (ILLUMINATUS) se activa D079 = invencible.
N $AA02 Tecla 5: rota D39E (0..3) y copia las 5+5 teclas del esquema elegido a $D3B6 (jugador 1) y $D3D3 (jugador 2). Los esquemas 1 y 3 (Kempston) sólo se admiten si D988<>0.
N $AA5D Tecla 7: alterna el color de fondo entre claro y oscuro en $F79B (1 <-> 5) y cambia el texto "LIGHT"/"DARK" del menú.
N $AA85 Inicio de partida: D91D = número de jugadores, nivel D39A=0. $AA8C: puesta a cero de puntuaciones, reintentos ($D2E8=4), energía ($D3EF=100), dibuja los indicadores de poder de ambos jugadores (#R$CE5C).
c $AAC7 Bucle principal del juego
@ $AAC7 label=BUCLE_PRINCIPAL
D $AAC7 Carga el nivel actual (#R$C563) con un efecto de transición y ejecuta indefinidamente el ciclo del juego. Cada vuelta (aprox. 2,5 interrupciones = unos 20 ciclos/s) hace, en orden:
N $ACEE Fin de partida (Game Over): limpia (#R$CB7D), textos D2AE y D282, espera 100 ciclos con #R$CCB2 y trata las puntuaciones: $AD0E inserta la del jugador 1 (D3BD) y, si hay 2 jugadores, la del jugador 2 (D3DA) con #R$ADAC; muestra la tabla (#R$AE09), restaura el intercambio de casillas si el nivel era $46 y vuelve al menú (#R$A8D1).
D $AAC7 1. Jugador 1: #R$B38D (interacción con casillas), #R$CCB5 (leer teclas), #R$B5DD (movimiento/salto), solapamiento con enemigos y daño (#R$CDF5), #R$BE7B (colocar/quitar bloque), #R$AEF7 (poderes/puertas).
D $AAC7 2. Jugador 2 (si D91D=2): lo mismo con IY=$D3C4.
D $AAC7 3. Esfera (#R$B767), enemigos (#R$B82C), dibujo (#R$C2DC, #R$B2F3, #R$CD43, #R$B296, #R$C338).
D $AAC7 4. Contador de ciclo D989 = (D989+1) AND 3 (se usa para ralentizar animaciones y temporizadores).
D $AAC7 5. Teclas globales: R (reintentar, $AB81), F (abandonar, $AB97), ENTER (usar poción, $ABBB), H (pausa, $ACB3) y, con la clave ILLUMINATUS, teclas de trucos.
D $AAC7 Un fin de partida lleva a #R$ACEE (GAME OVER) y #R$AD45.
N $AAF4 Turno del jugador 1 (D91E=1, IY=$D3A7). El registro IY apunta siempre al "registro de jugador" (29 bytes) del jugador en curso; la dirección del turno 2 es $D3C4.
N $AB81 Tecla R (código $0D): si quedan reintentos (D2E8) las descuenta y reinicia el nivel actual. Con 0 reintentos se ignora.
N $AB97 Tecla F (código $0E): abandona la partida -> $AD2F (vuelta al menú, restaura gráficos del nivel 70 si procede).
N $ABA6 Tecla T (código $05): si D920 <> 0 lo reinicia a $0101 [VERIFICADO con teclasjuego.py: con D920=5 la tecla T lo deja a $0101 y el reloj termina en el ciclo siguiente: T CANCELA el reloj de arena (la esfera vuelve a moverse). Tecla T = fila $FB, bit 4.]
N $ABBB Tecla ENTER (código $21): USAR POCIÓN. Requiere D98C>0 (nº de pociones recogidas, casilla $36). Resta una, borra el icono del marcador (50E0+n), reproduce la animación de beber (frames $05,$05,$38,$38,$39,$39,$39 desde $D98D y $39,$38,$38,$05,$05 desde $D995) mientras el mundo sigue en marcha, y elimina todos los enemigos de tipos 0-3 y 5-8 (el tipo 4 no) y las casillas $41/$42 (proyectiles/peligros) de la pantalla. VERIFICADO simulando: con D98C=2, ENTER lo deja en 1 y los enemigos pasan a x=$FF. [VERIFICADO con pociontest2.py: la poción mata a los enemigos de tipo 0 (y 1-3, 5-8), NO a los de tipo 4 ni 9+, borra las casillas $41 y $42 pero no la $43, y resta una poción.]
N $AC92 Trucos con la clave ILLUMINATUS (D079<>0): tecla $10 (M) = pasar de nivel, tecla $08 (N) = nivel anterior. [VERIFICADO con teclasjuego.py: con D079=255 M lleva del 5 al 6 y N del 5 al 4; con D079=0 no hacen nada.]
N $ACB3 Tecla H (código $01): pausa. Espera a soltar y a pulsar otra vez. [VERIFICADO con teclasjuego.py: al pulsar H los atributos de pantalla pasan a $01 (azul sobre negro) y al pulsar H de nuevo vuelven los originales (copia en $F192); el juego no avanza mientras tanto.]
c $AD45 Fin de partida / juego completado
D $AD45 Se llega aquí con la pila reiniciada al terminar los niveles (D39A=$51) o al jugar el nivel final. Muestra el mensaje y la lista de puntuaciones.
N $AD45 Pantalla final 'The End': limpia el búfer y copia 64 líneas de 16 bytes (128 px) desde $9064 (dentro del bloque del mundo 8, en la zona que en otros mundos son mapas) a $E400 y los atributos (8 filas de 16) a $F27A, vuelca a pantalla y espera la tecla de acción (#R$AD8F), tras lo cual vuelve a $AD0E (puntuaciones). [verificado: imagen extraída en assets/pantallas/final_the_end.png]. Esto explica el formato 'raro' del mundo 8: sus bytes en $9064 no son mapas 2P.
c $AD8F Esperar una tecla del jugador
D $AD8F Espera a que se pulse (y se suelte) la tecla de disparo de cada jugador (códigos $D3BA / $D3D7). Utilidad de pantallas de texto.
N $AD8F Z = pulsada la tecla de acción del jugador 1 (D3BA), o el disparo Kempston (IN $1F XOR $10, bit 4), o la tecla de acción del jugador 2 (D3D7).
c $ADAC Insertar puntuación en la tabla de mejores jugadores
D $ADAC Entrada: HL = puntuación; $D0C0 = '1' o '2' (jugador). Si la puntuación entra en el top 5 ($D109, 5 entradas de 15 bytes: 2 de posición + 13 caracteres) pide el nombre con #R$AE6B y desplaza el resto.
N $ADAC Tabla de 5 entradas de 15 bytes en $D109 (2 de puntuación + 13 de nombre, mejor primero). Si HL=0 no hace nada. Compara con SBC HL,DE (NC = mayor o igual), desplaza las inferiores con LDDR, guarda la puntuación, muestra D09D y pide el nombre con #R$AE6B (búfer $DC44, 13 bytes) copiándolo a la entrada.
c $AE09 Pantalla de mejores puntuaciones
D $AE09 Dibuja "BEST PLAYERS" ($D0C5) y las 5 entradas de $D109 con nombre y puntos; espera una tecla.
N $AE09 5 filas: la puntuación con #R$CEC1 y los 13 caracteres del nombre con #R$CF82; después espera la tecla de acción.
c $AE6B Entrada de texto (nombre o clave)
D $AE6B Edición de texto con el teclado: lee las teclas (códigos de letra por semifila), borra con la tecla de código $21... y termina con $23 ($21 = ENTER). Deja el texto en $DC44 (terminado en $FF). Se usa para claves y para el nombre en la tabla de récords.
N $AE6B ENTER ($21) termina, '0' ($23, borrar) retrocede (E = longitud, máx. 13) y el resto se busca en la tabla de $DC51 (27 pares: código de tecla, ASCII) con #R$CDD3; al encontrarla espera a que se suelte ($AEA7), guarda el carácter, lo imprime con #R$CF6F y avanza el cursor $D087/$D089.
c $AEF7 Puertas de colores y estado de poderes del jugador
@ $AEF7 label=PODERES_Y_PUERTAS
D $AEF7 Tres veces (tabla $D07C, 3 entradas de 3 bytes: código de casilla de puerta $55/$56/$57, x, y de barrido): cuando el jugador recoge una llave (casillas $3B-$3D, ver #R$B38D) la entrada correspondiente se activa y, mientras no haya partículas en marcha (DCB4=0), se barre el mapa casilla a casilla (x+8, y+16 al final de cada fila) hasta encontrar una casilla de puerta de ese color: se pone a 0, se redibuja con la casilla de la CAPA DE FONDO situada en la misma posición (dirección +$8C = $DEE6) y se lanza una chispa (#R$B23C). Así la puerta se deshace de una en una. Después gestiona el temporizador del escudo (bit 1 de +$15, +$18 cuenta atrás cada 4 ciclos; al acabar muestra #R$D2A0) y el poder mágico (bits 3-4, temporizador +$19): el orbe mágico (D3E1 / D3E8) gira alrededor del jugador en 16 posiciones de la tabla $D948 y mata a los enemigos que toca (#R$B099).
D $AEF7 Ver #R$B099.
c $B038 Auxiliar: avanza el orbe un paso de la tabla de órbita
N $B038 Orbe lanzado: IX = registro del orbe, IY = jugador. Llama a #R$C19C con el orbe para saber qué lados están libres (E). +$1A del jugador pasa a ser entonces una máscara de dirección (bit0 arriba, bit1 derecha, bit2 abajo, bit3 izquierda; $09 = arriba+izquierda). Cada bit activo mueve el orbe: vertical 2 unidades de y ($B060/$B079), horizontal 1 unidad de x ($B06E/$B087). Si el lado está bloqueado, #R$B092 invierte esa componente haciendo XOR con $05 (vertical) o $0A (horizontal): el orbe REBOTA en diagonal como una pelota. [VERIFICADO con orbebounce.py: tras el lanzamiento (bit 6 de +$15 = 1) +$1A recorre los valores 9, 12, 3, 6...: el orbe sube/baja a 2 unidades por ciclo y se mueve 1 unidad en horizontal, rebota en paredes, techo y suelo (invirtiendo con XOR $05/$0A) y sigue indefinidamente; tras rebotar contra la pared izquierda se mueve hacia la derecha ($B06E).]
c $B060 Auxiliar del orbe (continuación)
c $B06E Auxiliar del orbe (continuación)
c $B079 Auxiliar del orbe (continuación)
c $B087 Auxiliar del orbe (continuación)
c $B099 Orbe mágico: órbita, daño a enemigos y disparo
N $B099 Lanzamiento: si el contador de pulsación del bloque (+$14) está entre $10 y $13 y el poder doble (+$15 bit 4) está activo, el orbe se lanza: +$1A=$09, +$15 bit 6=1, y se alinea la y del orbe a múltiplos de 16 [VERIFICADO en el simulador (orbtest.py): con +$15=$18 y SPACE mantenida, al llegar el contador +$14 a 16 el bit 6 de +$15 se activa y el orbe sale volando y rebotando; el lanzamiento ocurre MIENTRAS se mantiene la tecla, no al soltarla].
N $B0C0 Orbe orbitando: +$1A = (+$1A+1) AND $0F; la posición del orbe es la del jugador más el par (dx,dy) de la tabla $D948 (círculo de radio 16). x se limita a $69 (si desborda por la derecha) o 0 (por la izquierda); y a $90 o 0. Frame del orbe: $3A (poder simple), $3B (doble, +$15 bit 4) o $3C en el nivel $50.
N $B11C Colisión orbe-enemigo (#R$BFD7 deja IX = enemigo tocado). Tipos 0 y 1 y 7-8: mueren (x=$FF, nube de 14 partículas con #R$B23C). Tipos 2-6 y 9-$11: inmunes. Tipos >= $12 (jefes): pierden 1 punto del contador $DC3A (0 o $FF = invulnerable); en el nivel $3C sólo se les daña si su frame está entre $88 y $9F. Si el contador llega a 0: en el nivel $50 se salta a #R$AD45 (final del juego); en el resto se llama a #R$CC0A, se eliminan los jefes y proyectiles (tipos $09-$0E y >= $12), se borran las casillas $43 y $4C y se redibuja la pantalla. Si aún le queda vida salen 8 partículas. [VERIFICADO en el simulador (bosstest.py, mundo 1, nivel 10): la vida del jefe empieza en $18 (24) y baja al tocarlo el orbe (24 -> 19); animación de segmentos por la tabla $DAFA confirmada; reglas de inmunidad por tipo leídas en el código]
N $B1FC Bloques aleatorios (frasco azul, +$15 bit 5): cada ciclo hay una probabilidad de 8/100 ($CD9F devuelve un valor aleatorio < A); se elige x < $6A, y < $91, y si la casilla no está ocupada por jugadores, esfera ni enemigos y está vacía se coloca allí una casilla $48 (bloque rojo) y se dibuja con #R$BFF6.
@ $B099 label=ORBE_MAGICO
D $B099 Posición del orbe = posición del jugador + desplazamiento de la tabla $D948 (16 pares dx,dy que describen una circunferencia de radio 16 px; el índice está en +$1A y avanza uno por ciclo). El sprite del orbe es el frame $3A ($3B con bit 4 = poder doble, $3C en el nivel $50). Si el orbe solapa un enemigo (#R$BFD7): tipos 0-1 y 9-$11 se destruyen con una explosión de partículas (#R$B23C); otros tipos (jefes, >= $12) reducen el contador $DC3A (puntos de vida del jefe) y al llegar a 0 comienza la secuencia de victoria (#R$C524 / #R$AD45).
D $B099 Con el poder doble (bit 4 de +$15) y la tecla de bloque mantenida entre 16 y 19 ciclos (+$14 en $10..$13) el orbe se "lanza" (bit 6, +$1A=9). ESTE ÚLTIMO COMPORTAMIENTO SE LEE EN EL CÓDIGO PERO NO ESTÁ VERIFICADO JUGANDO. [VERIFICADO con varios.py: con el orbe en vuelo, mantener otra vez la tecla de bloque 10-13 ciclos (+$14 en $0A..$0D) LO RECUPERA: bit 6 de +$15 = 0, +$14 = $1E y vuelve a orbitar. Jefe del nivel 60 verificado con jefe60test.py: el orbe sólo le quita vida cuando el fotograma de su segmento está entre $88 y $9F.]
D $B099 Bit 5 de +$15 (casilla $37, matraz azul): cada ciclo hay una probabilidad (aprox. 8%) de que aparezca un bloque rojo ($48) en una posición aleatoria libre de la pantalla (#R$B1FC).
c $B23C Generar explosión de partículas
@ $B23C label=EXPLOSION
D $B23C Crea hasta B partículas alrededor de (L,H) en la tabla $DCB6 (5 bytes cada una: x, y, vx, vy, byte de fondo guardado). A = duración en ciclos, C = dispersión. Inicia además el sonido DCAE.
R $B23C A Duración (ciclos)
R $B23C B Número de partículas
R $B23C C Radio de dispersión
R $B23C HL Posición (L=x, H=y)
c $B296 Partículas: mover
D $B296 Cada ciclo avanza cada partícula con su velocidad (la vertical se aplica dos veces, simulando gravedad) y escribe un byte de color en el búfer de pantalla ($DF72).
c $B2F3 Partículas: guardar fondo y dibujar
D $B2F3 Guarda el byte de fondo del búfer bajo cada partícula (antes de dibujarla) y después pinta los píxeles con una máscara que depende de x AND 3 ($C0,$30,$0C,$03).
c $B38D Jugador: interacción con casillas
@ $B38D label=JUGADOR_CASILLAS
D $B38D Examina las casillas que ocupa el jugador (IY) y aplica el efecto de la que toca (ver tabla de casillas en el documento de formatos). Códigos: $2D gema +30, $2E gema +1, $2F anillo +10 (cuenta D07B; con 50 anillos se completa el nivel), $30 anillo +10, $39 +40, $31 energía al 100, $32 bit 0 (+$15), $33 poder mágico (1ª vez orbe, 2ª poder doble), $34 reloj de arena (D920=$14), $35 bit 2, $36 poción (D98C+1), $37 bit 5 (bloques aleatorios), $38 escudo ($96 ciclos), $3A fin de nivel (#R$C524), $3B-$3D llaves, $41-$43 peligros (-1 energía por ciclo), $3E bit 7. Las casillas se vacían al recogerlas (#R$BFF6 redibuja). [VERIFICADO con recogetest.py, una casilla bajo el jugador 1: $2D +30 puntos, $2E +1, $2F +10 y D07B+1, $30 +10, $31 energía a 100, $32 +15 bit 0, $33 +15 bit 3 y temporizador +$19≈$C0 (la segunda poción $33 activa además el bit 4 = poder doble), $34 D920=$13, $35 +15 bit 2, $36 D98C+1, $37 +15 bit 5, $38 +15 bit 1 y +$18≈$96, $39 +40, $3A fin de nivel, $3E +15 bit 7; $41-$43 restan energía cada ciclo; todas las recogibles desaparecen del mapa; las llaves $3B/$3C/$3D eliminan la puerta $55/$56/$57; al caducar +$18/+$19 se apagan los bits del escudo/poderes.]
N $B38D Recorre las casillas bajo el jugador: C = columnas (1 si x AND 7 < 2, si no 2), B = filas. Observación: B se queda siempre en 1 (el 'JP Z' de $B3AB salta a la instrucción siguiente y nunca se incrementa), así que sólo se examina la fila superior (y>>4). Para cada casilla con código $2D-$43 se aplica el efecto; el resto se ignora ($B5BA).
N $B3C1 Casillas >= $41 (peligros): #R$CDF5 con C=$FF (daño por contacto, -1 de energía), la casilla no se recoge. $32: +$15 bit 0 (movimiento más rápido en el aire). $2D/$2E/$30/$39: suman 30/1/10/40 puntos a +$16/+$17 y se actualiza el marcador con #R$CEC1 (columna $0E para el jugador 1, $38 para el 2). $2F: anillo, con D07B>=$32 (50) se sale al fin de nivel #R$C524.
N $B43E $38: escudo (+$15 bit 1, +$18=$96) y texto D290. $34: reloj de arena, D920=$14 (sólo si D920 <> 0 ya estaba, ver nota en #R$B767 [suposición: la comprobación de $B45A impide re-recoger]). $31: energía a $64 (100). $3A: fin de nivel. $3E: frasco rosa: si no se cumple BIT 1 de x, pone +$15 bit 7 = 1, que BLOQUEA la creación de bloques (#R$BE7B) para ese jugador [leído, nuevo respecto al índice anterior]. $36: poción +1 (D98C), dibuja el icono en $50E0+n / $F472+n. $35: +$15 bit 2 (congela enemigos 0/1) [VERIFICADO en el simulador: el tipo 0 queda inmóvil]. $33: poder mágico (+$19=$C0; 1ª vez bit 3, 2ª vez bit 4). $3B-$3D: llaves (activa la entrada de puerta $55+n en $D07C). $37: +$15 bit 5 (bloques aleatorios) [VERIFICADO en el simulador: aparecen bloques rojos al azar, 4 -> 8 en 300 frames].
N $B522 Casilla $40 (copa): CC0A, C49F, texto D273 y fin: D39B=$57 y salta a #R$AAC7 (bucle principal) tras esperar con #R$AD8F [leído; probablemente pantalla/final de bonificación]. Casilla $3F (pergamino): busca el nivel actual D39A en el PRIMER byte de cada entrada de la tabla de claves (D2E9 1 jugador / D2FD 2 jugadores: niveles 12, 21, 41, 61, 75); si está, muestra el texto de esa entrada (la clave que da acceso al nivel 9, 19, 39, 59 o 75), espera a que se pulse la acción ($B586) y restaura la pantalla; si no está, simplemente se recoge. [VERIFICADO en el simulador (casillatest.py)]. Casilla $40 (copa): [VERIFICADO: tras la pausa D39B=$57].
N $B5A0 Tras recoger: se repinta la casilla de la capa de fondo (+$8C) con #R$BFF6, suena DC96 y la casilla del mapa pasa a 0.
c $B5DD Jugador: movimiento, salto y animación
@ $B5DD label=JUGADOR_MOVER
D $B5DD Interpreta D98A (bit0 arriba/salto, bit1 derecha, bit2 abajo/agachar, bit3 izquierda, bit4 acción de bloque). En suelo: 2 unidades (4 px) por ciclo, en el aire 1 unidad (algo más con el bit 0 de +$15). Usa #R$C092 para saber qué lados están libres. El salto sigue la tabla $D922 (-4, -2x6, +2x6, +4x9, +8 terminal) con +$09 como fase (0 = en el suelo). Frames: 0-3 caminar izq., 4-6 giro, 7-$0A caminar der., $0B/$0C agachado.
N $B5DD Giro: si el frame está en 4-6 (animación de giro) se avanza el frame sumando la dirección (+7: 1=derecha, $FF=izquierda) y se salta a $B6FE sin leer más teclas, o sea el giro dura 3 ciclos y no se puede interrumpir. [verificado leyendo el código]
N $B5F5 Si el frame es < $0B se guarda en +8 (último frame de caminar). Agacharse ($B600): si el jugador está en el suelo (+9=0) y D98A bit 2 (abajo) -> frame $0C (mira a la derecha) o $0B (izquierda). Soltar la tecla restaura +8.
N $B627 Se llama a #R$C092: E = lados libres (bit0 arriba, bit1 derecha, bit2 abajo, bit3 izquierda). Izquierda ($B62D, bit 3 de D98A): si el frame >= 4 (mirando a la derecha) NO se mueve: se pone frame 6 (giro) y dirección $FF. Si ya mira a la izquierda y el lado está libre, x-1 (1 unidad = 2 px); en suelo, o con +$15 bit 0 (más rápido en el aire), se vuelve a llamar a #R$C092 y se resta otra unidad: 2 unidades (4 px) por ciclo en suelo, 1 en el aire.
N $B672 El frame de caminar (0-3) sólo cambia en ciclos pares de D989 (bit 0 = 0) y se reproduce el sonido DC90 (pasos) únicamente si está en el suelo.
N $B693 Derecha: igual que izquierda pero con frames 7-$0A (al alcanzar $0B vuelve a 7) y el giro empieza en el frame 4, dirección 1.
N $B6FE Salto y caída (+9 = fase; 0 = en suelo). Se recalcula E con #R$C092. En el suelo: si hay hueco debajo (E bit 2) la fase pasa a 8 (empieza a caer, dy=+2). Si no, y D98A bit 0 (arriba) está pulsado, el jugador no está agachado (frame < $0B) y y<>0: fase 1 (salto, dy=-4) si hay espacio encima; si hay techo, fase 7 (salto casi sin altura). En el aire: si la fase es < 8 (subiendo) y hay techo, la fase pasa a 8 (empieza a caer). Si no hay suelo debajo continúa y si lo hay ($B73F) y &= $F8 (se alinea a la rejilla de 8 px) y fase 0. $B751: y += D922[fase-1]; fase += 1. Tabla D922 (verificada): -4, -2x6, +2x6, +4x9, +8 hasta el final (38 entradas). [suposición: la fase no llega nunca al final porque la caída máxima del tablero es 144 px]
c $B767 Esfera: física
@ $B767 label=ESFERA
D $B767 Mueve la esfera (registro $D3F0). Consulta #R$C19C: E = bits de casillas libres (bit0 arriba, bit1 derecha, bit2 abajo, bit3 izquierda); D=1 si toca la salida ($44) -> #R$C524. Algoritmo: si hay vacío debajo cae 4 px por ciclo (D91F = velocidad vertical); si no, avanza 1 unidad en horizontal en la dirección +$07 (+1/-1); al chocar con una pared invierte la dirección y suena el rebote (descriptor $DCA2). Frames de giro $1A-$23. [VERIFICADO con salidatest.py: al tocar la esfera la casilla $44 se ejecuta $B7BB y el nivel pasa al siguiente.]
N $B767 Si D3F0 = $FF la esfera no existe (todavía no ha salido o ha terminado) y no hace nada.
N $B76D Reloj de arena (casilla $34): mientras D920 <> 0 la esfera está CONGELADA. D921 cuenta 16 ciclos; cada vez que llega a 0 se decrementa D920 y se actualiza el indicador (#R$CE98 con HL=$0D1E). Al llegar D920 a 0 el frame de la esfera pasa a $23. Mientras dura sólo anima el frame ($1A-$1D, sólo en ciclos pares de D989). [VERIFICADO en el simulador: con D920=5 la esfera permanece inmóvil unos 16 ciclos por unidad de D920 y después se mueve]
N $B7AF Movimiento normal. Se pide #R$C19C (E = lados libres, D=1 si toca la salida: se descarta la dirección de retorno y se salta a #R$C524, nivel completado).
N $B7BF Vertical: D91F es la velocidad vertical con signo (normalmente +4, las flechas de diamante $58-$5A la ponen a ±4). Si es positiva y hay hueco abajo (E bit 2), o si es negativa y hay hueco arriba (bit 0), y += D91F y termina ($B7CC). Si no puede moverse en vertical sigue con el movimiento horizontal.
N $B7DD Horizontal: D3F7 es la dirección (+1 derecha, $FF izquierda). Si hay pared en esa dirección (bit 1 para derecha, bit 3 para izquierda de E) se invierte la dirección y se reproduce el rebote (#R$DCA2); si no, x += dirección (1 unidad = 2 px por ciclo). El frame de giro avanza sólo en ciclos pares con la dirección: rango $1E-$23, y si baja de $1E se salta a $23 (rodar a un lado o al otro). El rebote NO se produce contra el suelo: la esfera sólo cae y rueda. [verificado en la lectura del código]
c $B82C Enemigos: despachador por tipo
@ $B82C label=ENEMIGOS
D $B82C Recorre los D52C enemigos (registros de 22 bytes desde $D3F8, IY = registro actual, B = contador) y salta a la rutina del tipo (+$08). Los tipos $0C y $0D se procesan aunque x=$FF; el resto se ignora si x=$FF (enemigo inactivo). Si algún jugador tiene el bit 2 de +$15 (matraz verde, casilla $35) los tipos 0 y 1 (caminantes) quedan congelados [L]. Tabla de saltos: 0 $B8AB, 1 $B90D, 2 $B984, 3 $B9A9, 4 $B9CE, 5 y 6 $BA25, 7 $BAE6, 8 $BB37, 9 $BBCD, $0A $BC0F, $0B $BC69, $0C $BCCF, $0D $BCFC, $0E $BD99, $0F-$11 $BDD2, >= $12 $BDFA. Todas terminan en $BE70 (IY += 22 y siguiente enemigo).
D $B82C Comportamientos VERIFICADOS ejecutando el juego con registros sintéticos (ver herramientas/enemytest.py) salvo el 3, el $0C y los jefes.
N $B844 Si x=$FF el enemigo no existe (muerto/inactivo) y se salta.
N $B84C Congelación: (D3BC OR D3D9) es el OR de las banderas +$15 de ambos jugadores; el bit 2 lo activa el matraz verde.
c $B8AB Enemigo tipo 0: caminante en el suelo
D $B8AB Se mueve 1 unidad (2 px) por ciclo en la dirección +$07 (+1 derecha, $FF izquierda) mientras haya casilla libre a ese lado (#R$C19C, bit 1 = derecha, bit 3 = izquierda). No comprueba el suelo: no cae. Al chocar invierte la dirección. Animación cada 4 ciclos (D989=0): derecha frames $24-$25, izquierda $26-$27. VERIFICADO.
c $B90D Enemigo tipo 1: caminante con gravedad
D $B90D Si hay vacío debajo (bit 2 de E) cae 4 px por ciclo. Si no, camina como el tipo 0 (1 unidad por ciclo, animación cada 2 ciclos): derecha frames $28-$2B, izquierda $2C-$2F. Al chocar invierte la dirección (el código siempre pone el frame $2C tras girar; el siguiente paso de animación lo corrige). VERIFICADO (cae por el borde de una plataforma).
c $B984 Enemigo tipo 2: burbuja que oscila verticalmente
D $B984 (+$09,+$0A) = puntero a la tabla de ruta $D99B (pares frame, dy terminados en $FF). Cada ciclo pone el frame y suma dy a y: -4,-4,-4,-2,-2,+2,+2,+4,+4,(+4) = ida y vuelta de 16 px. Al llegar a $FF vuelve a $D99B. VERIFICADO.
c $B9A9 Enemigo tipo 3: burbuja que oscila (amplitud mayor)
D $B9A9 Igual que el tipo 2 pero con la tabla $D9B0: pares (frame,dy) en x fijo: dy -4,-4,-4,-2,-2,-2,+2,+2,+2,+4,+4,+4 (12 pasos, frames $30-$31). Es una lectura determinista de la tabla. [VERIFICADO en el simulador (levtest.py, nivel 5): frames $30/$31 y la y oscila entre 112 y 94]
c $B9CE Enemigo tipo 4: gota
D $B9CE Máquina de estados por frame (+$02): $46 = oculta (cada ciclo 10% de probabilidad de pasar a $32); $32-$34 = formándose (frame+1 cada 4 ciclos); $35 = cayendo (y += 4 por ciclo hasta que no haya vacío debajo, entonces $36); $36 = salpicadura; $37 = reinicio: y = (+$0A) (y original), frame $46. Es inofensiva mientras está oculta ($46). VERIFICADO.
c $BA25 Enemigos tipos 5 y 6: lanzadores de proyectiles
D $BA25 Anima la boca con la tabla $D9C9 (40 entradas, índice +$09; el tipo 6 suma $12 al frame) y, cuando el índice es $0C, dispara: +$07 pasa a ser el número de casillas recorridas por el proyectil. El proyectil es una casilla del mapa ($3C + tipo = $41 para el tipo 5 que viaja a la derecha y $42 para el 6 que viaja a la izquierda): cada ciclo borra la casilla anterior (redibujando el fondo), avanza 8 unidades (1 casilla), y se detiene al salir de pantalla (x >= $6A) o chocar con una casilla no vacía. Las casillas $41/$42 quitan 1 de energía por ciclo al jugador. VERIFICADO el ciclo de animación y el disparo.
c $BAE6 Enemigo tipo 7: disco que rebota en vertical
D $BAE6 Frames $47,$48,$49,$48 (tabla $D9F1) cada 2 ciclos. Se mueve 4 px por ciclo: +$07 con bit 7 activo = sube, en caso contrario baja; al toparse con una casilla ocupada invierte. VERIFICADO.
c $BB37 Enemigo tipo 8: criatura que sigue las paredes
D $BB37 Frames de las tablas $D9F5/$DA03 (se elige una al azar al llegar a $FF). Rumbo +$07 (0 arriba, 1 derecha, 2 abajo, 3 izquierda): avanza 1 unidad (horizontal) o 2 px (vertical) por ciclo mientras la casilla esté libre. Si se bloquea gira: +$07 = (+$07 +/-1) AND 3; el sentido de giro (operando autoparcheado en $BBBE) se invierte cada 8 giros (+$0D). VERIFICADO.
c $BBCD Enemigo tipo 9: proyectil que cruza la pantalla hacia la izquierda
D $BBCD Avanza 4 unidades (8 px) por ciclo a la izquierda y varía y en 4*(+$07)-12 px. Al salir (x<0 o y >= $91) reaparece en el punto de origen (+$0B,+$0A), incrementa +$07 (0-6, abanico de 7 pendientes) y suena $DCA8. VERIFICADO.
c $BC0F Enemigo tipo $0A: torbellino
D $BC0F Cada ciclo suma a x (-2 + dx) e y (+$07 + dy) un par de la tabla circular $D968 (16 pares, índice +$09 AND $0F): deriva hacia la izquierda describiendo círculos. Al salir de pantalla reaparece en (+$0B,+$0A) con +$07 = aleatorio(11)-5 e índice 5, con sonido. VERIFICADO.
c $BC69 Enemigo tipo $0B: pelota que bota (y generador de anillos en el nivel 50)
D $BC69 Llama a #R$BC99 (movimiento). En el nivel D39A=$32 (50) la llama dos veces y, con un 6% de probabilidad por ciclo, deja una casilla de anillo $2F en su posición si está vacía. VERIFICADO el movimiento.
c $BC99 Movimiento de la pelota (tipo $0B)
D $BC99 x += +$07 (rebota en x >= $6A cambiando de signo); y = tabla $DA14[+$09] (arco parabólico $90 -> $32 -> $90 terminado en $FF), +$09 avanza cada ciclo.
c $BCCF Enemigo tipo $0C: disparo del jefe
D $BCCF Si x < $6A vuela hacia la izquierda 2 unidades por ciclo. En espera (x >= $6A) dispara solo cuando el frame del enemigo 0 ($D3FA, primer segmento del jefe) está en $9A-$9F y ese enemigo está activo (x <> $FF): x = $48-2 = $46, suena $DCA8. Al salir por la izquierda x pasa de 0 a $FE (>= $6A) y vuelve a quedar en espera; la y es la de la cabecera del nivel. [VERIFICADO en el simulador (levtest.py, nivel 60, mundo 6): el disparo aparece en x=$46 justo cuando el primer segmento del jefe llega al frame $9A, avanza 2 unidades por ciclo y al salir queda en espera con x=$FE]
c $BCFC Enemigo tipo $0D: proyectil en espiral de 8 direcciones
D $BCFC Si sale de pantalla reaparece en (+$0B,+$0A). Cada ciclo se mueve según el contador compartido D07A (0-7): arriba, arriba-derecha, derecha, abajo-derecha, abajo, abajo-izquierda, izquierda, arriba-izquierda (pasos de 4 en x y 8 en y). El contador D07A lo comparten todos los enemigos de este tipo. VERIFICADO.
c $BD99 Enemigo tipo $0E: proyectil diagonal
D $BD99 x -= 2 por ciclo; y += 4*D078 (D078 = 0..3 compartido). Si sale (x<0 o y >= $91) reaparece en (+$0B,+$0A) con sonido. VERIFICADO.
c $BDD2 Enemigos tipos $0F-$11: partes animadas de una criatura de 3 sprites
D $BDD2 Cada 2 ciclos toma el frame de la tabla apuntada por (+$09,+$0A) con índice +$07 ($DA3F, $DA68 o $DA91, terminadas en $FF): las tres partes usan frames $5B-$6F; las tres tablas ($DA3F, $DA68, $DA91) tienen 12 pasos de reposo (frame $46 = invisible) y después una secuencia de animación de 28 pasos (p. ej. $5B,$5E,$5E,$5E,$61...). Lectura determinista de tabla. [VERIFICADO en el simulador (levtest.py, nivel 52): las tres partes siguen $5E,$61,$6A,$6D... y el segundo trío espera en $46 (invisible) como indica la tabla]
c $BDFA Jefes y serpientes (tipos >= $12)
D $BDFA Un registro "cabeza" gobierna a (+$0D) registros siguientes: toma el frame de una tabla de animación (+$09,+$0A / índice +$07, cada 2 ciclos) y asigna a los segmentos consecutivos los frames f+1, f+2, ... (escribiendo en +$18 de los registros siguientes) y descuenta esos registros del contador del bucle (no se despachan por separado). En el mundo 4 (D98B=4) ademas desplaza 9 registros en vertical con la tabla de ondas $DB7A. Las tablas de animación de cada jefe (por mundo, apuntadas por los bytes +6/+7 de $DABA: $DAFA, $DB17, $DB2C, $DB4F, -, $DBA5, -, $DC19) contienen el frame de la cabeza (valores $70-$AF = sprites propios del mundo, en grupos de 9 consecutivos, uno por segmento); el segmento k usa el frame cabeza+k y su posición (x,y) es fija, la de la cabecera del nivel. En el mundo 3 los 8 segmentos forman dos bloques 2x2 de 32x32 px (las mandíbulas) superpuestos a la imagen grande. [VERIFICADO en el simulador (bosstest.py, mundos 1-8): todos los jefes cargan con la vida de $DC3B (24, 32, $FF, $FF, $FF, 48, 0, 64), animan sus segmentos según su tabla; el orbe baja la vida en los mundos 1, 2 y 8; en los mundos 3-5 ($FF) no se les puede dañar. Con la vida del jefe del mundo 8 a 0 se ejecuta #R$AD45 (finaltest.py). Ensamblado en assets/jefes_animados]
c $BE7B Poner / quitar bloque
@ $BE7B label=BLOQUE
D $BE7B Se ejecuta cuando el bit 4 de D98A está activo (el jugador SOLTÓ la tecla de bloque; ver #R$CCB5). Casilla destino: x AND $F8, y AND $F0. Mirando a la derecha (+$07=1): se rechaza si x >= $62, destino +8 (otro +8 si x AND 7 >= 2); a la izquierda: se rechaza si x < 8, destino -8. Con frame >= $0B (agachado) la fila destino es la inferior (y+16; se rechaza si y=$90). Se rechaza si el bloque solaparía con la esfera, con el otro jugador o con un enemigo. Casilla vacía -> $45 (animación de creación $45,$46,$47,$48 cada ~3 interrupciones; $48 = bloque rojo del jugador). Casilla $48 -> $49 (animación de destrucción $49-$4C, luego $00). Casillas especiales $2E y $58-$5A tienen efectos propios.
N $BE7B Se sale si es el nivel $50 (final) y D39B=0 (en esa pantalla no se pueden poner bloques). Si +$0A (animación de bloque en curso) <> 0 se salta a #R$BF71 para avanzar la animación. Si no, se sale si D98A bit 4 (tecla de bloque, ya filtrada por el tiempo de pulsación en #R$CCB5) no está activo o si +$15 bit 7 está activo [VERIFICADO en el simulador: con +$15 bit 7 = 1 no se crea ningún bloque; lo activa la casilla $3E (frasco rosa)].
N $BE9A Casilla destino: E = x AND $F8 (alineado a casilla), D = y AND $F0. Mirando a la derecha (+7=1): no hace nada si x >= $62; E += 8 y, si x AND 7 >= 2 (el jugador ya ocupa parte de la casilla siguiente), E += 8 más. Mirando a la izquierda: no hace nada si x < 8; E -= 8. Si el frame es >= $0B (agachado): no hace nada si y = $90 (suelo del tablero) y D += 16, es decir la fila inferior. [verificado por lectura; contrastar con el juego]
N $BEE9 Comprobaciones de solapamiento (#R$BFBA): el bloque no se crea si en esa casilla está el OTRO jugador, la esfera o cualquier enemigo (#R$BFD7). Se usa D91E para saber qué jugador es el actual (HL = posición del otro).
N $BF06 Se calcula la dirección de la casilla en el mapa con #R$C037 y su dirección en el búfer de pantalla. Casilla vacía (0): se coloca $45 (primer paso de creación). Casilla $48 (bloque rojo): se pone $49 (primer paso de destrucción). Cualquier otra: #R$BF8D. Se guardan en el registro del jugador el valor (+$0A), la dirección del mapa (+$0B/$0C), la del búfer (+$0D/$0E) y la de atributos (+$1B/$1C); suena DC9C.
N $BF3D Redibujo de la casilla: primero se pinta la casilla de la capa de fondo (+$8C, $DEE6) y luego, con #R$CB2D, la casilla actual del mapa. Animación #R$BF71: en cada ciclo el código de la casilla aumenta en 1: $45->$46->$47->$48 (queda como bloque rojo, +$0A se pone a 0 al llegar a $48) y $49->$4A->$4B->$4C (al llegar a $4C se vacía la casilla a 0). [verificado con blocktest.py en sesiones anteriores]
N $BF8D La acción de bloque sobre otras casillas: $2E -> D39B=$42 y se reinicia el bucle principal (#R$AAC7) [VERIFICADO en el simulador: D39B=$42 y se carga el mapa especial de $9550 (sala de bonus)]; $58 (flecha de diamante) pone la velocidad vertical de la esfera D91F=$FC (-4, sube), $5A la pone a +4 (baja) y $59 invierte su signo. Otras casillas: nada. [VERIFICADO en el simulador: $58 -> D91F=$FC, $5A -> $04, $59 invierte el signo]
N $BFBA Prueba de solapamiento: con HL=(x,y) de una entidad y DE=(x,y) de la casilla devuelve A=1 (NZ) si |x1-x2| < 8 y |y1-y2| < 16, A=0 (Z) si no. $BFD7 aplica esta prueba a los enemigos (IX desde $D3F8, 22 bytes cada uno).
N $BFF6 Dibuja una casilla (código en A) en el búfer de pantalla DE: copia 16 líneas de 2 bytes desde $9B00+36*A (salto de línea de 29 bytes en el búfer), y después los 4 bytes de atributos (2+2 en el búfer de atributos HL', stride 32), con el bit 7 borrado (AND $7F) [suposición: bit 7 = marca de uso propia del juego].
N $C037 Dada la posición (E=x, D=y) devuelve DE = dirección del mapa $DE5A+14*(y>>4)+(x>>3) y deja en D08C la dirección del búfer de atributos ($F1D4+...) y en HL' la del búfer de pantalla ($DF72+29*y+x/4...). Lo usa la colocación de bloques y la recogida de casillas.
c $BFBA Prueba de solapamiento
D $BFBA Entradas: HL = (x,y) de una entidad, DE = (x,y) de otra. Z=0 (NZ) si |dx| < 8 unidades (16 px) y |dy| < 16 px.
c $BFD7 Solapamiento con enemigos
D $BFD7 Compara (E,D) con todos los enemigos activos (x <> $FF). Devuelve Z=0 si hay solapamiento, con IX apuntando al enemigo.
c $BFF6 Redibujar una casilla
D $BFF6 Redibuja la casilla de la dirección de mapa DE con el código A en el búfer de pantalla ($DF72) y los atributos ($F1D4).
c $C037 Dirección de mapa de una posición
D $C037 Convierte (x,y) de la entidad en la dirección dentro del mapa $DE5A: índice = (y>>4)*14 + (x>>3).
c $C092 Colisión del jugador con las casillas
D $C092 Como #R$C19C pero para el jugador: las casillas >= $44 le bloquean, mientras que la esfera es bloqueada por todas las >= $2D excepto la $43.
N $C092 Devuelve en E los lados libres (empieza en $FF y se borran bits): bit0 arriba, bit1 derecha, bit2 abajo, bit3 izquierda. Posición del tile en el mapa: HL = $DE5A + 14*(y>>4) + (x>>3) (el tablero es de 14 columnas; x en unidades de 2 px, 8 unidades = 1 casilla de 16 px). Un lado se bloquea si la casilla vecina vale >= $44. El jugador ocupa 1 casilla si x es múltiplo de 8 / y múltiplo de 16 y hasta 2x2 si no está alineado; por eso se comprueban las casillas siguientes cuando (x AND 7) <> 0 o (y AND 15) <> 0.
N $C0BA Izquierda: x=0 o casilla a la izquierda >= $44 borra el bit 3 (también la inferior-izquierda si y no está alineado). $C0E4 Derecha: x>=$68 o casilla derecha. $C115 Arriba: y=0 o casilla superior. $C167 Abajo: y>=$90 o casilla inferior.
N $C19C Versión para la esfera: bloquea con casillas >= $2D salvo la $43; además pone D=1 si la casilla vecina es la $44 (salida): en los lados izquierdo/derecho siempre, y para la casilla superior sólo si D91F tiene el bit 7 a 1, es decir, si la esfera SUBE ($C264-$C272; con D91F positivo se salta el LD D,1). [VERIFICADO ejecutando $C19C con D91F=$FC (D=1) y D91F=$04 (D=0) con la casilla $44 encima; ultimos.py. Corrige un comentario anterior que decía bit 7 a 0]
c $C19C Colisión de la esfera/enemigos con las casillas
D $C19C Devuelve en E los bits de casillas libres (0 arriba, 1 derecha, 2 abajo, 3 izquierda) y D=1 si toca la salida $44.
c $C2DC Dibujar entidades (guardar fondo y pintar sprites)
@ $C2DC label=DIBUJAR_ENTIDADES
D $C2DC Para cada entidad (enemigos, esfera, J1, orbe 1, J2 con frames +13, orbe 2) llama a #R$C384.
N $C2DC Orden de dibujo (el último queda encima): enemigos (de 0 a n-1), esfera, jugador 1, orbe del jugador 1 (sólo si +$15 bits 3-4, o sea D3BC AND $18 <> 0), y con 2 jugadores el jugador 2 y su orbe. El jugador 2 usa el mismo conjunto de frames desplazado en +$0D (la maga): $C318 suma $0D al frame justo antes de dibujar y lo resta justo después [verificado en el código y en las hojas de sprites: frames $0E-$19 son la maga].
N $C338 Orden de borrado: inverso al de dibujo (orbe 2, jugador 2, orbe 1, jugador 1, esfera, enemigos del último al primero con IX -= $16), para que cada fondo guardado se restaure correctamente aunque los sprites se solapen.
c $C338 Borrar entidades (restaurar fondo)
D $C338 Restaura el fondo guardado de cada entidad (en orden inverso) mediante #R$C45D.
c $C384 Dibujar un sprite 16x16 con máscara
D $C384 Entrada: IX = registro de entidad. Si x >= $6A o y >= $91 no se dibuja. Sprite = $6100 + frame*32. Genera la máscara con las tablas $5B00/$5C00, desplaza el sprite según x AND 3 (cuatro posiciones de subpíxel dentro del byte), calcula la dirección en el búfer ($DF72, 29 bytes por línea) y la guarda en +5/+6, y mezcla con AND/OR. El fondo original se guarda en el búfer de la entidad (+3/+4).
c $C45D Restaurar el fondo de una entidad
c $C488 Mezclar un bloque con máscara en el búfer
D $C488 Rutina genérica: C=ancho en bytes, B=alto, DE=datos (máscara,dato alternados), HL=destino.
c $C49F Limpiar el área de juego
D $C49F Pone a 0 las 160 líneas del búfer y atributos $47 (blanco sobre negro).
c $C4D5 Interrupción: sonido
@ $C4D5 label=INTERRUPCION_SONIDO
D $C4D5 Rutina de interrupción (IM 2, vía $FDFD). Si hay un descriptor de sonido activo ($D076 <> 0) toca un tramo de onda cuadrada con el altavoz (OUT ($FE), bit 4). Descriptor de 6 bytes: +0 periodo, +1 número de ciclos, +2 incremento del periodo por interrupción, +3 interrupciones restantes, +4 periodo de reinicio, +5 cuenta de reinicio. Al terminar pone $D076=0.
c $C524 Nivel completado
@ $C524 label=NIVEL_COMPLETADO
D $C524 Se llega al tocar la esfera la salida $44, al recoger la casilla $3A o al conseguir 50 anillos. NO suma bonus (corrección: no hay puntuación aquí): restaura el intercambio de casillas del mundo 7 si el nivel es $46, avanza D39A (con $4E salta el $4F: $4E+2=$50; en consecuencia el nivel 79 NO EXISTE, ni tampoco el 81-89: los datos de esas posiciones son relleno; verificado con colortest.py), y con D39A=$51 va a #R$AD45 (fin del juego). Pone D39B a 0 y vuelve al bucle principal #R$AAC7 (que carga el nivel). [VERIFICADO con niveltest.py (la carga de cinta se simula en $D01F): 3->4; 9->10 carga el mundo 1 de cinta; 69->70 carga el mundo 7 y hace el intercambio de las casillas $18-$2B (bitmaps de $6F00, atributos = F79B); 70->71 restaura las casillas originales; 78->80 (carga el mundo 8); 80->81 llega a $AD45; con D39B=$57 avanza 2 niveles y con $42 uno.]
N $C546 D39B es el selector de pantalla especial: 0 = nivel normal, $42 = mapa especial n.º $14 en $9550 (se entra pulsando bloque sobre una casilla $2E, #R$BF8D), $54 = entrenamiento (menú tecla 3), $57 = mapa especial $15 en $95DC (tras la copa $40). Si el valor era $57 se avanza además un nivel más ($C554). [leído; el contenido de las pantallas especiales aún no se ha extraído visualmente]
N $C563 Carga de nivel: en el nivel $50 con D39B=0 se ponen los reintentos a 0 (D2E8) y los dos jugadores en (+$0C? x=$18,y=$C0) [suposición sobre direcciones D3BC/D3C0]. Con D39B<>0 y <>$54 se copia el mapa especial ($9550 o $95DC) a $DE5A y se salta a #R$C66E. Si no, se calcula el mundo = nivel/10 (bucle $C5B4); si cambia, #R$CFB3 carga el bloque de esa cinta/mundo y, para el nivel $46, se intercambian 20 casillas ($71D0 <-> $9E60, 720 bytes) y se cambia el atributo con el color de fondo $F79B.
N $C603 Posición del mapa: se calcula el número de nivel local n = nivel - 10*mundo y se apunta a $8A60 (1 jugador) o $8FD8 (2 jugadores) + 140*n; se copian 140 bytes a $DE5A. A continuación $C64E recorre las cabeceras de nivel saltando n entradas (cada cabecera = 8 bytes + 1 + 4*enemigos) hasta localizar la del nivel; $C66E lee el fondo (+4B00 base) a $DEE6, aplica relleno de color fijo en los niveles $0A, $14 y $32, la posición de la esfera -> D3F0, del jugador 1 -> D3A7 y del jugador 2 -> D3C4 (FFFF en un jugador). [verificado contra extraer_niveles.py]
c $C563 Cargar nivel
@ $C563 label=CARGAR_NIVEL
D $C563 Copia el mapa del nivel (140 bytes = 14x10 casillas) al mapa de trabajo $DE5A: mapas de 1 jugador en $8A60+140*n y de 2 jugadores en $8FD8+140*n (n = D39A - 10*D98B). Los niveles de 1 y 2 jugadores son DISTINTOS. Si el nivel pertenece a otro mundo (D98B <> D39A/10) llama a #R$CFB3 para cargarlo de la cinta. Copia 140 bytes de capa de fondo ($4B00 + desplazamiento leído de la cabecera) a $DEE6. Después interpreta la cabecera del nivel (#R$C65B). Niveles especiales: D39B=$42 y otros usan los mapas de $9550 y $95DC y las cabeceras 20 y 21 de la tabla.
c $C64E Saltar cabeceras de nivel
D $C64E Avanza HL por B registros de cabecera (8 + 1 + 4*enemigos bytes cada uno).
c $C65B Interpretar la cabecera del nivel
@ $C65B label=CABECERA_NIVEL
D $C65B En los mundos 1-8 el primer nivel (D39A múltiplo de 10) es un nivel de jefe/guardián (ver #R$C9F5). Registro: fondo (2 bytes), esfera (x,y), J1 (x,y), J2 (x,y, $FFFF si 1 jugador), nº de enemigos y, por enemigo, x,y,tipo,frame. Inicializa los registros de esfera ($D3F0), jugadores ($D3A7/$D3C4) y enemigos ($D3F8, 22 bytes) con sus estados iniciales y rutas. Dibuja el marcador (reintentos, energía, nivel, puntuación).
N $C6D2 Estado inicial común del nivel: D989=0, frames/animación de jugadores a 0, tabla de puertas D07C/D07F/D082=0, partículas DCB4=0, anillos D07B=0, banderas +$15 de los jugadores conservan sólo los bits 3-4 (poder mágico) más el bit 1 (escudo) si hay invencibilidad (D079), D91F=4 (velocidad de caída), esfera con frame $1A, direcciones $FF, D920=$1014.
N $C730 Lista de enemigos: D52C = número. Por cada uno la cabecera aporta x, y, tipo y frame. Inicialización por tipo: 2 y 3 reciben el puntero a su tabla de ruta ($D99B/$D9B0); 4 guarda su y original en +$0A; 5 y 6 ignoran el frame de la cabecera y empiezan en un índice aleatorio (0-39) de la tabla $D9C9 con el proyectil parado; 8 elige al azar la tabla $D9F5/$DA03 e ignora el frame; el resto usa el frame de la cabecera y dirección +$07=1 (derecha).
N $C7EE Segunda pasada sobre los enemigos: tipos 9-$0E guardan su origen (x en +$0B, y en +$0A) para reaparecer; el tipo $0B arranca en un punto aleatorio (0-29) de su arco y con velocidad horizontal +2 o -2 unidades; los tipos $0F-$11 son un grupo de 3 registros consecutivos (cabeza, torso, pies) con índice de animación aleatorio común y tablas $DA3F/$DA68/$DA91; los tipos >= $12 son jefes: el byte "frame" de la cabecera es el NÚMERO DE SEGMENTOS que siguen a la cabeza, la tabla de animación sale de $DABA (+6/+7 de la entrada del mundo) y los segmentos reciben frames consecutivos.
N $C931 Vida del jefe: DC3A = tabla $DC3B[mundo] = 0, $18, $20, $FF, $FF, $FF, $30, 0, $40 para los mundos 0-8 ($FF = el orbe no le hace daño; 0 = sin jefe). Se resta 1 por cada contacto del orbe mágico (#R$B099).
c $C9D7 Pintar un icono de 2 columnas
D $C9D7 Copia filas de 2 bytes del icono HL a la pantalla DE, bajando de línea correctamente (cálculo de dirección de pantalla del Spectrum).
c $C9F5 Dibujar el nivel completo
D $C9F5 Dibuja el nivel completo: primero la CAPA DE FONDO ($DEE6, papel pintado 14x10 con #R$BFF6) y encima el MAPA ($DE5A, con #R$CB2D) mediante #R$CAFE; en el nivel $50 desplaza antes la fila de fondo. Al final, si hay jefe activo ($DC3A<>0) dibuja el jefe del mundo (tabla $DABA, 8 bytes por mundo) y decoraciones propias de los mundos 3, 4 y 8.
N $C9F5 En el nivel $50 se desplazan 5 casillas del fondo (LDDR/LDIR en $CA05) para dejar libre una franja [leído, efecto exacto sin comprobar]. $CA22: se pinta la capa de fondo ($DEE6) con $BFF6 y luego el mapa ($DE5A) con $CB2D, parcheando el puntero de llamada en $CB13.
N $CA3C Imagen del jefe: si la vida de jefe DC3A <> 0, D39B = 0, el mundo (D98B) <> 0 y el nivel es 10*mundo (nivel de jefe de cada mundo: 10, 20, ..., 80), se lee la entrada del mundo de la tabla $DABA (8 bytes: ancho en bytes, alto en filas, dirección de los datos, dirección de destino en el búfer $DF72, 2 bytes sin identificar) y se dibuja con #R$C488 una IMAGEN GRANDE con máscara (pares máscara,dato) como parte del escenario. Estas imágenes viven en la zona $6F00-$85FF del bloque de cada mundo, que por eso parecía 'basura' si se interpretaba como sprites 16x16. Mundo 3: segunda imagen (otro bloque 12x69 en $7A78 -> $E9D1, parche en $CA83); mundo 4: pinta atributos blancos ($CA8F); mundo 8: copia más atributos ($CAD5). Extraídas en assets/jefes/. [verificado: imágenes reconocibles]
c $CAED Copiar filas de gráfico
c $CAFE Dibujar el mapa de casillas
D $CAFE Recorre IX (10 filas x 14 columnas = 140 bytes) y para cada código llama a la rutina cuyo puntero está parcheado en $CB13 (#R$BFF6 para la capa de fondo, #R$CB2D para el mapa del nivel).
c $CB2D Dibujar una casilla 16x16
D $CB2D A = código de casilla del mapa. Los códigos 0, $41-$43 y $4C se dibujan con máscara en #R$CB40 (el resto se delega en #R$BFF6, sin máscara, que sobrescribe todo). Gráfico de casilla = $9B00 + 36*código (32 bytes de bitmap, 16 filas x 2 bytes, + 4 bytes de atributos).
c $CB7D Efecto de pantalla: fundido a negro
D $CB7D Copia los atributos actuales ($5800, 768 bytes) a $F192 y durante 7 pasos (una interrupción por paso con #R$CCB2) resta 1 al color de tinta y 1 al de papel de cada atributo hasta llegar a 0: la pantalla se apaga a negro. Parchea el byte $CD93 con $C9 (RET) para que #R$CD43 deje de copiar atributos mientras dura el efecto (en $CC04/$CCAE se restaura a $01).
c $CBBA Efecto de pantalla: aparecer
D $CBBA Inverso de #R$CB7D: durante 8 pasos acerca cada atributo de la pantalla al guardado en $F192 (primero la tinta/papel poco a poco: +1 en brillo de cada componente hasta igualar). Al terminar restaura $CD93 a $01.
c $CC0A Efecto de pantalla: fundido rápido
D $CC0A Fundido rápido a blanco: silencia el sonido ($D076=0), parchea $CD93 y sube 7 pasos tinta y papel hasta 7 (blanco), cambiando el borde con OUT ($FE) en cada paso. Se usa al morir un jefe y al terminar el nivel.
c $CC5A Efecto de pantalla: aparición con borde
D $CC5A Aparición desde blanco a los atributos guardados en $F192, con borde decreciente (OUT ($FE) con el contador); restaura $CD93=$01.
c $CCB2 Esperar una interrupción (EI + HALT)
c $CCB5 Leer los controles del jugador en curso
N $CCB5 Lectura de controles del jugador IY a D98A (E): 5 teclas (+$0F..+$13) probadas con #R$CDD3 (Z = pulsada). Bit 0 arriba, 1 derecha, 2 abajo, 3 izquierda, 4 acción de bloque. Si es el jugador 1 y D39E bit 0 (esquemas Kempston) se lee el puerto $1F en $CD1D: bit0 derecha, bit1 izquierda, bit2 abajo, bit3 arriba, bit4 disparo.
N $CCFC Tecla de bloque: mientras está pulsada se incrementa +$14 (máximo $40); al SOLTARLA ($CD0B), si +$14 <> 0 se activa el bit 4 de E y el contador vuelve a 0. Es decir la acción de bloque ocurre al soltar la tecla y +$14 guarda cuántos ciclos estuvo pulsada (usado por #R$B099 para el lanzamiento del orbe). [verificado con simulación en sesiones anteriores]
@ $CCB5 label=LEER_CONTROLES
D $CCB5 Construye en E el byte de entrada y lo guarda en D98A. Bits: 0 arriba, 1 derecha, 2 abajo, 3 izquierda, 4 acción de bloque. Las 5 teclas de cada jugador están en su registro (+$0F..+$13). Con Kempston (D39E bit 0 y J1) se lee el puerto $1F. La tecla de bloque (+$13) funciona por flanco de bajada: mientras está pulsada el contador +$14 sube hasta $40; al soltarla, si el contador es > 0, se activa el bit 4 y el contador vuelve a 0. [VERIFICADO con kempstontest.py: Kempston bit0 = derecha, bit1 = izquierda, bit2 = abajo, bit3 = arriba, bit4 = disparo (acción de bloque); sólo lo usa el jugador 1.]
c $CD43 Volcar el búfer a pantalla
N $CD43 Vuelca el búfer de pantalla a la pantalla real: para cada una de las 160 líneas (tabla DD1A de direcciones) copia 28 bytes con 28 LDI desde $DF72 (el búfer usa 29 bytes por línea, se salta el último) y después copia 768 bytes de atributos desde $F192 a $5800 con un LDIR. 28 bytes = 14 casillas de 16 px.
D $CD43 Copia las 160 líneas del búfer ($DF72, 28 bytes por línea) a la pantalla con 28 LDI por línea y copia los atributos de $F192 a $5800 (ver CD93).
c $CD9F Número aleatorio
N $CD9F Generador pseudoaleatorio: A = límite N; devuelve en A un valor 0..N-1. Estado de 16 bits en D085 (se incrementa y se mezcla con desplazamientos y sumas con acarreo, $CDC9-$CDD0), y el resultado se escala por multiplicación de 8 bits (bucle ADD HL,HL / ADD HL,DE: A = (rand8 * N) >> 8). Se usa en partículas, bloques aleatorios y enemigos. [leído]
D $CD9F Entrada A = máximo; salida A = valor 0..A-1 con un generador congruencial con semilla $D085.
c $CDC9 Auxiliar del generador aleatorio
c $CDD3 Probar una tecla
@ $CDD3 label=PROBAR_TECLA
D $CDD3 Entrada A = código de tecla = 8*(4-bit) + (7-semifila). Devuelve Z (A=0) si la tecla está pulsada. Semifilas: 0 $FE (CAPS..V), 1 $FD (A..G), 2 $FB (Q..T), 3 $F7 (1..5), 4 $EF (0..6), 5 $DF (P..Y), 6 $BF (ENTER..H), 7 $7F (ESPACIO..B).
c $CDF5 Cambiar la energía
@ $CDF5 label=ENERGIA
D $CDF5 Entrada C = incremento con signo. Sin efecto si el escudo está activo (bit 1 de +$15). Energía D3EF limitada entre 0 y 100; actualiza el tono del sonido de energía ($DC8A) y el marcador (#R$CE2D).
c $CE5C Marcador de poder mágico
D $CE5C Dibuja la barra de temporizador del poder mágico (+$19) del jugador en curso en $4080 (J1) o $40C0 (J2).
c $CE98 Imprimir el número de nivel (2 dígitos)
c $CEC1 Imprimir la puntuación (5 dígitos)
c $CEFB Dividir DE y escribir un dígito ASCII
c $CF0C Imprimir un texto descriptor
@ $CF0C label=IMPRIMIR_TEXTO
D $CF0C Interpreta una cadena en IX: $00 x y = posición (columna = (x-8)/2, fila = y); $01 a = atributo; $FF = fin; otro = carácter a pintar con #R$CF82.
c $CF6F Pintar atributo en la posición actual
c $CF82 Dibujar un carácter 8x8
D $CF82 Fuente en $F592 (ASCII-32 * 8 bytes).
c $CFB3 Cargar un mundo desde cinta
@ $CFB3 label=CARGAR_MUNDO
D $CFB3 Muestra SEARCHING FOR n, carga con la rutina de la ROM $0562 (LD-BYTES) primero una cabecera de 17 bytes ($D031: tipo, nombre de 10 caracteres, longitud, dirección de inicio) y, si el nombre es el del mundo esperado (D98B+'0'), el bloque de datos en la dirección de la cabecera. VERIFICADO con la cinta TZX: cada mundo ('0'..'8') es un bloque estándar de 11264 bytes que se carga en $6F00-$9AFF; los nombres son un carácter ASCII (D98B+$30). [VERIFICADO con tapetest.py usando la ROM real: la señal EAR se genera desde el TZX; con una cinta que empieza por un bloque de otro mundo, el juego lo rechaza (compara el nombre de la cabecera con D98B+$30) y carga el mundo pedido; el contenido de $6F00 coincide byte a byte con el bloque de la cinta (11264 bytes).]
c $D01F Llamar a LD-BYTES de la ROM
b $D031 Cabecera de cinta (17 bytes)
D $D031 Zona donde LD-BYTES carga la cabecera: tipo, nombre (10), longitud, dirección de inicio, 2 parámetros. Ver #R$CFB3.
B $D031,1 Tipo
T $D032,10 Nombre del bloque
W $D03C,2 Longitud y dirección de inicio
B $D040,2
b $D042 Texto SEARCHING FOR
B $D042,3,3 Posición (columna*2+8, fila)
T $D045,14
B $D053,1 Fin
b $D054 Texto FOUND
B $D054,3,3 Posición (columna*2+8, fila)
T $D057,12
B $D063,1 Fin
b $D064 Texto LOADING
B $D064,3,3 Posición (columna*2+8, fila)
T $D067,14
B $D075,1 Fin
b $D075 Variables globales de textos, sonido y puertas
B $D075,1
W $D076,2 Puntero al descriptor de sonido activo (0 = ninguno)
B $D078,1
B $D079,1 Invencible (clave ILLUMINATUS)
B $D07A,1
B $D07B,1 Contador de anillos recogidos (50 = fin de nivel)
B $D07C,9,3 Tabla de puertas (código $55-$57, x, y de barrido)
W $D085,2 Semilla del generador aleatorio
W $D087,2 Dirección de pantalla del carácter
W $D089,2 Dirección del atributo
B $D08B,1 Atributo actual
B $D08C,2
b $D08E Descriptor de la puntuación (5 dígitos)
B $D08E,3,3 Posición (columna*2+8, fila)
T $D091,5
B $D096,1 Fin
b $D097 Descriptor del número de nivel (2 dígitos)
B $D097,3,3 Posición (columna*2+8, fila)
T $D09A,2
B $D09C,1 Fin
b $D09D Texto PLEASE ENTER YOUR NAME
B $D09D,3,3 Posición (columna*2+8, fila)
T $D0A0,22
B $D0B6,3,3 Posición (columna*2+8, fila)
T $D0B9,8
B $D0C1,3,3 Posición (columna*2+8, fila)
B $D0C4,1 Fin
b $D0B6 Texto PLAYER 1/2 (el dígito se parchea en $D0C0)
B $D0B6,3,3 Posición (columna*2+8, fila)
T $D0B9,8
B $D0C1,3,3 Posición (columna*2+8, fila)
B $D0C4,1 Fin
b $D0C5 Texto BEST PLAYERS y créditos
B $D0C5,3,3 Posición (columna*2+8, fila)
T $D0C8,12
B $D0D4,3,3 Posición (columna*2+8, fila)
T $D0D7,23
B $D0EE,3,3 Posición (columna*2+8, fila)
T $D0F1,23
B $D108,1 Fin
b $D109 Tabla de mejores puntuaciones: 5 entradas de 15 bytes (00 x y + 12 caracteres)
B $D109,75,15
b $D154 Texto del menú principal
B $D154,3,3 Posición (columna*2+8, fila)
B $D157,2,2 Atributo
T $D159,19
B $D16C,3,3 Posición (columna*2+8, fila)
T $D16F,19
B $D182,3,3 Posición (columna*2+8, fila)
T $D185,21
B $D19A,3,3 Posición (columna*2+8, fila)
T $D19D,18
B $D1AF,3,3 Posición (columna*2+8, fila)
T $D1B2,3
B $D1B5,3,3 Posición (columna*2+8, fila)
T $D1B8,20
B $D1CC,3,3 Posición (columna*2+8, fila)
T $D1CF,21
B $D1E4,1 Fin
t $D1E5 Textos DARK / LIGHT (se copian en $D1D2)
T $D1E5,10
B $D1EF,0
b $D1EF Esquema de mandos 0: SINCLAIR . SINCLAIR
D $D1EF Códigos de tecla = 8*(4-bit)+(7-semifila), ver #R$CDD3. $25=Q $22=P $26=A $1A=O $20=ESPACIO; $1B,$0B,$13,$03,$23 = 9,7,8,6,0 (Sinclair 2); $0C,$1C,$14,$24,$04 = 4,2,3,1,5 (Sinclair 1).
B $D1EF,3,3 Posición (columna*2+8, fila)
T $D1F2,19
B $D205,1 Fin
B $D206,10,5 Teclas (J1: arriba,der,abajo,izq,bloque | J2: idem)
b $D210 Esquema 1: KEMPSTON . SINCLAIR
D $D210 Códigos de tecla = 8*(4-bit)+(7-semifila), ver #R$CDD3. $25=Q $22=P $26=A $1A=O $20=ESPACIO; $1B,$0B,$13,$03,$23 = 9,7,8,6,0 (Sinclair 2); $0C,$1C,$14,$24,$04 = 4,2,3,1,5 (Sinclair 1).
B $D210,3,3 Posición (columna*2+8, fila)
T $D213,19
B $D226,1 Fin
B $D227,10,5 Teclas (J1: arriba,der,abajo,izq,bloque | J2: idem)
b $D231 Esquema 2: KEYBOARD . SINCLAIR
D $D231 Códigos de tecla = 8*(4-bit)+(7-semifila), ver #R$CDD3. $25=Q $22=P $26=A $1A=O $20=ESPACIO; $1B,$0B,$13,$03,$23 = 9,7,8,6,0 (Sinclair 2); $0C,$1C,$14,$24,$04 = 4,2,3,1,5 (Sinclair 1).
B $D231,3,3 Posición (columna*2+8, fila)
T $D234,19
B $D247,1 Fin
B $D248,10,5 Teclas (J1: arriba,der,abajo,izq,bloque | J2: idem)
b $D252 Esquema 3: KEMPSTON . KEYBOARD
D $D252 Códigos de tecla = 8*(4-bit)+(7-semifila), ver #R$CDD3. $25=Q $22=P $26=A $1A=O $20=ESPACIO; $1B,$0B,$13,$03,$23 = 9,7,8,6,0 (Sinclair 2); $0C,$1C,$14,$24,$04 = 4,2,3,1,5 (Sinclair 1).
B $D252,3,3 Posición (columna*2+8, fila)
T $D255,19
B $D268,1 Fin
B $D269,10,5 Teclas (J1: arriba,der,abajo,izq,bloque | J2: idem)
b $D273 Texto WARP LEVEL
B $D273,3,3 Posición (columna*2+8, fila)
T $D276,11
B $D281,1 Fin
b $D282 Texto GAME OVER
B $D282,3,3 Posición (columna*2+8, fila)
T $D285,10
B $D28F,1 Fin
b $D290 Texto INVINCIBLE
B $D290,3,3 Posición (columna*2+8, fila)
B $D293,2,2 Atributo
T $D295,10
B $D29F,1 Fin
b $D2A0 Borra el texto INVINCIBLE
B $D2A0,3,3 Posición (columna*2+8, fila)
T $D2A3,10
B $D2AD,1 Fin
b $D2AE Borra la línea de mensajes
B $D2AE,3,3 Posición (columna*2+8, fila)
T $D2B1,32
B $D2D1,1 Fin
b $D2D2 Texto ENTER CODEWORD
B $D2D2,3,3 Posición (columna*2+8, fila)
T $D2D5,15
B $D2E4,3,3 Posición (columna*2+8, fila)
B $D2E7,1 Fin
b $D2E8 Reintentos y tablas de claves (codewords)
B $D2E8,1 Reintentos restantes (tecla R)
D $D2E9 Cada entrada (4 bytes): nivel en el que aparece el pergamino $3F que revela la clave (12, 21, 41, 61, 75; lo usa #R$B522), nivel de inicio D39A que da la clave (9, 19, 39, 59, 75; lo usa #R$A983) y puntero al texto. 5 claves de 1 jugador (D2E9) y 6 de 2 jugadores (D2FD); nivel $FF = ILLUMINATUS (invencible).
B $D2E9,20,4 Claves 1 jugador
B $D2FD,24,4 Claves 2 jugadores
b $D315 Clave: RADAGAST
B $D315,3,3 Posición (columna*2+8, fila)
T $D318,8
B $D320,1 Fin
b $D321 Clave: YARMAK
B $D321,3,3 Posición (columna*2+8, fila)
T $D324,6
B $D32A,1 Fin
b $D32B Clave: ORCSLAYER
B $D32B,3,3 Posición (columna*2+8, fila)
T $D32E,9
B $D337,1 Fin
b $D338 Clave: SKYFIRE
B $D338,3,3 Posición (columna*2+8, fila)
T $D33B,7
B $D342,1 Fin
b $D343 Clave: MIRGAL
B $D343,3,3 Posición (columna*2+8, fila)
T $D346,6
B $D34C,1 Fin
b $D34D Clave: GHANIMA
B $D34D,3,3 Posición (columna*2+8, fila)
T $D350,7
B $D357,1 Fin
b $D358 Clave: GLIEP
B $D358,3,3 Posición (columna*2+8, fila)
T $D35B,5
B $D360,1 Fin
b $D361 Clave: MOURNBLADE
B $D361,3,3 Posición (columna*2+8, fila)
T $D364,10
B $D36E,1 Fin
b $D36F Clave: JADAWIN
B $D36F,3,3 Posición (columna*2+8, fila)
T $D372,7
B $D379,1 Fin
b $D37A Clave: GUMBACHACHMA
B $D37A,3,3 Posición (columna*2+8, fila)
T $D37D,13
B $D38A,1 Fin
b $D38B Clave: ILLUMINATUS
B $D38B,3,3 Posición (columna*2+8, fila)
T $D38E,11
B $D399,1 Fin
b $D399 Variables de partida y registros de entidades
B $D399,1
B $D39A,1 Nivel actual (0-based)
B $D39B,1 Modo especial (0 normal, $54 entrenamiento, $42, $46, $4E, $50, $57)
B $D39C,2
B $D39E,1 Esquema de mandos (0-3)
W $D39F,8 Direcciones de pantalla de los iconos de reintentos
D $D3A7 Registro de jugador (29 bytes): +0 x, +1 y, +2 frame, +3/4 búfer de fondo, +5/6 dirección en el búfer, +7 dirección, +8 frame guardado, +9 fase de salto, +A..+E animación de bloque, +F..+13 teclas, +14 contador de la tecla de bloque, +15 banderas, +16/17 puntos, +18 temporizador de escudo, +19 de poder mágico, +1A índice del orbe, +1B/1C puntero de atributos.
B $D3A7,29,29 Jugador 1
B $D3C4,29,29 Jugador 2
B $D3E1,7,7 Orbe mágico jugador 1 (x,y,frame,búfer,dirección)
B $D3E8,7,7 Orbe mágico jugador 2
B $D3EF,1 Energía (0-100)
B $D3F0,8,8 Esfera (x,y,frame,búfer(2),dirección en búfer(2),dirección horizontal)
D $D3F8 Enemigos: hasta 14 registros de 22 bytes: +0 x ($FF = inactivo), +1 y, +2 frame, +3/4 búfer, +5/6 dirección, +7 dirección, +8 tipo, +9.. estado de ruta y aparición.
B $D3F8,22,22 Enemigo 0
B $D40E,22,22 Enemigo 1
B $D424,22,22 Enemigo 2
B $D43A,22,22 Enemigo 3
B $D450,22,22 Enemigo 4
B $D466,22,22 Enemigo 5
B $D47C,22,22 Enemigo 6
B $D492,22,22 Enemigo 7
B $D4A8,22,22 Enemigo 8
B $D4BE,22,22 Enemigo 9
B $D4D4,22,22 Enemigo 10
B $D4EA,22,22 Enemigo 11
B $D500,22,22 Enemigo 12
B $D516,22,22 Enemigo 13
B $D52C,1 Número de enemigos
b $D52D Búfer temporal de sprite y copias de fondo (48 bytes por entidad)
B $D52D,48,3
B $D55D,48,3
B $D58D,48,3 Fondo de J1
B $D5BD,48,3 Fondo de J2
B $D5ED,48,3 Fondo de orbe J1
B $D61D,48,3 Fondo de orbe J2
B $D64D,48,3 Fondo de esfera
B $D67D,48,3 Fondo del enemigo 0
B $D6AD,48,3 Fondo del enemigo 1
B $D6DD,48,3 Fondo del enemigo 2
B $D70D,48,3 Fondo del enemigo 3
B $D73D,48,3 Fondo del enemigo 4
B $D76D,48,3 Fondo del enemigo 5
B $D79D,48,3 Fondo del enemigo 6
B $D7CD,48,3 Fondo del enemigo 7
B $D7FD,48,3 Fondo del enemigo 8
B $D82D,48,3 Fondo del enemigo 9
B $D85D,48,3 Fondo del enemigo 10
B $D88D,48,3 Fondo del enemigo 11
B $D8BD,48,3 Fondo del enemigo 12
B $D8ED,48,3 Fondo del enemigo 13
b $D91D Variables de juego
B $D91D,1 Nº de jugadores
B $D91E,1 Jugador en curso
B $D91F,1 Velocidad vertical de la esfera
W $D920,2 Contador del reloj de arena (suposición)
B $D922,38 Tabla del salto (dy por ciclo)
B $D948,32,2 Órbita del orbe mágico: 16 pares (dx,dy)
B $D968,32,2 Trayectorias circulares (enemigos tipo $0A)
B $D988,1 Kempston presente
B $D989,1 Contador de ciclo (0-3)
B $D98A,1 Entrada del jugador en curso (bits 0-4)
B $D98B,1 Mundo cargado (D39A/10)
B $D98C,1 Pociones recogidas
B $D98D,7 Animación de beber (parte 1)
B $D994,1 Fin
B $D995,5 Animación de beber (parte 2)
B $D99A,1 Fin
b $D99B Ruta del enemigo tipo 2 (burbuja): 10 pares (frame, dy), terminada en $FF. dy: -4 x3, -2 x2, +2 x3, +4 x2 (ver #R$B984)
B $D99B,20,2
B $D9AF,1 Fin ($FF)
b $D9B0 Ruta del enemigo tipo 3 (burbuja de mayor amplitud): 12 pares (frame, dy) y $FF
B $D9B0,24,2
B $D9C8,1 Fin ($FF)
b $D9C9 Animación de los tiradores (tipos 5 y 6): 40 índices de frame ($3D-$46); el disparo se produce en el índice 12 (ver #R$BA25)
B $D9C9,40,8
b $D9F1 Frames del disco vertical (tipo 7): $47,$48,$49,$48
B $D9F1,4
b $D9F5 Animación A de la criatura que sigue paredes (tipo 8), terminada en $FF
B $D9F5,14
b $DA03 Animación B de la criatura que sigue paredes (tipo 8), terminada en $FF
B $DA03,17
b $DA14 Arco de la pelota que bota (tipo $0B): 40 valores de y ($90 -> $32 -> $90) y 3 x $FF de relleno/fin
B $DA14,43,8
b $DA3F Secuencia de frames de la criatura de 3 partes, parte 1 (tipo $0F): 12 pasos de $46 (invisible) + animación, terminada en $FF
B $DA3F,41,8
b $DA68 Idem parte 2 (tipo $10)
B $DA68,41,8
b $DA91 Idem parte 3 (tipo $11)
B $DA91,41,8
b $DABA Tabla de jefes por mundo (8 bytes por mundo 1-8): ancho (bytes), alto (filas), dirección de la imagen grande, destino en el búfer $DF72, puntero a la tabla de animación del jefe (#R$CA3C, #R$C864)
B $DABA,64,8
b $DAFA Tabla de animación del jefe del mundo 1 (frames de la cabeza, $70-$AF), terminada en $FF
B $DAFA,29,8
b $DB17 Tabla de animación del jefe del mundo 2
B $DB17,21,8
b $DB2C Tabla de animación del jefe del mundo 3
B $DB2C,35,8
b $DB4F Tabla de animación del jefe del mundo 4
B $DB4F,43,8
b $DB7A Tabla de ondas del mundo 4: desplazamiento vertical de 9 segmentos (valores con signo, $FF final; ver #R$BE43)
B $DB7A,43,8
b $DBA5 Tabla de animación del jefe del mundo 6
B $DBA5,116,8
b $DC19 Tabla de animación del jefe del mundo 8
B $DC19,33,8
b $DC3A Vida de jefe: $DC3A = vida actual del jefe en el nivel; $DC3B = tabla por mundo 0-8 (0, $18, $20, $FF, $FF, $FF, $30, 0, $40; $FF = no se le puede matar con el orbe, 0 = sin jefe)
B $DC3A,1 Vida actual
B $DC3B,9 Vida inicial por mundo
b $DC44 Búfer de texto introducido (claves y nombres, 13 bytes; el contenido mostrado es basura de arranque)
B $DC44,13,13
b $DC51 Tabla de teclas de #R$AE6B: 26 pares (código de tecla, carácter ASCII) Q W E R T Y U I O P A S D F G H J K L Z X C V B N M; el par 27 (SPACE, ' ') son los bytes $20,$20 de $DC85-$DC86
B $DC51,51,3
b $DC84 Fin de la tabla de teclas: carácter 'M' (par 26), par 27 (SPACE, ' ') y relleno
B $DC84,1 'M'
B $DC85,2 Par 27: SPACE, ' '
B $DC87,3 Relleno
B $DC8A,6 Sonido de energía (el periodo se escribe en CE1E)
B $DC90,6
B $DC96,6
B $DC9C,6
B $DCA2,6 Rebote de la esfera
B $DCA8,6
B $DCAE,6 Explosión
B $DCB4,2 Estado de partículas (DCB4 = contador, DCB5 = número)
B $DCB6,100,5 Partículas (5 bytes cada una)
b $DD1A Tabla de direcciones de línea de pantalla (160 entradas)
W $DD1A,320,2
b $DE5A Mapa de trabajo del nivel (14x10 casillas)
B $DE5A,140,14
b $DEE6 Capa de fondo del nivel (14x10)
B $DEE6,140,14
b $DF72 Búfer de pantalla del área de juego (160 líneas x 29 bytes)
B $DF72,4640,29
b $F192 Copia de atributos del área de juego (24x32 pero se usa 20x28)
B $F192,768,32
b $F492 Iconos del HUD: 8 iconos de 16x16 (32 bytes cada uno); $F4B2 y $F516+ forman la barra de energía, $F57A/$F586 la del poder mágico
B $F492,$0100,32
b $F592 Fuente de caracteres 8x8 (ASCII 32.. x 8 bytes)
B $F592,520,8
B $F79A,1 Byte sobrante
b $F79B Color de tinta de los fondos del menú: 1 = oscuro (azul), 5 = claro (cian); lo alterna la tecla 7 del menú (#R$AA5D)
B $F79B,1
W $F79C,30,2
N $F79C Lista de 15 direcciones de bytes de atributo de casillas de fondo (tiles $01-$04, $09, $0A, $0F-$17, offset +32 de cada casilla = $9B00+36*código+32) que #R$A8D1 repinta con el color de $F79B
b $F7BA Fin de la lista ($FF,$FF) y relleno a cero hasta $FDFD (sin uso)
B $F7BA,1603,16
c $FDFD Vector de interrupción (JP $C4D5)
b $FE00 Tabla de vectores de interrupción IM 2 (257 bytes con $FD)
B $FE00,257,16
b $FF01 Pila
B $FF01,$FF,16
