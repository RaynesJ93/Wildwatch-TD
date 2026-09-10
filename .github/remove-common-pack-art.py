from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='<button class="primary chestBtn packArtBtn" data-chest="common"><img src="assets/common-pack.jpg" alt="Common Pack artwork" class="packArtwork"><span>⚪ Common Pack • 🟡 250 Coins</span></button>'
new='<button class="primary chestBtn simplePackBtn commonPack" data-chest="common"><span class="simplePackArt"><span class="simplePaw">🐾</span><b>COMMON</b><small>PACK</small></span><span class="simplePackPrice">🟡 250 Coins</span></button>'
if old not in s:
    raise SystemExit('Common artwork pack button not found')
s=s.replace(old,new,1)
css='''\n#packsScreen .commonPack .simplePackArt{background:linear-gradient(145deg,#ffffff,#d7d7d7 58%,#f4f4f4);border-color:#ffffff}\n#packsScreen .commonPack .simplePackArt b,#packsScreen .commonPack .simplePackArt small{color:#242424;text-shadow:none}\n'''
if '#packsScreen .commonPack .simplePackArt{' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s)
