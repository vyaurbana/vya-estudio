"""Publica una versión nueva de VYA ESTUDIO para que se actualice sola.

Uso: python3 publicar.py <carpeta_del_programa> <numero_version>
Deja VYA_ESTUDIO-<N>.zip y version.json en este repositorio (y borra los zips viejos).
"""
import hashlib, json, os, sys, zipfile, glob

BASE = 'https://raw.githubusercontent.com/vyaurbana/vya-estudio/main/'
src, n = sys.argv[1], int(sys.argv[2])
aqui = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(src, 'version.txt'), 'w') as f:
    f.write(str(n))
for viejo in glob.glob(os.path.join(aqui, 'VYA_ESTUDIO-*.zip')):
    os.remove(viejo)
nombre = f'VYA_ESTUDIO-{n}.zip'
ruta = os.path.join(aqui, nombre)
with zipfile.ZipFile(ruta, 'w', zipfile.ZIP_DEFLATED) as z:
    for r, dirs, fs in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', 'bin', 'python', 'modelos')]
        for f in sorted(fs):
            p = os.path.join(r, f)
            z.write(p, 'VYA_ESTUDIO/' + os.path.relpath(p, src).replace(os.sep, '/'))
h = hashlib.sha256(open(ruta, 'rb').read()).hexdigest()
json.dump({'version': n, 'zip': BASE + nombre, 'sha256': h}, open(os.path.join(aqui, 'version.json'), 'w'), indent=1)
print(nombre, h)
