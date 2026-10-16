"""jefe60test.py - regla de daño del jefe del nivel $3C (60, mundo 6): el orbe sólo le quita vida si su fotograma está entre $88 y $9F ($B15C-$B16E).
Se teletransporta al jugador (con orbe) sobre cada segmento del jefe y se registra la vida DC3A junto al fotograma de los segmentos.
Uso: python3 -I jefe60test.py tape/mundo6.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
sched = lambda f: {'1'} if 5 <= f < 12 else ({'r'} if 150 <= f < 156 else set())
tr.pressed = sched(0); log = []; ult = None; nops = 0
while frame < 1200 and nops < 80000000:
    pc = reg[24]; ops[mem[pc]](); nops += 1
    t = reg[25]
    if t >= nxt:                       # el tiempo (y las teclas) avanza siempre; la interrupción sólo se acepta si IFF=1
        if t < nxt+ia and reg[26]: sim.accept_interrupt(reg, mem, pc)
        frame += 1; nxt += fd; tr.pressed = sched(frame)
        if frame == 140: mem[0xD39A] = 60; mem[0xD98B] = 6
        if frame >= 200:
            mem[0xD079] = 255; mem[0xD3BC] = (mem[0xD3BC] & 0xF7) | 0x08; mem[0xD3C0] = 0xC0
            n = mem[0xD52C]; jefes = [k for k in range(n) if mem[0xD3F8+22*k+8] >= 0x12]
            if jefes:
                k = jefes[(frame // 40) % len(jefes)]
                mem[0xD3A7] = max(0, mem[0xD3F8+22*k] - 4); mem[0xD3A8] = max(0, mem[0xD3F9+22*k] - 8)
            hp = mem[0xDC3A]
            if hp != ult:
                log.append((frame, 'vida', hp, [(k, mem[0xD3F8+22*k+2]) for k in jefes][:6])); ult = hp
print('frames', frame, 'ops', nops, 'jefes', len([1 for k in range(mem[0xD52C]) if mem[0xD3F8+22*k+8] >= 0x12]))
for l in log[:30]: print(l)
