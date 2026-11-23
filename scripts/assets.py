"""Rebuild the editorial SVG covers and catalog without third-party packages."""
from pathlib import Path
import json, html, textwrap
ROOT=Path(__file__).resolve().parents[1]
movies=[]
for line in (ROOT/'scripts/catalog.txt').read_text().splitlines():
    if line.startswith('@'):
        theme=line[1:];continue
    title,year,description=line.split('|')
    movies.append(dict(id=f'm{len(movies)+1:03}',title=title,year=int(year),theme=theme,description=description))
(ROOT/'dist/movies.json').write_text(json.dumps(movies,ensure_ascii=False,indent=2))
themes=list(dict.fromkeys(m['theme'] for m in movies))
colors=['#b5f58c','#a3caee','#f0b77d','#a7b3de','#e2b386','#87d1d0','#a9afca','#b9c68f','#eeb2b9','#ebd483','#edc69a','#a2c8b3','#e6c08b','#d4ed94','#dbb4e6','#d6bca4','#b9c1b1','#a7cbe4']
for n,m in enumerate(movies):
    g=themes.index(m['theme']);c=colors[g];seed=n%5
    stars=''.join(f'<circle cx="{(i*73+n*11)%300}" cy="{(i*47+n*7)%290}" r="1" fill="{c}" opacity=".35"/>' for i in range(30))
    if g==0:
        shape=''.join(f'<path d="M {25+i*25} {15+(i*31)%70} v {120+(i*17)%80}" stroke="{c}" stroke-width="{2 if i%2 else 4}" opacity="{.15+i*.04}"/>' for i in range(11))+f'<circle cx="150" cy="145" r="70" fill="#0c1913" stroke="{c}"/><path d="M120 172V117l30 35 30-35v55" fill="none" stroke="{c}" stroke-width="7"/>'
    elif g==1:
        shape=f'<circle cx="{145+seed*5}" cy="140" r="77" fill="url(#planet)"/><ellipse cx="150" cy="148" rx="125" ry="25" transform="rotate(-25 150 148)" fill="none" stroke="{c}" opacity=".7"/>'
    elif g==2:
        shape=f'<path d="M150 48l14 77 82 51v15l-80-25 2 42 29 22v12l-47-12-47 12v-12l29-22 2-42-80 25v-15l82-51z" fill="{c}" opacity=".85"/><path d="M50 260L250 60M10 235L190 55" stroke="{c}" opacity=".18" stroke-width="20"/>'
    elif g in [3,4,5,6,7]:
        shape=f'<circle cx="150" cy="140" r="83" fill="none" stroke="{c}" opacity=".4"/><circle cx="150" cy="140" r="{38+seed*6}" fill="none" stroke="{c}" stroke-width="{12+seed}" opacity=".6"/><path d="M45 245L255 35M50 50L250 250" stroke="{c}" opacity=".2"/><path d="M150 60V220M70 140H230" stroke="{c}" opacity=".7"/>'
    elif g in [8,9,10,15]:
        shape=f'<circle cx="110" cy="135" r="65" fill="{c}" opacity=".65"/><circle cx="185" cy="135" r="65" fill="{c}" opacity=".4"/><path d="M40 245Q150 185 260 245" stroke="{c}" stroke-width="2" fill="none"/>'
    elif g in [11,12,16,17]:
        shape=f'<circle cx="150" cy="100" r="58" fill="{c}" opacity=".65"/><path d="M0 270L100 105 165 210 215 140 300 270Z" fill="#13221d" stroke="{c}" stroke-opacity=".4"/><path d="M110 270L160 170 190 270" fill="{c}" opacity=".25"/>'
    elif g==13:
        shape=f'<circle cx="150" cy="140" r="83" fill="none" stroke="{c}" stroke-width="5"/><path d="M70 190Q150 20 230 190M70 90Q150 260 230 90M150 57V223" stroke="{c}" opacity=".6" fill="none"/>'
    else:
        shape=''.join(f'<rect x="{45+i*23}" y="{140-(40+(i*31+n*13)%70)/2}" width="10" height="{40+(i*31+n*13)%70}" rx="5" fill="{c}" opacity=".7"/>' for i in range(10))
    lines=textwrap.wrap(m['title'].upper(),width=20,break_long_words=False)
    size=24 if len(lines)<=3 else 20
    title=''.join(f'<text x="24" y="{310+i*(size+3)}" font-size="{size}" font-weight="800">{html.escape(line)}</text>' for i,line in enumerate(lines))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="440" viewBox="0 0 300 440"><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#182b24"/><stop offset="1" stop-color="#070c0a"/></linearGradient><radialGradient id="planet" cx=".3" cy=".2"><stop stop-color="{c}"/><stop offset="1" stop-color="#182c35"/></radialGradient></defs><rect width="300" height="440" fill="url(#bg)"/>{stars}{shape}<g fill="{c}" font-family="Arial,sans-serif"><text x="24" y="28" font-size="10" letter-spacing="3">C I N E V E T O R  /  {m['year']}</text>{title}<text x="24" y="416" font-size="10" letter-spacing="1.4">{html.escape(m['theme'].upper())}</text></g><path d="M24 390H276" stroke="{c}" opacity=".25"/></svg>'''
    (ROOT/f"dist/assets/{m['id']}.svg").write_text(svg)
(ROOT/'dist/assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#b9ed87"/><path d="M35 12L12 36H36M21 27Q27 30 27 36" stroke="#162318" stroke-width="3" fill="none"/></svg>')
print(f'{len(movies)} filmes e capas editoriais gerados.')
