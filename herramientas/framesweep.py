"""framesweep.py - recorre TODOS los niveles existentes de un mundo (1P o 2P), con teclas de juego inyectadas, y registra
(mundo, fotograma) de cada sprite dibujado por $C384 (COVER=fichero activa el registro, ver keytrace.py).
Sirve para comprobar que la extraccion de sprites contiene todos los fotogramas que el juego llega a dibujar.
Uso: COVER=cov_w.txt python3 -I framesweep.py tape/mundoN.sna N modo(1|2) [frames_por_nivel]"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap, w, modo = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); per = int(sys.argv[4]) if len(sys.argv) > 4 else 260
import keytrace
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
niveles = [l for l in range(10*w, 10*w+10) if l != 79 and l <= 80]
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
seq = [{'o'}, {'p'}, {'q'}, {'a'}, {'SPACE'}, {'p', 'q'}, {'o', 'q'}, {'a', 'SPACE'}, set()]
def sched(f):
    if f < 12: return {'1'} if modo == 1 else {'2'}
    k = (f - 150) % per
    if k < 6 and f >= 150: return {'r'}
    return seq[(k // 14) % len(seq)]
tr.pressed = sched(0); idx = 0; nops = 0
while frame < 150 + per*len(niveles) + 5:
    pc = reg[24]; ops[mem[pc]](); nops += 1
    if nops % 3000000 == 0: print("SP", hex(reg[12]), [hex(mem[(reg[12]+2*i)&0xFFFF]|mem[(reg[12]+2*i+1)&0xFFFF]<<8) for i in range(5)], 'ops', nops, 'frame', frame, 'PC', hex(reg[24]), 'IFF', reg[26], 'D39A', mem[0xD39A], flush=True)
    if nops > 80000000: break
    t = reg[25]
    if t >= nxt:                       # fin de trama: la interrupcion se acepta si es posible, pero el tiempo (y las teclas) avanzan siempre
        if t < nxt+ia and reg[26]: sim.accept_interrupt(reg, mem, pc)
        frame += 1; nxt += fd; tr.pressed = sched(frame)
        if frame > 20: mem[0xD079] = 255      # invencible (clave ILLUMINATUS) y vidas
        if frame >= 140 and (frame - 140) % per == 0 and idx < len(niveles):
            mem[0xD39A] = niveles[idx]; mem[0xD98B] = w; mem[0xD91D] = modo; idx += 1

print('mundo', w, 'modo', modo, 'niveles', niveles)
