"""velocidad_cont.py - como velocidad.py pero con un MODELO DE CONTENCION DE MEMORIA del Spectrum 48K:
cada acceso (lectura/escritura/busqueda de opcode) a $4000-$7FFF durante las 192 lineas de pantalla se retrasa 6,5,4,3,2,1,0,0 T-estados
segun la posicion dentro de cada grupo de 8 T de los primeros 128 T de la linea (la linea dura 224 T; la primera linea contendida empieza en T=14335).
Aproximacion: el retraso se calcula con el T del inicio de la instruccion (error de unos pocos T por acceso) y no se modela la contencion de puertos.
Uso: python3 -I velocidad_cont.py snapshot.sna [frames]"""
import sys; sys.path.insert(0, '/home/claude/tools'); sys.path.insert(0, '/home/claude/sk')
from skoolkit.simulator import Simulator
from skoolkit.simutils import from_snapshot
from skoolkit.snapshot import Snapshot
from keytrace import KeyTracer
PAT = (6, 5, 4, 3, 2, 1, 0, 0)
class Mem(list):
    reg = None; fd = 69888; n = 0
    def __getitem__(self, a):
        if type(a) is int and 0x4000 <= a < 0x8000:
            tf = self.reg[25] % self.fd - 14335
            if 0 <= tf < 192*224:
                o = tf % 224
                if o < 128:
                    d = PAT[o & 7]
                    if d: self.reg[25] += d; Mem.n += d
        return list.__getitem__(self, a)
    def __setitem__(self, a, v):
        if type(a) is int and 0x4000 <= a < 0x8000:
            tf = self.reg[25] % self.fd - 14335
            if 0 <= tf < 192*224:
                o = tf % 224
                if o < 128:
                    d = PAT[o & 7]
                    if d: self.reg[25] += d; Mem.n += d
        list.__setitem__(self, a, v)
class SimC(Simulator):
    def __init__(self, memory, registers=None, state=None, config=None):
        m = Mem(memory); super().__init__(m, registers, state, config); m.reg = self.registers; m.fd = self.frame_duration
def medir(path, N, contencion):
    snap = Snapshot.get(path)
    if snap.type == 'SNA' and len(snap.tail) == 0xC000: snap.sp = (snap.sp + 2) % 65536
    sim = from_snapshot(SimC if contencion else Simulator, snap, {}, {}, {})
    tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    if contencion: mem.reg = reg
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; last = mem[0xD989]; cambios = []; tcamb = []; Mem.n = 0
    while frame < N:
        ops[mem[reg[24]]]()
        t = reg[25]
        if mem[0xD989] != last: last = mem[0xD989]; cambios.append(frame); tcamb.append(reg[25])
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, reg[24]): frame += 1; nxt += fd
            else: nxt += fd
    d = [b-a for a, b in zip(cambios, cambios[1:])]
    dt = [b-a for a, b in zip(tcamb, tcamb[1:])]
    return sum(d)/len(d), Mem.n, sum(dt)/len(dt)
for cont in (False, True):
    media, ret, tpc = medir(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600, cont)
    print('%s: %.3f frames/ciclo -> %.2f ciclos/s (retraso total %d T) | %.0f T-estados por ciclo de juego -> %.2f ciclos/s a 3,5 MHz' % ('CON contencion' if cont else 'SIN contencion', media, 50.08/media, ret, tpc, 3500000/tpc))
