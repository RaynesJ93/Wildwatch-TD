from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Placement: current game places towers directly with an object literal, so hook that real path.
old='battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost});'
new=old+'\n  addQuestProgress("placed",1);'
if 'addQuestProgress("placed",1);' not in s:
    if old not in s: raise SystemExit('Active tower placement marker not found')
    s=s.replace(old,new,1)

# Kills: centralize quest progress in killEnemy so every tower/projectile kill counts.
oldkill='function killEnemy(e){if(e.dead)return;e.dead=true;battle.coins+=e.reward;updateHud()}'
newkill='function killEnemy(e){if(e.dead)return;e.dead=true;battle.coins+=e.reward;addQuestProgress("kills",1);updateHud()}'
if newkill not in s:
    if oldkill not in s: raise SystemExit('killEnemy marker not found')
    s=s.replace(oldkill,newkill,1)

p.write_text(s,encoding='utf-8')
