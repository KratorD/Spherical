"""completitud_sprites.py - argumento de completitud de los sprites SIN depender de lo que hayan dibujado las pruebas:
 (1) DOMINIO: $C384 lee el fotograma de (IX+2), un BYTE; luego solo puede dibujar los fotogramas $00-$FF (direccion $6100+32*f). El manifiesto debe contener
     los $00-$6F del bloque base y los $70-$FF de CADA mundo (0-8). (2) CABECERAS: los fotogramas de enemigos de las cabeceras de los 90 niveles x 2 modos.
Uso: python3 -I completitud_sprites.py manifiesto_sprites.json dir_niveles_json"""
import sys, json, glob
man = {(e['mundo'], e['frame']): e for e in json.load(open(sys.argv[1]))['fotogramas']}
falta = [(m, f) for f in range(0x70) for m in ('base',) if (m, f) not in man] + [(w, f) for w in range(9) for f in range(0x70, 0x100) if (w, f) not in man]
print('(1) dominio $00-$FF: fotogramas que faltan en el manifiesto: %s (esperados: %d base + %d x 9 mundos)' % (falta or 'ninguno', 0x70, 0x90))
mal = []
for fn in sorted(glob.glob(sys.argv[2] + '/mundo*_niveles.json')):
    d = json.load(open(fn))
    for modo in ('1P', '2P'):
        for lv in d[modo]:
            if not lv.get('existe', True): continue
            for e in lv['enemigos']:
                fr = e['frame']; k = ('base', fr) if fr < 0x70 else (lv['mundo'], fr)
                if man.get(k, {}).get('tipo') not in ('sprite', 'vacio'): mal.append((lv['nivel_global'], modo, hex(fr)))
print('(2) fotogramas de cabecera no clasificados como sprite/vacio: %s' % (mal or 'ninguno'))
