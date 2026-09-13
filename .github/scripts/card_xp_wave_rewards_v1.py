from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CARD_XP_WAVE_REWARDS_V1'
if marker in s:
    print('Card XP wave rewards already applied')
    raise SystemExit(0)

old='''function awardUsedCardXp(completed){
  const used=[...new Set((battle&&battle.usedCards)||[])].filter(k=>save.unlocked.includes(k));
  if(!used.length)return 0;
  const amount=completed?(hardMode?150:100):(hardMode?50:35);
  used.forEach(k=>addCardXp(k,amount));
  return amount;
}'''
new='''// CARD_XP_WAVE_REWARDS_V1: every deck card earns 300 XP per cleared wave; used cards also earn +2 XP per enemy killed that wave.
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
if old not in s:
    raise RuntimeError('awardUsedCardXp anchor not found')
s=s.replace(old,new,1)

# Count kills within the current wave. killEnemy already owns the canonical enemy-death path.
kill_patterns=[
    'battle.mapKills=(battle.mapKills||0)+1;',
    'battle.mapKills = (battle.mapKills||0) + 1;',
    'battle.mapKills=(battle.mapKills||0) + 1;',
]
replaced=False
for pat in kill_patterns:
    if pat in s:
        s=s.replace(pat, pat+'\n  battle.waveKills=(battle.waveKills||0)+1;',1)
        replaced=True
        break
if not replaced:
    # Fall back to adding beside the existing kills quest progress in killEnemy.
    pat='addQuestProgress("kills",1);'
    if pat in s:
        s=s.replace(pat,'battle.waveKills=(battle.waveKills||0)+1;\n  '+pat,1)
        replaced=True
if not replaced:
    raise RuntimeError('kill counter anchor not found')

# Award XP at every successful wave clear before the map-complete branch.
anchor='''  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+permanentWaveCoins;
  if(autoWave && clearedWave<15 && !battle.ended){'''
insert='''  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+permanentWaveCoins;
  const waveCardXp=awardWaveDeckXp();
  battle.waveKills=0;
  if(autoWave && clearedWave<15 && !battle.ended){'''
if anchor not in s:
    raise RuntimeError('finishWave XP anchor not found')
s=s.replace(anchor,insert,1)

# Remove old map-completion XP payout and keep the summary compatible.
s=s.replace('''    const cardXp=awardUsedCardXp(true);
    setTimeout(()=>showMapSummary(cardXp),120);''','''    const cardXp=0;
    setTimeout(()=>showMapSummary(cardXp),120);''',1)

# Remove old defeat XP payout.
s=s.replace('''  const cardXp=awardUsedCardXp(false);
  levelCheck();persist();
  message.textContent=`Defeat! You reached wave ${battle.wave}.${cardXp?` Used cards earned +${cardXp} XP each.`:""} Tap Start wave to restart.`;startWave.textContent="Restart";''','''  const cardXp=0;
  levelCheck();persist();
  message.textContent=`Defeat! You reached wave ${battle.wave}. Tap Start wave to restart.`;startWave.textContent="Restart";''',1)

# Update the map-summary XP copy so it reflects the new system instead of the removed completion bonus.
s=s.replace('''  modal.querySelector('#mapSummaryXp').textContent=cardXp?`+${cardXp} EXP to each used card`:'No card EXP earned';''','''  modal.querySelector('#mapSummaryXp').textContent='Each cleared wave: +300 EXP to every deck card • used cards also gain +2 EXP per enemy killed';''',1)

# Update normal wave-clear feedback with the new XP reward.
s=s.replace('''  message.textContent=`Wave cleared! +${waveCoins} 🟡 battle coins`;''','''  message.textContent=`Wave cleared! +${waveCoins} 🟡 battle coins • +300 EXP to every deck card${waveCardXp.usedCount&&waveCardXp.bonus?` • used cards +${waveCardXp.bonus} EXP from ${waveCardXp.kills} kills`:''}`;''',1)

p.write_text(s,encoding='utf-8')
print('Applied',marker)
