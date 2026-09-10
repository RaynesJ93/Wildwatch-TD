from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

# Persist per-card XP alongside existing levels/shards.
s=s.replace('save.cardLevels={...defaults.cardLevels,...save.cardLevels};', 'save.cardLevels={...defaults.cardLevels,...save.cardLevels};\nsave.cardXP=save.cardXP||{};')
s=s.replace('Object.keys(animals).forEach(k=>{if(save.cardLevels[k]==null)save.cardLevels[k]=1;if(save.shards[k]==null)save.shards[k]=0;});', 'Object.keys(animals).forEach(k=>{if(save.cardLevels[k]==null)save.cardLevels[k]=1;if(save.shards[k]==null)save.shards[k]=0;if(save.cardXP[k]==null)save.cardXP[k]=0;});')

# EXP progression replaces shard-spending for card levels.
needle='function cardLevel(k){return Math.max(1,Math.min(MAX_CARD_LEVEL,save.cardLevels[k]||1));}\nfunction cardLevelCost(k){const lvl=cardLevel(k);return lvl>=MAX_CARD_LEVEL?0:3+lvl*2;}'
replacement='''function cardLevel(k){return Math.max(1,Math.min(MAX_CARD_LEVEL,save.cardLevels[k]||1));}\nfunction cardLevelCost(k){return 0;}\nfunction cardXpNeeded(k){const lvl=cardLevel(k);return lvl>=MAX_CARD_LEVEL?0:100+(lvl-1)*50;}\nfunction addCardXp(k,amount){\n  if(!save.unlocked.includes(k)||cardLevel(k)>=MAX_CARD_LEVEL)return;\n  save.cardXP[k]=(save.cardXP[k]||0)+Math.max(0,Math.floor(amount));\n  while(cardLevel(k)<MAX_CARD_LEVEL){\n    const need=cardXpNeeded(k);\n    if(save.cardXP[k]<need)break;\n    save.cardXP[k]-=need;\n    save.cardLevels[k]=cardLevel(k)+1;\n  }\n  if(cardLevel(k)>=MAX_CARD_LEVEL)save.cardXP[k]=0;\n}\nfunction awardUsedCardXp(completed){\n  const used=[...new Set((battle&&battle.usedCards)||[])].filter(k=>save.unlocked.includes(k));\n  if(!used.length)return 0;\n  const amount=completed?(hardMode?150:100):(hardMode?50:35);\n  used.forEach(k=>addCardXp(k,amount));\n  return amount;\n}'''
if needle not in s: raise SystemExit('card level function marker not found')
s=s.replace(needle,replacement,1)

# Every battle tracks only cards actually placed/used.
s=s.replace('puddles:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};','puddles:[],usedCards:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};',1)
s=s.replace('battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost});\n  message.textContent=`${a.name} placed!`;updateHud();', 'battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost});\n  if(!battle.usedCards.includes(selectedCard))battle.usedCards.push(selectedCard);\n  message.textContent=`${a.name} placed!`;updateHud();',1)

# Failed maps give reduced card XP.
old='function gameOver(){\n  battle.ended=true;clearBattleState();save.bestWave=Math.max(save.bestWave,battle.wave);save.metaCoins+=Math.max(10,battle.wave*6);save.xp+=battle.wave*8;levelCheck();persist();\n  message.textContent=`Defeat! You reached wave ${battle.wave}. Tap Start wave to restart.`;startWave.textContent="Restart";\n}'
new='''function gameOver(){\n  battle.ended=true;clearBattleState();save.bestWave=Math.max(save.bestWave,battle.wave);save.metaCoins+=Math.max(10,battle.wave*6);save.xp+=battle.wave*8;\n  const cardXp=awardUsedCardXp(false);\n  levelCheck();persist();\n  message.textContent=`Defeat! You reached wave ${battle.wave}.${cardXp?` Used cards earned +${cardXp} XP each.`:""} Tap Start wave to restart.`;startWave.textContent="Restart";\n}'''
if old not in s: raise SystemExit('gameOver marker not found')
s=s.replace(old,new,1)

# Completed maps give full card XP to used cards only.
s=s.replace('  if(clearedWave>=15){\n    save.metaCoins+=hardMode?300:200;', '  if(clearedWave>=15){\n    const cardXp=awardUsedCardXp(true);\n    save.metaCoins+=hardMode?300:200;',1)
s=s.replace('message.textContent=`🏆 ${seriesName} ${currentSeries}-${currentMap} complete! ${nextText} • 🟡 200 bonus Coins!`;', 'message.textContent=`🏆 ${seriesName} ${currentSeries}-${currentMap} complete! ${nextText} • 🟡 200 bonus Coins!${cardXp?` • Used cards +${cardXp} XP each`:""}`;',1)

# Collection cards show EXP progress, and the old manual shard level-up control becomes non-interactive EXP status.
s=s.replace('<span>🧩 ${save.shards[k]||0}</span></div><button class="secondary cardLevelBtn"', '<span>✨ XP ${(save.cardXP[k]||0)}/${cardLevel(k)>=MAX_CARD_LEVEL?"MAX":cardXpNeeded(k)}</span></div><button class="secondary cardLevelBtn"',1)
s=s.replace('    if(levelBtn)levelBtn.onclick=ev=>{ev.stopPropagation();levelUpCard(k)};', '    if(levelBtn){levelBtn.disabled=true;levelBtn.style.opacity=".8";levelBtn.textContent=maxed?"MAX LEVEL":`EXP ${save.cardXP[k]||0}/${cardXpNeeded(k)}`;}')

# Disable/remove any remaining shard-spending level-up function behaviour.
s=re.sub(r'function levelUpCard\(k\)\{.*?\n\}', 'function levelUpCard(k){return;}', s, count=1, flags=re.S)

p.write_text(s)
