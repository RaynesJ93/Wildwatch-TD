from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='function updateHud(){battleCoins.textContent=Math.floor(battle.coins); lives.textContent=battle.lives; wave.textContent=`${Math.min(battle.wave,15)}/15`;document.querySelectorAll(".battle-card").forEach(b=>b.classList.toggle("disabled",animals[b.dataset.key].cost>battle.coins))}'
new='''function updateHud(){
  battleCoins.textContent=Math.floor(battle.coins);
  lives.textContent=battle.lives;
  wave.textContent=`${Math.min(battle.wave,15)}/15`;
  document.querySelectorAll(".battle-card").forEach(b=>b.classList.toggle("disabled",animals[b.dataset.key].cost>battle.coins));
  if(selectedTower && towerModal.classList.contains("show")){
    const a=animals[selectedTower.key], up=Math.floor(a.cost*.595*selectedTower.level), cash=Math.floor(battle.coins);
    towerInfo.textContent=`Damage ${Math.round(towerDamage(selectedTower))} • Range ${Math.round(cardBaseRange(selectedTower.key)*(1+(selectedTower.level-1)*.06))} • Upgrade cost 🥩 ${up} • You have 🥩 ${cash}`;
    upgradeTower.textContent=`Upgrade • 🥩 ${up}`;
    upgradeTower.disabled=cash<up;
    upgradeTower.style.opacity=cash<up?".55":"1";
  }
}'''
if old not in s:
    raise SystemExit('updateHud marker not found')
s=s.replace(old,new,1)
p.write_text(s)
