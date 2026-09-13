from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='REPAIR_ELITES_SUMMARY_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)

# 1) Correct live coin rewards to the requested values.
coin_pat=re.compile(r"function battleCoinReward\(kind\)\{.*?\n\}",re.S)
coin_new="""function battleCoinReward(kind){
  // REPAIR_ELITES_SUMMARY_V1: requested Normal/Hard reward tables.
  const normalBase=kind==='wave'?12:kind==='elite'?22:kind==='boss'?60:0;
  const hardBase=kind==='wave'?20:kind==='elite'?36:kind==='boss'?99:0;
  const base=hardMode?hardBase:normalBase;
  return Math.round(base*regionCoinMultiplier());
}"""
s,n=coin_pat.subn(coin_new,s,count=1)
if n!=1: raise RuntimeError('battleCoinReward function not found')

old_perm="""  // Permanent coin economy: 7 Coins per Normal wave, 12 Coins per Hard wave.
  save.metaCoins+=hardMode?12:7;
  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+(hardMode?12:7);"""
new_perm="""  // REPAIR_ELITES_SUMMARY_V1: permanent wave rewards match the requested table.
  const permanentWaveCoins=hardMode?20:12;
  save.metaCoins+=permanentWaveCoins;
  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+permanentWaveCoins;"""
if old_perm not in s: raise RuntimeError('permanent coin anchor not found')
s=s.replace(old_perm,new_perm,1)

# 2) Wave 5 = 2 bonus elites, Wave 10 = 6 bonus elites, without removing normal enemies.
old_elite="""  if(!boss && battle.wave%10===0 && !battle.eliteSpawned){
    e.hp*=3;
    e.coinRewardKind='elite';
    e.size=Math.round(e.size*1.18);
    e.elite=true;
    battle.eliteSpawned=true;
  }"""
new_elite="""  // REPAIR_ELITES_SUMMARY_V1: 2 elites on Wave 5 and 6 elites on Wave 10.
  const eliteTarget=battle.wave===5?2:battle.wave===10?6:0;
  battle.elitesSpawned=Number(battle.elitesSpawned||0);
  if(!boss && eliteTarget>0 && battle.elitesSpawned<eliteTarget){
    e.hp*=3;
    e.coinRewardKind='elite';
    e.size=Math.round(e.size*1.18);
    e.elite=true;
    battle.elitesSpawned++;
  }"""
if old_elite not in s: raise RuntimeError('elite conversion anchor not found')
s=s.replace(old_elite,new_elite,1)

old_reset="""  battle.eliteSpawned=false;
  battle.finalBossSpawned=false;
  const isBossWave=battle.wave===15;"""
new_reset="""  battle.eliteSpawned=false;
  battle.elitesSpawned=0;
  battle.finalBossSpawned=false;
  const isBossWave=battle.wave===15;"""
if old_reset not in s: raise RuntimeError('elite reset anchor not found')
s=s.replace(old_reset,new_reset,1)

old_count="""  const normalWaveCount=Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));
  const previousWaveCount=Math.ceil((6+(battle.wave-1)*2)*(hardMode?1.25:1));
  const bossEscortCount=Math.max(8,Math.ceil(previousWaveCount*.55));
  battle.spawnLeft=isBossWave?1+bossEscortCount:normalWaveCount;"""
new_count="""  const normalWaveCount=Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));
  const previousWaveCount=Math.ceil((6+(battle.wave-1)*2)*(hardMode?1.25:1));
  const bossEscortCount=Math.max(8,Math.ceil(previousWaveCount*.55));
  const bonusEliteCount=battle.wave===5?2:battle.wave===10?6:0;
  battle.spawnLeft=isBossWave?1+bossEscortCount:normalWaveCount+bonusEliteCount;"""
if old_count not in s: raise RuntimeError('spawn count anchor not found')
s=s.replace(old_count,new_count,1)

# 3) Track actual direct damage per tower without rewriting every attack branch.
if 'function towerTickCore(t,dt){' not in s:
    anchor='function towerTick(t,dt){'
    if anchor not in s: raise RuntimeError('towerTick anchor not found')
    s=s.replace(anchor,'function towerTickCore(t,dt){',1)
    wrap="""
function towerTick(t,dt){
  const hpBefore=((battle&&battle.enemies)||[]).reduce((sum,e)=>sum+Math.max(0,Number(e.hp)||0),0);
  towerTickCore(t,dt);
  const hpAfter=((battle&&battle.enemies)||[]).reduce((sum,e)=>sum+Math.max(0,Number(e.hp)||0),0);
  const dealt=Math.max(0,hpBefore-hpAfter);
  if(dealt>0){
    t.damageDealt=(Number(t.damageDealt)||0)+dealt;
    const best=battle.topDamageTower;
    if(!best || t.damageDealt>best.damage){
      battle.topDamageTower={key:t.key,level:t.level,damage:t.damageDealt};
    }else if(best && best.key===t.key && t.damageDealt>=best.damage){
      best.level=t.level;best.damage=t.damageDealt;
    }
  }
}
"""
    show_anchor='function showMapSummary(cardXp){'
    if show_anchor not in s: raise RuntimeError('showMapSummary anchor not found')
    s=s.replace(show_anchor,wrap+'\n'+show_anchor,1)

# 4) Replace the old "strongest by stat" summary with actual map damage.
summary_pat=re.compile(r"  const towers=\(battle&&battle\.towers\)\|\|\[\];\n  let strongest=null;\n  towers\.forEach\(t=>\{.*?    : `<b>No towers deployed</b>`;",re.S)
summary_new="""  const towers=(battle&&battle.towers)||[];
  const top=battle&&battle.topDamageTower;
  const strongestHtml=top&&animals[top.key]
    ? `${animals[top.key].emoji} <b>${animals[top.key].name}</b><div class=\"small\">Tower Lv ${top.level} • ${Math.round(top.damage).toLocaleString()} total damage dealt</div>`
    : `<b>No tower damage recorded</b>`;"""
s,n=summary_pat.subn(summary_new,s,count=1)
if n!=1: raise RuntimeError('summary strongest block not found')

s=s.replace('Strongest tower deployed','Top damage tower',1)

old_sub="modal.querySelector('#mapSummarySubtitle').textContent=`${seriesName} ${currentMap} • ${hardMode?'Hard':'Normal'}`;"
new_sub="""const rewardRates=hardMode?'20/wave • 36/elite • 99/boss':'12/wave • 22/elite • 60/boss';
  modal.querySelector('#mapSummarySubtitle').textContent=`${seriesName} ${currentMap} • ${hardMode?'Hard':'Normal'} • ${rewardRates}`;"""
if old_sub not in s: raise RuntimeError('summary subtitle anchor not found')
s=s.replace(old_sub,new_sub,1)

p.write_text(s,encoding='utf-8')
print('Applied REPAIR_ELITES_SUMMARY_V1 successfully')
