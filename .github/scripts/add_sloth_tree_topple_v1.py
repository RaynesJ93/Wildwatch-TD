from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='SLOTH_TREE_TOPPLE_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='sloth:{name:"Sloth",emoji:"🦥",rarity:"Uncommon",cost:92,range:150,rate:1/.60,dmg:34,color:"#876",desc:"Slow heavy attacker that throws spinning sticks at enemies."},'
new='sloth:{name:"Sloth",emoji:"🦥",rarity:"Uncommon",cost:92,range:150,rate:1/.60,dmg:34,color:"#876",desc:"Throws spinning sticks. At Level 10, every 8th attack triggers Tree Topple: a whole tree crashes across the path, dealing 2x current tower damage to enemies in range and slowing them by 30% for 3s."},'
if old not in s: raise RuntimeError('Updated Sloth card anchor not found')
s=s.replace(old,new,1)
old_attack='''  // SLOTH_STICK_THROW_V1: spinning stick projectile attack.\n  if(t.key==="sloth"){target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.38,maxLife:.38,type:"slothStick",spin:Math.random()*6.28});t.cd=cardRate(t.key);return;}'''
new_attack='''  // SLOTH_STICK_THROW_V1: spinning stick projectile attack.\n  // SLOTH_TREE_TOPPLE_V1: Level 10 every 8th attack drops a tree across enemies in range.\n  if(t.key==="sloth"){let topple=false;if(t.level>=10){t.slothAttackCount=(t.slothAttackCount||0)+1;topple=t.slothAttackCount%8===0;}if(topple){const hit=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);for(const e of hit){e.hp-=dmg*2;e.slothSlowTimer=Math.max(e.slothSlowTimer||0,3);}battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:.9,maxLife:.9,type:"treeTopple",radius:range});}else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.38,maxLife:.38,type:"slothStick",spin:Math.random()*6.28});}t.cd=cardRate(t.key);return;}'''
if old_attack not in s: raise RuntimeError('Sloth attack anchor not found')
s=s.replace(old_attack,new_attack,1)
# integrate slow beside a known enemy slow timer update if possible
slow_candidates=['if((e.cricketSlowTimer||0)>0)','if((e.zebraSlowTimer||0)>0)','if((e.crowSlowTimer||0)>0)']
for a in slow_candidates:
    if a in s:
        s=s.replace(a,'if((e.slothSlowTimer||0)>0){e.slothSlowTimer=Math.max(0,e.slothSlowTimer-dt);speed*=.70;}\n      '+a,1);break
else: raise RuntimeError('Enemy slow integration anchor not found')
draw_anchor='    // SLOTH_STICK_THROW_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Sloth draw anchor not found')
draw='''    // SLOTH_TREE_TOPPLE_DRAW_V1\n    }else if(s.type==="treeTopple"){const q=1-Math.max(0,s.life)/(s.maxLife||.9),x=s.tx,y=s.ty;ctx.save();ctx.translate(x,y);const fall=Math.min(1,q*2.2),ang=-1.35+fall*1.35;ctx.rotate(ang);ctx.globalAlpha=Math.max(.25,1-Math.max(0,q-.72)*3.2);ctx.strokeStyle="#6b3f1f";ctx.lineWidth=15;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-65,0);ctx.lineTo(58,0);ctx.stroke();ctx.strokeStyle="#9b6333";ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-58,-3);ctx.lineTo(50,-3);ctx.stroke();ctx.fillStyle="#3f7f3e";for(let i=0;i<7;i++){const px=-45+i*17,py=(i%2?8:-9);ctx.beginPath();ctx.arc(px,py,12,0,Math.PI*2);ctx.fill();}ctx.restore();ctx.save();ctx.translate(x,y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#dff7b0";ctx.strokeStyle="#2b4b20";ctx.lineWidth=3;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.strokeText("TREE TOPPLE!",0,-38-q*12);ctx.fillText("TREE TOPPLE!",0,-38-q*12);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Sloth Tree Topple')