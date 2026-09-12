from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = 'SKUNK_STINK_BOMB_V1'
if marker in s:
    print('Skunk Stink Bomb already installed')
    raise SystemExit(0)

old = 'skunk:{name:"Skunk",emoji:"🦨",rarity:"Uncommon",cost:82,range:155,rate:1,dmg:21,color:"#eee",desc:"Solid mid-range attacker."},'
new = 'skunk:{name:"Skunk",emoji:"🦨",rarity:"Uncommon",cost:82,range:155,rate:1,dmg:21,color:"#eee",desc:"Sprays a drifting stink cloud at enemies. At Level 10, every 5th attack becomes Stink Bomb: a toxic cloud lingers for 4s, deals 40% base damage each second and slows enemies by 25%."},'
assert old in s, 'Skunk card definition not found'
s = s.replace(old, new, 1)

old = '  if((e.zebraSlowTimer||0)>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);\n  if((e.goatConfuseTimer||0)>0)e.goatConfuseTimer=Math.max(0,e.goatConfuseTimer-dt);'
new = '  if((e.zebraSlowTimer||0)>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);\n  if((e.skunkSlowTimer||0)>0)e.skunkSlowTimer=Math.max(0,e.skunkSlowTimer-dt);\n  if((e.goatConfuseTimer||0)>0)e.goatConfuseTimer=Math.max(0,e.goatConfuseTimer-dt);'
assert old in s, 'Enemy slow timer section not found'
s = s.replace(old, new, 1)

old = '  let mult=e.slowTimer>0?.55:(e.zebraSlowTimer||0)>0?.75:(e.goatConfuseTimer||0)>0?.50:1, dist=e.speed*mult*dt;'
new = '  let mult=e.slowTimer>0?.55:(e.zebraSlowTimer||0)>0?.75:(e.skunkSlowTimer||0)>0?.75:(e.goatConfuseTimer||0)>0?.50:1, dist=e.speed*mult*dt;'
assert old in s, 'Enemy speed multiplier not found'
s = s.replace(old, new, 1)

anchor = '  if(t.key==="raccoon"){\n'
insert = '''  // SKUNK_STINK_BOMB_V1: normal spray plus Level 10 every-5th lingering toxic cloud.\n  if(t.key==="skunk"){\n    let stinkBomb=false;\n    if(t.level>=10){\n      t.skunkAttackCount=(t.skunkAttackCount||0)+1;\n      stinkBomb=t.skunkAttackCount%5===0;\n    }\n    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:stinkBomb?.56:.38,maxLife:stinkBomb?.56:.38,type:"skunkSpray",special:stinkBomb});\n    target.hp-=dmg;\n    if(target.hp<=0)killEnemy(target);\n    t.cd=cardRate(t.key);\n    return;\n  }\n\n'''
assert anchor in s, 'Raccoon tower block anchor not found'
s = s.replace(anchor, insert + anchor, 1)

old = '''  battle.trashZones=battle.trashZones.filter(z=>z.life>0);\n  battle.roars=battle.roars||[];'''
new = '''  battle.trashZones=battle.trashZones.filter(z=>z.life>0);\n\n  // SKUNK_STINK_BOMB_V1 toxic zones.\n  battle.skunkCloudZones=battle.skunkCloudZones||[];\n  battle.skunkCloudZones.forEach(z=>{\n    z.life-=dt;\n    z.tick=(z.tick??1)-dt;\n    if(z.life>0){\n      battle.enemies.forEach(e=>{\n        if(!e.dead && Math.hypot(e.x-z.x,e.y-z.y)<=z.radius){\n          e.skunkSlowTimer=Math.max(e.skunkSlowTimer||0,.14);\n        }\n      });\n      while(z.tick<=0){\n        battle.enemies.forEach(e=>{\n          if(e.dead || Math.hypot(e.x-z.x,e.y-z.y)>z.radius)return;\n          e.hp-=z.damage;\n          if(e.hp<=0)killEnemy(e);\n        });\n        z.tick+=1;\n      }\n    }\n  });\n  battle.skunkCloudZones=battle.skunkCloudZones.filter(z=>z.life>0);\n  battle.roars=battle.roars||[];'''
assert old in s, 'Trash-zone update anchor not found'
s = s.replace(old, new, 1)

