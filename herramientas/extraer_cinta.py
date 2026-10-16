"""extraer_cinta.py - Trocea un TZX estandar (bloques 0x10) de Spherical y crea un snapshot .sna por mundo.
Uso: python3 -I extraer_cinta.py cinta.tzx base.sna directorio_salida
 base.sna = cualquier snapshot del juego (aporta el codigo y los graficos); se le superpone el bloque del mundo en 6F00.
Salida: <n>_<nombre>.bin por bloque y mundoN.sna (N=0..8). Verifica la paridad de cada bloque."""
import struct, sys, os
tzx, base, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
d = open(tzx, 'rb').read(); p = 10; blocks = []
while p < len(d):
    t = d[p]; p += 1
    if t == 0x10:
        _, ln = struct.unpack('<HH', d[p:p+4]); blocks.append(d[p+4:p+4+ln]); p += 4+ln
    elif t == 0x32:
        p += 2 + struct.unpack('<H', d[p:p+2])[0]
    else:
        raise SystemExit('bloque TZX no soportado: %#x' % t)
def ok(b):
    x = 0
    for c in b: x ^= c
    return x == 0
assert all(ok(b) for b in blocks), 'paridad incorrecta'
snap = open(base, 'rb').read(); hdr, ram = snap[:27], bytearray(snap[27:])
for i in range(0, len(blocks), 2):
    h, data = blocks[i], blocks[i+1][1:-1]
    name = bytes(h[2:12]).decode('latin1').strip()
    start = h[14] | h[15] << 8
    open(os.path.join(out, '%d_%s.bin' % (i//2, name)), 'wb').write(data)
    print(i//2, name, len(data), hex(start))
    if name.isdigit():
        r = bytearray(ram); r[start-0x4000:start-0x4000+len(data)] = data
        open(os.path.join(out, 'mundo%s.sna' % name), 'wb').write(hdr + bytes(r))
