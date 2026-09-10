from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''  towerInfo.textContent=`Damage ${Math.round(towerDamage(t))} • Range ${Math.round(cardBaseRange(t.key)*(1+(t.level-1)*.06))} • Upgrade cost ${up}`;\n  upgradeTower.textContent=`Upgrade • 🥩 ${up}`; towerModal.classList.add("show");'''
if old not in s:
    old='''  towerInfo.textContent=`Damage ${Math.round(towerDamage(t))} • Range ${Math.round(cardBaseRange(t.key)*(1+(t.level-1)*.06))} • Upgrade cost ${up}`;\n  upgradeTower.textContent=`Upgrade • 🪙 ${up}`; towerModal.classList.add("show");'''
new='''  const cash=Math.floor(battle.coins);\n  towerInfo.textContent=`Damage ${Math.round(towerDamage(t))} • Range ${Math.round(cardBaseRange(t.key)*(1+(t.level-1)*.06))} • Upgrade cost 🥩 ${up} • You have 🥩 ${cash}`;\n  upgradeTower.textContent=`Upgrade • 🥩 ${up}`;\n  upgradeTower.disabled=cash<up;\n  upgradeTower.style.opacity=cash<up?".55":"1";\n  towerModal.classList.add("show");'''
if old not in s: raise SystemExit('upgrade panel marker not found')
s=s.replace(old,new,1)
p.write_text(s)
