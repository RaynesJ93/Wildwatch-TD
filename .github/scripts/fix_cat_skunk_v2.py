from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# --- Card descriptions ---
cat_old='cat:{name:"Cat",emoji:"🐱",rarity:"Uncommon",cost:75,range:170,rate:1/1.30,dmg:17,color:"#d99",desc:"Fast balanced attacker."},'
cat_new='cat:{name:"Cat",emoji:"🐱",rarity:"Uncommon",cost:75,range:170,rate:1/1.30,dmg:17,color:"#d99",desc:"Fast Paw Slash attacker. At tower level 10, every 9th attack triggers Nine Lives: 9 rapid claw strikes dealing 50% current tower damage each across enemies in range."},'
if cat_old in s:s=s.replace(cat_old,cat_new,1)

sk_old='skunk:{name:"Skunk",emoji:"🦨",rarity:"Uncommon",cost:82,range:155,rate:1,dmg:21,color:"#eee",desc:"Solid mid-range attacker."},'
sk_new='skunk:{name:"Skunk",emoji:"🦨",rarity:"Uncommon",cost:82,range:155,rate:1,dmg:21,color:"#eee",desc:"Sprays a drifting stink cloud. At Level 10, every 5th attack becomes Stink Bomb: a toxic cloud lasts 4s, deals 40% base damage each second and slows enemies by 25%."},'
if sk_old in s:s=s.replace(sk_old,sk_new,1)

# --- Tower attacks ---
attack_anchor='  if(t.key==="raccoon"){\n'
if 'CAT_NINE_LIVES_V2' not in s:
    cat_block='''  // CAT_NINE_LIVES_V2\n  if(t.key==="cat"){\n    let nineLives=false;\n    if(t.level>=10){t.catAttackCount=(t.catAttackCount||0)+1;nineLives=t.catAttackCount%9===0;}\n    if(nineLives){\n      battle.shots.push({x:t.x,y:t.y-18,tx:t.x,ty:t.y-18,life:.60,maxLife:.60,type:"catNineLives"});\n      for(let i=0;i<9;i++){\n        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);\n        if(!pool.length)break;\n        const e=pool[i%pool.length];\n        e.hp-=dmg*.5;\n        battle.shots.push({x:t.x,y:t.y-6,tx:e.x,ty:e.y,life:.18+i*.035,maxLife:.18+i*.035,type:"catClaw",special:true,clawIndex:i});\n        if(e.hp<=0)killEnemy(e);\n      }\n    }else{\n      target.hp-=dmg;\n      battle.shots.push({x:t.x,y:t.y-6,tx:target.x,ty:target.y,life:.22,maxLife:.22,type:"catClaw",special:false});\n      if(target.hp<=0)killEnemy(target);\n    }\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
    if attack_anchor not in s:raise SystemExit('Attack anchor missing for cat')
    s=s.replace(attack_anchor,cat_block+attack_anchor,1)

if 'SKUNK_STINK_BOMB_V2' not in s:
    sk_block='''  // SKUNK_STINK_BOMB_V2\n  if(t.key==="skunk"){\n    let stinkBomb=false;\n    if(t.level>=10){t.skunkAttackCount=(t.skunkAttackCount||0)+1;stinkBomb=t.skunkAttackCount%5===0;}\n    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:stinkBomb?.56:.38,maxLife:stinkBomb?.56:.38,type:"skunkSpray",special:stinkBomb});\n    target.hp-=dmg;if(target.hp<=0)killEnemy(target);\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
    if attack_anchor not in s:raise SystemExit('Attack anchor missing for skunk')
    s=s.replace(attack_anchor,sk_block+attack_anchor,1)

# --- Skunk cloud lifecycle ---
if 'SKUNK_CLOUD_UPDATE_V2' not in s:
    anchor='  battle.trashZones=battle.trashZones.filter(z=>z.life>0);\n'
    add='''  // SKUNK_CLOUD_UPDATE_V2\n  battle.skunkCloudZones=battle.skunkCloudZones||[];\n  battle.skunkCloudZones.forEach(z=>{\n    z.life-=dt;z.tick=(z.tick??1)-dt;\n    if(z.life>0){\n      battle.enemies.forEach(e=>{if(!e.dead&&Math.hypot(e.x-z.x,e.y-z.y)<=z.radius)e.zebraSlowTimer=Math.max(e.zebraSlowTimer||0,.14);});\n      while(z.tick<=0){\n        battle.enemies.forEach(e=>{if(!e.dead&&Math.hypot(e.x-z.x,e.y-z.y)<=z.radius){e.hp-=z.damage;if(e.hp<=0)killEnemy(e);}});\n        z.tick+=1;\n      }\n    }\n  });\n  battle.skunkCloudZones=battle.skunkCloudZones.filter(z=>z.life>0);\n'''
    if anchor not in s:raise SystemExit('Trash zone anchor missing')
    s=s.replace(anchor,anchor+add,1)

