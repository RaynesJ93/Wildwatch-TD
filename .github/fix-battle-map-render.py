from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
changed=False

# Keep the global battle reset/render repair in place.
if 'function resetBattle' not in s:
    marker='startWave.onclick=()=>{'
    if marker not in s:
        raise SystemExit('startWave marker not found')
    reset_fn=r'''
// GLOBAL_MAP_RESET_FIX: restore shared battle initialisation used by every map.
function resetBattle(){
  cancelAnimationFrame(raf);raf=0;
  battle={
    started:true,
    hardMode,
    coins:hardMode?110:130,
    lives:hardMode?15:20,
    mapStartLives:hardMode?15:20,
    wave:1,
    enemies:[],towers:[],shots:[],puddles:[],needles:[],pineapples:[],
    trashZones:[],roars:[],pigHamZones:[],eggSplashes:[],usedCards:[],
    mapKills:0,mapCoinsEarned:0,
    spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false
  };
  selectedCard=null;selectedTower=null;
  speed=1;autoWave=false;autoWaveTimer=0;
  if(typeof speedBtn!=="undefined"&&speedBtn)speedBtn.textContent="⏩ Speed: 1×";
  if(typeof autoWaveBtn!=="undefined"&&autoWaveBtn){autoWaveBtn.textContent="▶️ Auto: OFF";autoWaveBtn.classList.remove("primary");autoWaveBtn.classList.add("secondary");}
  if(typeof startWave!=="undefined"&&startWave)startWave.textContent="Start wave";
  if(typeof message!=="undefined"&&message)message.textContent="Choose an animal card, then tap anywhere on the grass to place it.";
  if(typeof renderDecks==="function")renderDecks();
  if(typeof updateHud==="function")updateHud();
  if(typeof updateDifficultyUI==="function")updateDifficultyUI();
  if(typeof draw==="function")draw();
  last=performance.now();
  raf=requestAnimationFrame(loop);
}

'''
    s=s.replace(marker,reset_fn+marker,1)
    changed=True

# Haunted Woods map-menu work accidentally removed the shared HUD and enemy-spawn
# helpers because they sat between the navigation handlers and startWave handler.
# Restore them before startWave. This also restores the old affordability dimming.
marker='startWave.onclick=()=>{'
if marker not in s:
    raise SystemExit('startWave marker not found')

helpers=''
if 'function updateHud(){' not in s:
    helpers += r'''
function updateHud(){
  battleCoins.textContent=Math.floor(battle.coins);
  lives.textContent=battle.lives;
  wave.textContent=`${Math.min(battle.wave,15)}/15`;
  document.querySelectorAll(".battle-card").forEach(b=>{
    const key=b.dataset.key;
    const unaffordable=!!animals[key] && animals[key].cost>battle.coins;
    b.classList.toggle("disabled",unaffordable);
    b.setAttribute("aria-disabled",unaffordable?"true":"false");
  });
  if(selectedTower && towerModal.classList.contains("show")){
    const a=animals[selectedTower.key];
    const mult=selectedTower.key==="pig"?.8:selectedTower.key==="tiger"?.64:1;
    const up=Math.floor(a.cost*.595*selectedTower.level*mult), cash=Math.floor(battle.coins);
    towerInfo.textContent=`Damage ${Math.round(towerDamage(selectedTower))} • Range ${Math.round(cardBaseRange(selectedTower.key)*(1+(selectedTower.level-1)*.06))} • Upgrade cost 🥩 ${up} • You have 🥩 ${cash}`;
    upgradeTower.textContent=`Upgrade • 🥩 ${up}`;
    upgradeTower.disabled=cash<up;
    upgradeTower.style.opacity=cash<up?".55":"1";
  }
}

'''

if 'function enemyForWave(){' not in s:
    helpers += r'''
function enemyForWave(){
  const w=battle.wave, r=Math.random();
  if(currentSeries===2){
    if(w>=7 && r<.12)return {type:"desertBoss",emoji:"🦂",hp:(170+w*18)*.8,speed:42,reward:16,size:22};
    if(w>=4 && r<.28)return {type:"camel",emoji:"🐪",hp:(95+w*12)*.8,speed:52,reward:10,size:19};
    if(r<.35)return {type:"lizard",emoji:"🦎",hp:(38+w*8)*.8,speed:82,reward:6,size:15};
    return {type:"scorpion",emoji:"🦂",hp:(58+w*10)*.8,speed:61,reward:8,size:17};
  }
  // Forest Pines and Haunted Woods retain the established woodland enemy set.
  if(w>=7 && r<.12)return {type:"boar",emoji:"🐗",hp:(170+w*18)*.8,speed:42,reward:16,size:30,boss:true};
  if(w>=4 && r<.28)return {type:"rabbit",emoji:"🐇",hp:(95+w*12)*.8,speed:68,reward:10,size:18};
  if(r<.35)return {type:"rat",emoji:"🐀",hp:(38+w*8)*.8,speed:82,reward:6,size:15};
  return {type:"raccoon",emoji:"🦝",hp:(58+w*10)*.8,speed:61,reward:8,size:17};
}

'''

if 'function spawnEnemy(){' not in s:
    helpers += r'''
function spawnEnemy(){
  const e=enemyForWave();
  if(hardMode){e.hp=Math.round(e.hp*1.75);e.speed*=1.15;e.reward=Math.ceil(e.reward*1.25);}
  if(battle.wave%10===0 && !battle.eliteSpawned){
    e.hp*=3;
    e.reward*=3;
    e.size=Math.round(e.size*1.18);
    e.elite=true;
    battle.eliteSpawned=true;
  }
  Object.assign(e,{maxHp:e.hp,seg:0,x:path[0][0],y:path[0][1],dirX:1,dirY:0,walkPhase:Math.random()*Math.PI*2,poison:0,poisonTick:0,poisonDmg:0,slowTimer:0,freezeTimer:0,puddleHits:{},dead:false});
  battle.enemies.push(e);
}

'''

if helpers:
    s=s.replace(marker,helpers+marker,1)
    changed=True

# Ensure selecting an unaffordable tower card does not make it look usable. The
# existing placement check still prevents spending more battle cash than available.
# updateHud() is called whenever coins change, so the dim state updates immediately.

# Keep map-entry routes repainting immediately.
old_continue='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));if(!loadBattleState())resetBattle();};'''
new_continue='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));document.body.classList.add("battle-mode");if(!loadBattleState())resetBattle();draw();if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}};'''
if old_continue in s:
    s=s.replace(old_continue,new_continue,1);changed=True

s=s.replace('applyMap(currentSeries,currentMap-1);resetBattle();return;','applyMap(currentSeries,currentMap-1);resetBattle();draw();return;')
s=s.replace('applyMap(currentSeries-1,10);resetBattle();','applyMap(currentSeries-1,10);resetBattle();draw();')
s=s.replace('applyMap(currentSeries,currentMap+1);resetBattle();}','applyMap(currentSeries,currentMap+1);resetBattle();draw();}')
s=s.replace('applyMap(currentSeries+1,1);resetBattle();}','applyMap(currentSeries+1,1);resetBattle();draw();}')

# Validation: all shared battle helpers must exist after this repair.
for required in ['function resetBattle(){','function updateHud(){','function enemyForWave(){','function spawnEnemy(){','startWave.onclick=()=>{']:
    if required not in s:
        raise SystemExit('missing after repair: '+required)

p.write_text(s,encoding='utf-8')
print('Restored wave spawning, battle HUD and unaffordable tower dimming')
