from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='HARD_BLOCK_GENERIC_BEAM_CUSTOM_FOUR_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)

# Use the stable start of the projectile render loop. The previous patch expected
# drawRecentAttackVisibility() immediately after this line, but that changed when
# the glow/laser overlay was removed.
anchor='  battle.shots?.forEach(s=>{'
if anchor not in s:
    raise RuntimeError('shot renderer loop anchor not found')

replacement='''  battle.shots?.forEach(s=>{
    // HARD_BLOCK_GENERIC_BEAM_CUSTOM_FOUR_V1: never render the legacy generic beam from these custom-animation towers.
    if(s.type==="beam"){
      const sourceTower=(battle.towers||[]).find(t=>Math.hypot((t.x||0)-(s.x||0),(t.y||0)-(s.y||0))<28);
      if(sourceTower && ["peacock","turtle","lizard","scorpion"].includes(sourceTower.key))return;
    }'''

s=s.replace(anchor,replacement,1)
p.write_text(s,encoding='utf-8')
print('Hard-blocked legacy generic beam rendering for Peacock Turtle Lizard Scorpion')
