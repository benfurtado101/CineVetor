"""Create a portable source archive; exclude hosting identity, credentials and caches."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]
archive=root/'dist/cinevetor-source.zip'
allowed=['dist','scripts','tests','.github','README.md','LICENSE','ASSETS.md','VALIDATION.md','package.json','requirements-transformer.txt','.gitignore']
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
    for entry in allowed:
        p=root/entry
        if not p.exists():continue
        files=sorted(p.rglob('*')) if p.is_dir() else [p]
        for f in files:
            if f.is_file() and f!=archive and '__pycache__' not in f.parts and f.suffix!='.pyc':
                z.write(f,str(Path('cinevetor')/f.relative_to(root)))
print(f'Portable archive: {archive.name} ({archive.stat().st_size:,} bytes)')
