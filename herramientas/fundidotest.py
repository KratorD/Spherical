"""fundidotest.py - efectos de fundido a negro ($CB7D) y de vuelta ($CBBA) con atributos que tienen PAPEL distinto de cero (ramas $CBA0 y $CBE4),
y el borde de la zona de bloques con el jugador agachado en la última fila ($BEDF-$BEE8).
Uso: python3 -I fundidotest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
def correr(sim, tr, frames, ret=0xFFF0, keys=lambda f: set()):
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
    while frame < frames and reg[24] != ret:
        pc = reg[24]; ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd; tr.pressed = keys(frame)
            else: nxt += fd
    return frame
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg = sim.memory, sim.registers
for i in range(0x300): mem[0x5800+i] = 0x38 | 0x07          # papel 7, tinta 7
reg[24] = 0xCB7D; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF
f = correr(sim, tr, 200)
print('fundido a negro ($CB7D): frames', f, '| atributo $5800 final =', hex(mem[0x5800]), '(0 = negro)')
for i in range(0x300): mem[0xF192+i] = 0x38 | 0x07
reg[24] = 0xCBBA; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF
f = correr(sim, tr, 200)
print('fundido de vuelta ($CBBA): frames', f, '| atributo $5800 final =', hex(mem[0x5800]), '(debe ser $3F)')
# bloque agachado en la última fila (y=$90): no se puede colocar debajo ($BEE4) ; y=$80: si ($BEE5)
for y in (0x90, 0x80):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem = sim.memory
    mem[0xD3A7] = 24; mem[0xD3A8] = y
    antes = bytes(mem[0xDE5A:0xDE5A+140])
    vis = set(); ops = sim.opcodes; reg = sim.registers
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
    keys = lambda f: ({'a'} if 6 <= f < 60 else set()) | ({'SPACE'} if 20 <= f < 28 else set())
    while frame < 90:
        pc = reg[24]; vis.add(pc); ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd; tr.pressed = keys(frame)
            else: nxt += fd
    nuevos = [i for i in range(140) if mem[0xDE5A+i] != antes[i]]
    print('agachado en y=%02X: celdas del mapa cambiadas %s | $BEE4 (rechaza): %s | $BEE5 (permite): %s' % (y, nuevos, 0xBEE4 in vis, 0xBEE5 in vis))
