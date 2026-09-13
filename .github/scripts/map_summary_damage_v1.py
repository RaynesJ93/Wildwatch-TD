from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='MAP_SUMMARY_DAMAGE_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)

# Add a helper that records actual damage dealt (capped at the enemy's remaining HP).
anchor='function towerTick(t,dt){'
if anchor not in s:
    raise RuntimeError('towerTick anchor missing')
helper='''// MAP_SUMMARY_DAMAGE_V1: record real damage dealt by each deployed tower.\nfunction towerDealDamage(t,e,amount){\n  if(!t||!e||e.dead)return 0;\n  const raw=Math.max(0,Number(amount)||0);\n  const before=Math.max(0,Number(e.hp)||0);\n  const dealt=Math.min(before,raw);\n  e.hp-=raw;\n  t.damageDealt=(Number(t.damageDealt)||0)+dealt;\n  return dealt;\n}\n'''
s=s.replace(anchor,helper+anchor,1)

# Convert direct tower damage inside towerTick into tracked damage.
start=s.index('function towerTick(t,dt){')
end=s.index('function showMapSummary(cardXp){', start)
block=s[start:end]
pattern=re.compile(r'\b([A-Za-z_$][\w$]*)\.hp-=(.*?);')

def repl(m):
    obj=m.group(1)
    expr=m.group(2).strip()
    return f'towerDealDamage(t,{obj},{expr});'

block2,count=pattern.subn(repl,block)
if count < 8:
    raise RuntimeError(f'Expected multiple tower damage sites, only replaced {count}')
s=s[:start]+block2+s[end:]

old='''  let strongest=null;\n  towers.forEach(t=>{\n    const power=towerDamage(t);\n    if(!strongest || power>strongest.power || (power===strongest.power&&t.level>strongest.t.level))strongest={t,power};\n  });\n  const strongestHtml=strongest\n    ? `${animals[strongest.t.key].emoji} <b>${animals[strongest.t.key].name}</b><div class="small">Tower Lv ${strongest.t.level} • ${Math.round(strongest.power)} damage</div>`\n    : `<b>No towers deployed</b>`;'''
new='''  let strongest=null;\n  towers.forEach(t=>{\n    const dealt=Math.round(Number(t.damageDealt)||0);\n    if(!strongest || dealt>strongest.dealt || (dealt===strongest.dealt&&t.level>strongest.t.level))strongest={t,dealt};\n  });\n  const strongestHtml=strongest\n    ? `${animals[strongest.t.key].emoji} <b>${animals[strongest.t.key].name}</b><div class="small">Tower Lv ${strongest.t.level} • ${strongest.dealt.toLocaleString()} total damage dealt</div>`\n    : `<b>No towers deployed</b>`;'''
if old not in s:
    raise RuntimeError('summary strongest-tower anchor missing')
s=s.replace(old,new,1)

s=s.replace('Strongest tower deployed','Top damage tower',1)

old_sub="modal.querySelector('#mapSummarySubtitle').textContent=`${seriesName} ${currentMap} • ${hardMode?'Hard':'Normal'}`;"
new_sub="""const rewardRates=hardMode?'20/wave • 36/elite • 99/boss':'12/wave • 22/elite • 60/boss';\n  modal.querySelector('#mapSummarySubtitle').textContent=`${seriesName} ${currentMap} • ${hardMode?'Hard':'Normal'} • ${rewardRates}`;"""
if old_sub not in s:
    raise RuntimeError('summary subtitle anchor missing')
s=s.replace(old_sub,new_sub,1)

p.write_text(s,encoding='utf-8')
print(f'Applied map summary damage tracking; converted {count} tower damage sites')
