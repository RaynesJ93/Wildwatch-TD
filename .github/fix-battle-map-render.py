from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
changed=False

# The blank-map failure affects every region because the shared battle reset/render
# pipeline can be missing even though the map data (paths/pads) is still present.
# Restore a safe resetBattle implementation if it is absent.
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

# Make all map-entry routes repaint immediately. These replacements are deliberately
# idempotent so re-running the workflow does not duplicate code.
if '// MAP_VISUAL_FIX: render battlefield immediately when a map is loaded' not in s:
    old='''  resetBattle();\n  updateDifficultyUI();'''
    new='''  resetBattle();\n  // MAP_VISUAL_FIX: render battlefield immediately when a map is loaded\n  draw();\n  if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}\n  updateDifficultyUI();'''
    if old in s:
        s=s.replace(old,new,1);changed=True

old_continue='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));if(!loadBattleState())resetBattle();};'''
new_continue='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));document.body.classList.add("battle-mode");if(!loadBattleState())resetBattle();draw();if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}};'''
if old_continue in s:
    s=s.replace(old_continue,new_continue,1);changed=True

# Also repaint when using previous/next map arrows or advancing to the next map.
s=s.replace('applyMap(currentSeries,currentMap-1);resetBattle();return;','applyMap(currentSeries,currentMap-1);resetBattle();draw();return;')
s=s.replace('applyMap(currentSeries-1,10);resetBattle();','applyMap(currentSeries-1,10);resetBattle();draw();')
s=s.replace('applyMap(currentSeries,currentMap+1);resetBattle();}','applyMap(currentSeries,currentMap+1);resetBattle();draw();}')
s=s.replace('applyMap(currentSeries+1,1);resetBattle();}','applyMap(currentSeries+1,1);resetBattle();draw();}')

p.write_text(s,encoding='utf-8')
print('Restored shared battle reset/render pipeline for all maps')
