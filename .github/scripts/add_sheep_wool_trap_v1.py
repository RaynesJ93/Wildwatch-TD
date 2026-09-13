from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='SHEEP_WOOL_TRAP_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='sheep:{name:"Sheep",emoji:"🐑",rarity:"Uncommon",cost:82,range:155,rate:1,dmg:21,color:"#eee",desc:"Balanced attacker."},'
new='sheep:{name:"Sheep",emoji:"🐑",rarity:"Uncommon",cost:82,range:155,rate:1,dmg:21,color:"#eee",desc:"Fires fluffy spinning Wool Balls. At Level 10, every 6th attack creates a Wool Trap for 5s: enemies inside are slowed by 50% and take 40% current tower damage each second."},'
if old not in s: raise RuntimeError('Sheep card anchor not found')
s=s.replace(old,new,1)
anchor='  // KOALA_FURY_V1: Branch Whack + Level 10 Koala Fury.\n'
if anchor not in s: anchor='  // SLOTH_STICK_THROW_V1: spinning stick projectile attack.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // SHEEP_WOOL_TRAP_V1: Wool Ball + Level 10 Wool Trap.\n  if(t.key==="sheep"){let trap=false;if(t.level>=10){t.sheepAttackCount=(t.sheepAttackCount||0)+1;trap=t.sheepAttackCount%6===0;}if(trap){battle.woolTraps=battle.woolTraps||[];battle.woolTraps.push({x:target.x,y:target.y,r:62,life:5,tick:0,dmg:dmg*.40});battle.shots.push({x:target.x,y:target.y,tx:target.x,ty:target.y,life:.8,maxLife:.8,type:"woolTrapBanner"});}else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-2,tx:target.x,ty:target.y,life:.34,maxLife:.34,type:"woolBall",spin:Math.random()*6.28});}t.cd=cardRate(t.key);return;}\n\n'''
s=s.replace(anchor,attack+anchor,1)
update_anchor='battle.shots=battle.shots.filter(s=>s.life>0);'
if update_anchor not in s: raise RuntimeError('Shot update anchor not found')
update='''// SHEEP_WOOL_TRAP_UPDATE_V1\n  battle.woolTraps=battle.woolTraps||[];for(const z of battle.woolTraps){z.life-=dt;z.tick=(z.tick||0)+dt;if(z.tick>=1){const ticks=Math.floor(z.tick);z.tick-=ticks;for(const e of battle.enemies){if(!e.dead&&e.hp>0&&Math.hypot(e.x-z.x,e.y-z.y)<=z.r)e.hp-=z.dmg*ticks;}}}battle.woolTraps=battle.woolTraps.filter(z=>z.life>0);\n  '''
s=s.replace(update_anchor,update+update_anchor,1)
slow_candidates=['if((e.slothSlowTimer||0)>0)','if((e.cricketSlowTimer||0)>0)','if((e.zebraSlowTimer||0)>0)']
for a in slow_candidates:
    if a in s:
        s=s.replace(a,'if((battle.woolTraps||[]).some(z=>z.life>0&&Math.hypot(e.x-z.x,e.y-z.y)<=z.r))speed*=.50;\n      '+a,1);break
else: raise RuntimeError('Enemy movement slow anchor not found')
draw_anchor='    // KOALA_FURY_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // SLOTH_TREE_TOPPLE_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // SHEEP_WOOL_TRAP_DRAW_V1\n    }else if(s.type==="woolBall"){const q=1-Math.max(0,s.life)/(s.maxLife||.34),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*9);ctx.fillStyle="#fff";ctx.strokeStyle="#c9d2d6";ctx.lineWidth=2;for(let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.arc(Math.cos(a)*5,Math.sin(a)*5,6,0,Math.PI*2);ctx.fill();ctx.stroke();}ctx.restore();\n    }else if(s.type==="woolTrapBanner"){const q=1-Math.max(0,s.life)/(s.maxLife||.8);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#fff";ctx.strokeStyle="#59656b";ctx.lineWidth=3;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.strokeText("WOOL TRAP!",0,-34-q*12);ctx.fillText("WOOL TRAP!",0,-34-q*12);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
zone_anchor='  battle.shots?.forEach(s=>{'
if zone_anchor not in s: raise RuntimeError('Shot draw loop anchor not found')
zone='''  // SHEEP_WOOL_TRAP_ZONE_DRAW_V1\n  for(const z of (battle.woolTraps||[])){ctx.save();ctx.globalAlpha=Math.min(.75,z.life);ctx.fillStyle="#f5f5f2";ctx.strokeStyle="#d5dde0";ctx.lineWidth=3;ctx.beginPath();ctx.arc(z.x,z.y,z.r,0,Math.PI*2);ctx.fill();ctx.stroke();for(let i=0;i<11;i++){const a=i*2.399,r=(i%4)*13+8;ctx.fillStyle="#fff";ctx.beginPath();ctx.arc(z.x+Math.cos(a)*r,z.y+Math.sin(a)*r,8+(i%3),0,Math.PI*2);ctx.fill();}ctx.restore();}\n'''
s=s.replace(zone_anchor,zone+zone_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Sheep Wool Ball and Wool Trap')