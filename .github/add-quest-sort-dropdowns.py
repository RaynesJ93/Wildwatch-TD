from pathlib import Path
p=Path('index.html'); s=p.read_text()
# Add sort controls above milestone/challenge panels.
old='''    <div id="milestoneQuestList" class="questPanel" style="display:none;gap:10px"></div>\n    <div id="challengeQuestList" class="questPanel" style="display:none;gap:10px"></div>'''
new='''    <div id="milestoneSortWrap" style="display:none;margin:0 0 10px"><select id="milestoneSort" class="secondary" style="width:100%;padding:11px 12px"><option value="not-completed">Not completed</option><option value="completed">Completed</option><option value="progress">Progress</option></select></div>\n    <div id="milestoneQuestList" class="questPanel" style="display:none;gap:10px"></div>\n    <div id="challengeSortWrap" style="display:none;margin:0 0 10px"><select id="challengeSort" class="secondary" style="width:100%;padding:11px 12px"><option value="not-completed">Not completed</option><option value="completed">Completed</option><option value="progress">Progress</option></select></div>\n    <div id="challengeQuestList" class="questPanel" style="display:none;gap:10px"></div>'''
if old not in s: raise SystemExit('milestone/challenge panels not found')
s=s.replace(old,new,1)
# Replace dropdown renderer + extra board renderer with sortable version.
start=s.find('function questDropdownCards(items)')
end=s.find('function setQuestTab(tab)', start)
if start<0 or end<0: raise SystemExit('quest dropdown render block not found')
replacement=r'''function questState(q){
 const goal=Number(q.goal||1),progress=Math.max(0,Number(q.progress||0));
 const completed=!!q.completed||progress>=goal;
 return {goal,progress,completed,ratio:goal?Math.min(1,progress/goal):0};
}
function sortQuestItems(items,mode){
 const a=[...items];
 if(mode==='completed')return a.filter(q=>questState(q).completed);
 if(mode==='not-completed')return a.filter(q=>!questState(q).completed);
 if(mode==='progress')return a.sort((x,y)=>questState(y).ratio-questState(x).ratio);
 return a;
}
function questDropdownCards(items,mode='not-completed'){
 const sorted=sortQuestItems(items,mode);
 if(!sorted.length)return `<div class="info-box center small">No quests in this category yet.</div>`;
 return sorted.map((q,i)=>{const st=questState(q);const status=st.completed?'✓ Completed':st.progress>0?`${st.progress}/${st.goal}`:'Not started';return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px;font-weight:900"><span>${q.icon} ${q.name}</span><span style="display:flex;align-items:center;gap:8px"><span>🟡 ${q.reward}</span><span class="dropArrow">▼</span></span></summary><div style="border-top:1px solid #315b47;margin-top:10px;padding-top:10px"><div class="small">${q.text}</div><div class="progress" style="margin-top:9px"><i style="width:${Math.round(st.ratio*100)}%"></i></div><div class="small" style="margin-top:7px">${status}</div></div></details>`}).join('')
}
function renderExtraQuestBoards(){
 const w=document.getElementById('weeklyQuestList'),m=document.getElementById('milestoneQuestList'),c=document.getElementById('challengeQuestList');
 if(w)w.innerHTML=questPlaceholderCards(WEEKLY_QUESTS);
 if(m)m.innerHTML=questDropdownCards(MILESTONE_QUESTS,document.getElementById('milestoneSort')?.value||'not-completed');
 if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
}
document.getElementById('milestoneSort')?.addEventListener('change',renderExtraQuestBoards);
document.getElementById('challengeSort')?.addEventListener('change',renderExtraQuestBoards);
'''
s=s[:start]+replacement+s[end:]
# Extend setQuestTab to show correct sort control.
needle=""" const tools=document.getElementById('dailyQuestTools');if(tools)tools.style.display=tab==='daily'?'block':'none';"""
replace=needle+"\n const ms=document.getElementById('milestoneSortWrap');if(ms)ms.style.display=tab==='milestones'?'block':'none';\n const cs=document.getElementById('challengeSortWrap');if(cs)cs.style.display=tab==='challenges'?'block':'none';"
if needle not in s: raise SystemExit('setQuestTab tools marker not found')
s=s.replace(needle,replace,1)
p.write_text(s)
