from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

new_func = r'''// ANIMAL_THEMED_TOWER_BASES_V2: large, unmistakable habitat/object base for every placed animal.
function drawAnimalBase(ctx,t){
  const k=t.key, x=t.x, y=t.y+15;
  const themes={
    monkey:["forest","🍌","🪨"],frog:["water","🪷","💧"],owl:["forest","🪵","🍂"],snake:["forest","🪨","🍃"],hedgehog:["forest","🍂","🌿"],goose:["water","🌾","💧"],crow:["forest","🪵","🪶"],snail:["water","🪨","💧"],beetle:["earth","🟤","🍂"],cricket:["grass","🌱","🌿"],worm:["earth","🕳️","🟫"],chicken:["farm","🌾","🥚"],bird:["urban","🏙️","🪶"],duck:["water","💧","🌾"],cat:["urban","🧱","🐾"],dog:["grass","🦴","🐾"],raccoon:["urban","🗑️","🌙"],badger:["earth","🕳️","🪨"],goat:["mountain","🪨","🌿"],skunk:["forest","🌿","🍂"],otter:["water","🪨","💧"],sloth:["forest","🪵","🌿"],koala:["eucalyptus","🪵","🍃"],sheep:["farm","🌱","☁️"],ram:["mountain","⛰️","🪨"],pig:["mud","🟤","💦"],turkey:["farm","🍂","🌾"],flamingo:["water","💧","🌸"],peacock:["garden","🌿","🪶"],swan:["water","🪷","💧"],turtle:["beach","🏖️","🪨"],lizard:["desert","🪨","☀️"],scorpion:["desert","🏜️","🪨"],spider:["cave","🕸️","🪨"],fox:["forest","🍂","🪵"],eagle:["mountain","⛰️","🪹"],panda:["bamboo","🎋","🪨"],lion:["savannah","🪨","🌾"],rhino:["savannah","🟤","🪨"],whiteRhino:["savannah","🪨","🌾"],tiger:["jungle","🌿","🪨"],zebra:["savannah","🌾","🪨"],penguin:["ice","🧊","❄️"],jaguar:["jungle","🌿","🪨"],elephant:["water","💧","🟤"],silverback:["jungle","🪨","🌿"],ant:["earth","🟫","🍂"],bee:["garden","🌼","🍯"]
  };
  const [kind,a,b]=themes[k]||["forest","🪨","🌿"];
  const palette={
    forest:["#355b36","#78934d","#213b24"], eucalyptus:["#567c67","#a7c99b","#294438"], water:["#3c8794","#8bd4da","#1f5964"],
    ice:["#b8efff","#f1fdff","#73b8d4"], desert:["#c99b56","#f0cf8b","#8c632f"], farm:["#78934d","#d3d99a","#4c632f"],
    mountain:["#6d7068","#c8c4af","#42453f"], earth:["#75563d","#b28a61","#432f22"], mud:["#6d4d38","#9d775a","#3f2b21"],
    grass:["#4f7e45","#9bc66c","#31512d"], urban:["#666b70","#bfc3c7","#3b3f43"], garden:["#4f814b","#d58ba9","#31532f"],
    beach:["#d4b66f","#f2dfa5","#91753c"], cave:["#4e4a51","#9b92a3","#2b292d"], bamboo:["#4f7740","#a4c872","#2c4824"],
    savannah:["#aa8d44","#e2cb78","#715d2d"], jungle:["#2f663f","#76a354","#1b4127"]
  };
  const c=palette[kind]||palette.forest;
  ctx.save();
  ctx.translate(x,y);

  // soft contact shadow kept BEHIND the habitat, never on top of it
  ctx.globalAlpha=.36;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(0,8,39,15,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;

  // thick, bright habitat platform
  ctx.fillStyle=c[2];ctx.beginPath();ctx.ellipse(0,3,37,16,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=c[0];ctx.strokeStyle=c[1];ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(0,-1,36,15,0,0,Math.PI*2);ctx.fill();ctx.stroke();

  // habitat texture so bases are visibly different even before seeing the accent objects
  ctx.strokeStyle=c[1];ctx.lineWidth=2;ctx.globalAlpha=.75;
  if(["water","ice"].includes(kind)){
    for(let i=-2;i<=2;i++){ctx.beginPath();ctx.arc(i*12,0,7,Math.PI*.15,Math.PI*.85);ctx.stroke();}
  }else if(["forest","eucalyptus","jungle","bamboo","grass","garden","farm","savannah"].includes(kind)){
    for(let i=-2;i<=2;i++){ctx.beginPath();ctx.moveTo(i*12,6);ctx.lineTo(i*12-3,-3);ctx.moveTo(i*12,4);ctx.lineTo(i*12+4,-5);ctx.stroke();}
  }else if(["desert","beach","mountain","earth","mud","cave"].includes(kind)){
    for(let i=-2;i<=2;i++){ctx.beginPath();ctx.arc(i*13,2,4,0,Math.PI*2);ctx.stroke();}
  }else{
    ctx.beginPath();ctx.moveTo(-28,3);ctx.lineTo(28,3);ctx.stroke();
  }
  ctx.globalAlpha=1;

  // unique animal-specific habitat props
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.font="24px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a,-16,-4);
  ctx.font="19px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(b,18,-2);

  // Koala gets a particularly obvious eucalyptus-log base.
  if(k==="koala"){
    ctx.strokeStyle="#6b4528";ctx.lineWidth=8;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-24,5);ctx.lineTo(22,1);ctx.stroke();
    ctx.font="22px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText("🍃",-20,-7);ctx.fillText("🍃",20,-8);
  }
  if(k==="penguin"){
    ctx.fillStyle="#eafbff";ctx.strokeStyle="#77c5df";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-27,4);ctx.lineTo(-18,-9);ctx.lineTo(3,-11);ctx.lineTo(26,-3);ctx.lineTo(20,9);ctx.lineTo(-13,11);ctx.closePath();ctx.fill();ctx.stroke();
  }
  ctx.restore();
}
'''

pattern = re.compile(r'// ANIMAL_THEMED_TOWER_BASES_V1:.*?\nfunction drawAnimalBase\(ctx,t\)\{.*?\n\}\n\nfunction animalVisual', re.S)
if not pattern.search(s):
    pattern = re.compile(r'// ANIMAL_THEMED_TOWER_BASES_V2:.*?\nfunction drawAnimalBase\(ctx,t\)\{.*?\n\}\n\nfunction animalVisual', re.S)
if not pattern.search(s):
    raise RuntimeError('Could not find drawAnimalBase block')
s = pattern.sub(new_func + '\nfunction animalVisual', s, count=1)

# Remove the later generic tower shadow that was still covering the habitat base.
old_shadow = '''    ctx.save();
    ctx.shadowColor="#000d";ctx.shadowBlur=14;ctx.shadowOffsetY=9;
    ctx.beginPath();ctx.ellipse(t.x,t.y+22,31,14,0,0,Math.PI*2);ctx.fillStyle="#0008";ctx.fill();
    ctx.shadowColor="transparent";
'''
new_shadow = '''    ctx.save();
    // V2: no generic oval is drawn over the themed habitat base.
    ctx.shadowColor="transparent";
'''
if old_shadow in s:
    s = s.replace(old_shadow, new_shadow, 1)
elif 'V2: no generic oval is drawn over the themed habitat base.' not in s:
    raise RuntimeError('Could not find covering tower shadow block')

p.write_text(s, encoding='utf-8')
print('ANIMAL_THEMED_TOWER_BASES_V2 applied: visible habitat platforms + no covering shadow')
