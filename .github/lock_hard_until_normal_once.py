from pathlib import Path
p=Path('index.html')
s=p.read_text()

# Add persistent normal-mode completion tracking.
old='''  battleDifficulty:"normal",\n  hardCompleted:{},\n  deck:["monkey","frog","owl","snake"]'''
new='''  battleDifficulty:"normal",\n  normalCompleted:{},\n  hardCompleted:{},\n  deck:["monkey","frog","owl","snake"]'''
if old not in s: raise SystemExit('defaults anchor missing')
s=s.replace(old,new,1)

old='''save.hardCompleted={...defaults.hardCompleted,...(save.hardCompleted||{})};\nlet hardMode=save.battleDifficulty==="hard";'''
new='''save.normalCompleted={...defaults.normalCompleted,...(save.normalCompleted||{})};\nsave.hardCompleted={...defaults.hardCompleted,...(save.hardCompleted||{})};\n// Reconstruct obvious Normal completions from existing unlocked-map progress so old saves keep access.\nfor(let m=1;m<(save.forestPinesUnlocked||1);m++)save.normalCompleted[`1-${m}`]=true;\nif((save.desertDunesUnlocked||0)>0)save.normalCompleted["1-10"]=true;\nfor(let m=1;m<(save.desertDunesUnlocked||0);m++)save.normalCompleted[`2-${m}`]=true;\nlet hardMode=save.battleDifficulty==="hard";'''
if old not in s: raise SystemExit('completion init anchor missing')
s=s.replace(old,new,1)

# Helper and UI state: Hard is locked until this exact map has a Normal clear.
old='''function updateDifficultyUI(){\n  if(!difficultyBtn)return;\n  difficultyBtn.textContent=hardMode?"🔥 Hard":"🌿 Normal";\n  difficultyBtn.style.borderColor=hardMode?"#ff8a4c":"#4b8469";\n  difficultyBtn.style.background=hardMode?"#6b2d1e":"#285842";\n  if(typeof mapLabel!=="undefined")mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?" • 🔥 HARD":""}`;\n}\ndifficultyBtn.onclick=()=>{'''
new='''function normalCompleteForCurrentMap(){return !!save.normalCompleted?.[`${currentSeries}-${currentMap}`];}\nfunction updateDifficultyUI(){\n  if(!difficultyBtn)return;\n  const hardUnlocked=normalCompleteForCurrentMap();\n  difficultyBtn.textContent=hardMode?"🔥 Hard":hardUnlocked?"🌿 Normal":"🔒 Hard Locked";\n  difficultyBtn.style.borderColor=hardMode?"#ff8a4c":hardUnlocked?"#4b8469":"#6b6b6b";\n  difficultyBtn.style.background=hardMode?"#6b2d1e":hardUnlocked?"#285842":"#343434";\n  if(typeof mapLabel!=="undefined")mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?" • 🔥 HARD":""}`;\n}\ndifficultyBtn.onclick=()=>{\n  if(!hardMode && !normalCompleteForCurrentMap()){\n    alert(`Complete map ${currentSeries}-${currentMap} on Normal Mode before Hard Mode unlocks.`);\n    message.textContent=`🔒 Hard Mode locked — complete ${currentSeries}-${currentMap} on Normal first.`;\n    return;\n  }'''
if old not in s: raise SystemExit('difficulty UI anchor missing')
s=s.replace(old,new,1)

# Force Normal when navigating to a map whose Hard clear is not yet unlocked.
old='''  currentSeries=targetSeries;\n  currentMap=Math.max(1,Math.min(10,n));\n  const maps=currentSeries===1?forestPinesMaps:desertDunesMaps;'''
new='''  currentSeries=targetSeries;\n  currentMap=Math.max(1,Math.min(10,n));\n  if(hardMode && !save.normalCompleted?.[`${currentSeries}-${currentMap}`]){\n    hardMode=false;save.battleDifficulty="normal";\n  }\n  const maps=currentSeries===1?forestPinesMaps:desertDunesMaps;'''
if old not in s: raise SystemExit('applyMap anchor missing')
s=s.replace(old,new,1)

# Save Normal completion on wave 15, separate from Hard completion.
old='''    save.metaCoins+=hardMode?300:200;\n    if(hardMode)save.hardCompleted[`${currentSeries}-${currentMap}`]=true;\n    if(currentSeries===1){'''
new='''    save.metaCoins+=hardMode?300:200;\n    if(hardMode)save.hardCompleted[`${currentSeries}-${currentMap}`]=true;\n    else save.normalCompleted[`${currentSeries}-${currentMap}`]=true;\n    if(currentSeries===1){'''
if old not in s: raise SystemExit('finishWave completion anchor missing')
s=s.replace(old,new,1)

# Make reset show the lock/unlock state immediately.
old='''  selectedCard=null; selectedTower=null; speed=1; speedBtn.textContent="⏩ Speed: 1×";\n  updateHud(); last=performance.now(); loop(last);'''
new='''  selectedCard=null; selectedTower=null; speed=1; speedBtn.textContent="⏩ Speed: 1×";\n  updateDifficultyUI();updateHud(); last=performance.now(); loop(last);'''
if old not in s: raise SystemExit('reset UI anchor missing')
s=s.replace(old,new,1)

p.write_text(s)
