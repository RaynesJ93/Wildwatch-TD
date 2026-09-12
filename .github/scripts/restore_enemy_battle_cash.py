from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = """  e.coinRewardKind=boss?'boss':'normal';
  e.reward=0;
  if(boss)battle.finalBossSpawned=true;"""
new = """  e.coinRewardKind=boss?'boss':'normal';
  if(boss)battle.finalBossSpawned=true;"""
if old not in s:
    raise SystemExit('spawn reward reset anchor not found')
s = s.replace(old, new, 1)

old = """function killEnemy(e){if(e.dead)return;e.dead=true;const coinReward=battleCoinReward(e.coinRewardKind);battle.coins+=coinReward;battle.mapKills=(battle.mapKills||0)+1;addQuestProgress(\"kills\",1);if(coinReward)addWeeklyProgress(\"weeklyCoins\",coinReward);updateHud()}"""
new = """function killEnemy(e){if(e.dead)return;e.dead=true;const killCash=Math.max(0,Math.round(Number(e.reward)||0));const coinReward=battleCoinReward(e.coinRewardKind);battle.coins+=killCash+coinReward;battle.mapKills=(battle.mapKills||0)+1;addQuestProgress(\"kills\",1);if(coinReward)addWeeklyProgress(\"weeklyCoins\",coinReward);updateHud()}"""
if old not in s:
    raise SystemExit('killEnemy anchor not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Restored per-enemy battle cash while keeping fixed regional coin rewards')
