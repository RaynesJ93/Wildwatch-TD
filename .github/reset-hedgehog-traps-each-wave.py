from pathlib import Path
p=Path('index.html'); s=p.read_text()
old='''function finishWave(){
  const clearedWave=battle.wave;
  battle.waveActive=false;'''
new='''function finishWave(){
  const clearedWave=battle.wave;
  battle.waveActive=false;
  // Hedgehog needle stacks only last for the current wave.
  battle.needles=[];
  battle.pendingNeedles=[];
  battle.shots=(battle.shots||[]).filter(s=>s.type!=="hedgehogNeedles");'''
if old not in s: raise SystemExit('finishWave marker not found')
s=s.replace(old,new,1)
p.write_text(s)
