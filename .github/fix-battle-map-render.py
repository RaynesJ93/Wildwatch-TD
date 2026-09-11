from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

marker='// MAP_VISUAL_FIX: render battlefield immediately when a map is loaded'
if marker in s:
    raise SystemExit('battle map render fix already present')

old='''  resetBattle();
  updateDifficultyUI();'''
new='''  resetBattle();
  // MAP_VISUAL_FIX: render battlefield immediately when a map is loaded
  // Keep the animation loop alive so the road, pads and placed towers are
  // visible before the player presses Start wave.
  draw();
  if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}
  updateDifficultyUI();'''

if old not in s:
    raise SystemExit('Sanctuary stage reset marker not found')

s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Inserted immediate battle-map rendering after Sanctuary stage reset')
