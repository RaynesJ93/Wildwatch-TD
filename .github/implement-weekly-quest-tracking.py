from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
marker='function renderExtraQuestBoards(){'
if marker not in s: raise SystemExit('weekly render marker missing')
helper='''function weekKey(){const d=new Date(),x=new Date(Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate()));x.setUTCDate(x.getUTCDate()+4-(x.getUTCDay()||7));const y=new Date(Date.UTC(x.getUTCFullYear(),0,1));return x.getUTCFullYear()+"-W"+String(Math.ceil((((x-y)/86400000)+1)/7)).padStart(2,"0")}
function ensureWeeklyQuests(){const k=weekKey();if(!save.weeklyQuests||save.weeklyQuests.week!==k)save.weeklyQuests={week:k,progress:{},claimed:{}}}
function addWeeklyProgress(type,n=1){ensureWeeklyQuests();save.weeklyQuests.progress[type]=(save.weeklyQuests.progress[type]||0)+n;persist();renderExtraQuestBoards()}
'''
if 'function addWeeklyProgress(' not in s:s=s.replace(marker,helper+marker,1)
# Make dropdown progress use weekly save data instead of missing generic counters.
old="const prog=Number(save.questStats?.[q.type]||save[q.type]||0);"
new="ensureWeeklyQuests(); const prog=q.type&&q.type.startsWith('weekly')?Number(save.weeklyQuests.progress[q.type]||0):Number(save.questStats?.[q.type]||save[q.type]||0);"
if old in s:s=s.replace(old,new,1)
# Wave completed hook: daily waves already has a reliable call.
needle='addQuestProgress("waves",1);'
if needle in s and 'addWeeklyProgress("weeklyWaves",1);' not in s:s=s.replace(needle,needle+'\n    addWeeklyProgress("weeklyWaves",1);',1)
# Coins earned from enemy kills.
needle='battle.coins+=e.reward;addQuestProgress("kills",1);'
if needle in s and 'weeklyCoins' not in s[s.find('function killEnemy'):s.find('function towerTick')]:s=s.replace(needle,'battle.coins+=e.reward;addQuestProgress("kills",1);addWeeklyProgress("weeklyCoins",e.reward);',1)
# Tower placement: count common/legendary rarity.
needle='addQuestProgress("placed",1);'
insert='addQuestProgress("placed",1);\n  if(animals[selectedCard]?.rarity==="Common")addWeeklyProgress("weeklyCommonPlaced",1);\n  if(animals[selectedCard]?.rarity==="Legendary")addWeeklyProgress("weeklyLegendaryPlaced",1);'
if needle in s and 'weeklyCommonPlaced' not in s[s.find(needle):s.find(needle)+300]:s=s.replace(needle,insert,1)
# Player level progress: derive from star/player level increments if a direct hook exists later; preserve existing display until hooked.
p.write_text(s,encoding='utf-8')
