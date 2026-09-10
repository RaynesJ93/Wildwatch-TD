from pathlib import Path

p=Path('index.html')
s=p.read_text()

# 1) Replace old damage-upgrade persistence with proper card-level migration.
old='''save.shards={...defaults.shards,...save.shards};\nsave.cardLevels={...defaults.cardLevels,...save.cardLevels};\nsave.damageUpgrades={...defaults.damageUpgrades,...save.damageUpgrades};'''
new='''save.shards={...defaults.shards,...save.shards};\nsave.cardLevels={...defaults.cardLevels,...save.cardLevels};\n// Preserve any old +7.5% damage upgrades by converting them into card levels.\nif(save.damageUpgrades){\n  Object.keys(save.cardLevels).forEach(k=>{\n    const oldUps=save.damageUpgrades[k]||0;\n    if(oldUps>0)save.cardLevels[k]=Math.max(save.cardLevels[k]||1,1+oldUps);\n  });\n}\ndelete save.damageUpgrades;'''
if old not in s: raise SystemExit('persistence anchor missing')
s=s.replace(old,new,1)

# 2) Replace damage-only card scaling with card-level scaling helpers.
old='''function cardBaseDamage(k){const a=animals[k];return a.dmg*(1+(save.damageUpgrades[k]||0)*.075);}\nfunction towerDamage(t){'''
new='''const MAX_CARD_LEVEL=20;\nfunction cardLevel(k){return Math.max(1,Math.min(MAX_CARD_LEVEL,save.cardLevels[k]||1));}\nfunction cardLevelCost(k){const lvl=cardLevel(k);return lvl>=MAX_CARD_LEVEL?0:3+lvl*2;}\nfunction cardBaseDamage(k){const a=animals[k];return a.dmg*(1+(cardLevel(k)-1)*.05);}\nfunction cardBaseRange(k){const a=animals[k];return a.range*(1+Math.floor((cardLevel(k)-1)/5)*.025);}\nfunction cardRate(k){const a=animals[k];return a.rate*Math.pow(.98,Math.floor((cardLevel(k)-1)/5));}\nfunction towerDamage(t){'''
if old not in s: raise SystemExit('cardBaseDamage anchor missing')
s=s.replace(old,new,1)

# 3) Make tower range use permanent card level range bonus.
old='''  const range=a.range*(1+(t.level-1)*.06);'''
new='''  const range=cardBaseRange(t.key)*(1+(t.level-1)*.06);'''
if old not in s: raise SystemExit('tower range anchor missing')
s=s.replace(old,new,1)

# 4) Make attack interval use permanent card level attack-speed bonus.
old='''  t.cool=a.rate;'''
new='''  t.cool=cardRate(t.key);'''
if old not in s: raise SystemExit('tower cooldown anchor missing')
s=s.replace(old,new,1)

