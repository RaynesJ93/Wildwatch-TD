from pathlib import Path

p = Path('index.html')
s = p.read_text()

old = '''function spawnEnemy(){
  const boss=finalMapBossForWave();
  const e=boss||enemyForWave();
  if(boss)battle.finalBossSpawned=true;
  if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}'''

new = '''function spawnEnemy(){
  const boss=finalMapBossForWave();
  const e=boss||enemyForWave();
  if(boss)battle.finalBossSpawned=true;
  // SERIES_DIFFICULTY_V1: later map series have a clear enemy HP step-up.
  // Forest Pines = 1.00x, Desert Dunes = 1.20x, Haunted Woods = 1.45x.
  const seriesDifficulty=currentSeries===1?1:currentSeries===2?1.20:1.45;
  e.hp=Math.round(e.hp*seriesDifficulty);
  if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}'''

if old not in s:
    raise SystemExit('spawnEnemy insertion point not found')

s = s.replace(old, new, 1)
p.write_text(s)
print('Added series difficulty multipliers: Forest 1.00x, Desert 1.20x, Haunted 1.45x')
