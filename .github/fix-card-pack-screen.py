from pathlib import Path
p=Path('index.html'); s=p.read_text()
repls={
'#chestScreen .chestBtn':'#packsScreen .chestBtn',
'<div style="font-size:70px">🧰</div>':'<div style="font-size:70px">🃏</div>',
'<h1>Animal Chests</h1>':'<h1>Animal Card Packs</h1>',
'<button data-screen="packsScreen"><span class="ico">🧰</span>Chests</button>':'<button data-screen="packsScreen"><span class="ico">🃏</span>Packs</button>'
}
for old,new in repls.items():
    if old not in s: raise SystemExit(f'marker not found: {old}')
    s=s.replace(old,new)
p.write_text(s)
