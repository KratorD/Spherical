"""cobertura.py - cobertura de ejecucion por rutina: cruza las direcciones ejecutadas (COVER=cov.txt, ver keytrace.py) con el .skool.
Uso: python3 -I cobertura.py spherical_anotado.skool cov.txt [salida.md]"""
import sys, re
skool, covf = sys.argv[1:3]
cov = set(map(int, open(covf).read().split()))
rut = []; cur = None; kind = None
for ln in open(skool, encoding='utf-8'):
    m = re.match(r'^([*c bwtsu]?)\$([0-9A-F]{4}) (.*)$', ln.rstrip('\n')) or re.match(r'^([*c bwtsu])\$([0-9A-F]{4}) (.*)$', ln)
    m = re.match(r'^(.)\$([0-9A-F]{4}) (\S.*)$', ln.rstrip('\n'))
    if not m: continue
    t, a, rest = m.groups(); a = int(a, 16)
    if t in 'cbwtsu':
        kind = t
        if t == 'c': cur = dict(addr=a, n=0, hit=0, miss=[]); rut.append(cur)
        else: cur = None
    if kind == 'c' and cur is not None and t in 'c *':
        cur['n'] += 1
        if a in cov: cur['hit'] += 1
        else: cur['miss'].append(a)
tot = sum(r['n'] for r in rut); hit = sum(r['hit'] for r in rut)
out = ['# Cobertura de ejecución del código por las pruebas en el simulador', '',
       'Instrucciones del programa: %d | ejecutadas por alguna prueba: %d (%.1f %%)' % (tot, hit, 100*hit/tot), '',
       'Rutinas con instrucciones no ejecutadas (las no ejecutadas están sólo LEÍDAS):', '', '| Rutina | Ejecutadas | Total | Direcciones sin ejecutar |', '|---|---|---|---|']
for r in rut:
    if r['hit'] < r['n']:
        ms = r['miss']; txt = ', '.join('%04X' % x for x in ms[:12]) + (' ...' if len(ms) > 12 else '')
        out.append('| `$%04X` | %d | %d | %s |' % (r['addr'], r['hit'], r['n'], txt))
full = [r for r in rut if r['hit'] == r['n']]
out += ['', 'Rutinas ejecutadas al 100 %%: %d de %d.' % (len(full), len(rut))]
open(sys.argv[3] if len(sys.argv) > 3 else 'cobertura.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:4]))
