from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Track map stats on reset.
old='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],needles:[],pineapples:[],usedCards:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'
new='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],needles:[],pineapples:[],usedCards:[],mapKills:0,mapCoinsEarned:0,spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'
if old not in s: raise SystemExit('resetBattle object marker not found')
s=s.replace(old,new,1)

# Count defeated enemies.
old='function killEnemy(e){if(e.dead)return;e.dead=true;battle.coins+=e.reward;addQuestProgress("kills",1);addWeeklyProgress("weeklyCoins",e.reward);updateHud()}'
new='function killEnemy(e){if(e.dead)return;e.dead=true;battle.coins+=e.reward;battle.mapKills=(battle.mapKills||0)+1;addQuestProgress("kills",1);addWeeklyProgress("weeklyCoins",e.reward);updateHud()}'
if old not in s: raise SystemExit('killEnemy marker not found')
s=s.replace(old,new,1)

# Count permanent coins earned from cleared waves.
old='save.metaCoins+=hardMode?12:7;'
new='save.metaCoins+=hardMode?12:7;\n  battle.mapCoinsEarned=(battle.mapCoinsEarned||0)+(hardMode?12:7);'
if old not in s: raise SystemExit('wave coin marker not found')
s=s.replace(old,new,1)

# Add the summary modal helper before gameOver.
anchor='function gameOver(){'
if anchor not in s: raise SystemExit('gameOver anchor not found')
helper=r'''function showMapSummary(cardXp){
  const towers=(battle&&battle.towers)||[];
  let strongest=null;
  towers.forEach(t=>{
    const power=towerDamage(t);
    if(!strongest || power>strongest.power || (power===strongest.power&&t.level>strongest.t.level))strongest={t,power};
  });
  const strongestHtml=strongest
    ? `${animals[strongest.t.key].emoji} <b>${animals[strongest.t.key].name}</b><div class="small">Tower Lv ${strongest.t.level} • ${Math.round(strongest.power)} damage</div>`
    : `<b>No towers deployed</b>`;
  let modal=document.getElementById('mapSummaryModal');
  if(!modal){
    modal=document.createElement('div');
    modal.id='mapSummaryModal';
    modal.className='modal';
    modal.style.zIndex='140';
    modal.innerHTML=`<div class="sheet" style="max-width:430px;text-align:center">
      <div style="font-size:46px;margin-bottom:4px">🏆</div>
      <h2 style="margin:0 0 4px">Map Complete!</h2>
      <div class="small" id="mapSummarySubtitle" style="margin-bottom:14px"></div>
      <div class="info-grid" style="text-align:left">
        <div class="info-box"><div class="small">Enemies defeated</div><div id="mapSummaryKills" style="font-size:25px;font-weight:900;margin-top:3px">0</div></div>
        <div class="info-box"><div class="small">Coins earned</div><div id="mapSummaryCoins" style="font-size:25px;font-weight:900;margin-top:3px">🟡 0</div></div>
      </div>
      <div class="info-box" style="text-align:left;margin-top:9px"><div class="small" style="margin-bottom:5px">Strongest tower deployed</div><div id="mapSummaryTower"></div></div>
      <div class="info-box" style="text-align:left;margin-top:9px"><div class="small">Card EXP earned</div><div id="mapSummaryXp" style="font-size:18px;font-weight:900;margin-top:3px"></div></div>
      <button class="primary" id="closeMapSummary" style="width:100%;margin-top:13px">Continue</button>
    </div>`;
    document.body.appendChild(modal);
    modal.querySelector('#closeMapSummary').onclick=()=>modal.classList.remove('show');
  }
  const seriesName=currentSeries===1?'Forest Pines':'Desert Dunes';
  modal.querySelector('#mapSummarySubtitle').textContent=`${seriesName} ${currentMap} • ${hardMode?'Hard':'Normal'}`;
  modal.querySelector('#mapSummaryKills').textContent=String(battle.mapKills||0);
  modal.querySelector('#mapSummaryCoins').textContent=`🟡 ${battle.mapCoinsEarned||0}`;
  modal.querySelector('#mapSummaryTower').innerHTML=strongestHtml;
  modal.querySelector('#mapSummaryXp').textContent=cardXp?`+${cardXp} EXP to each used card`:'No card EXP earned';
  modal.classList.add('show');
}
'''
s=s.replace(anchor,helper+anchor,1)

# Show it after the map completion stack finishes so all completion bookkeeping is done.
old='if(clearedWave>=15){\n    const cardXp=awardUsedCardXp(true);'
new='if(clearedWave>=15){\n    const cardXp=awardUsedCardXp(true);\n    setTimeout(()=>showMapSummary(cardXp),120);'
if old not in s: raise SystemExit('map completion marker not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Added map completion summary popup with kills, strongest tower, coins and card XP')
