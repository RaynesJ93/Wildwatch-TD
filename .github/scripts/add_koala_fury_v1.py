from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='KOALA_FURY_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='koala:{name:"Koala",emoji:"🐨",rarity:"Uncommon",cost:85,range:175,rate:1/.95,dmg:22,color:"#aaa",desc:"Balanced attacker."},'
new='koala:{name:"Koala",emoji:"🐨",rarity:"Uncommon",cost:85,range:175,rate:1/.95,dmg:22,color:"#aaa",desc:"Attacks with eucalyptus Branch Whacks. At Level 10, every 7th attack triggers Koala Fury for 4s: attack speed doubles and each attack strikes with 3 leafy branches instead of one."},'
if old not in s: raise RuntimeError('Koala card anchor not found')
s=s.replace(old,new,1)
anchor='  // SLOTH_STICK_THROW_V1: spinning stick projectile attack.\n'
if anchor not in s: anchor='  // OTTER_RIVER_RUSH_V1: Pebble Toss + Level 10 River Rush.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // KOALA_FURY_V1: Branch Whack + Level 10 Koala Fury.\n  if(t.key==="koala"){\n    t.koalaFury=Math.max(0,(t.koalaFury||0)-dt);let trigger=false;if(t.level>=10&&t.koalaFury<=0){t.koalaAttackCount=(t.koalaAttackCount||0)+1;trigger=t.koalaAttackCount%7===0;if(trigger){t.koalaFury=4;battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.8,maxLife:.8,type:"koalaFuryBanner"});}}\n    if(t.koalaFury>0){const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);for(let i=0;i<3&&pool.length;i++){const e=pool[i%pool.length];e.hp-=dmg;battle.shots.push({x:t.x,y:t.y,tx:e.x,ty:e.y,life:.22+i*.035,maxLife:.22+i*.035,type:"koalaBranch",fury:1,offset:i-1});}t.cd=cardRate(t.key)*.5;}else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:.27,maxLife:.27,type:"koalaBranch",fury:0,offset:0});t.cd=cardRate(t.key);}return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // SLOTH_TREE_TOPPLE_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // SLOTH_STICK_THROW_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // KOALA_FURY_DRAW_V1\n    }else if(s.type==="koalaBranch"){const q=1-Math.max(0,s.life)/(s.maxLife||.27),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,a=Math.atan2(s.ty-s.y,s.tx-s.x)+Math.sin(q*Math.PI)*.45+(s.offset||0)*.13;ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.strokeStyle=s.fury?"#8f5b2e":"#72502e";ctx.lineWidth=s.fury?6:5;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-14,0);ctx.lineTo(14,0);ctx.stroke();ctx.fillStyle=s.fury?"#74d85d":"#579b49";for(let i=-1;i<=1;i+=2){ctx.beginPath();ctx.ellipse(i*7,-5,6,3,i*.5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(i*3,5,5,3,-i*.5,0,Math.PI*2);ctx.fill();}ctx.restore();\n    }else if(s.type==="koalaFuryBanner"){const q=1-Math.max(0,s.life)/(s.maxLife||.8);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle="#1f521e";ctx.fillStyle="#9cff78";ctx.lineWidth=3;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.strokeText("KOALA FURY!",0,-34-q*12);ctx.fillText("KOALA FURY!",0,-34-q*12);for(let i=0;i<7;i++){const a=i*.9+q*5,r=20+q*24;ctx.fillText("🍃",Math.cos(a)*r,Math.sin(a)*r);}ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Koala Branch Whack and Koala Fury')