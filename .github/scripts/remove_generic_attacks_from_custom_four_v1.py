from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CUSTOM_FOUR_NO_GENERIC_ATTACK_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)

old='''  battle.shots?.forEach(s=>{\n    drawRecentAttackVisibility(s);\n'''
new='''  battle.shots?.forEach(s=>{\n    // CUSTOM_FOUR_NO_GENERIC_ATTACK_V1: Peacock, Turtle, Lizard and Scorpion use only their bespoke attack animations.\n    if(s.type==="beam" && (battle.towers||[]).some(t=>["peacock","turtle","lizard","scorpion"].includes(t.key) && Math.hypot((s.x??0)-t.x,(s.y??0)-t.y)<6)) return;\n    drawRecentAttackVisibility(s);\n'''
if old not in s:
    raise RuntimeError('shot render loop anchor missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Removed generic beam rendering for Peacock Turtle Lizard Scorpion')
