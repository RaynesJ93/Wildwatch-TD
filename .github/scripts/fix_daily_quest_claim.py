from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = "el.querySelectorAll('.questClaim').forEach(b=>b.onclick=()=>{const x=save.dailyQuests.items[+b.dataset.i],q=questDef(x.id);if(!x.claimed&&x.progress>=q.goal){x.claimed=true;save.metaCoins+=q.reward;persist();renderHome();renderCards();renderDailyQuests()}});"
new = "el.querySelectorAll('.questClaim').forEach(b=>b.onclick=()=>{const x=save.dailyQuests.items[+b.dataset.i],q=questDef(x.id);if(!x.claimed&&x.progress>=q.goal){x.claimed=true;save.metaCoins+=q.reward;persist();b.textContent='✓ Claimed';b.disabled=true;b.className='secondary questClaim';renderDailyQuests();if(typeof renderMeta==='function')renderMeta();renderCards()}});"
if old not in s:
    raise SystemExit('Daily quest claim handler not found; no changes made')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
print('Updated daily quest claim UI to show Claimed immediately')
