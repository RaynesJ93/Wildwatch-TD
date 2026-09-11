from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# ---------- CSS ----------
css=r'''
/* Sanctuary-style map selection screen */
#battleScreen.map-select-mode{display:block!important;height:auto!important;overflow:visible!important}
#battleScreen.map-select-mode>:not(#mapSanctuary){display:none!important}
#mapSanctuary{display:none;min-height:calc(100vh - 96px);padding:8px 2px 24px}
#battleScreen.map-select-mode #mapSanctuary{display:block}
.sanctuary-shell{background:linear-gradient(180deg,#112a20 0%,#0b1b15 100%);border:1px solid #8b7440;border-radius:24px;padding:14px;box-shadow:0 18px 48px #0008,inset 0 0 45px #ffffff05}
.sanctuary-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}.sanctuary-head h2{margin:0;font-size:27px;color:#ffe17c;font-family:Georgia,serif}.sanctuary-head .small{font-size:11px}
.region-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0 12px}.region-tab{border:1px solid #6f805f;background:#10251c;border-radius:14px;padding:9px 5px;min-height:62px;font-weight:900;font-size:11px;letter-spacing:.3px;color:#c5d1c8}.region-tab b{display:block;font-size:13px;margin-top:4px}.region-tab.active{border-color:#ffd65a;background:linear-gradient(180deg,#2b553d,#173525);color:#ffe58a;box-shadow:0 0 0 2px #ffd65a22,inset 0 0 18px #ffd65a0d}.region-tab.locked{opacity:.35;filter:grayscale(1)}
.region-hero{position:relative;overflow:hidden;border:1px solid #806d40;border-radius:20px;padding:20px 16px 16px;min-height:200px;background:radial-gradient(circle at 80% 10%,#58735a55,transparent 38%),linear-gradient(145deg,#214a34,#0f241a 68%)}
.region-hero.desert{background:radial-gradient(circle at 78% 18%,#e7bc6050,transparent 38%),linear-gradient(145deg,#6a4c24,#231b12 72%)}
.region-hero.haunted{background:radial-gradient(circle at 79% 16%,#9c84ff55,transparent 26%),radial-gradient(circle at 75% 14%,#d8d0ff40 0 8%,transparent 9%),linear-gradient(145deg,#251d39,#0d1715 70%)}
.region-hero:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,transparent 55%,#0004)}
.region-hero h1{position:relative;z-index:1;margin:0 0 7px;font-family:Georgia,serif;color:#ffe68b;font-size:31px;letter-spacing:.4px}.region-hero.haunted h1{color:#d9c5ff;text-shadow:0 0 16px #8d67ff99}.region-hero p{position:relative;z-index:1;margin:0;max-width:72%;line-height:1.35;color:#d6e2da;font-size:14px}.region-badge{position:absolute;z-index:2;right:14px;bottom:15px;border:1px solid #a98b46;border-radius:16px;padding:9px 13px;text-align:center;background:#0a1813cc;color:#ffe27c}.region-badge small{display:block;letter-spacing:2px;color:#b9c6bd}.region-badge b{font-family:Georgia,serif;font-size:21px}
.sanctuary-mode{margin:12px 0;background:#0a1712;border:1px solid #5c6d60;border-radius:18px;padding:10px}.sanctuary-mode-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}.mode-choice{border:1px solid #69786d;border-radius:14px;padding:12px 8px;background:#111d18;font-weight:900;font-size:15px;letter-spacing:.5px}.mode-choice.active{background:linear-gradient(#356747,#1f4b33);border-color:#ffd65a;color:#ffe27a;box-shadow:0 0 0 2px #ffd65a22}.mode-hint{text-align:center;margin-top:8px;color:#a9b8af;font-size:12px;min-height:16px}
.stage-map{position:relative;margin-top:13px;border:1px solid #76663f;border-radius:22px;padding:18px 10px 14px;background:linear-gradient(180deg,#0d2118,#09150f);overflow:hidden}.stage-map:before{content:"";position:absolute;left:50%;top:63px;bottom:30px;width:3px;transform:translateX(-50%);background:linear-gradient(#b89540,#7d6330);opacity:.65}.stage-map-title{position:relative;z-index:2;width:max-content;max-width:90%;margin:0 auto 14px;border:1px solid #9b7e39;border-radius:999px;padding:7px 22px;background:#12251c;color:#ffe17a;font-weight:900;letter-spacing:2px;font-size:12px}.stage-grid{position:relative;z-index:2;display:grid;grid-template-columns:1fr 1fr;gap:12px 10px}.stage-card{position:relative;display:grid;grid-template-columns:54px 1fr auto;gap:8px;align-items:center;text-align:left;background:linear-gradient(145deg,#173627,#10261c);border:2px solid #407d57;border-radius:17px;padding:9px 8px;min-height:92px;box-shadow:0 9px 18px #0005}.stage-card:nth-child(even){transform:translateY(24px)}.stage-card.cleared{border-color:#54bd76;box-shadow:0 0 18px #3fd46a24,0 9px 18px #0005}.stage-card.locked{border-color:#5b6260;background:linear-gradient(145deg,#1b2220,#111716);opacity:.72}.stage-thumb{width:54px;height:64px;border-radius:11px;display:grid;place-items:center;font-size:30px;border:1px solid #ffffff22;background:radial-gradient(circle at 55% 25%,#8dc08d55,transparent 35%),linear-gradient(#163522,#0a1811)}.stage-thumb.desert{background:radial-gradient(circle at 50% 20%,#eac45e66,transparent 32%),linear-gradient(#62451f,#23170c)}.stage-thumb.haunted{background:radial-gradient(circle at 58% 22%,#a78cff66,transparent 30%),linear-gradient(#241d3b,#0a1512)}.stage-copy{min-width:0}.stage-num{font-size:11px;color:#ffe17a;font-weight:900}.stage-name{font-family:Georgia,serif;font-weight:900;font-size:15px;line-height:1.05;margin:3px 0;color:#f7fff9}.stage-status{font-size:10px;color:#a9b8af}.stage-stars{font-size:13px;letter-spacing:0;line-height:1.1;text-align:center;color:#ffd65a}.stage-lock{font-size:24px}.sanctuary-footnote{text-align:center;margin-top:34px;color:#90a297;font-size:11px}
@media(max-width:430px){.sanctuary-shell{padding:10px}.region-tab{font-size:9px;min-height:58px}.region-tab b{font-size:11px}.region-hero{padding:17px 13px;min-height:185px}.region-hero h1{font-size:27px}.region-hero p{font-size:12px;max-width:68%}.stage-grid{gap:10px 7px}.stage-card{grid-template-columns:44px 1fr auto;padding:7px 6px;min-height:84px}.stage-thumb{width:44px;height:58px;font-size:25px}.stage-name{font-size:13px}.stage-status{font-size:9px}.stage-stars{font-size:11px}.stage-map{padding-left:7px;padding-right:7px}}
'''
if '/* Sanctuary-style map selection screen */' not in s:
    if '</style>' not in s: raise SystemExit('style close not found')
    s=s.replace('</style>',css+'\n</style>',1)

