"""clavetest.py - salta al comparador de claves del menú ($A996) con el texto tecleado ya en $DC44 y comprueba el nivel de inicio.
Uso: python3 -I clavetest.py menu.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
for texto, grupo in (('SKYFIRE', 1), ('RADAGAST', 1), ('MIRGAL', 1), ('GLIEP', 2), ('GUMBACHACHMAL', 2), ('ILLUMINATUS', 1), ('XXXX', 1)):
    sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    buf = (texto.ljust(13)).encode()
    for i, b in enumerate(buf): mem[0xDC44+i] = b
    mem[0xD91D] = grupo
    reg[24] = 0xA996; reg[12] = 0xFFFE & 0xFFFF
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; hit = None
    for _ in range(3000000):
        pc = reg[24]
        if pc == 0xAA8C: hit = True; break
        if pc in (0xA8D1,) and _ > 0: break
        ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): nxt += fd
            else: nxt += fd
        if frame > 0: break
    print(texto, 'inicia partida' if hit else 'vuelve al menú', '| D39A', mem[0xD39A], '| vidas/D91D', mem[0xD91D], '| D39B', hex(mem[0xD39B]), '| D079', mem[0xD079])
