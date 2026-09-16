from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'MASTERY_REWARDS_V2' in s:
    print('Mastery Rewards V2 already installed'); raise SystemExit(0)
old='''function masteryRewardText(k){
  const lv=masteryLevel(k),skin=lv>=10?' • 🥇 Golden skin':lv>=5?' • 🥉 Bronze skin':'';
  return `⭐ Mastery ${lv}/${MASTERY_MAX}${skin}`;
}
function masteryDamageMult(k){const lv=masteryLevel(k);return 1+(lv>=3?.02:0)+(lv>=9?.03:0);}
function masteryRangeMult(k){return masteryLevel(k)>=7?1.02:1;}'''
new='''// MASTERY_REWARDS_V2 — high-value mastery progression; M10 ability intentionally reserved for later.
function masteryRewardText(k){
  const lv=masteryLevel(k), rewards=[];
  if(lv>=1)rewards.push('+5% DMG');
  if(lv>=2)rewards.push('+5% ATK SPD','Mastery border');
  if(lv>=3)rewards.push('+5% RNG');
  if(lv>=4)rewards.push('+5% DMG','Enhanced attack VFX');
  if(lv>=5)rewards.push('Bronze skin','+10% Card XP');
  if(lv>=6)rewards.push('+5% ATK SPD','Placement VFX');
  if(lv>=7)rewards.push('+10% DMG','Upgraded attack VFX');
  if(lv>=8)rewards.push('+10% RNG','Animated mastery frame');
  if(lv>=9)rewards.push('+10% DMG','+10% ATK SPD');
  if(lv>=10)rewards.push('Golden Evolution','Golden attacks','Animated card');
  return `⭐ Mastery ${lv}/${MASTERY_MAX}${rewards.length?' • '+rewards.join(' • '):''}`;
}
function masteryDamageMult(k){const lv=masteryLevel(k);return 1+(lv>=1?.05:0)+(lv>=4?.05:0)+(lv>=7?.10:0)+(lv>=9?.10:0);}
function masteryRangeMult(k){const lv=masteryLevel(k);return 1+(lv>=3?.05:0)+(lv>=8?.10:0);}
function masteryAttackSpeedMult(k){const lv=masteryLevel(k);return 1+(lv>=2?.05:0)+(lv>=6?.05:0)+(lv>=9?.10:0);}
function masteryXpMult(k){return masteryLevel(k)>=5?1.10:1;}'''
if old not in s: raise SystemExit('Mastery reward anchor not found')
s=s.replace(old,new,1)
old_rate='function cardRate(k){const a=animals[k];return a.rate*Math.pow(.98,Math.floor(cardLevel(k)/5));}'
new_rate='function cardRate(k){const a=animals[k];return a.rate*Math.pow(.98,Math.floor(cardLevel(k)/5))/masteryAttackSpeedMult(k);}'
if old_rate not in s: raise SystemExit('cardRate anchor not found')
s=s.replace(old_rate,new_rate,1)
old_xp='save.cardXP[k]=(save.cardXP[k]||0)+Math.max(0,Math.floor(amount));'
new_xp='save.cardXP[k]=(save.cardXP[k]||0)+Math.max(0,Math.floor(amount*masteryXpMult(k)));'
if old_xp not in s: raise SystemExit('Card XP anchor not found')
s=s.replace(old_xp,new_xp,1)
# Show mastery status/rewards directly in unlocked card details.
old_details='Card level ${lvl}/${MAX_CARD_LEVEL} • Mastery ${masteryLevel(k)}/${MASTERY_MAX}'
new_details='Card level ${lvl}/${MAX_CARD_LEVEL} • ${masteryRewardText(k)}'
s=s.replace(old_details,new_details)
p.write_text(s,encoding='utf-8')
print('Installed Mastery Rewards V2 (M10 ability reserved)')
