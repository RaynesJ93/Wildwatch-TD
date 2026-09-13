from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='ANIMAL_THEMED_TOWER_BASES_V1'
if marker in s: print('Already applied');raise SystemExit(0)
# Inject helper before tower drawing. It deliberately uses bold, simple shapes/emojis so bases stay readable on iPhone.
anchor='function animalVisual('
idx=s.find(anchor)
if idx<0: raise RuntimeError('animalVisual anchor not found')
helper=r'''// ANIMAL_THEMED_TOWER_BASES_V1: unique habitat/object plinth for every placed animal.
function drawAnimalBase(ctx,t){
  const k=t.key,x=t.x,y=t.y+11;
  ctx.save();ctx.translate(x,y);ctx.textAlign="center";ctx.textBaseline="middle";
  // universal shadow keeps each themed base readable over every map.
  ctx.globalAlpha=.45;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(0,5,22,9,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
  const themes={
    monkey:["🪨","🍌"],frog:["🪷","💧"],owl:["🪵","🍂"],snake:["🪨","🍃"],
    hedgehog:["🍂","🌿"],goose:["💧","🌾"],crow:["🪵","🪶"],snail:["🪨","💧"],
    beetle:["🟤","🟤"],cricket:["🌱","🌿"],worm:["🟫","🕳️"],chicken:["🌾","🥚"],
    bird:["🏙️","🪶"],duck:["💧","🌾"],cat:["🧱","🐾"],dog:["🦴","🐾"],
    raccoon:["🗑️","🌙"],badger:["🕳️","🪨"],goat:["🪨","🌿"],skunk:["🌿","🍂"],
    otter:["🪨","💧"],sloth:["🪵","🌿"],koala:["🪵","🍃"],sheep:["🌱","☁️"],
    ram:["⛰️","🪨"],pig:["🟤","💦"],turkey:["🍂","🌾"],flamingo:["💧","🌸"],
    peacock:["🌿","🪶"],swan:["💧","🪷"],turtle:["🏖️","🪨"],lizard:["🪨","☀️"],
    scorpion:["🏜️","🪨"],spider:["🕸️","🪨"],fox:["🍂","🪵"],eagle:["⛰️","🪹"],
    panda:["🎋","🪨"],lion:["🪨","🌾"],rhino:["🟤","🪨"],whiteRhino:["🪨","🌾"],
    tiger:["🌿","🪨"],zebra:["🌾","🪨"],penguin:["🧊","❄️"],jaguar:["🌿","🪨"],
    elephant:["💧","🟤"],silverback:["🪨","🌿"],ant:["🟫","🍂"],bee:["🌼","🍯"]
  };
  const a=themes[k]||["🪨","🌿"];
  // sturdy habitat pad beneath the icon props
  ctx.fillStyle="#493d31";ctx.strokeStyle="#1d1813";ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(0,0,20,8,0,0,Math.PI*2);ctx.fill();ctx.stroke();
  ctx.font="16px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[0],-7,-1);ctx.font="12px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[1],10,1);
  ctx.restore();
}

'''
s=s[:idx]+helper+s[idx:]
# Find placed tower loop and add themed base immediately before animal/tower visual. Multiple historical draw layouts supported.
candidates=['for(const t of battle.towers){','battle.towers.forEach(t=>{']
for c in candidates:
    pos=s.find(c)
    if pos>=0:
        insert=pos+len(c);s=s[:insert]+'drawAnimalBase(ctx,t);'+s[insert:];break
else: raise RuntimeError('tower draw loop not found')
p.write_text(s,encoding='utf-8');print('Added animal themed bases')