# ---------- HTML ----------
html=r'''
    <div id="mapSanctuary">
      <div class="sanctuary-shell">
        <div class="sanctuary-head"><div><h2>← Sanctuary</h2><div class="small">Choose a region and stage</div></div><div class="pill">🗺️ 30 Stages</div></div>
        <div class="region-tabs" id="regionTabs"></div>
        <div class="region-hero" id="regionHero">
          <h1 id="sanctuaryRegionName">Forest Pines</h1>
          <p id="sanctuaryRegionDesc"></p>
          <div class="region-badge"><small id="sanctuaryRegionNumber">REGION 1</small><b>10 STAGES</b></div>
        </div>
        <div class="sanctuary-mode">
          <div class="sanctuary-mode-row"><button class="mode-choice active" id="sanctuaryNormal">NORMAL</button><button class="mode-choice" id="sanctuaryHard">HARD 🔥</button></div>
          <div class="mode-hint" id="sanctuaryModeHint">Complete a stage on Normal to unlock Hard for that stage.</div>
        </div>
        <div class="stage-map"><div class="stage-map-title" id="sanctuaryStageTitle">FOREST PINES</div><div class="stage-grid" id="sanctuaryStageGrid"></div><div class="sanctuary-footnote">Complete each stage to unlock the next path.</div></div>
      </div>
    </div>
'''
if 'id="mapSanctuary"' not in s:
    anchor='<section id="battleScreen" class="screen">'
    if anchor not in s: raise SystemExit('battleScreen anchor not found')
    s=s.replace(anchor,anchor+'\n'+html,1)

