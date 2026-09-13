from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CROW_BLACKOUT_V1'
if marker in s:
 print('Already applied'); raise SystemExit(0)
old='crow:{name:"Crow",emoji:"🐦‍⬛",rarity:"Common",cost:62,range:195,rate:1/1.15,dmg:12,color:"#222",desc:"Long-range basic attacker."},'
new='crow:{name:"Crow",emoji:"🐦‍⬛",rarity:"Common",cost:62,range:195,rate:1/1.15,dmg:12,color:"#222",desc:"Fires spinning Feather Darts. At Level 10, every 8th attack creates Blackout for 4s: enemies in the dark cloud take 40% current tower damage each second and are slowed by 25%."},'
if old not in s: raise RuntimeError('Crow card anchor not found')
s=s.replace(old,new,1)
anchor='  // GOOSE_ANGRY_GOOSE_V1: Honk Blast + Level 10 Angry Goose.\n'
if anchor not in s: anchor='  // HEDGEHOG_QUILL_STORM_V1: Quill Shot + Level 10 Quill Storm.\n'
if anchor not in s: raise RuntimeError('Attack insertion anchor not found')
attack='''  // CROW_BLACKOUT_V1: Feather Dart + Level 10 Blackout.\n  if(t.key==="crow"){\n    let blackout=false;\n    if(t.level>=10){t.crowAttackCount=(t.crowAttackCount||0)+1;blackout=t.crowAttackCount%8===0;}\n    target.hp-=dmg;\n    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.28,maxLife:.28,type:"crowFeather",special:blackout});\n    if(blackout){\n      battle.crowClouds=battle.crowClouds||[];\n      battle.crowClouds.push({x:target.x,y:target.y,life:4,tick:1,damage:dmg*.4,radius:72});\n      battle.shots.push({x:target.x,y:target.y,tx:target.x,ty:target.y,life:.8,maxLife:.8,type:"crowBlackoutBurst"});\n    }\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
# Update lingering clouds in battle update near skunk clouds if available.
update_anchor='// SKUNK_CLOUD_UPDATE_V2'
idx=s.find(update_anchor)
if idx<0: raise RuntimeError('Cloud update anchor not found')
line_start=s.rfind('\n',0,idx)+1
cloud_update='''// CROW_BLACKOUT_UPDATE_V1\n  if(battle.crowClouds){for(const c of battle.crowClouds){c.life-=dt;c.tick-=dt;if(c.tick<=0){c.tick+=1;for(const e of battle.enemies){if(!e.dead&&e.hp>0&&Math.hypot(e.x-c.x,e.y-c.y)<=c.radius){e.hp-=c.damage;e.crowSlowTimer=Math.max(e.crowSlowTimer||0,1.05);}}}}battle.crowClouds=battle.crowClouds.filter(c=>c.life>0);}\n  '''
s=s[:line_start]+cloud_update+s[line_start:]
# Apply 25% slow using existing enemy speed calculation hook.
slow='if((e.crowSlowTimer||0)>0){e.crowSlowTimer=Math.max(0,e.crowSlowTimer-dt);speed*=.75;}\n    '
for hook in ['if((e.gooseSlowTimer||0)>0)','if((e.zebraSlowTimer||0)>0)']:
 if hook in s:
  s=s.replace(hook,slow+hook,1); break
# Draw projectile/cloud using existing projectile chain.
draw_anchor='    // GOOSE_ANGRY_GOOSE_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // CAT_SKUNK_PROJECTILE_DRAW_V2\n'
if draw_anchor not in s: raise RuntimeError('Projectile draw anchor not found')
draw='''    // CROW_BLACKOUT_DRAW_V1\n    }else if(s.type==="crowFeather"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.28),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x)+q*9;ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.strokeStyle=s.special?"#9b6cff":"#17131d";ctx.fillStyle=s.special?"#5d35a8":"#27212d";ctx.shadowColor=s.special?"#8e5cff":"#000";ctx.shadowBlur=s.special?12:5;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-11,0);ctx.quadraticCurveTo(0,-7,12,0);ctx.quadraticCurveTo(0,7,-11,0);ctx.fill();ctx.beginPath();ctx.moveTo(-10,0);ctx.lineTo(12,0);ctx.stroke();ctx.restore();\n    }else if(s.type==="crowBlackoutBurst"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.8);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#17101f";ctx.shadowColor="#6f43a8";ctx.shadowBlur=18;for(let i=0;i<9;i++){const a=i*2.4+q*4,r=12+(i%4)*7+q*20;ctx.beginPath();ctx.arc(Math.cos(a)*r,Math.sin(a)*r*.55,8+(i%3)*3,0,Math.PI*2);ctx.fill();}ctx.fillStyle="#b995ff";ctx.font="bold 14px system-ui";ctx.textAlign="center";ctx.fillText("BLACKOUT!",0,-30-q*10);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
# Draw persistent Blackout zones before shots so projectiles remain visible.
shots_anchor='  battle.shots.forEach(s=>{'
if shots_anchor not in s: raise RuntimeError('Shots draw loop anchor not found')
zone='''  // CROW_BLACKOUT_ZONE_DRAW_V1\n  if(battle.crowClouds){for(const c of battle.crowClouds){ctx.save();const pulse=.82+.12*Math.sin(performance.now()/180);ctx.globalAlpha=Math.min(.58,c.life*.3);ctx.fillStyle="#130f19";ctx.shadowColor="#4e326a";ctx.shadowBlur=18;ctx.beginPath();ctx.arc(c.x,c.y,c.radius*pulse,0,Math.PI*2);ctx.fill();ctx.fillStyle="#28202f";for(let i=0;i<8;i++){const a=i*2.1+c.life,r=(i%3)*16+12;ctx.beginPath();ctx.arc(c.x+Math.cos(a)*r,c.y+Math.sin(a)*r*.55,9+(i%2)*5,0,Math.PI*2);ctx.fill();}ctx.restore();}}\n'''
s=s.replace(shots_anchor,zone+shots_anchor,1)
p.write_text(s,encoding='utf-8')
print('Added Crow Feather Dart and Blackout')
