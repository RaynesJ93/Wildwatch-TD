from pathlib import Path
p=Path('index.html'); s=p.read_text()
# Add tab controls and extra quest lists to the existing Daily Quests screen.
old='''    <div id="dailyQuestList" style="display:grid;gap:10px;margin-top:14px"></div>'''
new='''    <div class="questTabs" style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:14px 0 10px">
      <button class="secondary questTab active" data-qtab="daily">Daily</button>
      <button class="secondary questTab" data-qtab="weekly">Weekly</button>
      <button class="secondary questTab" data-qtab="milestones">Milestones</button>
      <button class="secondary questTab" data-qtab="challenges">Challenges</button>
    </div>
    <div id="dailyQuestList" class="questPanel" style="display:grid;gap:10px"></div>
    <div id="weeklyQuestList" class="questPanel" style="display:none;gap:10px"></div>
    <div id="milestoneQuestList" class="questPanel" style="display:none;gap:10px"></div>
    <div id="challengeQuestList" class="questPanel" style="display:none;gap:10px"></div>'''
if old not in s: raise SystemExit('daily quest list marker not found')
s=s.replace(old,new,1)
# Only show daily reset/reroll box on Daily tab.
s=s.replace('<div class="info-box" style="margin-top:12px;text-align:center">\n      <div class="small" id="questResetText">','<div class="info-box" id="dailyQuestTools" style="margin-top:12px;text-align:center">\n      <div class="small" id="questResetText">',1)
# Insert simple functional placeholder boards before the Daily quest system comment.
marker='// ---- Daily quest board ----'
if marker not in s: raise SystemExit('daily quest JS marker not found')
js=r'''// ---- Quest category tabs ----
const WEEKLY_QUESTS=[
 {icon:'🌊',name:'Weekly Wave Runner',text:'Clear 75 waves',reward:200},
 {icon:'🗺️',name:'Weekly Explorer',text:'Complete 5 maps',reward:175},
 {icon:'🔥',name:'Hard Week',text:'Complete 2 Hard maps',reward:225}
];
const MILESTONE_QUESTS=[
 {icon:'🃏',name:'Growing Collection',text:'Own 10 animal cards',reward:150},
 {icon:'⭐',name:'Veteran Defender',text:'Clear 100 total waves',reward:250},
 {icon:'🏆',name:'Master Collector',text:'Own your first Legendary card',reward:300}
];
const CHALLENGE_QUESTS=[
 {icon:'⚪',name:'Common Ground',text:'Complete a map using only Common cards',reward:100},
 {icon:'❤️',name:'Untouchable',text:'Complete a map without losing a life',reward:125},
 {icon:'⏩',name:'Full Speed Ahead',text:'Clear 5 waves at 3× speed',reward:75}
];
function questPlaceholderCards(items){return items.map(q=>`<div class="info-box"><div style="display:flex;justify-content:space-between;gap:8px"><b>${q.icon} ${q.name}</b><b>🟡 ${q.reward}</b></div><div class="small" style="margin-top:6px">${q.text}</div><div class="small" style="margin-top:9px;opacity:.8">Ready for tracking rules</div></div>`).join('')}
function renderExtraQuestBoards(){
 const w=document.getElementById('weeklyQuestList'),m=document.getElementById('milestoneQuestList'),c=document.getElementById('challengeQuestList');
 if(w)w.innerHTML=questPlaceholderCards(WEEKLY_QUESTS);
 if(m)m.innerHTML=questPlaceholderCards(MILESTONE_QUESTS);
 if(c)c.innerHTML=questPlaceholderCards(CHALLENGE_QUESTS);
}
function setQuestTab(tab){
 const ids={daily:'dailyQuestList',weekly:'weeklyQuestList',milestones:'milestoneQuestList',challenges:'challengeQuestList'};
 Object.entries(ids).forEach(([k,id])=>{const el=document.getElementById(id);if(el)el.style.display=k===tab?'grid':'none'});
 document.querySelectorAll('.questTab').forEach(b=>b.classList.toggle('active',b.dataset.qtab===tab));
 const tools=document.getElementById('dailyQuestTools');if(tools)tools.style.display=tab==='daily'?'block':'none';
 const title=document.querySelector('#questScreen h1');if(title)title.textContent={daily:'Daily Quests',weekly:'Weekly Quests',milestones:'Milestone Quests',challenges:'Challenge Quests'}[tab];
}
document.querySelectorAll('.questTab').forEach(b=>b.onclick=()=>setQuestTab(b.dataset.qtab));
renderExtraQuestBoards();
setQuestTab('daily');

'''
s=s.replace(marker,js+marker,1)
p.write_text(s)
