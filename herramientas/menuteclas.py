"""menuteclas.py - comprueba cada tecla del menú (1-7) y la inserción de puntuaciones ($ADAC).
Uso: python3 -I menuteclas.py menu.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
import keytrace
from keytrace import *
keytrace.KEYS.update({'3': (0xF7, 2), '4': (0xF7, 3), '5': (0xF7, 4), '6': (0xEF, 4), '7': (0xEF, 3)})
dest = {'1': (0xA96C, '1 jugador'), '2': (0xA971, '2 jugadores'), '3': (0xA976, 'entrenamiento'), '4': (0xA983, 'clave'), '5': (0xAA02, 'cambiar mandos'), '6': (0xAA57, 'mejores puntuaciones'), '7': (0xAA5D, 'fondo claro/oscuro')}
def prueba(k):
    sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
    while frame < 260:
        pc = reg[24]
        if pc == dest[k][0]: return frame
        ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc):
                    frame += 1; nxt += fd; tr.pressed = {k} if frame >= 150 else set()
            else: nxt += fd
    return None
for k in '1234567':
    print('tecla', k, dest[k][1], '->', 'alcanza $%04X en el frame %s' % (dest[k][0], prueba(k)))
# --- inserción de puntuaciones: tabla 5000,3000,1000,500,100 + 1234
sim = load(sys.argv[1]); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
tabla = lambda: [(mem[0xD109+15*i] | mem[0xD10A+15*i] << 8) for i in range(5)]
for i, v in enumerate((5000, 3000, 1000, 500, 100)): mem[0xD109+15*i] = v & 255; mem[0xD10A+15*i] = v >> 8
print('tabla antes   :', tabla())
reg[24] = 0xADAC; reg[12] = 0xFFFC; mem[0xFFFC] = 0; mem[0xFFFD] = 0
reg[6], reg[7] = 0x04, 0xD2         # HL = 1234
for _ in range(2000000):
    if reg[24] == 0xAE6B: break
    ops[mem[reg[24]]]()
print('tabla despues :', tabla(), '(llega a pedir el nombre en $AE6B: %s)' % (reg[24] == 0xAE6B))
