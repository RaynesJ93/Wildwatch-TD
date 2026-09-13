from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='MAP_SUMMARY_CARD_XP_BREAKDOWN_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)

old='''  if(kills>0)used.forEach(k=>addCardXp(k,kills*2));
  return {kills,bonus:kills*2,usedCount:used.length};'''
new='''  battle.cardKillXp=battle.cardKillXp||{};
  if(kills>0)used.forEach(k=>{
    const earned=kills*2;
    addCardXp(k,earned);
    battle.cardKillXp[k]=(battle.cardKillXp[k]||0)+earned;
  });
  return {kills,bonus:kills*2,usedCount:used.length};'''
if old not in s: raise RuntimeError('kill XP anchor not found')
s=s.replace(old,new,1)

old2='''function showMapSummary(cardXp){
  const towers=(battle&&battle.towers)||[];'''
new2='''function showMapSummary(cardXp){
  // MAP_SUMMARY_CARD_XP_BREAKDOWN_V1: show exact XP earned by every card in the deck.
  const deck=[...new Set(save.deck||[])].filter(k=>save.unlocked.includes(k));
  const used=new Set((battle&&battle.usedCards)||[]);
  const killXp=(battle&&battle.cardKillXp)||{};
  const cardXpHtml=deck.map(k=>{
    const a=animals[k];
    if(!a)return '';
    const bonus=Math.max(0,Number(killXp[k]||0));
    const total=(cardXp||0)+bonus;
    return `<div style="display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.08)"><span>${a.emoji} <b>${a.name}</b>${used.has(k)?'':' <span class="small">(not used)</span>'}</span><span style="text-align:right"><b>+${total} XP</b><div class="small">${cardXp||0} map${bonus?` + ${bonus} kills`:''}</div></span></div>`;
  }).join('');
  const towers=(battle&&battle.towers)||[];'''
if old2 not in s: raise RuntimeError('summary function anchor not found')
s=s.replace(old2,new2,1)

old3='''  modal.querySelector('#mapSummaryXp').textContent=cardXp?`+${cardXp} EXP to every deck card for completing the map • used cards also gained +2 EXP per enemy killed`:'Used cards gained +2 EXP per enemy killed';'''
new3='''  modal.querySelector('#mapSummaryXp').innerHTML=cardXpHtml||'No card EXP earned';'''
if old3 not in s: raise RuntimeError('summary XP text anchor not found')
s=s.replace(old3,new3,1)

p.write_text(s,encoding='utf-8')
print('Applied',marker)
