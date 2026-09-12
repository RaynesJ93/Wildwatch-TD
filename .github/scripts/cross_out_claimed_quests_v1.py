from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CLAIMED_QUEST_STRIKETHROUGH_V1'
if marker in s:
    print('already installed')
    raise SystemExit(0)
old='''return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px"><b>${q.icon} ${q.name}</b><b>${reward}</b></summary><div class="small" style="margin-top:7px">${q.text}</div><div class="small" style="margin-top:7px">${status}</div>${claim}</details>`;'''
new='''// CLAIMED_QUEST_STRIKETHROUGH_V1: visibly cross out Milestone/Challenge quest names only after the reward is claimed.\n   const questNameStyle=claimed?'text-decoration:line-through;text-decoration-thickness:2px;opacity:.62;':'';\n   return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px"><b style="${questNameStyle}">${q.icon} ${q.name}</b><b>${reward}</b></summary><div class="small" style="margin-top:7px">${q.text}</div><div class="small" style="margin-top:7px">${status}</div>${claim}</details>`;'''
if old not in s:
    raise SystemExit('quest dropdown anchor missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Claimed Milestone and Challenge quest names now strike through after reward claim.')
