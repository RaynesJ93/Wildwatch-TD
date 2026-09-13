from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8'); marker='SNAIL_TOXIC_TRAIL_V1'
if marker in s: print('Already applied'); raise SystemExit(0)
old='snail:{name:"Snail",emoji:"🐌",rarity:"Common",cost:55,range:110,rate:1/.55,dmg:18,color:"#a87",desc:"Slow but heavy basic attacker."},'
new='snail:{name:"Snail",emoji:"🐌",rarity:"Common",cost:55,range:110,rate:1/.55,dmg:18,color:"#a87",desc:"Fires Acid Slime. At Level 10, every 6th attack creates Toxic Trail for 5s: enemies inside take 40% current tower damage each second and take 15% extra damage from other towers."},'
if old not in s: raise RuntimeError('Snail card anchor not found')
s=s.replace(old,new,1)
anchor='  // CROW_BLACKOUT_V1: Feather Dart + Level 10 Blackout.\n'
if anchor not in s: anchor='  // HEDGEHOG_QUILL_STORM_V1: Quill Shot + Level 10 Quill Storm.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // SNAIL_TOXIC_TRAIL_V1: Acid Slime + Level 10 Toxic Trail.\n  if(t.key==="snail"){\n    let toxic=false;if(t.level>=10){t.snailAttackCount=(t.snailAttackCount||0)+1;toxic=t.snailAttackCount%6===0;}\n    target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.38,maxLife:.38,type:"snailAcid",special:toxic});\n    if(toxic){battle.snailTrails=battle.snailTrails||[];battle.snailTrails.push({x:target.x,y:target.y,life:5,tick:1,damage:dmg*.4,radius:68});battle.shots.push({x:target.x,y:target.y,tx:target.x,ty:target.y,life:.75,maxLife:.75,type:"snailToxicBurst"});}\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
# Zone update and vulnerability timer. Damage amplification is applied in tower wrapper so it affects other tower damage.
upd_anchor='// CROW_BLACKOUT_UPDATE_V1'
if upd_anchor not in s: upd_anchor='// SKUNK_CLOUD_UPDATE_V2'
idx=s.find(upd_anchor)
if idx<0: raise RuntimeError('Zone update anchor not found')
ls=s.rfind('\n',0,idx)+1
upd='''// SNAIL_TOXIC_TRAIL_UPDATE_V1\n  if(battle.snailTrails){for(const c of battle.snailTrails){c.life-=dt;c.tick-=dt;for(const e of battle.enemies){if(!e.dead&&e.hp>0&&Math.hypot(e.x-c.x,e.y-c.y)<=c.radius)e.snailVulnerableTimer=Math.max(e.snailVulnerableTimer||0,.25);}if(c.tick<=0){c.tick+=1;for(const e of battle.enemies){if(!e.dead&&e.hp>0&&Math.hypot(e.x-c.x,e.y-c.y)<=c.radius)e.hp-=c.damage;}}}battle.snailTrails=battle.snailTrails.filter(c=>c.life>0);}\n  '''
s=s[:ls]+upd+s[ls:]
# Tick vulnerability timer near enemy speed/status code.
hook='if((e.crowSlowTimer||0)>0)'
if hook not in s: hook='if((e.zebraSlowTimer||0)>0)'
if hook in s: s=s.replace(hook,'if((e.snailVulnerableTimer||0)>0)e.snailVulnerableTimer=Math.max(0,e.snailVulnerableTimer-dt);\n    '+hook,1)
# Amplify damage caused by non-snail tower ticks by 15% using existing top-damage wrapper snapshot.
wrap='const dealt=Math.max(0,before-after);'
if wrap in s:
 s=s.replace(wrap,'let dealt=Math.max(0,before-after);\n  // SNAIL_TOXIC_VULNERABILITY_V1: other towers deal 15% extra damage to enemies standing in Toxic Trail.\n  if(t.key!=="snail"&&dealt>0){const victims=battle.enemies.filter(e=>!e.dead&&(e.snailVulnerableTimer||0)>0&&Math.hypot(e.x-t.x,e.y-t.y)<=cardRange(t.key));if(victims.length){const bonus=dealt*.15/victims.length;for(const e of victims)e.hp-=bonus;dealt*=1.15;}}',1)
# Draw acid projectile and toxic burst.
draw_anchor='    // CROW_BLACKOUT_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // CAT_SKUNK_PROJECTILE_DRAW_V2\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // SNAIL_TOXIC_TRAIL_DRAW_V1\n    }else if(s.type==="snailAcid"){const q=1-Math.max(0,s.life)/(s.maxLife||.38),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.fillStyle=s.special?"#c8ff32":"#7dff3b";ctx.shadowColor="#70ff28";ctx.shadowBlur=s.special?16:9;ctx.beginPath();ctx.arc(0,0,s.special?8:5,0,Math.PI*2);ctx.fill();ctx.restore();\n    }else if(s.type==="snailToxicBurst"){const q=1-Math.max(0,s.life)/(s.maxLife||.75);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#b6ff38";ctx.shadowColor="#65ff22";ctx.shadowBlur=18;ctx.font="bold 14px system-ui";ctx.textAlign="center";ctx.fillText("TOXIC TRAIL!",0,-27-q*10);for(let i=0;i<8;i++){const a=i*Math.PI/4,r=12+q*30;ctx.beginPath();ctx.arc(Math.cos(a)*r,Math.sin(a)*r*.6,4+(i%3),0,Math.PI*2);ctx.fill();}ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
shots='  battle.shots.forEach(s=>{'
if shots not in s: raise RuntimeError('Shots loop not found')
zone='''  // SNAIL_TOXIC_TRAIL_ZONE_DRAW_V1\n  if(battle.snailTrails){for(const c of battle.snailTrails){ctx.save();ctx.globalAlpha=Math.min(.62,c.life*.25);ctx.fillStyle="#6fbd24";ctx.shadowColor="#8dff35";ctx.shadowBlur=14;ctx.beginPath();ctx.ellipse(c.x,c.y,c.radius,c.radius*.55,0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#c5ff58";for(let i=0;i<10;i++){const a=i*2.3+c.life,r=8+(i%4)*12;ctx.beginPath();ctx.arc(c.x+Math.cos(a)*r,c.y+Math.sin(a)*r*.45,2+(i%3),0,Math.PI*2);ctx.fill();}ctx.restore();}}\n'''
s=s.replace(shots,zone+shots,1)
p.write_text(s,encoding='utf-8'); print('Added Snail Acid Slime and Toxic Trail')
