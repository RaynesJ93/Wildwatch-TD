from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='WORM_MUD_SHOT_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='worm:{name:"Worm",emoji:"🪱",rarity:"Common",cost:42,range:110,rate:1/1.30,dmg:7,color:"#b87",desc:"Cheap fast attacker."},'
new='worm:{name:"Worm",emoji:"🪱",rarity:"Common",cost:42,range:110,rate:1/1.30,dmg:16,color:"#b87",desc:"Throws globs of sludge and mud that splatter enemies."},'
if old not in s: raise RuntimeError('Worm card anchor not found')
s=s.replace(old,new,1)
anchor='  // CRICKET_DEAFENING_CHIRP_V1: Chirp Wave + Level 10 Deafening Chirp.\n'
if anchor not in s: anchor='  // HEDGEHOG_QUILL_STORM_V1: Quill Shot + Level 10 Quill Storm.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // WORM_MUD_SHOT_V1: sludge/mud projectile attack.\n  if(t.key==="worm"){target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.34,maxLife:.34,type:"wormMud",spin:Math.random()*6.28});t.cd=cardRate(t.key);return;}\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // CRICKET_DEAFENING_CHIRP_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // CAT_SKUNK_PROJECTILE_DRAW_V2\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // WORM_MUD_SHOT_DRAW_V1\n    }else if(s.type==="wormMud"){const q=1-Math.max(0,s.life)/(s.maxLife||.34),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*7);ctx.fillStyle="#66503a";ctx.strokeStyle="#3d3024";ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(0,0,6,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle="#8b7355";ctx.beginPath();ctx.arc(-2,-2,2,0,Math.PI*2);ctx.fill();if(q>.78){ctx.fillStyle="#594330";for(let i=0;i<7;i++){const a=i*.9,r=(q-.78)*65;ctx.beginPath();ctx.arc(Math.cos(a)*r,Math.sin(a)*r*.7,2+(i%2),0,Math.PI*2);ctx.fill();}}ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Worm base damage set to 16 and Mud Shot added')