"""parchear_tzx.py - aplica un parche de bytes a un bloque CODE de una cinta TZX (bloques estándar $10) y recalcula el byte de paridad del bloque.
Uso: python3 -I parchear_tzx.py entrada.tzx salida.tzx NOMBRE_BLOQUE DIRECCION_HEX BYTES_HEX
Ejemplo (poner $4D en el primer byte del mapa 1P del nivel 50, bloque del mundo 5): parchear_tzx.py in.tzx out.tzx 5 8A60 4D
La DIRECCION es la de memoria del juego (p. ej. $AAA6); se traduce al desplazamiento dentro del bloque con la dirección de inicio de su cabecera."""
import sys, struct
src, dst, nombre, dirh, datos = sys.argv[1:6]
direc = int(dirh, 16); parche = bytes.fromhex(datos)
d = bytearray(open(src, 'rb').read()); p = 10; bloques = []
while p < len(d):
    t = d[p]
    if t == 0x10:
        ln = struct.unpack('<H', d[p+3:p+5])[0]; bloques.append((p + 5, ln)); p += 5 + ln
    elif t == 0x32: p += 3 + struct.unpack('<H', d[p+1:p+3])[0]
    else: raise SystemExit('bloque TZX no soportado: %#x' % t)
hecho = False
for i, (off, ln) in enumerate(bloques):
    h = d[off:off+ln]
    if ln == 19 and h[0] == 0 and h[1] == 3 and h[2:12].decode('latin1').strip() == nombre and i+1 < len(bloques):
        largo = struct.unpack('<H', bytes(h[12:14]))[0]; inicio = struct.unpack('<H', bytes(h[14:16]))[0]
        do, dl = bloques[i+1]
        if not inicio <= direc and direc + len(parche) <= inicio + largo: raise SystemExit('la direccion cae fuera del bloque (%04X-%04X)' % (inicio, inicio + largo - 1))
        pos = do + 1 + (direc - inicio)                     # +1: byte de bandera
        d[pos:pos+len(parche)] = parche
        x = 0
        for b in d[do:do+dl-1]: x ^= b
        d[do+dl-1] = x                                      # paridad
        hecho = True; print('parcheado: bloque "%s" (inicio %04X, %d bytes), %d byte(s) en %04X; paridad = %02X' % (nombre, inicio, largo, len(parche), direc, x)); break
if not hecho: raise SystemExit('no se encontro el bloque CODE "%s"' % nombre)
open(dst, 'wb').write(d)
