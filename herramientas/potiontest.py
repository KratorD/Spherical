import sys; sys.path.insert(0,'/home/claude/tools')
from keytrace import *
def go(path, pokes, sched, frames, probe):
    sim=load(path); tr=KeyTracer(); sim.set_tracer(tr)
    mem,reg,ops=sim.memory,sim.registers,sim.opcodes
    for a,v in pokes.items(): mem[a]=v
    fd,ia=sim.frame_duration,sim.int_active
    t=reg[25]; nxt=((t+fd-ia)//fd)*fd; frame=0; tr.pressed=set(sched(0))
    out=[]
    while frame<frames:
        pc=reg[24]; ops[mem[pc]]()
        t=reg[25]
        if t>=nxt:
            if t<nxt+ia:
                if reg[26] and sim.accept_interrupt(reg,mem,pc):
                    frame+=1; tr.pressed=set(sched(frame)); nxt+=fd
                    if frame%4==0: out.append((frame,probe(mem)))
            else: nxt+=fd
    return out
def probe(mem):
    n=mem[0xD52C]
    return dict(pot=mem[0xD98C], enemies=[(mem[0xD3F8+22*k],mem[0xD3F8+22*k+8]) for k in range(n)], orb=(mem[0xD3E1],mem[0xD3E2]), p1=(mem[0xD3A7],mem[0xD3A8]), flags=mem[0xD3BC], tmr=mem[0xD3C0])
print('--- POCION (ENTER) ---')
for r in go('/home/claude/work/nivel2.sna',{0xD98C:2},lambda f:{'ENTER'} if 8<=f<12 else set(),60,probe)[:10]: print(r)
print('--- VARITA (bit3) ---')
for r in go('/home/claude/work/nivel2.sna',{0xD3BC:0x08,0xD3C0:0xC0},lambda f:set(),48,probe)[:12]: print(r)
