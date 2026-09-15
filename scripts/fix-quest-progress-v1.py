from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# placements: track unique tower types and weekly placement
old='addQuestProgress("placed",1);\n  if(animals[selectedCard]?.rarity==="Common")'
new='addQuestProgress("placed",1);addWeeklyProgress("placed",1);\n  battle.questTowerTypes=battle.questTowerTypes||[];if(!battle.questTowerTypes.includes(selectedCard)){battle.questTowerTypes.push(selectedCard);addQuestProgress("uniqueTowerTypes",1);}\n  if(animals[selectedCard]?.rarity==="Common")'
if old not in s: raise SystemExit('placement marker missing')
s=s.replace(old,new,1)
# upgrades
old='battle.upgradeCount=Math.max(0,Number(battle.upgradeCount||0))+1;\n  if((battle.towers||[]).filter'
new='battle.upgradeCount=Math.max(0,Number(battle.upgradeCount||0))+1;addQuestProgress("upgrades",1);addWeeklyProgress("upgrades",1);\n  if((battle.towers||[]).filter'
if old not in s: raise SystemExit('upgrade marker missing')
s=s.replace(old,new,1)
# kill tracking + targeting mode
old='battle.waveKills=(battle.waveKills||0)+1;addQuestProgress("kills",1);if(coinReward)addWeeklyProgress("weeklyCoins",coinReward);updateHud()}'
new='battle.waveKills=(battle.waveKills||0)+1;addQuestProgress("kills",1);addWeeklyProgress("kills",1);\n  const killer=battle.lastAttackingTower||null;if(killer){const mode=killer.targetMode||"first";if(mode==="first"){addQuestProgress("firstKills",1);addWeeklyProgress("firstKills",1);}else if(mode==="strongest"){addQuestProgress("strongestKills",1);addWeeklyProgress("strongestKills",1);}}\n  if(coinReward){addQuestProgress("battleCurrency",coinReward);addWeeklyProgress("battleCurrency",coinReward);}updateHud()}'
if old not in s: raise SystemExit('kill marker missing')
s=s.replace(old,new,1)
# identify attacking tower while tower tick executes
old='function towerTickCore(t,dt){\n  t.cd-=dt;'
new='function towerTickCore(t,dt){\n  battle.lastAttackingTower=t;\n  t.cd-=dt;'
if old not in s: raise SystemExit('tower tick marker missing')
s=s.replace(old,new,1)
# damage quest: approximate actual tower damage dealt per attack at computed damage point
old='const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;'
new='const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;addQuestProgress("damage",Math.max(0,Math.round(dmg)));addWeeklyProgress("damage",Math.max(0,Math.round(dmg)));'
if old not in s: raise SystemExit('damage marker missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Quest progress tracking patched')
