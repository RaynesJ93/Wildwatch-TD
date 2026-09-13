from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='BADGER_SAVAGE_MAUL_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='badger:{name:"Badger",emoji:"🦡",rarity:"Uncommon",cost:88,range:140,rate:1/.85,dmg:26,color:"#777",desc:"Hard-hitting close attacker."},'
new='badger:{name:"Badger",emoji:"🦡",rarity:"Uncommon",cost:88,range:140,rate:1/.85,dmg:26,color:"#777",desc:"Attacks with heavy Claw Swipes. At Level 10, every 5th attack triggers Savage Maul: 3 rapid strikes dealing 100%, 100% and 150% current tower damage, retargeting if an enemy is defeated."},'
if old not in s: raise RuntimeError('Badger card anchor not found')
s=s.replace(old,new,1)
anchor='  // DOG_FETCH_V1: Bark Blast + Level 10 Fetch bouncing bone.\n'
if anchor not in s: anchor='  // WORM_MUD_SHOT_V1: sludge/mud projectile attack.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // BADGER_SAVAGE_MAUL_V1: Claw Swipe + Level 10 Savage Maul.\n  if(t.key==="badger"){\n    let maul=false;if(t.level>=10){t.badgerAttackCount=(t.badgerAttackCount||0)+1;maul=t.badgerAttackCount%5===0;}\n    if(maul){const mult=[1,1,1.5];let cur=target;for(let i=0;i<3;i++){if(!cur||cur.dead||cur.hp<=0||Math.hypot(cur.x-t.x,cur.y-t.y)>range){cur=battle.enemies.find(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);}if(!cur)break;cur.hp-=dmg*mult[i];battle.shots.push({x:t.x,y:t.y,tx:cur.x,ty:cur.y,life:.25+i*.09,maxLife:.25+i*.09,type:"badgerMaul",hit:i});}battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.65,maxLife:.65,type:"savageMaulBanner"});}\n    else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:.24,maxLife:.24,type:"badgerClaw",hit:0});}\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // DOG_FETCH_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // WORM_STAMPEDE_DRAW_V1\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // BADGER_SAVAGE_MAUL_DRAW_V1\n    }else if(s.type==="badgerClaw"||s.type==="badgerMaul"){const q=1-Math.max(0,s.life)/(s.maxLife||.24),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,a=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.globalAlpha=Math.max(0,1-q*.55);ctx.strokeStyle=s.type==="badgerMaul"?"#ff765f":"#e7e7e7";ctx.shadowColor=s.type==="badgerMaul"?"#ff3c2e":"#ffffff";ctx.shadowBlur=s.type==="badgerMaul"?10:5;ctx.lineWidth=s.type==="badgerMaul"?3.5:2.5;for(let i=-1;i<=1;i++){ctx.beginPath();ctx.moveTo(-10,i*5-6);ctx.quadraticCurveTo(0,i*5,11,i*5+6);ctx.stroke();}ctx.restore();\n    }else if(s.type==="savageMaulBanner"){const q=1-Math.max(0,s.life)/(s.maxLife||.65);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#ff8b72";ctx.strokeStyle="#431a15";ctx.lineWidth=3;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.strokeText("SAVAGE MAUL!",0,-31-q*12);ctx.fillText("SAVAGE MAUL!",0,-31-q*12);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Badger Claw Swipe and Savage Maul')