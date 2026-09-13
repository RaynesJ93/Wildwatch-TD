from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='DOG_FETCH_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='dog:{name:"Dog",emoji:"🐶",rarity:"Uncommon",cost:80,range:165,rate:1/1.20,dmg:19,color:"#b87",desc:"Balanced attacker."},'
new='dog:{name:"Dog",emoji:"🐶",rarity:"Uncommon",cost:80,range:165,rate:1/1.20,dmg:19,color:"#b87",desc:"Attacks with Bark Blast soundwaves. At Level 10, every 5th attack triggers Fetch: a spinning bone bounces between up to 6 enemies, dealing 1.25x current tower damage to each."},'
if old not in s: raise RuntimeError('Dog card anchor not found')
s=s.replace(old,new,1)
anchor='  // WORM_MUD_SHOT_V1: sludge/mud projectile attack.\n'
if anchor not in s: anchor='  // CRICKET_DEAFENING_CHIRP_V1: Chirp Wave + Level 10 Deafening Chirp.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // DOG_FETCH_V1: Bark Blast + Level 10 Fetch bouncing bone.\n  if(t.key==="dog"){\n    let fetch=false;if(t.level>=10){t.dogAttackCount=(t.dogAttackCount||0)+1;fetch=t.dogAttackCount%5===0;}\n    if(fetch){let pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);let prev={x:t.x,y:t.y};for(let i=0;i<6&&pool.length;i++){pool.sort((a,b)=>Math.hypot(a.x-prev.x,a.y-prev.y)-Math.hypot(b.x-prev.x,b.y-prev.y));const e=pool.shift();e.hp-=dmg*1.25;battle.shots.push({x:prev.x,y:prev.y,tx:e.x,ty:e.y,life:.26+i*.035,maxLife:.26+i*.035,type:"dogBone",spin:i*1.2});prev=e;}battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.65,maxLife:.65,type:"fetchBanner"});}\n    else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.28,maxLife:.28,type:"dogBark"});}\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // WORM_STAMPEDE_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // WORM_MUD_SHOT_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // DOG_FETCH_DRAW_V1\n    }else if(s.type==="dogBark"){const q=1-Math.max(0,s.life)/(s.maxLife||.28),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,a=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.strokeStyle="#ffe8a8";ctx.shadowColor="#ffd66b";ctx.shadowBlur=7;ctx.lineWidth=2.5;for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(0,0,5+i*6,-.72,.72);ctx.stroke();}ctx.restore();\n    }else if(s.type==="dogBone"){const q=1-Math.max(0,s.life)/(s.maxLife||.26),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*10);ctx.font="18px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🦴",0,0);ctx.restore();\n    }else if(s.type==="fetchBanner"){const q=1-Math.max(0,s.life)/(s.maxLife||.65);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#fff1bd";ctx.strokeStyle="#5a3a22";ctx.lineWidth=3;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.strokeText("FETCH!",0,-30-q*12);ctx.fillText("FETCH!",0,-30-q*12);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Dog Bark Blast and Fetch')