from pathlib import Path
p=Path('index.html'); s=p.read_text()
old='<button class="primary chestBtn" data-chest="common">⚪ Common Pack • 🟡 250 Coins</button>'
new='''<button class="primary chestBtn packArtBtn" data-chest="common" aria-label="Common Pack, 250 Coins">
          <img src="assets/common-pack.jpg" alt="Common card pack artwork" class="packArtwork">
          <span class="packPrice">🟡 250 Coins</span>
        </button>'''
if old not in s: raise SystemExit('common pack button not found')
s=s.replace(old,new,1)
marker='</style>'
css='''
/* Common pack artwork */
#packsScreen .packArtBtn[data-chest="common"]{height:auto;min-height:0;padding:12px;background:rgba(255,255,255,.04);display:flex;flex-direction:column;align-items:center;gap:8px;overflow:visible}
#packsScreen .packArtBtn[data-chest="common"]:before,#packsScreen .packArtBtn[data-chest="common"]:after{display:none}
#packsScreen .packArtwork{display:block;width:min(58%,250px);height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:12px;box-shadow:0 7px 18px rgba(0,0,0,.35)}
#packsScreen .packPrice{font-size:18px;font-weight:900;color:#d71920;text-shadow:none}
'''
if marker not in s: raise SystemExit('style marker not found')
s=s.replace(marker,css+'\n'+marker,1)
p.write_text(s)
