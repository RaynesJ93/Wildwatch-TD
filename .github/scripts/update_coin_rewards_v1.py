from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = "const base=kind==='wave'?12:kind==='elite'?20:kind==='boss'?45:0;"
new = "const base=kind==='wave'?12:kind==='elite'?22:kind==='boss'?60:0;"
if old not in s and new not in s:
    raise RuntimeError('Battle coin reward anchor not found')
s = s.replace(old, new, 1)

old2 = "// Permanent coin economy: 7 Coins per Normal wave, 12 Coins per Hard wave.\n  save.metaCoins+=hardMode?12:7;\n  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+(hardMode?12:7);"
new2 = "// COIN_REWARD_UPDATE_V1: 12 permanent Coins per completed wave in Normal and Hard modes.\n  save.metaCoins+=12;\n  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+12;"
if old2 not in s and new2 not in s:
    raise RuntimeError('Permanent wave coin anchor not found')
s = s.replace(old2, new2, 1)

p.write_text(s, encoding='utf-8')
print('Updated coin rewards: 12/wave, elite base 22, boss base 60')
