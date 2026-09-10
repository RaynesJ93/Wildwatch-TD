from pathlib import Path
p=Path('index.html'); s=p.read_text()
repls={
'<button class="primary chestBtn" data-chest="uncommon">🟢 Uncommon Pack • 🟡 500 Coins</button>':'<button class="primary chestBtn simplePackBtn uncommonPack" data-chest="uncommon"><span class="simplePackArt"><span class="simplePaw">🐾</span><b>UNCOMMON</b><small>PACK</small></span><span class="simplePackPrice">🟡 500 Coins</span></button>',
'<button class="primary chestBtn" data-chest="epic">🔵 Rare Pack • 🟡 750 Coins</button>':'<button class="primary chestBtn simplePackBtn rarePack" data-chest="epic"><span class="simplePackArt"><span class="simplePaw">🐾</span><b>RARE</b><small>PACK</small></span><span class="simplePackPrice">🟡 750 Coins</span></button>',
'<button class="primary chestBtn" data-chest="legendary">🟡 Legendary Pack • 🟡 1500 Coins</button>':'<button class="primary chestBtn simplePackBtn legendaryPack" data-chest="legendary"><span class="simplePackArt"><span class="simplePaw">🐾</span><b>LEGENDARY</b><small>PACK</small></span><span class="simplePackPrice">🟡 1500 Coins</span></button>'
}
for old,new in repls.items():
    if old not in s: raise SystemExit('pack button not found: '+old[:60])
    s=s.replace(old,new,1)
css='''
/* Simple rarity pack assets */
#packsScreen .simplePackBtn{height:auto;min-height:0;padding:12px;display:flex;flex-direction:column;align-items:center;gap:8px}
#packsScreen .simplePackArt{width:min(180px,48vw);aspect-ratio:2/3;border-radius:10px;border:2px solid rgba(255,255,255,.55);box-shadow:inset 0 0 18px rgba(255,255,255,.2),0 5px 14px rgba(0,0,0,.3);display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden}
#packsScreen .simplePackArt:before,#packsScreen .simplePackArt:after{content:"";position:absolute;left:0;right:0;height:11px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.55) 0 6px,rgba(0,0,0,.14) 6px 11px)}
#packsScreen .simplePackArt:before{top:0}#packsScreen .simplePackArt:after{bottom:0}
#packsScreen .simplePaw{font-size:42px;filter:grayscale(1);margin-bottom:12px}
#packsScreen .simplePackArt b{font-size:20px;letter-spacing:1px;color:#fff;text-shadow:0 2px 3px #0008}
#packsScreen .simplePackArt small{font-size:12px;letter-spacing:3px;color:#fff;font-weight:900;margin-top:5px;text-shadow:0 2px 3px #0008}
#packsScreen .uncommonPack .simplePackArt{background:linear-gradient(145deg,#45df6b,#08752b 58%,#20b84b)}
#packsScreen .rarePack .simplePackArt{background:linear-gradient(145deg,#55adff,#0754b8 58%,#2389ed)}
#packsScreen .legendaryPack .simplePackArt{background:linear-gradient(145deg,#ffe879,#b87800 58%,#f4c32d);border-color:#fff0a0}
#packsScreen .legendaryPack .simplePackArt b,#packsScreen .legendaryPack .simplePackArt small{color:#402800;text-shadow:none}
#packsScreen .simplePackPrice{font-weight:1000;color:#e53935}
'''
if '</style>' not in s: raise SystemExit('style marker not found')
s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s)
