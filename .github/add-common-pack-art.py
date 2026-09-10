from pathlib import Path
p=Path('index.html');s=p.read_text()
old='<button class="primary chestBtn" data-chest="common">⚪ Common Pack • 🟡 250 Coins</button>'
new='<button class="primary chestBtn packArtBtn" data-chest="common"><img src="assets/common-pack.jpg" alt="Common Pack artwork" class="packArtwork"><span>⚪ Common Pack • 🟡 250 Coins</span></button>'
if old not in s: raise SystemExit('common pack button not found')
s=s.replace(old,new,1)
css='''\n#packsScreen .packArtBtn[data-chest="common"]{height:auto;min-height:0;padding:12px;display:flex;flex-direction:column;align-items:center;gap:8px;background:linear-gradient(135deg,#fff,#d7d7d7 55%,#fff);color:#c62828}\n#packsScreen .packArtwork{display:block;width:min(180px,48vw);height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:9px;box-shadow:0 5px 14px rgba(0,0,0,.3)}\n#packsScreen .packArtBtn span{font-weight:900;color:#c62828}\n'''
if '</style>' not in s: raise SystemExit('style marker missing')
s=s.replace('</style>',css+'</style>',1)
p.write_text(s)
