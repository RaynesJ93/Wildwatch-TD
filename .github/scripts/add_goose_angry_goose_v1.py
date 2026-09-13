from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='GOOSE_ANGRY_GOOSE_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old='goose:{name:"Goose",emoji:"🪿",rarity:"Common",cost:62,range:155,rate:1/.95,dmg:20,color:"#ddd",desc:"Strong basic attacker."},'
new='goose:{name:"Goose",emoji:"🪿",rarity:"Common",cost:62,range:155,rate:1/.95,dmg:20,color:"#ddd",desc:"Fires cone-shaped Honk Blasts. At Level 10, every 7th attack triggers Angry Goose for 4s: 75% faster attacks hit up to 3 enemies for 100% current damage and slow them by 15% for 1s."},'
if old not in s: raise RuntimeError('Goose card anchor not found')
s=s.replace(old,new,1)
anchor='  // HEDGEHOG_QUILL_STORM_V1: Quill Shot + Level 10 Quill Storm.\n'
if anchor not in s: raise RuntimeError('Hedgehog attack anchor not found')
attack='''  // GOOSE_ANGRY_GOOSE_V1: Honk Blast + Level 10 Angry Goose.\n  if(t.key==="goose"){\n    if(t.level>=10){t.gooseAttackCount=(t.gooseAttackCount||0)+1;if(t.gooseAttackCount%7===0){t.gooseRage=4;battle.shots.push({x:t.x,y:t.y-10,tx:t.x,ty:t.y-10,life:.75,maxLife:.75,type:"gooseRageBurst"});}}\n    const raging=(t.gooseRage||0)>0;\n    if(raging)t.gooseRage=Math.max(0,t.gooseRage-dt);\n    const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range).sort((a,b)=>Math.hypot(a.x-target.x,a.y-target.y)-Math.hypot(b.x-target.x,b.y-target.y));\n    const hits=raging?pool.slice(0,3):[target];\n    hits.forEach((e,i)=>{e.hp-=dmg;if(raging){e.gooseSlowTimer=Math.max(e.gooseSlowTimer||0,1);e.gooseSlow=.15;}battle.shots.push({x:t.x,y:t.y-8,tx:e.x,ty:e.y,life:.26,maxLife:.26,type:"gooseHonk",special:raging,offset:i});});\n    t.cd=cardRate(t.key)/(raging?1.75:1);\n    return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
draw_anchor='    // CAT_SKUNK_PROJECTILE_DRAW_V2\n'
if draw_anchor not in s: raise RuntimeError('Projectile draw anchor not found')
draw='''    // GOOSE_ANGRY_GOOSE_DRAW_V1\n    }else if(s.type==="gooseHonk"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.26),ang=Math.atan2(s.ty-s.y,s.tx-s.x),dist=Math.hypot(s.tx-s.x,s.ty-s.y);ctx.save();ctx.translate(s.x,s.y);ctx.rotate(ang);ctx.strokeStyle=s.special?"#ffb347":"#e8f6ff";ctx.shadowColor=s.special?"#ff7a22":"#bdeaff";ctx.shadowBlur=s.special?14:7;ctx.lineWidth=s.special?4:3;ctx.globalAlpha=Math.max(.2,1-q);for(let i=0;i<3;i++){const r=Math.min(dist,(q*dist)+i*13);ctx.beginPath();ctx.arc(0,0,r,-.42,.42);ctx.stroke();}ctx.restore();\n    }else if(s.type==="gooseRageBurst"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.75);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#ffb347";ctx.shadowColor="#ff542e";ctx.shadowBlur=16;ctx.font="bold 15px system-ui";ctx.textAlign="center";ctx.fillText("ANGRY GOOSE!",0,-26-q*14);ctx.strokeStyle="#ff6b35";ctx.lineWidth=4;ctx.beginPath();ctx.arc(0,0,18+q*20,0,Math.PI*2);ctx.stroke();ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
# Integrate temporary Goose slow into enemy speed where zebra slow is already processed.
slow_anchor='if((e.zebraSlowTimer||0)>0)'
if slow_anchor in s:
    s=s.replace(slow_anchor,'if((e.gooseSlowTimer||0)>0){e.gooseSlowTimer=Math.max(0,e.gooseSlowTimer-dt);speed*=.85;}\n    '+slow_anchor,1)
p.write_text(s,encoding='utf-8')
print('Added Goose Honk Blast and Angry Goose')
