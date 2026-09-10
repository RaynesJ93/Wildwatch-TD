from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('<div class="pill">🪙 <span id="battleCoins">120</span></div>','<div class="pill">🥩 <span id="battleCoins">120</span></div>')
s=s.replace('<div class="cost">🪙 ${a.cost}</div>','<div class="cost">🥩 ${a.cost}</div>')
p.write_text(s)
