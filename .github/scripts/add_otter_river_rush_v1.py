from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='OTTER_RIVER_RUSH_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='otter:{name:"Otter",emoji:"🦦",rarity:"Uncommon",cost:82,range:190,rate:1/1.25,dmg:18,color:"#986",desc:"Fast ranged attacker."},'
new='otter:{name:"Otter",emoji:"🦦",rarity:"Uncommon",cost:82,range:190,rate:1/1.25,dmg:18,color:"#986",desc:"Throws spinning pebbles with a splash. At Level 10, every 8th attack triggers River Rush: a huge wave hits every enemy in range for 1.5x current tower damage and pushes them back along the path."},'
if old not in s: raise RuntimeError('Otter card anchor not found')
s=s.replace(old,new,1)
anchor='  // BADGER_SAVAGE_MAUL_V1: Claw Swipe + Level 10 Savage Maul.\n'
if anchor not in s: anchor='  // DOG_FETCH_V1: Bark Blast + Level 10 Fetch bouncing bone.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // OTTER_RIVER_RUSH_V1: Pebble Toss + Level 10 River Rush.\n  if(t.key==="otter"){\n    let rush=false;if(t.level>=10){t.otterAttackCount=(t.otterAttackCount||0)+1;rush=t.otterAttackCount%8===0;}\n    if(rush){const hit=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);for(const e of hit){e.hp-=dmg*1.5;if(typeof e.progress==="number")e.progress=Math.max(0,e.progress-.035);else if(typeof e.pathProgress==="number")e.pathProgress=Math.max(0,e.pathProgress-.035);}battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.75,maxLife:.75,type:"riverRush",radius:range});}\n    else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-3,tx:target.x,ty:target.y,life:.32,maxLife:.32,type:"otterPebble",spin:Math.random()*6.28});}\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // BADGER_SAVAGE_MAUL_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // DOG_FETCH_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // OTTER_RIVER_RUSH_DRAW_V1\n    }else if(s.type==="otterPebble"){const q=1-Math.max(0,s.life)/(s.maxLife||.32),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*10);ctx.fillStyle="#858585";ctx.strokeStyle="#414141";ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(0,0,7,4,0,0,Math.PI*2);ctx.fill();ctx.stroke();if(q>.72){ctx.strokeStyle="#73d8ff";ctx.lineWidth=2;ctx.globalAlpha=(q-.72)/.28;for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(0,0,5+i*5,0,Math.PI*2);ctx.stroke();}}ctx.restore();\n    }else if(s.type==="riverRush"){const q=1-Math.max(0,s.life)/(s.maxLife||.75),r=(s.radius||190)*Math.min(1,q*1.3);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q*.75);ctx.strokeStyle="#55cfff";ctx.shadowColor="#25aee8";ctx.shadowBlur=14;ctx.lineWidth=12;ctx.beginPath();ctx.arc(0,0,r,-2.75,-.38);ctx.stroke();ctx.strokeStyle="#d9f7ff";ctx.lineWidth=4;ctx.beginPath();ctx.arc(0,0,Math.max(0,r-5),-2.75,-.38);ctx.stroke();ctx.fillStyle="#c9f5ff";ctx.strokeStyle="#124a68";ctx.lineWidth=3;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.strokeText("RIVER RUSH!",0,-32-q*15);ctx.fillText("RIVER RUSH!",0,-32-q*15);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Otter Pebble Toss and River Rush')