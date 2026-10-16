import sys; sys.path.insert(0,'/home/claude/tools')
from writewatch import run
import itertools
def sch_factory(pre, space_keys, period):
    def f(fr):
        s=set()
        if fr<40: s|=pre
        else:
            if (fr-40)%period<3: s|=space_keys|{'SPACE'}
            else: s|=set(space_keys)-{'a'} if False else set()
        return s
    return f
for snap in ('nivel4','nivel2'):
    for pre in (set(),{'o'},{'p'}):
        for sk in (set(),{'a'}):
            for period in (15,):
                out,sim=run('/home/claude/work/%s.sna'%snap, sch_factory(pre,sk,period), 160)
                w=[(fr,'%04X'%pc,'%04X'%a,'%02X'%v) for fr,pc,a,v in out if 0xDE5A<=a<0xDF02]
                print(snap,sorted(pre),sorted(sk),'escrituras mapa:',len(w), w[:6])
