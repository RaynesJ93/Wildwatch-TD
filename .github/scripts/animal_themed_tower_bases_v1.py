from pathlib import Path
import re
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='ANIMAL_THEMED_TOWER_BASES_V1'
if marker in s: print('Already applied');raise SystemExit(0)
anchor='function animalVisual('
idx=s.find(anchor)
if idx<0: raise RuntimeError('animalVisual anchor not found')
helper=r'''// ANIMAL_THEMED_TOWER_BASES_V1: unique habitat/object plinth for every placed animal.
function drawAnimalBase(ctx,t){
  const k=t.key,x=t.x,y=t.y+11;
  ctx.save();ctx.translate(x,y);ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.globalAlpha=.45;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(0,5,22,9,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
  const themes={
    monkey:["🪨","🍌"],frog:["🪷","💧"],owl:["🪵","🍂"],snake:["🪨","🍃"],hedgehog:["🍂","🌿"],goose:["💧","🌾"],crow:["🪵","🪶"],snail:["🪨","💧"],beetle:["🟤","🟤"],cricket:["🌱","🌿"],worm:["🟫","🕳️"],chicken:["🌾","🥚"],bird:["🏙️","🪶"],duck:["💧","🌾"],cat:["🧱","🐾"],dog:["🦴","🐾"],raccoon:["🗑️","🌙"],badger:["🕳️","🪨"],goat:["🪨","🌿"],skunk:["🌿","🍂"],otter:["🪨","💧"],sloth:["🪵","🌿"],koala:["🪵","🍃"],sheep:["🌱","☁️"],ram:["⛰️","🪨"],pig:["🟤","💦"],turkey:["🍂","🌾"],flamingo:["💧","🌸"],peacock:["🌿","🪶"],swan:["💧","🪷"],turtle:["🏖️","🪨"],lizard:["🪨","☀️"],scorpion:["🏜️","🪨"],spider:["🕸️","🪨"],fox:["🍂","🪵"],eagle:["⛰️","🪹"],panda:["🎋","🪨"],lion:["🪨","🌾"],rhino:["🟤","🪨"],whiteRhino:["🪨","🌾"],tiger:["🌿","🪨"],zebra:["🌾","🪨"],penguin:["🧊","❄️"],jaguar:["🌿","🪨"],elephant:["💧","🟤"],silverback:["🪨","🌿"],ant:["🟫","🍂"],bee:["🌼","🍯"]
  };
  const a=themes[k]||["🪨","🌿"];
  ctx.fillStyle="#493d31";ctx.strokeStyle="#1d1813";ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(0,0,20,8,0,0,Math.PI*2);ctx.fill();ctx.stroke();
  ctx.font="16px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[0],-7,-1);ctx.font="12px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[1],10,1);
  ctx.restore();
}

'''
s=s[:idx]+helper+s[idx:]
# Support current and historical tower-loop styles, including optional chaining and alternate tower arrays.
patterns=[
 r'for\s*\(\s*const\s+t\s+of\s+battle\.towers\s*\)\s*\{',
 r'battle\.towers\?*\.forEach\s*\(\s*t\s*=>\s*\{',
 r'battle\.towers\?*\.forEach\s*\(\s*\(t\)\s*=>\s*\{',
 r'for\s*\(\s*const\s+t\s+of\s+towers\s*\)\s*\{',
 r'towers\?*\.forEach\s*\(\s*t\s*=>\s*\{'
]
match=None
for pat in patterns:
    match=re.search(pat,s)
    if match: break
if not match:
    # Fallback: find a drawing callback that references tower coordinates and insert at its opening brace.
    match=re.search(r'(?:battle\.)?towers\??\.forEach\s*\(\s*(?:\(\s*)?t(?:\s*\))?\s*=>\s*\{',s)
if not match: raise RuntimeError('tower draw loop not found')
insert=match.end();s=s[:insert]+'drawAnimalBase(ctx,t);'+s[insert:]
p.write_text(s,encoding='utf-8');print('Added animal themed bases')