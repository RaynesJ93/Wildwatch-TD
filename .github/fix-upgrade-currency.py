from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='upgradeTower.textContent=`Upgrade • 🪙 ${up}`; towerModal.classList.add("show");'
new='upgradeTower.textContent=`Upgrade • 🥩 ${up}`; towerModal.classList.add("show");'
if old not in s: raise SystemExit('upgrade currency marker not found')
s=s.replace(old,new,1)
p.write_text(s)
