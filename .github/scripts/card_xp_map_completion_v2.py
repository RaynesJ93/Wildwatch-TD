from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CARD_XP_MAP_COMPLETION_V2'
if marker in s:
    print('Already applied')
    raise SystemExit(0)

old='''// CARD_XP_WAVE_REWARDS_V1: every deck card earns 300 XP per cleared wave; used cards also earn +2 XP per enemy killed that wave.
function awardWaveDeckXp(){
  const deck=[...new Set(save.deck||[])].filter(k=>save.unlocked.includes(k));
  const used=[...new Set((battle&&battle.usedCards)||[])].filter(k=>deck.includes(k));
  const kills=Math.max(0,Number(battle&&battle.waveKills||0));
  deck.forEach(k=>addCardXp(k,300));
  if(kills>0)used.forEach(k=>addCardXp(k,kills*2));
  return {base:300,kills,bonus:kills*2,usedCount:used.length,deckCount:deck.length};
}
// Legacy hook retained for compatibility; map completion/defeat no longer grants a separate used-card XP payout.
function awardUsedCardXp(completed){return 0;}'''

new='''// CARD_XP_MAP_COMPLETION_V2: +300 XP is awarded once on full map completion, not after every wave.
// Cards that have been used still gain +2 XP for every enemy killed in each cleared wave.
function awardWaveUsedKillXp(){
  const deck=[...new Set(save.deck||[])].filter(k=>save.unlocked.includes(k));
  const used=[...new Set((battle&&battle.usedCards)||[])].filter(k=>deck.includes(k));
  const kills=Math.max(0,Number(battle&&battle.waveKills||0));
  if(kills>0)used.forEach(k=>addCardXp(k,kills*2));
  return {kills,bonus:kills*2,usedCount:used.length};
}
function awardMapDeckXp(){
  const deck=[...new Set(save.deck||[])].filter(k=>save.unlocked.includes(k));
  deck.forEach(k=>addCardXp(k,300));
  return deck.length?300:0;
}
// Legacy hook retained for compatibility.
function awardUsedCardXp(completed){return 0;}'''

if old not in s:
    raise RuntimeError('V1 XP function block not found')
s=s.replace(old,new,1)

old2='''  const waveCardXp=awardWaveDeckXp();
  battle.waveKills=0;'''
new2='''  const waveCardXp=awardWaveUsedKillXp();
  battle.waveKills=0;'''
if old2 not in s:
    raise RuntimeError('wave XP call not found')
s=s.replace(old2,new2,1)

old3='''    const cardXp=0;
    setTimeout(()=>showMapSummary(cardXp),120);'''
new3='''    const cardXp=awardMapDeckXp();
    setTimeout(()=>showMapSummary(cardXp),120);'''
if old3 not in s:
    raise RuntimeError('map completion XP anchor not found')
s=s.replace(old3,new3,1)

old4="""  modal.querySelector('#mapSummaryXp').textContent='Each cleared wave: +300 EXP to every deck card • used cards also gain +2 EXP per enemy killed';"""
new4="""  modal.querySelector('#mapSummaryXp').textContent=cardXp?`+${cardXp} EXP to every deck card for completing the map • used cards also gained +2 EXP per enemy killed`:'Used cards gained +2 EXP per enemy killed';"""
if old4 not in s:
    raise RuntimeError('summary copy anchor not found')
s=s.replace(old4,new4,1)

old5='''  message.textContent=`Wave cleared! +${waveCoins} 🟡 battle coins • +300 EXP to every deck card${waveCardXp.usedCount&&waveCardXp.bonus?` • used cards +${waveCardXp.bonus} EXP from ${waveCardXp.kills} kills`:''}`;'''
new5='''  message.textContent=`Wave cleared! +${waveCoins} 🟡 battle coins${waveCardXp.usedCount&&waveCardXp.bonus?` • used cards +${waveCardXp.bonus} EXP from ${waveCardXp.kills} kills`:''}`;'''
if old5 not in s:
    raise RuntimeError('wave message anchor not found')
s=s.replace(old5,new5,1)

# Update map-completion message so the one-time deck reward is visible.
old6='''    message.textContent=`🏆 ${seriesName} ${currentSeries}-${currentMap} complete! ${nextText} • 🟡 200 bonus Coins!${cardXp?` • Used cards +${cardXp} XP each`:""}`;'''
new6='''    message.textContent=`🏆 ${seriesName} ${currentSeries}-${currentMap} complete! ${nextText} • 🟡 200 bonus Coins!${cardXp?` • Every deck card +${cardXp} XP`:""}`;'''
if old6 in s:
    s=s.replace(old6,new6,1)

p.write_text(s,encoding='utf-8')
print('Applied',marker)
