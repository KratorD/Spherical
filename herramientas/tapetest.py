"""tapetest.py - prueba la CARGA DE MUNDOS POR CINTA con la ROM REAL del Spectrum (el simulador incluye la ROM 48K):
se genera la señal EAR (bit 6 del puerto $FE) a partir de los bloques del TZX (tono piloto, sincronismo y bits a velocidad normal) y se deja que
$CFB3 -> $D01F -> LD-BYTES de la ROM cargue el mundo pedido. La cinta empieza con un bloque de OTRO mundo para comprobar que el juego lo rechaza y sigue buscando.
Uso: python3 -I tapetest.py Spherical_Erbe.tzx dir_cinta(tape/) [mundo_pedido] [mundo_en_memoria] [mundo_equivocado_en_cinta]"""
import sys, struct, os; sys.path.insert(0, '/home/claude/tools')
import keytrace
from keytrace import *
tzx, tape = sys.argv[1], sys.argv[2]
want = int(sys.argv[3]) if len(sys.argv) > 3 else 5
cur = int(sys.argv[4]) if len(sys.argv) > 4 else 4
wrong = int(sys.argv[5]) if len(sys.argv) > 5 else 3
d = open(tzx, 'rb').read(); p = 10; blocks = []
while p < len(d):
    t = d[p]; p += 1
    if t == 0x10:
        pause, ln = struct.unpack('<HH', d[p:p+4]); blocks.append((d[p+4:p+4+ln], pause)); p += 4+ln
    elif t == 0x32: p += 2 + struct.unpack('<H', d[p:p+2])[0]
    else: raise SystemExit('bloque no soportado %#x' % t)
class Cinta:
    """lista de duraciones de pulso (T-estados) -> nivel EAR en cada instante"""
    def __init__(self, bl, t0):
        pulsos = []
        for data, pausa in bl:
            pulsos += [2168]*(8063 if data[0] < 128 else 3223) + [667, 735]
            for byte in data:
                for b in range(7, -1, -1): pulsos += [1710, 1710] if (byte >> b) & 1 else [855, 855]
            pulsos += [3500]                      # 1 ms de pulso final
            pulsos += [pausa * 3500]
        acc = t0; self.bordes = []
        for x in pulsos: acc += x; self.bordes.append(acc)
        self.i = 0; self.final = acc
    def level(self, T):
        while self.i < len(self.bordes) and self.bordes[self.i] <= T: self.i += 1
        return self.i & 1
sim = load(os.path.join(tape, 'mundo%d.sna' % cur)); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
sec = [blocks[2*(4+wrong)], blocks[2*(4+wrong)+1], blocks[2*(4+want)], blocks[2*(4+want)+1]]
if os.environ.get('CORRUPT'):            # primer intento con error de paridad en los datos: el juego debe repetir la carga ($D019 -> $CFB3)
    dat, pa = blocks[2*(4+want)+1]; mal = bytearray(dat); mal[-1] ^= 0xFF
    sec = [blocks[2*(4+want)], (bytes(mal), 50), blocks[2*(4+want)], blocks[2*(4+want)+1]]
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
mem[0xD39A] = 10*want - 1; mem[0xD98B] = cur; mem[0xD91D] = 1; mem[0xD079] = 255
reg[24] = 0xC524; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF
tr.tape = Cinta(sec, reg[25] + 200000)           # la cinta empieza poco despues
visto = {}; ops_n = 0
while ops_n < 400000000 and frame < 14000:
    pc = reg[24]
    if pc in (0xCFB3, 0xCFC8, 0xCFD8, 0xCFF2, 0xD002, 0xD019, 0xD017, 0xC603, 0xD01C) and pc not in visto: visto[pc] = (frame, reg[25])
    if pc == 0xD017 or pc == 0xC603: break
    ops[mem[pc]](); ops_n += 1
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia and reg[26]: sim.accept_interrupt(reg, mem, pc)
        frame += 1; nxt += fd
bloque = blocks[2*(4+want)+1][0][1:-1]
print('rutas alcanzadas (frame):', {hex(k): v[0] for k, v in visto.items()})
print('instrucciones simuladas:', ops_n, '| D98B =', mem[0xD98B], '| D39A =', mem[0xD39A])
print('datos cargados en $6F00 iguales al bloque del mundo %d de la cinta: %s (%d bytes)' % (want, bytes(mem[0x6F00:0x6F00+len(bloque)]) == bloque, len(bloque)))
print('cabecera leida en $D031:', bytes(mem[0xD031:0xD031+17]))
