from pathlib import Path
p=Path('index.html')
s=p.read_text()

old='''function spawnEnemy(){\n  const e=enemyForWave();\n  if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}\n  if(battle.wave%10===0 && !battle.eliteSpawned){'''
new='''function finalMapBossForWave(){\n  if(currentMap!==10 || battle.wave!==15 || battle.finalBossSpawned)return null;\n  const bosses={\n    1:{type:"alphaBearBoss",emoji:"🐻",name:"Alpha Bear",hp:4200,speed:31,reward:150,size:42,boss:true,bossAbility:"roar"},\n    2:{type:"giantScorpionBoss",emoji:"🦂",name:"Giant Scorpion",hp:4700,speed:29,reward:175,size:43,boss:true,bossAbility:"venom"},\n    3:{type:"hauntedReaperBoss",emoji:"💀",name:"Haunted Reaper",hp:5200,speed:27,reward:200,size:45,boss:true,bossAbility:"terror"}\n  };\n  return {...bosses[currentSeries]};\n}\nfunction spawnEnemy(){\n  const boss=finalMapBossForWave();\n  const e=boss||enemyForWave();\n  if(boss)battle.finalBossSpawned=true;\n  if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}\n  if(!boss && battle.wave%10===0 && !battle.eliteSpawned){'''
if old not in s: raise SystemExit('spawnEnemy anchor not found')
s=s.replace(old,new,1)

old2='''  battle.eliteSpawned=false;\n  battle.spawnLeft=Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));'''
new2='''  battle.eliteSpawned=false;\n  battle.finalBossSpawned=false;\n  const isFinalBossWave=currentMap===10&&battle.wave===15;\n  if(isFinalBossWave){\n    const bossNames={1:"ALPHA BEAR",2:"GIANT SCORPION",3:"HAUNTED REAPER"};\n    message.textContent=`⚠️ BOSS WAVE — ${bossNames[currentSeries]}!`;\n  }\n  battle.spawnLeft=isFinalBossWave?1:Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));'''
if old2 not in s: raise SystemExit('wave anchor not found')
s=s.replace(old2,new2,1)

# Add a prominent boss bar in the normal enemy HP drawing by widening boss health bars if anchor exists.
old3='''e.elite=true;\n    battle.eliteSpawned=true;'''
# no need to alter rendering here; boss size + HP distinguish it safely.

p.write_text(s)
print('Added Wave 15 bosses to map 10 of each series')