old = '''    if(s.type==="raccoonBin" && s.special && !s.spilled && s.life-dt<=0){\n      s.spilled=true;\n      battle.trashZones=battle.trashZones||[];\n      battle.trashZones.push({x:s.tx,y:s.ty,life:4,maxLife:4,radius:90});\n    }'''
new = '''    if(s.type==="raccoonBin" && s.special && !s.spilled && s.life-dt<=0){\n      s.spilled=true;\n      battle.trashZones=battle.trashZones||[];\n      battle.trashZones.push({x:s.tx,y:s.ty,life:4,maxLife:4,radius:90});\n    }\n    if(s.type==="skunkSpray" && s.special && !s.cloudMade && s.life-dt<=0){\n      s.cloudMade=true;\n      battle.skunkCloudZones=battle.skunkCloudZones||[];\n      battle.skunkCloudZones.push({x:s.tx,y:s.ty,life:4,maxLife:4,radius:92,damage:animals.skunk.dmg*.40,tick:1});\n    }'''
assert old in s, 'Shot landing anchor not found'
s = s.replace(old, new, 1)

old = '''  // Free-placement mode: no fixed tower pads are shown.\n  ctx.textAlign="center";ctx.textBaseline="middle";'''
new = '''  // SKUNK_STINK_BOMB_V1 lingering toxic clouds.\n  (battle.skunkCloudZones||[]).forEach(z=>{\n    const a=Math.max(.12,Math.min(.62,z.life/z.maxLife*.62));\n    const pulse=1+Math.sin(performance.now()/170)*.06;\n    ctx.save();ctx.globalAlpha=a;ctx.translate(z.x,z.y);ctx.scale(pulse,pulse);\n    ctx.fillStyle="#8ccf35";ctx.strokeStyle="#d7ff72";ctx.lineWidth=3;\n    ctx.shadowColor="rgba(130,230,60,.55)";ctx.shadowBlur=14;\n    ctx.beginPath();ctx.ellipse(0,0,z.radius,z.radius*.58,0,0,Math.PI*2);ctx.fill();ctx.stroke();\n    ctx.fillStyle="#b8e85b";ctx.globalAlpha=a*.75;\n    [[-38,-12,22],[0,5,30],[35,-7,19],[-12,23,16],[28,22,13]].forEach(([x,y,r])=>{ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();});\n    ctx.globalAlpha=Math.min(.9,a+0.18);ctx.fillStyle="#e6ff9b";ctx.font="bold 20px system-ui";ctx.textAlign="center";ctx.fillText("☁",-25,-22);ctx.fillText("☁",18,-30);\n    ctx.restore();\n  });\n\n  // Free-placement mode: no fixed tower pads are shown.\n  ctx.textAlign="center";ctx.textBaseline="middle";'''
assert old in s, 'Battlefield draw anchor not found'
s = s.replace(old, new, 1)

old = '''    }else if(s.type==="raccoonBin"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.48);'''
new = '''    }else if(s.type==="skunkSpray"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.38);\n      const sx=s.x,sy=s.y,ex=s.x+(s.tx-s.x)*q,ey=s.y+(s.ty-s.y)*q;\n      const dx=ex-sx,dy=ey-sy,len=Math.hypot(dx,dy)||1,nx=-dy/len,ny=dx/len;\n      const spread=s.special?24:15;\n      ctx.save();ctx.globalAlpha=s.special?.88:.72;ctx.fillStyle=s.special?"#a6e84b":"#8fcd42";\n      ctx.shadowColor="#a8f45a";ctx.shadowBlur=s.special?18:10;\n      ctx.beginPath();ctx.moveTo(sx+nx*4,sy+ny*4);ctx.lineTo(ex+nx*spread,ey+ny*spread);ctx.quadraticCurveTo(ex+dx*.08,ey+dy*.08,ex-nx*spread,ey-ny*spread);ctx.lineTo(sx-nx*4,sy-ny*4);ctx.closePath();ctx.fill();\n      ctx.globalAlpha=s.special?.95:.78;ctx.fillStyle="#d9ff79";\n      for(let i=0;i<(s.special?9:6);i++){const qq=Math.max(0,q-i*.055),px=s.x+(s.tx-s.x)*qq,py=s.y+(s.ty-s.y)*qq,off=Math.sin(i*2.4+q*12)*(s.special?14:8);ctx.beginPath();ctx.arc(px+nx*off,py+ny*off,2.5+(i%3)*1.2,0,Math.PI*2);ctx.fill();}\n      ctx.restore();\n    }else if(s.type==="raccoonBin"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.48);'''
assert old in s, 'Projectile draw anchor not found'
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Installed SKUNK_STINK_BOMB_V1')
