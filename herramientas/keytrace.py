"""keytrace.py - simula un snapshot .sna de Spectrum 48K inyectando teclas por frame
y devuelve el conjunto de direcciones ejecutadas (mapa de ejecucion).
Usa el simulador Python de SkoolKit (solo lectura de sus modulos)."""
import sys
sys.path.insert(0, '/home/claude/sk')
from skoolkit.simulator import Simulator
from skoolkit.simutils import from_snapshot
from skoolkit.snapshot import Snapshot

# (fila de semi-puerto -> byte alto, bit) de las teclas que usa Spherical
KEYS = {'q': (0xFB, 0), 'a': (0xFD, 0), 'o': (0xDF, 1), 'p': (0xDF, 0),
        'SPACE': (0x7F, 0), 'ENTER': (0xBF, 0), 'r': (0xFB, 3), 'h': (0xBF, 4),
        'f': (0xFD, 3), 'z': (0xFE, 1), 'x': (0xFE, 2), 'w': (0xFB, 1), 's': (0xFD, 1),
        '1': (0xF7, 0), '2': (0xF7, 1), '0': (0xEF, 0)}

class KeyTracer:
    def __init__(self):
        self.pressed = set()
        self.reads = {}                    # puerto -> nº lecturas
    def read_port(self, registers, port):
        self.reads[port] = self.reads.get(port, 0) + 1
        if (port & 0xFF) == 0x1F and getattr(self, 'kemp', None) is not None:
            return self.kemp                    # joystick Kempston: bit0 derecha, 1 izquierda, 2 abajo, 3 arriba, 4 disparo
        if port & 1:
            return 0xFF
        # semifilas: la fila se selecciona cuando su bit en el byte alto es 0
        v = 0xFF
        hiport = port >> 8
        for k in self.pressed:
            rowmask, bit = KEYS[k]            # rowmask tiene un solo 0 = fila seleccionada
            if hiport & (~rowmask & 0xFF) == 0:
                v &= ~(1 << bit) & 0xFF
        tape = getattr(self, 'tape', None)
        if tape is not None:                      # señal EAR de la cinta en el bit 6
            v = (v & ~0x40) | (0x40 if tape.level(registers[25]) else 0)
        return v

def load(path):
    snap = Snapshot.get(path)
    if snap.type == 'SNA' and len(snap.tail) == 0xC000:
        snap.sp = (snap.sp + 2) % 65536      # el .sna guarda PC en la pila
    sim = from_snapshot(Simulator, snap, {}, {}, {})
    import os
    if os.environ.get('COVER'):            # cobertura: guarda las direcciones de inicio de instruccion ejecutadas
        import atexit
        cov = set(); fr = set(); roles = set(); reg = sim.registers
        def wrap(f):
            def w():
                p = reg[24]; cov.add(p)
                if p == 0xC384:                 # dibujar sprite: registra (mundo, fotograma)
                    ix = (reg[8] << 8) | reg[9]; m = sim.memory
                    fr.add((m[0xD98B], m[ix + 2]))
                    rol = {0xD3F0: 'esfera', 0xD3A7: 'J1', 0xD3E1: 'orbe1', 0xD3C4: 'J2', 0xD3E8: 'orbe2'}.get(ix)
                    if rol is None: rol = 'enemigo%02X' % m[ix + 8]
                    roles.add((m[0xD98B], rol, m[ix + 2], m[0xD91D]))
                    if os.environ.get('CALLERS'):
                        sp = reg[12]; open(os.environ['CALLERS'], 'a').write('%s %d %04X\n' % (rol, m[ix + 2], m[sp] | (m[(sp + 1) & 0xFFFF] << 8)))
                f()
            return w
        ops = sim.opcodes
        for i in range(len(ops)): ops[i] = wrap(ops[i])
        def dump(path=os.environ['COVER']):
            old = set()
            if os.path.exists(path): old = set(map(int, open(path).read().split()))
            open(path, 'w').write(' '.join(map(str, sorted(old | cov))))
            o2 = set()
            if os.path.exists(path + '.frames'): o2 = {tuple(map(int, l.split())) for l in open(path + '.frames') if l.strip()}
            open(path + '.frames', 'w').write('\n'.join('%d %d' % x for x in sorted(o2 | fr)) + '\n')
        def dump_roles():
            if os.environ.get('ROLES'):
                p = os.environ['ROLES']; o = set()
                if os.path.exists(p): o = {tuple(l.split()) for l in open(p) if l.strip()}
                o |= {tuple(str(x) for x in r) for r in roles}
                open(p, 'w').write('\n'.join(' '.join(x) for x in sorted(o)) + '\n')
        atexit.register(dump_roles)
        atexit.register(dump)
    return sim

def run(path, schedule, frames, stop_log=None):
    """schedule(frame) -> conjunto de teclas pulsadas en ese frame."""
    sim = load(path)
    tr = KeyTracer()
    sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    fd, ia = sim.frame_duration, sim.int_active
    executed = set()
    t = reg[25]
    next_int = ((t + fd - ia) // fd) * fd
    frame = 0
    tr.pressed = set(schedule(0))
    while frame < frames:
        pc = reg[24]
        executed.add(pc)
        ops[mem[pc]]()
        t = reg[25]
        if t >= next_int:
            if t < next_int + ia:
                if reg[26]:
                    if sim.accept_interrupt(reg, mem, pc):
                        frame += 1
                        tr.pressed = set(schedule(frame))
                        next_int += fd
            else:
                next_int += fd
    return executed, sim, tr

if __name__ == '__main__':
    ex, sim, tr = run(sys.argv[1], lambda f: set(), 50)
    print(len(ex), 'dirs;', 'puertos leidos:', {hex(k): v for k, v in tr.reads.items()})
