from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='REMOVE_ALL_ATTACK_LASER_OVERLAYS_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)

# Disable the supplemental visibility overlay that adds bright rings/trails over attack projectiles.
old='''function drawRecentAttackVisibility(s){\n  const types=new Set(['''
if old not in s:
    raise RuntimeError('drawRecentAttackVisibility anchor not found')
start=s.index('function drawRecentAttackVisibility(s){')
end=s.index('\n}\n', start)+3
replacement='''// REMOVE_ALL_ATTACK_LASER_OVERLAYS_V1: keep only each card's native projectile/attack animation.\nfunction drawRecentAttackVisibility(s){\n  return;\n}\n'''
s=s[:start]+replacement+s[end:]

p.write_text(s,encoding='utf-8')
print('Removed supplemental laser/glow/trail overlays from all attack animations')