# ---------- JS ----------
js=r'''
// Sanctuary map-selection interface
const SANCTUARY_META={
  1:{name:'Forest Pines',icon:'🌲',desc:'A lush opening region of winding woodland trails, ancient pines and quiet clearings.',className:'forest',stages:["Keeper's Path","Whispering Woods","Broken Bridge","Mosswood Village","Riverbend Trail","Old Watchtower","Pine Hollow","Foxglove Trail","Ancient Grove","Guardian's Gate"]},
  2:{name:'Desert Dunes',icon:'🏜️',desc:'Scorching dunes, ruined oases and dangerous sandstone paths where enemies press harder.',className:'desert',stages:['Sunscorched Trail','Dune Crossing','Oasis Ruins','Scorpion Pass','Sandstone Arch','Mirage Basin','Caravan Road','Dust Temple','Vulture Ridge',"Pharaoh's Gate"]},
  3:{name:'Haunted Woods',icon:'👻',desc:'A dark and mysterious woodland filled with twisted trees, forgotten graves, drifting fog and restless spirits.',className:'haunted',stages:['Shadow Path','Cursed Glade','Gravestone Grove','The Hollow','Whispering Brook','Ruined Chapel','Spectral Crossing',"Witch's Circle",'Fallen Giant','The Final Stand']}
};
let mapMenuSeries=1,mapMenuDifficulty='normal';
function sanctuaryUnlocked(series){
  if(typeof seriesUnlocked==='function')return seriesUnlocked(series);
  return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):(save.hauntedWoodsUnlocked||0);
}
function sanctuaryStageIcon(series,n){
  const sets={1:['🌿','🌲','🌉','🏡','💧','🗼','🌳','🌸','🪵','🏰'],2:['☀️','🏜️','🌴','🦂','🪨','🌫️','🐪','🏛️','🦅','👑'],3:['🌙','🕯️','🪦','🕳️','🌫️','⛪','🌉','🔮','💀','🏰']};
  return sets[series][n-1]||'🗺️';
}
function renderMapSanctuary(){
  const wrap=document.getElementById('mapSanctuary');if(!wrap)return;
  if(!sanctuaryUnlocked(mapMenuSeries))mapMenuSeries=1;
  const meta=SANCTUARY_META[mapMenuSeries],unlocked=Math.max(mapMenuSeries===1?1:0,sanctuaryUnlocked(mapMenuSeries));
  const tabs=document.getElementById('regionTabs');
  tabs.innerHTML=[1,2,3].map(series=>{const m=SANCTUARY_META[series],locked=series>1&&sanctuaryUnlocked(series)<1;return `<button class="region-tab ${series===mapMenuSeries?'active':''} ${locked?'locked':''}" data-region="${series}" ${locked?'disabled':''}>REGION ${series}<b>${locked?'🔒 LOCKED':m.icon+' '+m.name.toUpperCase()}</b></button>`}).join('');
  tabs.querySelectorAll('.region-tab:not(.locked)').forEach(btn=>btn.onclick=()=>{mapMenuSeries=+btn.dataset.region;renderMapSanctuary()});
  const hero=document.getElementById('regionHero');hero.className=`region-hero ${meta.className}`;
  document.getElementById('sanctuaryRegionName').textContent=meta.name;
  document.getElementById('sanctuaryRegionDesc').textContent=meta.desc;
  document.getElementById('sanctuaryRegionNumber').textContent=`REGION ${mapMenuSeries}`;
  document.getElementById('sanctuaryStageTitle').textContent=meta.name.toUpperCase();
  const normalBtn=document.getElementById('sanctuaryNormal'),hardBtn=document.getElementById('sanctuaryHard');
  normalBtn.classList.toggle('active',mapMenuDifficulty==='normal');hardBtn.classList.toggle('active',mapMenuDifficulty==='hard');
  normalBtn.onclick=()=>{mapMenuDifficulty='normal';renderMapSanctuary()};hardBtn.onclick=()=>{mapMenuDifficulty='hard';renderMapSanctuary()};
  document.getElementById('sanctuaryModeHint').textContent=mapMenuDifficulty==='hard'?'Hard stages require that same stage to be cleared on Normal first.':'Complete each Normal stage to unlock the next stage and its Hard mode.';
  const grid=document.getElementById('sanctuaryStageGrid');
  grid.innerHTML=meta.stages.map((name,i)=>{
    const n=i+1,key=`${mapMenuSeries}-${n}`,locked=n>unlocked,normalDone=!!save.normalCompleted?.[key],hardDone=!!save.hardCompleted?.[key];
    const modeLocked=mapMenuDifficulty==='hard'&&!normalDone;
    const inaccessible=locked||modeLocked;
    const cleared=mapMenuDifficulty==='hard'?hardDone:normalDone;
    const stars=hardDone?3:normalDone?2:0;
    const starText=[0,1,2].map(x=>x<stars?'★':'☆').join('<br>');
    let status=locked?'Locked':modeLocked?'Clear Normal first':cleared?'Cleared • 15/15 waves':`Unlocked • 15 waves`;
    return `<button class="stage-card ${cleared?'cleared':''} ${inaccessible?'locked':''}" data-stage="${n}" ${inaccessible?'disabled':''}><div class="stage-thumb ${meta.className}">${sanctuaryStageIcon(mapMenuSeries,n)}</div><div class="stage-copy"><div class="stage-num">${mapMenuSeries}-${n}</div><div class="stage-name">${name}</div><div class="stage-status">${status}</div></div><div>${inaccessible?'<div class="stage-lock">🔒</div>':`<div class="stage-stars">${starText}</div>`}</div></button>`;
  }).join('');
  grid.querySelectorAll('.stage-card:not(.locked)').forEach(btn=>btn.onclick=()=>startSanctuaryStage(+btn.dataset.stage));
}
function startSanctuaryStage(stage){
  if(!applyMap(mapMenuSeries,stage))return;
  hardMode=mapMenuDifficulty==='hard';
  save.battleDifficulty=hardMode?'hard':'normal';
  const battleScreen=document.getElementById('battleScreen');battleScreen?.classList.remove('map-select-mode');
  document.body.classList.add('battle-mode');
  resetBattle();
  updateDifficultyUI();
}
'''
if '// Sanctuary map-selection interface' not in s:
    anchor='document.querySelectorAll(".nav button").forEach(b=>b.onclick=()=>showScreen(b.dataset.screen));'
    if anchor not in s: raise SystemExit('showScreen nav anchor not found')
    s=s.replace(anchor,js+'\n'+anchor,1)