if 'SKUNK_CLOUD_LANDING_V2' not in s:
    anchor='''    if(s.type==="raccoonBin" && s.special && !s.spilled && s.life-dt<=0){\n      s.spilled=true;\n      battle.trashZones=battle.trashZones||[];\n      battle.trashZones.push({x:s.tx,y:s.ty,life:4,maxLife:4,radius:90});\n    }\n'''
    add='''    // SKUNK_CLOUD_LANDING_V2\n    if(s.type==="skunkSpray" && s.special && !s.cloudMade && s.life-dt<=0){\n      s.cloudMade=true;\n      battle.skunkCloudZones=battle.skunkCloudZones||[];\n      battle.skunkCloudZones.push({x:s.tx,y:s.ty,life:4,maxLife:4,radius:92,damage:animals.skunk.dmg*.40,tick:1});\n    }\n'''
    if anchor not in s:raise SystemExit('Raccoon landing anchor missing')
    s=s.replace(anchor,anchor+add,1)

# --- Draw lingering stink cloud before traps/projectiles ---
if 'SKUNK_CLOUD_DRAW_V2' not in s:
    anchor='  battle.needles?.forEach(n=>{\n'
    add='''  // SKUNK_CLOUD_DRAW_V2\n  (battle.skunkCloudZones||[]).forEach(z=>{\n    const a=Math.max(.15,Math.min(.62,z.life/z.maxLife*.62)),pulse=1+Math.sin(performance.now()/170)*.05;\n    ctx.save();ctx.globalAlpha=a;ctx.translate(z.x,z.y);ctx.scale(pulse,pulse);\n    ctx.fillStyle="#8fcb3d";ctx.strokeStyle="#d9ff7b";ctx.lineWidth=3;ctx.shadowColor="#9ee85a";ctx.shadowBlur=14;\n    ctx.beginPath();ctx.ellipse(0,0,z.radius,z.radius*.58,0,0,Math.PI*2);ctx.fill();ctx.stroke();\n    ctx.fillStyle="#b8e85b";[[-38,-10,22],[0,5,30],[35,-6,19],[-12,23,16],[28,22,13]].forEach(([x,y,r])=>{ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();});\n    ctx.restore();\n  });\n'''
    if anchor not in s:raise SystemExit('Needles draw anchor missing')
    s=s.replace(anchor,add+anchor,1)

# --- Projectile renderers ---
if 'CAT_SKUNK_PROJECTILE_DRAW_V2' not in s:
    anchor='    }else if(s.type==="raccoonBin"){\n'
    add='''    // CAT_SKUNK_PROJECTILE_DRAW_V2\n    }else if(s.type==="catClaw"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.22),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);\n      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.strokeStyle=s.special?"#ffe889":"#fff";ctx.shadowColor=s.special?"#ffd64a":"#fff";ctx.shadowBlur=s.special?10:4;ctx.lineWidth=s.special?3.2:2.4;ctx.lineCap="round";\n      for(let i=-1;i<=1;i++){ctx.beginPath();ctx.moveTo(-13,i*5-4);ctx.quadraticCurveTo(0,i*5+5,13,i*5-2);ctx.stroke();}ctx.restore();\n    }else if(s.type==="catNineLives"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.60);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.shadowColor="#ffd64a";ctx.shadowBlur=14;ctx.fillStyle="#ffe98a";ctx.font="bold 16px system-ui";ctx.textAlign="center";ctx.fillText("9 LIVES!",0,-25-q*12);ctx.font="18px serif";for(let i=0;i<5;i++){const a=i*Math.PI*2/5+q;ctx.fillText("🐾",Math.cos(a)*(22+q*12),Math.sin(a)*(15+q*8));}ctx.restore();\n    }else if(s.type==="skunkSpray"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.38),ex=s.x+(s.tx-s.x)*q,ey=s.y+(s.ty-s.y)*q,dx=ex-s.x,dy=ey-s.y,len=Math.hypot(dx,dy)||1,nx=-dy/len,ny=dx/len,spread=s.special?24:15;\n      ctx.save();ctx.globalAlpha=s.special?.9:.72;ctx.fillStyle=s.special?"#a8e94d":"#8fcd42";ctx.shadowColor="#a8f45a";ctx.shadowBlur=s.special?18:10;ctx.beginPath();ctx.moveTo(s.x+nx*4,s.y+ny*4);ctx.lineTo(ex+nx*spread,ey+ny*spread);ctx.quadraticCurveTo(ex+dx*.08,ey+dy*.08,ex-nx*spread,ey-ny*spread);ctx.lineTo(s.x-nx*4,s.y-ny*4);ctx.closePath();ctx.fill();ctx.fillStyle="#ddff7f";for(let i=0;i<(s.special?9:6);i++){const qq=Math.max(0,q-i*.055),px=s.x+(s.tx-s.x)*qq,py=s.y+(s.ty-s.y)*qq,off=Math.sin(i*2.4+q*12)*(s.special?14:8);ctx.beginPath();ctx.arc(px+nx*off,py+ny*off,2.5+(i%3),0,Math.PI*2);ctx.fill();}ctx.restore();\n'''
    if anchor not in s:raise SystemExit('Projectile renderer anchor missing')
    s=s.replace(anchor,add+anchor,1)

p.write_text(s,encoding='utf-8')
print('Cat + Skunk V2 patch applied')
