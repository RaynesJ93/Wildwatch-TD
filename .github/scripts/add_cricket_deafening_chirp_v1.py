from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8');marker='CRICKET_DEAFENING_CHIRP_V1'
if marker in s: print('Already applied');raise SystemExit(0)
old='cricket:{name:"Cricket",emoji:"🦗",rarity:"Common",cost:48,range:145,rate:1/1.45,dmg:8,color:"#697",desc:"Very fast basic attacker."},'
new='cricket:{name:"Cricket",emoji:"🦗",rarity:"Common",cost:48,range:145,rate:1/1.45,dmg:8,color:"#697",desc:"Fires Chirp Wave sound rings. At Level 10, every 7th attack triggers Deafening Chirp: all enemies in range take 2x current tower damage and are slowed by 30% for 2s."},'
if old not in s: raise RuntimeError('Cricket card anchor not found')
s=s.replace(old,new,1)
anchor='  // BEETLE_DUNG_AVALANCHE_V1: Dung Ball + Level 10 Dung Avalanche.\n'
if anchor not in s: anchor='  // HEDGEHOG_QUILL_STORM_V1: Quill Shot + Level 10 Quill Storm.\n'
if anchor not in s: raise RuntimeError('Attack anchor not found')
attack='''  // CRICKET_DEAFENING_CHIRP_V1: Chirp Wave + Level 10 Deafening Chirp.\n  if(t.key==="cricket"){\n    let deaf=false;if(t.level>=10){t.cricketAttackCount=(t.cricketAttackCount||0)+1;deaf=t.cricketAttackCount%7===0;}\n    if(deaf){for(const e of battle.enemies){if(!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range){e.hp-=dmg*2;e.cricketSlowTimer=Math.max(e.cricketSlowTimer||0,2);}}battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.8,maxLife:.8,type:"deafeningChirp",radius:range});}\n    else{target.hp-=dmg;battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.30,maxLife:.30,type:"chirpWave"});}\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
s=s.replace(anchor,attack+anchor,1)
# 30% slow for two seconds.
for hook in ['if((e.snailVulnerableTimer||0)>0)','if((e.crowSlowTimer||0)>0)','if((e.zebraSlowTimer||0)>0)']:
 if hook in s:
  s=s.replace(hook,'if((e.cricketSlowTimer||0)>0){e.cricketSlowTimer=Math.max(0,e.cricketSlowTimer-dt);speed*=.70;}\n    '+hook,1);break
# Draw normal travelling sound rings and big 360 degree pulse.
draw_anchor='    // BEETLE_DUNG_AVALANCHE_DRAW_V1\n'
if draw_anchor not in s: draw_anchor='    // CAT_SKUNK_PROJECTILE_DRAW_V2\n'
if draw_anchor not in s: raise RuntimeError('Draw anchor not found')
draw='''    // CRICKET_DEAFENING_CHIRP_DRAW_V1\n    }else if(s.type==="chirpWave"){const q=1-Math.max(0,s.life)/(s.maxLife||.30),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,a=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.strokeStyle="#b8ff7a";ctx.shadowColor="#8cff55";ctx.shadowBlur=8;ctx.lineWidth=2.5;for(let i=0;i<3;i++){const r=5+i*6;ctx.beginPath();ctx.arc(0,0,r,-.75,.75);ctx.stroke();}ctx.restore();\n    }else if(s.type==="deafeningChirp"){const q=1-Math.max(0,s.life)/(s.maxLife||.8);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle="#d8ff87";ctx.shadowColor="#a7ff45";ctx.shadowBlur=15;ctx.lineWidth=4;for(let i=0;i<4;i++){const r=Math.min(s.radius||145,(q*1.15-i*.10)*(s.radius||145));if(r>0){ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.stroke();}}ctx.fillStyle="#eaffb0";ctx.font="bold 14px system-ui";ctx.textAlign="center";ctx.fillText("DEAFENING CHIRP!",0,-30-q*15);ctx.restore();\n'''
s=s.replace(draw_anchor,draw+draw_anchor,1)
p.write_text(s,encoding='utf-8');print('Added Cricket Chirp Wave and Deafening Chirp')