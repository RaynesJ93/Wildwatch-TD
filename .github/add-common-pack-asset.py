from pathlib import Path
p=Path('index.html'); s=p.read_text()
old='<button class="primary chestBtn" data-chest="common">⚪ Common Pack • 🟡 250 Coins</button>'
new='''<button class="primary chestBtn commonPackAsset" data-chest="common"><span class="packArt" aria-hidden="true"><span class="packSeal"></span><span class="packPaw">🐾</span><span class="packWord">COMMON</span><span class="packMini">PACK</span></span><span class="packPrice">🟡 250 Coins</span></button>'''
if old not in s: raise SystemExit('common pack button not found')
s=s.replace(old,new,1)
css='''
/* Simple in-game Common pack asset */
#packsScreen .commonPackAsset{min-height:150px;display:flex;align-items:center;justify-content:center;gap:22px;background:linear-gradient(135deg,#ffffff,#e5e5e5 55%,#fafafa);color:#b51f2e!important;text-shadow:none!important}
#packsScreen .packArt{width:88px;height:120px;border:2px solid #b9b9b9;border-radius:8px;background:linear-gradient(145deg,#fff,#dcdcdc 55%,#fff);box-shadow:inset 0 0 12px rgba(0,0,0,.12),0 4px 8px rgba(0,0,0,.2);display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden;flex:none}
#packsScreen .packArt:before,#packsScreen .packArt:after{content:"";position:absolute;left:0;right:0;height:8px;background:repeating-linear-gradient(90deg,#aaa 0 4px,#f5f5f5 4px 8px)}
#packsScreen .packArt:before{top:0}#packsScreen .packArt:after{bottom:0}
#packsScreen .packPaw{font-size:27px;filter:grayscale(1);margin-bottom:5px}
#packsScreen .packWord{font-size:14px;font-weight:1000;letter-spacing:.6px;color:#b51f2e}
#packsScreen .packMini{font-size:10px;font-weight:900;letter-spacing:1.4px;color:#b51f2e;margin-top:2px}
#packsScreen .packPrice{font-size:18px;font-weight:1000;color:#b51f2e}
'''
marker='</style>'
if marker not in s: raise SystemExit('style marker not found')
s=s.replace(marker,css+'\n'+marker,1)
p.write_text(s)
