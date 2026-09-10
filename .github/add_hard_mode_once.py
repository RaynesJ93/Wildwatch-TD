from pathlib import Path

p=Path('index.html')
s=p.read_text()

repls=[]

repls.append((
'''        <div style="display:flex;gap:6px"><button class="secondary" id="prevMap" style="padding:8px 11px">◀</button><button class="secondary" id="nextMap" style="padding:8px 11px">▶</button></div>''',
'''        <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end"><button class="secondary" id="difficultyBtn" style="padding:8px 11px">🌿 Normal</button><button class="secondary" id="prevMap" style="padding:8px 11px">◀</button><button class="secondary" id="nextMap" style="padding:8px 11px">▶</button></div>'''
))

repls.append((
'''  selectedSeries:1,
  selectedSeriesMap:1,
  deck:["monkey","frog","owl","snake"]''',
'''  selectedSeries:1,
  selectedSeriesMap:1,
  battleDifficulty:"normal",
  hardCompleted:{},
  deck:["monkey","frog","owl","snake"]'''
))

repls.append((
'''save.damageUpgrades={...defaults.damageUpgrades,...save.damageUpgrades};
function cardBaseDamage''',
'''save.damageUpgrades={...defaults.damageUpgrades,...save.damageUpgrades};
save.hardCompleted={...defaults.hardCompleted,...(save.hardCompleted||{})};
let hardMode=save.battleDifficulty==="hard";
function cardBaseDamage'''
))

repls.append((
'''    cancelAnimationFrame(raf);if(b.mapNumber){currentSeries=b.mapSeries||1;currentMap=b.mapNumber;applyMap(currentSeries,currentMap);}battle=b;battle.shots=[];battle.puddles=battle.puddles||[];selectedCard=null;selectedTower=null;speed=1;
    speedBtn.textContent="⏩ Speed: 1×";updateHud();last=performance.now();raf=requestAnimationFrame(loop);return true;''',
'''    cancelAnimationFrame(raf);hardMode=!!b.hardMode;save.battleDifficulty=hardMode?"hard":"normal";if(b.mapNumber){currentSeries=b.mapSeries||1;currentMap=b.mapNumber;applyMap(currentSeries,currentMap);}battle=b;battle.shots=[];battle.puddles=battle.puddles||[];selectedCard=null;selectedTower=null;speed=1;
    speedBtn.textContent="⏩ Speed: 1×";updateDifficultyUI();updateHud();last=performance.now();raf=requestAnimationFrame(loop);return true;'''
))

repls.append((
'''  mapLabel.textContent=`${currentSeries}-${currentMap}`;''',
'''  mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?" • 🔥 HARD":""}`;'''
))

repls.append((
'''function resetBattle(){
  cancelAnimationFrame(raf);
  applyMap(currentSeries,currentMap);
  battle={started:true,coins:130,lives:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};''',
'''function resetBattle(){
  cancelAnimationFrame(raf);
  applyMap(currentSeries,currentMap);
  battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'''
))

repls.append((
'''function spawnEnemy(){
  const e=enemyForWave();''',
'''function spawnEnemy(){
  const e=enemyForWave();
  if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}'''
))

repls.append((
'''  battle.spawnLeft=6+battle.wave*2;''',
'''  battle.spawnLeft=Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));'''
))

repls.append((
'''  save.xp+=12+clearedWave*3;
  save.metaCoins+=20;
  if(clearedWave%3===0)save.metaCoins+=50;
  if(clearedWave>=15){
    save.metaCoins+=200;''',
'''  save.xp+=Math.round((12+clearedWave*3)*(hardMode?1.5:1));
  save.metaCoins+=hardMode?30:20;
  if(clearedWave%3===0)save.metaCoins+=hardMode?75:50;
  if(clearedWave>=15){
    save.metaCoins+=hardMode?300:200;
    if(hardMode)save.hardCompleted[`${currentSeries}-${currentMap}`]=true;'''
))

for old,new in repls:
    if old not in s:
        raise SystemExit('Missing expected anchor:\n'+old[:180])
    s=s.replace(old,new,1)

# Insert difficulty controls after continue button handler.
anchor='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));if(!loadBattleState())resetBattle();};\n'''
insert='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));if(!loadBattleState())resetBattle();};
function updateDifficultyUI(){
  if(!difficultyBtn)return;
  difficultyBtn.textContent=hardMode?"🔥 Hard":"🌿 Normal";
  difficultyBtn.style.borderColor=hardMode?"#ff8a4c":"#4b8469";
  difficultyBtn.style.background=hardMode?"#6b2d1e":"#285842";
  if(typeof mapLabel!=="undefined")mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?" • 🔥 HARD":""}`;
}
difficultyBtn.onclick=()=>{
  if(battle?.started && (battle.waveActive||battle.towers?.length||battle.wave>1)){
    if(!confirm("Changing difficulty restarts this map. Continue?"))return;
  }
  hardMode=!hardMode;
  save.battleDifficulty=hardMode?"hard":"normal";
  persist();
  clearBattleState();
  resetBattle();
  updateDifficultyUI();
  message.textContent=hardMode?"🔥 Hard Mode: stronger, faster and more numerous enemies — with 50% better permanent rewards.":"🌿 Normal Mode selected.";
};
'''
if anchor not in s:
    raise SystemExit('Difficulty control insertion anchor missing')
s=s.replace(anchor,insert,1)

# Make reset UI reflect current difficulty immediately.
anchor2='''  speedBtn.textContent="⏩ Speed: 1×";updateHud(); last=performance.now(); loop(last);'''
if anchor2 in s:
    s=s.replace(anchor2,'''  speedBtn.textContent="⏩ Speed: 1×";updateDifficultyUI();updateHud(); last=performance.now(); loop(last);''',1)

p.write_text(s)
