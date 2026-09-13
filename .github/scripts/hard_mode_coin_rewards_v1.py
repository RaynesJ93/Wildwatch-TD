from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='HARD_MODE_COIN_REWARDS_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
# Elite/boss rewards: apply regional multiplier first, then exact Hard Mode base equivalents 36/99.
old="""function battleCoinReward(kind){
  const base=kind==='wave'?12:kind==='elite'?22:kind==='boss'?60:0;
  const hardModeMultiplier=hardMode?1.30:1;
  return Math.round(base*regionCoinMultiplier()*hardModeMultiplier);
}"""
new="""function battleCoinReward(kind){
  // HARD_MODE_COIN_REWARDS_V1: Hard rewards are 1.65x Normal, rounded to whole coins.
  const normalBase=kind==='wave'?12:kind==='elite'?22:kind==='boss'?60:0;
  const hardBase=kind==='wave'?20:kind==='elite'?36:kind==='boss'?99:0;
  const base=hardMode?hardBase:normalBase;
  return Math.round(base*regionCoinMultiplier());
}"""
if old not in s: raise RuntimeError('battleCoinReward anchor missing; coin reward update may not have deployed yet')
s=s.replace(old,new,1)
old2="""  // COIN_REWARD_UPDATE_V1: 12 permanent Coins per completed wave in Normal and Hard modes.
  save.metaCoins+=12;
  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+12;"""
new2="""  // HARD_MODE_COIN_REWARDS_V1: Normal = 12 coins/wave; Hard = 20 coins/wave (1.65x rounded).
  const permanentWaveCoins=hardMode?20:12;
  save.metaCoins+=permanentWaveCoins;
  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+permanentWaveCoins;"""
if old2 not in s: raise RuntimeError('permanent wave reward anchor missing; coin reward update may not have deployed yet')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('Applied Hard Mode rewards: 20/wave, 36/elite, 99/boss before regional multipliers')
