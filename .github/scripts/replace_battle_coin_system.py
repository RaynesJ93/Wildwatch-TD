from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''function spawnEnemy(){
  const boss=finalMapBossForWave();
  const e=boss||enemyForWave();
  if(boss)battle.finalBossSpawned=true;'''
new = '''// COIN_REWARDS_V2: fixed battle rewards with regional multipliers.
// Normal enemies give no coins. Wave clear = 12, elite = 20, Wave 15 boss = 45 in Forest Pines.
// Desert Dunes = 1.10x, Haunted Woods = 1.25x, Tundra Falls = 1.40x.
function regionCoinMultiplier(){
  return currentSeries===1?1:currentSeries===2?1.10:currentSeries===3?1.25:1.40;
}
function battleCoinReward(kind){
  const base=kind==='wave'?12:kind==='elite'?20:kind==='boss'?45:0;
  return Math.round(base*regionCoinMultiplier());
}
function spawnEnemy(){
  const boss=finalMapBossForWave();
  const e=boss||enemyForWave();
  e.coinRewardKind=boss?'boss':'normal';
  e.reward=0;
  if(boss)battle.finalBossSpawned=true;'''
if old not in s:
    raise SystemExit('spawnEnemy anchor not found')
s = s.replace(old, new, 1)

old = '''if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}'''
new = '''if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;}'''
if old not in s:
    raise SystemExit('hard mode reward anchor not found')
s = s.replace(old, new, 1)

old = '''    e.hp*=3;
    e.reward*=3;
    e.size=Math.round(e.size*1.18);
    e.elite=true;'''
new = '''    e.hp*=3;
    e.coinRewardKind='elite';
    e.size=Math.round(e.size*1.18);
    e.elite=true;'''
if old not in s:
    raise SystemExit('elite reward anchor not found')
s = s.replace(old, new, 1)

old = '''function killEnemy(e){if(e.dead)return;e.dead=true;battle.coins+=e.reward;battle.mapKills=(battle.mapKills||0)+1;addQuestProgress("kills",1);addWeeklyProgress("weeklyCoins",e.reward);updateHud()}'''
new = '''function killEnemy(e){if(e.dead)return;e.dead=true;const coinReward=battleCoinReward(e.coinRewardKind);battle.coins+=coinReward;battle.mapKills=(battle.mapKills||0)+1;addQuestProgress("kills",1);if(coinReward)addWeeklyProgress("weeklyCoins",coinReward);updateHud()}'''
if old not in s:
    raise SystemExit('killEnemy anchor not found')
s = s.replace(old, new, 1)

old = '''  battle.wave++;
  levelCheck();persist();
  battle.coins+=35+Math.floor(battle.wave*3);
  saveBattleState();
  startWave.textContent="Start wave";
  message.textContent=`Wave cleared! Battle cash awarded • 🟡 Coins earned${clearedWave%3===0?" • Bonus Coins!":""}`;'''
new = '''  battle.wave++;
  levelCheck();persist();
  const waveCoins=battleCoinReward('wave');
  battle.coins+=waveCoins;
  addWeeklyProgress("weeklyCoins",waveCoins);
  saveBattleState();
  startWave.textContent="Start wave";
  message.textContent=`Wave cleared! +${waveCoins} 🟡 battle coins`;'''
if old not in s:
    raise SystemExit('wave clear reward anchor not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Replaced old battle coin rewards with fixed regional reward system')
