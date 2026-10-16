import sys; sys.path.insert(0,'/home/claude/tools')
import keytrace
from keytrace import KeyTracer, load
from collections import Counter
def watch(path, sched, frames):
    sim=load(path); tr=KeyTracer(); sim.set_tracer(tr)
    mem,reg,ops=sim.memory,sim.registers,sim.opcodes
    fd,ia=sim.frame_duration,sim.int_active
    next_int=((reg[25]+fd-ia)//fd)*fd; frame=0; tr.pressed=set(sched(0))
    prev=list(mem[0x5B00:]); cnt=Counter(); first={}
    while frame<frames:
        pc=reg[24]; ops[mem[pc]](); t=reg[25]
        if t>=next_int:
            if t<next_int+ia:
                if reg[26] and sim.accept_interrupt(reg,mem,pc):
                    frame+=1; tr.pressed=set(sched(frame)); next_int+=fd
                    cur=mem[0x5B00:]
                    for i,(a,b) in enumerate(zip(prev,cur)):
                        if a!=b: cnt[0x5B00+i]+=1; first.setdefault(0x5B00+i,(frame,a,b))
                    prev=list(cur)
            else: next_int+=fd
    return cnt,first
if __name__=='__main__':
    for n in ('nivel2','nivel4'):
        cnt,first=watch('/home/claude/work/%s.sna'%n,lambda f:set(),200)
        print(n,len(cnt),'direcciones cambian')
        print(' '.join('%04X:%d'%(a,c) for a,c in sorted(cnt.items()) if a<0x8000 or a>0x9000)[:3000])
