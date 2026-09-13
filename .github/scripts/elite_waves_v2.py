from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='ELITE_WAVES_V2'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old="""  if(!boss && battle.wave%10===0 && !battle.eliteSpawned){
    e.hp*=3;
    e.coinRewardKind='elite';
    e.size=Math.round(e.size*1.18);
    e.elite=true;
    battle.eliteSpawned=true;
  }"""
new="""  // ELITE_WAVES_V2: Wave 5 has 2 elites; Wave 10 has 6 elites, alongside the full normal wave.
  const eliteTarget=battle.wave===5?2:battle.wave===10?6:0;
  battle.elitesSpawned=Number(battle.elitesSpawned||0);
  if(!boss && eliteTarget>0 && battle.elitesSpawned<eliteTarget){
    e.hp*=3;
    e.coinRewardKind='elite';
    e.size=Math.round(e.size*1.18);
    e.elite=true;
    battle.elitesSpawned++;
  }"""
if old not in s: raise RuntimeError('old elite spawn anchor missing')
s=s.replace(old,new,1)
old2="""  battle.eliteSpawned=false;
  battle.finalBossSpawned=false;
  const isBossWave=battle.wave===15;"""
new2="""  battle.eliteSpawned=false;
  battle.elitesSpawned=0;
  battle.finalBossSpawned=false;
  const isBossWave=battle.wave===15;"""
if old2 not in s: raise RuntimeError('wave reset anchor missing')
s=s.replace(old2,new2,1)
# Add elites on top of the normal enemy count, rather than converting normal enemies.
old3="""  battle.spawnLeft=isBossWave?1:Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));"""
new3="""  const normalWaveCount=Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));
  const bonusEliteCount=battle.wave===5?2:battle.wave===10?6:0;
  battle.spawnLeft=isBossWave?1:normalWaveCount+bonusEliteCount;"""
if old3 not in s: raise RuntimeError('spawn count anchor missing')
s=s.replace(old3,new3,1)
p.write_text(s,encoding='utf-8')
print('Applied elite waves V2')
