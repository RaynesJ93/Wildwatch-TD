from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='HARD_BLOCK_GENERIC_BEAM_CUSTOM_FOUR_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)
anchor='''  battle.shots?.forEach(s=>{\n    drawRecentAttackVisibility(s);'''
if anchor not in s:
    raise RuntimeError('shot renderer anchor not found')
replacement='''  battle.shots?.forEach(s=>{\n    // HARD_BLOCK_GENERIC_BEAM_CUSTOM_FOUR_V1: never render the legacy generic beam from these custom-animation towers.\n    if(s.type==="beam"){\n      const sourceTower=(battle.towers||[]).find(t=>Math.hypot((t.x||0)-(s.x||0),(t.y||0)-(s.y||0))<24);\n      if(sourceTower && ["peacock","turtle","lizard","scorpion"].includes(sourceTower.key))return;\n    }\n    drawRecentAttackVisibility(s);'''
s=s.replace(anchor,replacement,1)
p.write_text(s,encoding='utf-8')
print('Hard-blocked legacy generic beam rendering for Peacock Turtle Lizard Scorpion')
