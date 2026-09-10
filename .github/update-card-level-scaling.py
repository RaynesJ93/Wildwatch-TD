from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

s=s.replace('const MAX_CARD_LEVEL=20;','const MAX_CARD_LEVEL=50;',1)

old='function cardXpNeeded(k){const lvl=cardLevel(k);return lvl>=MAX_CARD_LEVEL?0:100+(lvl-1)*50;}'
new='''function cardXpNeeded(k){
  const lvl=cardLevel(k);
  if(lvl>=MAX_CARD_LEVEL)return 0;
  if(lvl===1)return 100;
  if(lvl===2)return 175;
  let need=175;
  for(let level=3;level<=lvl;level++)need=Math.ceil(need*1.60);
  return need;
}'''
if old not in s:
    raise SystemExit('cardXpNeeded marker not found')
s=s.replace(old,new,1)

old='function cardBaseDamage(k){const a=animals[k];return a.dmg*(1+(cardLevel(k)-1)*.05);}'
new='function cardBaseDamage(k){const a=animals[k];return a.dmg*(1+(cardLevel(k)-1)*.06);}'
if old not in s:
    raise SystemExit('cardBaseDamage marker not found')
s=s.replace(old,new,1)

old='function cardBaseRange(k){const a=animals[k];return a.range*(1+Math.floor(cardLevel(k)/5)*.025);}'
new='function cardBaseRange(k){const a=animals[k];return a.range*(1+(cardLevel(k)-1)*.035);}'
if old not in s:
    raise SystemExit('cardBaseRange marker not found')
s=s.replace(old,new,1)

s=s.replace('Each card level gives +5% base damage. Levels 5, 10, 15 and 20 also improve range and attack speed.','Each card level gives +6% base damage and +3.5% attack range. Cards can reach Level 50.',1)

p.write_text(s)
