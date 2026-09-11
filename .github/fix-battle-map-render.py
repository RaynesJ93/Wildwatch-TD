from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

marker='// MAP_VISUAL_FIX: render battlefield immediately when a map is loaded'
if marker in s:
    raise SystemExit('battle map render fix already present')

start=s.find('function resetBattle')
if start < 0:
    raise SystemExit('resetBattle function not found')
brace=s.find('{', start)
if brace < 0:
    raise SystemExit('resetBattle opening brace not found')

depth=0
end=None
in_single=in_double=in_template=False
escape=False
for i in range(brace, len(s)):
    ch=s[i]
    if escape:
        escape=False
        continue
    if ch=='\\':
        escape=True
        continue
    if not in_double and not in_template and ch=="'":
        in_single=not in_single
        continue
    if not in_single and not in_template and ch=='"':
        in_double=not in_double
        continue
    if not in_single and not in_double and ch=='`':
        in_template=not in_template
        continue
    if in_single or in_double or in_template:
        continue
    if ch=='{':
        depth+=1
    elif ch=='}':
        depth-=1
        if depth==0:
            end=i
            break

if end is None:
    raise SystemExit('resetBattle closing brace not found')

insert='''\n  // MAP_VISUAL_FIX: render battlefield immediately when a map is loaded\n  // and keep the animation loop alive so roads, pads and placed towers are\n  // visible before the player presses Start wave.\n  draw();\n  if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}\n'''

s=s[:end]+insert+s[end:]
p.write_text(s,encoding='utf-8')
print('Inserted immediate battle-map rendering into resetBattle')
