from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''startWave.onclick=()=>{\n  if(battle.ended){resetBattle();return}'''
new='''startWave.onclick=()=>{\n  if(battle.ended && battle.mapComplete){\n    battle.mapComplete=false;\n    clearBattleState();\n    if(currentMap<10){applyMap(currentSeries,currentMap+1);resetBattle();}\n    else if(currentSeries===1 && (save.desertDunesUnlocked||0)>=1){applyMap(2,1);resetBattle();}\n    else{message.textContent="🏆 All available levels complete!";startWave.textContent="Completed";}\n    return;\n  }\n  if(battle.ended){resetBattle();return}'''
if old not in s: raise SystemExit('startWave handler marker not found')
s=s.replace(old,new,1)
old2='''    battle.ended=true;\n    startWave.textContent="Map complete!";'''
new2='''    battle.ended=true;\n    battle.mapComplete=true;\n    startWave.textContent="Start Next Level";'''
if old2 not in s: raise SystemExit('map complete marker not found')
s=s.replace(old2,new2,1)
p.write_text(s)
