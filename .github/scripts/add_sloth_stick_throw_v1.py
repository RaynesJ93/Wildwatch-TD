from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='SLOTH_STICK_THROW_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='sloth:{name:"Sloth",emoji:"🦥",rarity:"Uncommon",cost:92,range:150,rate:1/.60,dmg:34,color:"#876",desc:"Slow heavy attacker."},'
new='sloth:{name:"Sloth",emoji:"🦥",rarity:"Uncommon",cost:92,range:150,rate:1/.60,dmg:34,color:"#876",desc:"Slow heavy attacker that throws spinning sticks at enemies."},'
if old not in s: raise RuntimeError('Sloth card anchor not found')
s=s.replace(old,new,1)
anchor='  // OTTER_RIVER_RUSH_V1: Pebble Toss + Level 10 River Rush.\n'
if anchor not in s: anchor='  // BADGER_SAVAGE_MAUL_V1: Claw Swipe + Level 10 Savage Maul.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // SLOTH_STICK_THROW_V1: spinning stick projectile attack.\n  if(t.key==="sloth"){target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.38,maxLife:.38,type:"slothStick",spin:Math.random()*6.28});t.cd=cardRate(t.key);return;}\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // OTTER_RIVER_RUSH_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // BADGER_SAVAGE_MAUL_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // SLOTH_STICK_THROW_DRAW_V1\n    }else if(s.type==="slothStick"){const q=1-Math.max(0,s.life)/(s.maxLife||.38),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*12);ctx.strokeStyle="#6b3f1f";ctx.lineWidth=5;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-10,0);ctx.lineTo(10,0);ctx.stroke();ctx.strokeStyle="#a56b38";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-8,-1);ctx.lineTo(8,-1);ctx.stroke();ctx.strokeStyle="#5f8d42";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(4,0);ctx.lineTo(8,-5);ctx.stroke();ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Sloth Stick Throw')