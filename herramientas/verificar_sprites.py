"""verificar_sprites.py - comprueba que la extraccion de sprites contiene TODOS los fotogramas que el juego dibuja.
Entrada: sprites.json (extraer_assets.py) y los ficheros *.frames que escribe keytrace.py cuando se ejecuta con COVER=fichero
(registran (mundo, fotograma) de cada llamada a la rutina de sprites $C384 durante las pruebas y el barrido de niveles).
Uso: python3 -I verificar_sprites.py sprites.json directorio_con_frames salida.md"""
import sys, json, glob, collections
sj, d, out = sys.argv[1:4]
J = json.load(open(sj))
ext = {}
for s in J['sprites']:
    m = s['mundo'] if s['mundo'] == 'base' else int(s['mundo']); ext[(m, s['frame'])] = s
usados = collections.defaultdict(set)
for f in glob.glob(d + '/**/*.frames', recursive=True):
    for l in open(f):
        if l.strip():
            w, fr = map(int, l.split()); usados[w].add(fr)
falta = []; vacios = []; total = set()
for w, frs in usados.items():
    for fr in frs:
        clave = ('base', fr) if fr < 0x70 else (w, fr)
        total.add(clave)
        if clave not in ext: falta.append((w, fr))
        elif ext[clave].get('vacio') or set(ext[clave]['hex']) == {'0'}: vacios.append((w, fr))
base = sorted(f for (m, f) in total if m == 'base')
L = ['# Verificación de la extracción de sprites', '',
     'Fotogramas distintos dibujados por el juego durante las pruebas: %d (base: %d; por mundo: %d).' % (len(total), len(base), len(total)-len(base)), '',
     'Fotogramas dibujados que NO están en sprites.json: %s' % (sorted(falta) or 'ninguno'), '',
     'Fotogramas dibujados cuyo gráfico está vacío (todo ceros): %s' % (sorted(vacios) or 'ninguno'), '',
     'Fotogramas base usados: ' + ' '.join('%02X' % f for f in base), '']
for w in sorted(k for k in set(m for m, _ in total) if k != 'base'):
    L.append('Mundo %s: ' % w + ' '.join('%02X' % f for (m, f) in sorted(total, key=str) if m == w))
base_ext = sorted(f for (m, f) in ext if m == 'base' and not ext[(m, f)].get('vacio') and set(ext[(m, f)]['hex']) != {'0'})
L += ['', 'Fotogramas base no vacíos extraídos pero NUNCA dibujados en las pruebas: ' + ' '.join('%02X' % f for f in base_ext if f not in set(base))]
open(out, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:8]))
