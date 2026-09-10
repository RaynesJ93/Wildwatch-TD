from pathlib import Path
p=Path('index.html'); s=p.read_text()
# 5-button nav
s=s.replace('grid-template-columns:repeat(4,1fr);padding:7px 8px', 'grid-template-columns:repeat(5,1fr);padding:7px 8px',1)
# Insert quest screen before closing app div
needle='''  </section>\n</div>\n\n<nav class="nav">'''
quest='''  </section>\n\n  <section id="questScreen" class="screen">\n    <div class="hero">\n      <div style="font-size:46px;text-align:center">📜</div>\n      <h1 style="text-align:center">Daily Quests</h1>\n      <p style="text-align:center">Complete 3 fresh quests each day for extra rewards.</p>\n    </div>\n    <div id="dailyQuestList" style="display:grid;gap:10px;margin-top:14px"></div>\n    <div class="info-box" style="margin-top:12px;text-align:center">\n      <div class="small" id="questResetText">New quests tomorrow.</div>\n      <button class="secondary" id="rerollQuestBtn" style="width:100%;margin-top:9px">🔄 Free Daily Reroll</button>\n    </div>\n  </section>\n</div>\n\n<nav class="nav">'''
if needle not in s: raise SystemExit('screen/nav marker not found')
s=s.replace(needle,quest,1)
# add nav button after Cards
needle2='''  <button data-screen="collectionScreen"><span class="ico">🃏</span>Cards</button>'''
if needle2 not in s: raise SystemExit('cards nav not found')
s=s.replace(needle2,needle2+'\n  <button data-screen="questScreen"><span class="ico">📜</span>Quests</button>',1)
# Add quest system before initial render call / script close using stable marker
marker='''renderAll();'''
idx=s.rfind(marker)
if idx<0: raise SystemExit('renderAll marker not found')
js=r'''
// ---- Daily quest board ----
const DAILY_QUEST_POOL=[
 {id:'waves8',name:'Wave Warrior',icon:'🌊',text:'Clear 8 waves',goal:8,reward:25,type:'waves'},
 {id:'waves12',name:'Defender',icon:'🛡️',text:'Clear 12 waves',goal:12,reward:35,type:'waves'},
 {id:'normal1',name:'Map Master',icon:'🗺️',text:'Complete 1 Normal map',goal:1,reward:35,type:'normalMaps'},
 {id:'hard1',name:'Hard Hitter',icon:'🔥',text:'Complete 1 Hard map',goal:1,reward:50,type:'hardMaps'},
 {id:'place12',name:'Tower Builder',icon:'🏗️',text:'Place 12 animal towers',goal:12,reward:30,type:'placed'},
 {id:'kills100',name:'Critter Control',icon:'💥',text:'Defeat 100 enemies',goal:100,reward:30,type:'kills'},
 {id:'noloss3',name:'Untouchable',icon:'❤️',text:'Clear 3 waves without losing a life',goal:3,reward:35,type:'noLossWaves'},
 {id:'speed5',name:'Need for Speed',icon:'⏩',text:'Clear 5 waves at 3× speed',goal:5,reward:35,type:'speedWaves'}
];
function questDay(){return new Date().toISOString().slice(0,10)}
function ensureDailyQuests(){
 save.dailyQuests=save.dailyQuests||{};
 if(save.dailyQuests.day!==questDay()){
   const pool=[...DAILY_QUEST_POOL].sort(()=>Math.random()-.5).slice(0,3);
   save.dailyQuests={day:questDay(),items:pool.map(q=>({id:q.id,progress:0,claimed:false})),rerolled:false};persist();
 }
}
function questDef(id){return DAILY_QUEST_POOL.find(q=>q.id===id)}
function addQuestProgress(type,n=1){
 ensureDailyQuests(); let changed=false;
 save.dailyQuests.items.forEach(x=>{const q=questDef(x.id);if(q&&q.type===type&&!x.claimed){x.progress=Math.min(q.goal,(x.progress||0)+n);changed=true}});
 if(changed){persist();renderDailyQuests()}
}
function renderDailyQuests(){
 const el=document.getElementById('dailyQuestList'); if(!el)return; ensureDailyQuests();
 el.innerHTML=save.dailyQuests.items.map((x,i)=>{const q=questDef(x.id),done=x.progress>=q.goal;return `<div class="info-box"><div style="display:flex;justify-content:space-between;gap:8px"><b>${q.icon} ${q.name}</b><b>🟡 ${q.reward}</b></div><div class="small" style="margin:5px 0">${q.text}</div><div class="progress"><i style="width:${Math.min(100,x.progress/q.goal*100)}%"></i></div><div style="display:flex;align-items:center;justify-content:space-between;margin-top:7px"><span class="small">${x.progress}/${q.goal}</span><button class="${done&&!x.claimed?'primary':'secondary'} questClaim" data-i="${i}" ${done&&!x.claimed?'':'disabled'}>${x.claimed?'✓ Claimed':done?'Claim':'In progress'}</button></div></div>`}).join('');
 document.getElementById('rerollQuestBtn').disabled=!!save.dailyQuests.rerolled;
 document.getElementById('rerollQuestBtn').textContent=save.dailyQuests.rerolled?'✓ Reroll Used':'🔄 Free Daily Reroll';
 el.querySelectorAll('.questClaim').forEach(b=>b.onclick=()=>{const x=save.dailyQuests.items[+b.dataset.i],q=questDef(x.id);if(!x.claimed&&x.progress>=q.goal){x.claimed=true;save.metaCoins+=q.reward;persist();renderAll();renderDailyQuests()}});
}
document.getElementById('rerollQuestBtn').onclick=()=>{ensureDailyQuests();if(save.dailyQuests.rerolled)return;const used=new Set(save.dailyQuests.items.map(x=>x.id));const choices=DAILY_QUEST_POOL.filter(q=>!used.has(q.id));if(!choices.length)return;const i=save.dailyQuests.items.findIndex(x=>!x.claimed);if(i<0)return;save.dailyQuests.items[i]={id:choices[Math.floor(Math.random()*choices.length)].id,progress:0,claimed:false};save.dailyQuests.rerolled=true;persist();renderDailyQuests()};
// Hook existing gameplay events without changing their normal behaviour.
const _questStartWave=startWave; startWave=function(){const before=battle?.wave;const lives=battle?.lives;const r=_questStartWave.apply(this,arguments);if(before&&battle)battle._questWaveStartLives=lives;return r};
const _questRenderAll=renderAll; renderAll=function(){_questRenderAll.apply(this,arguments);renderDailyQuests()};
ensureDailyQuests();
'''
s=s[:idx]+js+s[idx:]
# Hook known reward/placement/enemy death locations conservatively
s=s.replace('save.bestWave=Math.max(save.bestWave,clearedWave);','save.bestWave=Math.max(save.bestWave,clearedWave);\n  addQuestProgress("waves",1);\n  if(speed===3)addQuestProgress("speedWaves",1);\n  if(battle?._questWaveStartLives===battle?.lives)addQuestProgress("noLossWaves",1);',1)
# map completion hook before card XP completion block, matching current completion marker
s=s.replace('const usedCards=[...(battle.usedCards||[])];','addQuestProgress(hardMode?"hardMaps":"normalMaps",1);\n    const usedCards=[...(battle.usedCards||[])];',1)
# tower placement: battle.towers.push is stable
s=s.replace('battle.towers.push(tower);','battle.towers.push(tower);\n    addQuestProgress("placed",1);',1)
# enemy kill common reward line: add after first dead assignment where hp<=0 if pattern exists
s=s.replace('e.dead=true;\n        battle.coins+=e.reward;','e.dead=true;\n        battle.coins+=e.reward;\n        addQuestProgress("kills",1);',1)
p.write_text(s)