# 5) Replace collection card old +7.5% button/UI with level system.
old='''    const shardNeed=shardRequirement(a), dmgNow=cardBaseDamage(k), dmgUps=save.damageUpgrades[k]||0;\n    d.innerHTML=`<span class="rarity">${a.rarity==="Legendary"?"🌟 LEGENDARY":a.rarity==="Epic"?"🟣 EPIC":a.rarity==="Rare"?"💎 RARE":a.rarity==="Uncommon"?"🟩 UNCOMMON":a.rarity==="Common"?"⚪ COMMON":a.rarity}</span>${animalVisual(k,"animal-portrait")}<h3>${a.name}</h3><div class="small">${unlocked?a.desc:`🔒 Locked • Collect ${shardNeed} shards to unlock. 🧩 ${save.shards[k]||0}/${shardNeed}`}</div>${unlocked?`<div class="statrow"><span>Lvl ${save.cardLevels[k]}</span><span>⚔️ ${Math.round(dmgNow*10)/10}</span><span>🎯 ${a.range}</span><span>🧩 ${save.shards[k]||0}</span></div><button class="secondary damageUpgradeBtn" style="width:100%;margin-top:8px;padding:8px;font-size:11px" data-key="${k}">⚔️ Damage +7.5% • 🧩 5</button><div class="small" style="margin-top:4px">Damage upgrades: ${dmgUps}</div>`:`<div class="statrow"><span>🔒 Not unlocked</span><span>⚔️ ${a.dmg}</span><span>🎯 ${a.range}</span></div>`}`;\n    if(unlocked)d.onclick=()=>toggleDeck(k);\n    collectionCards.appendChild(d);\n    const upgradeBtn=d.querySelector(".damageUpgradeBtn");\n    if(upgradeBtn)upgradeBtn.onclick=ev=>{ev.stopPropagation();upgradeCardDamage(k)};'''
new='''    const shardNeed=shardRequirement(a), lvl=cardLevel(k), lvlCost=cardLevelCost(k), dmgNow=cardBaseDamage(k), rangeNow=cardBaseRange(k), maxed=lvl>=MAX_CARD_LEVEL;\n    d.innerHTML=`<span class="rarity">${a.rarity==="Legendary"?"🌟 LEGENDARY":a.rarity==="Epic"?"🟣 EPIC":a.rarity==="Rare"?"💎 RARE":a.rarity==="Uncommon"?"🟩 UNCOMMON":a.rarity==="Common"?"⚪ COMMON":a.rarity}</span>${animalVisual(k,"animal-portrait")}<h3>${a.name}</h3><div class="small">${unlocked?a.desc:`🔒 Locked • Collect ${shardNeed} shards to unlock. 🧩 ${save.shards[k]||0}/${shardNeed}`}</div>${unlocked?`<div class="statrow"><span>⭐ Card Lv ${lvl}/${MAX_CARD_LEVEL}</span><span>⚔️ ${Math.round(dmgNow*10)/10}</span><span>🎯 ${Math.round(rangeNow*10)/10}</span><span>🧩 ${save.shards[k]||0}</span></div><button class="secondary cardLevelBtn" style="width:100%;margin-top:8px;padding:8px;font-size:11px" data-key="${k}" ${maxed?'disabled':''}>${maxed?'⭐ MAX LEVEL':`⬆️ Level Up • 🧩 ${lvlCost}`}</button><div class="small" style="margin-top:4px">Each level: +5% base damage. Every 5 levels: +2.5% range and +2% attack speed.</div>`:`<div class="statrow"><span>🔒 Not unlocked</span><span>⚔️ ${a.dmg}</span><span>🎯 ${a.range}</span></div>`}`;\n    if(unlocked)d.onclick=()=>toggleDeck(k);\n    collectionCards.appendChild(d);\n    const levelBtn=d.querySelector(".cardLevelBtn");\n    if(levelBtn)levelBtn.onclick=ev=>{ev.stopPropagation();levelUpCard(k)};'''
if old not in s: raise SystemExit('collection upgrade UI anchor missing')
s=s.replace(old,new,1)

# 6) Replace old upgrade function.
old='''function upgradeCardDamage(k){\n  if(!save.unlocked.includes(k))return;\n  if((save.shards[k]||0)<5){alert("You need 5 duplicate shards to upgrade attack damage.");return}\n  save.shards[k]-=5;\n  save.damageUpgrades[k]=(save.damageUpgrades[k]||0)+1;\n  persist();\n}'''
new='''function levelUpCard(k){\n  if(!save.unlocked.includes(k))return;\n  const lvl=cardLevel(k);\n  if(lvl>=MAX_CARD_LEVEL){alert("This card is already max level.");return}\n  const cost=cardLevelCost(k);\n  if((save.shards[k]||0)<cost){alert(`You need ${cost} duplicate shards to level up ${animals[k].name}.`);return}\n  save.shards[k]-=cost;\n  save.cardLevels[k]=lvl+1;\n  persist();\n}'''
if old not in s: raise SystemExit('upgrade function anchor missing')
s=s.replace(old,new,1)

# 7) Ensure newly-added animals exist in save level/shard maps after merging old saves.
anchor='''save.cardLevels={...defaults.cardLevels,...save.cardLevels};'''
insert='''save.cardLevels={...defaults.cardLevels,...save.cardLevels};\nObject.keys(animals).forEach(k=>{if(save.cardLevels[k]==null)save.cardLevels[k]=1;if(save.shards[k]==null)save.shards[k]=0;});'''
s=s.replace(anchor,insert,1)

p.write_text(s)
