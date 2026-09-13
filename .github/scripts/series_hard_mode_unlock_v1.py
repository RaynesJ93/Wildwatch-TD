from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='SERIES_HARD_MODE_UNLOCK_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old='''function normalCompleteForCurrentMap(){return !!save.normalCompleted?.[`${currentSeries}-${currentMap}`];}
function updateDifficultyUI(){
  if(!difficultyBtn)return;
  const hardUnlocked=normalCompleteForCurrentMap();
  difficultyBtn.textContent=hardMode?"🔥 Hard":hardUnlocked?"🌿 Normal":"🔒 Hard Locked";
  difficultyBtn.style.borderColor=hardMode?"#ff8a4c":hardUnlocked?"#4b8469":"#6b6b6b";
  difficultyBtn.style.background=hardMode?"#6b2d1e":hardUnlocked?"#285842":"#343434";
  if(typeof mapLabel!=="undefined")mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?" • 🔥 HARD":""}`;
}
difficultyBtn.onclick=()=>{
  if(!hardMode && !normalCompleteForCurrentMap()){
    alert(`Complete map ${currentSeries}-${currentMap} on Normal Mode before Hard Mode unlocks.`);
    message.textContent=`🔒 Hard Mode locked — complete ${currentSeries}-${currentMap} on Normal first.`;
    return;
  }'''
new='''// SERIES_HARD_MODE_UNLOCK_V1: clearing map 10 on Normal unlocks Hard Mode for the whole series.
function hardModeUnlockedForSeries(series=currentSeries){return !!save.normalCompleted?.[`${series}-10`];}
function updateDifficultyUI(){
  if(!difficultyBtn)return;
  const hardUnlocked=hardModeUnlockedForSeries(currentSeries);
  difficultyBtn.textContent=hardMode?"🔥 Hard":hardUnlocked?"🌿 Normal":"🔒 Hard Locked";
  difficultyBtn.style.borderColor=hardMode?"#ff8a4c":hardUnlocked?"#4b8469":"#6b6b6b";
  difficultyBtn.style.background=hardMode?"#6b2d1e":hardUnlocked?"#285842":"#343434";
  if(typeof mapLabel!=="undefined")mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?" • 🔥 HARD":""}`;
}
difficultyBtn.onclick=()=>{
  if(!hardMode && !hardModeUnlockedForSeries(currentSeries)){
    alert(`Complete map ${currentSeries}-10 on Normal Mode to unlock Hard Mode for every map in this series.`);
    message.textContent=`🔒 Hard Mode locked — complete ${currentSeries}-10 on Normal first.`;
    return;
  }'''
if old not in s:
    raise RuntimeError('Hard Mode unlock block anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Applied series-wide Hard Mode unlock rules')
# trigger workflow after workflow file exists
