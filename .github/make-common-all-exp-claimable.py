from pathlib import Path
p=Path('index.html'); s=p.read_text()
old="""function questDropdownCards(items,mode='not-completed'){
 const sorted=sortQuestItems(items,mode);
 if(!sorted.length)return `<div class="info-box center small">No quests in this category yet.</div>`;
 return sorted.map((q,i)=>{const st=questState(q);const status=st.completed?'✓ Completed':st.progress>0?`${st.progress}/${st.goal}`:'Not started';return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px;font-weight:900"><span>${q.icon} ${q.name}</span><span style="display:flex;align-items:center;gap:8px"><span>${q.rewardType==='exp'?'⭐':'🟡'} ${q.reward}${q.rewardType==='exp'?' EXP':''}</span><span class="dropArrow">▼</span></span></summary><div style="border-top:1px solid #315b47;margin-top:10px;padding-top:10px"><div class="small">${q.text}</div><div class="progress" style="margin-top:9px"><i style="width:${Math.round(st.ratio*100)}%"></i></div><div class="small" style="margin-top:7px">${status}</div></div></details>`}).join('')
}"""
new="""function questDropdownCards(items,mode='not-completed'){
 const sorted=sortQuestItems(items,mode);
 if(!sorted.length)return `<div class="info-box center small">No quests in this category yet.</div>`;
 return sorted.map((q,i)=>{const st=questState(q),claimed=!!save.milestoneClaims?.[q.id];const status=claimed?'✓ Reward claimed':st.completed?'✓ Completed':st.progress>0?`${st.progress}/${st.goal}`:'Not started';const claim=q.id==='commonAll'&&st.completed?`<button class="primary milestoneClaimBtn" data-id="${q.id}" style="width:100%;margin-top:10px" ${claimed?'disabled':''}>${claimed?'✓ 500 EXP given to every Common card':'Claim ⭐ 500 EXP for every Common card'}</button>`:'';return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px;font-weight:900"><span>${q.icon} ${q.name}</span><span style="display:flex;align-items:center;gap:8px"><span>${q.rewardType==='exp'?'⭐':'🟡'} ${q.reward}${q.rewardType==='exp'?' EXP each':''}</span><span class="dropArrow">▼</span></span></summary><div style="border-top:1px solid #315b47;margin-top:10px;padding-top:10px"><div class="small">${q.text}</div><div class="progress" style="margin-top:9px"><i style="width:${Math.round(st.ratio*100)}%"></i></div><div class="small" style="margin-top:7px">${status}</div>${claim}</div></details>`}).join('')
}
function bindMilestoneClaimButtons(){
 document.querySelectorAll('.milestoneClaimBtn').forEach(btn=>btn.onclick=()=>{
   if(btn.dataset.id!=='commonAll'||save.milestoneClaims?.commonAll||!questState(MILESTONE_QUESTS.find(q=>q.id==='commonAll')).completed)return;
   save.cardXP=save.cardXP||{};save.milestoneClaims=save.milestoneClaims||{};
   Object.keys(animals).filter(k=>animals[k].rarity==='Common'&&(save.unlocked||[]).includes(k)).forEach(k=>save.cardXP[k]=(save.cardXP[k]||0)+500);
   save.milestoneClaims.commonAll=true;persist();renderMeta();renderExtraQuestBoards();
 });
}"""
if old not in s: raise SystemExit('questDropdownCards current block not found')
s=s.replace(old,new,1)
old2=""" if(m)m.innerHTML=questDropdownCards(MILESTONE_QUESTS,document.getElementById('milestoneSort')?.value||'not-completed');
 if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
}"""
new2=""" if(m)m.innerHTML=questDropdownCards(MILESTONE_QUESTS,document.getElementById('milestoneSort')?.value||'not-completed');
 if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
 bindMilestoneClaimButtons();
}"""
if old2 not in s: raise SystemExit('renderExtraQuestBoards tail not found')
s=s.replace(old2,new2,1)
p.write_text(s)
