import sys; sys.path.insert(0,'/home/claude/tools')
from keytrace import KeyTracer, load
def log(path, frames, sched=lambda f:set()):
    sim=load(path); tr=KeyTracer(); sim.set_tracer(tr)
    mem,reg,ops=sim.memory,sim.registers,sim.opcodes
    fd,ia=sim.frame_duration,sim.int_active
    next_int=((reg[25]+fd-ia)//fd)*fd; frame=0; tr.pressed=set(sched(0)); rows=[]
    def snap(): return (frame,mem[0xD3F0],mem[0xD3F1],mem[0xD3F2],mem[0xD3F7],mem[0xD91F],mem[0xD989],mem[0xD98A])
    rows.append(snap())
    while frame<frames:
        pc=reg[24]; ops[mem[pc]](); t=reg[25]
        if t>=next_int:
            if t<next_int+ia:
                if reg[26] and sim.accept_interrupt(reg,mem,pc):
                    frame+=1; tr.pressed=set(sched(frame)); next_int+=fd; rows.append(snap())
            else: next_int+=fd
    return rows
if __name__=='__main__':
    for n in ('nivel2','nivel4'):
        print(n,'frame x y frm dir D91F D989 D98A')
        prev=None
        for r in log('/home/claude/work/%s.sna'%n,70):
            if r[1:]!=prev: print(' ',r[0],'x=%02X y=%02X frm=%02X dir=%02X v=%02X d989=%02X d98a=%02X'%r[1:])
            prev=r[1:]