# Make Battle nav open Sanctuary when there is no active battle (or after completion/defeat).
old='document.body.classList.toggle("battle-mode",id==="battleScreen");'
new='const choosingMap=id==="battleScreen" && (!battle?.started || battle.ended);\n  document.body.classList.toggle("battle-mode",id==="battleScreen" && !choosingMap);'
if old in s:s=s.replace(old,new,1)
else:
    if 'const choosingMap=id==="battleScreen"' not in s: raise SystemExit('battle-mode showScreen marker not found')

old='if(id==="battleScreen" && !battle.started) resetBattle();'
new='if(id==="battleScreen" && choosingMap){document.getElementById("battleScreen")?.classList.add("map-select-mode");mapMenuSeries=(currentSeries&&sanctuaryUnlocked(currentSeries))?currentSeries:1;mapMenuDifficulty="normal";renderMapSanctuary();}\n  else if(id==="battleScreen"){document.getElementById("battleScreen")?.classList.remove("map-select-mode");}'
if old in s:s=s.replace(old,new,1)
elif 'renderMapSanctuary();' not in s[s.find('function showScreen(id)'):s.find('function showScreen(id)')+1200]:raise SystemExit('battle reset showScreen marker not found')

# After completed map, returning via Battle tab should show Sanctuary rather than auto-restarting.
# No battle mechanics are changed: stage starts still call existing resetBattle().

for marker in ['id="mapSanctuary"','const SANCTUARY_META=','function startSanctuaryStage(stage)','stage-grid','choosingMap=id==="battleScreen"']:
    if marker not in s: raise SystemExit('missing final marker '+marker)

p.write_text(s,encoding='utf-8')
print('Added Sanctuary-style interactive map selection screen')
