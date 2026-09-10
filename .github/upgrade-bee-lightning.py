from pathlib import Path
p=Path('index.html')
s=p.read_text()

# 1) Raise Bee base damage from 9 to 15.
old='bee:{name:"Bee",emoji:"🐝",rarity:"Common",cost:55,range:165,rate:1/1.55,dmg:9,color:"#fc3",desc:"Very fast basic attacker."}'
new='bee:{name:"Bee",emoji:"🐝",rarity:"Common",cost:55,range:165,rate:1/1.55,dmg:15,color:"#fc3",desc:"Chain-lightning attacker that strikes multiple enemies."}'
if old not in s:
    raise SystemExit('Bee card marker not found')
s=s.replace(old,new,1)

# 2) Give Bee its own multi-target lightning attack before the normal projectile path.
marker='''  const selfDamageBoost=t.key==="ant"?(1+(t.antDamageBoost||0)):1;
  const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;
  let parrotBomb=false;'''
insert='''  const selfDamageBoost=t.key==="ant"?(1+(t.antDamageBoost||0)):1;
  const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;

  // Bee: chain lightning. Levels 1-9 hit up to 3 enemies; level 10+ hits up to 5.
  // At level 10+, the 4th and 5th targets take 4x the Bee's raw base damage.
  if(t.key==="bee"){
    const maxTargets=t.level>=10?5:3;
    const beeTargets=battle.enemies
      .filter(e=>!e.dead&&Math.hypot(e.x-t.x,e.y-t.y)<=range)
      .sort((a,b)=>(b.seg+(1-Math.hypot(b.x-t.x,b.y-t.y)/1000))-(a.seg+(1-Math.hypot(a.x-t.x,a.y-t.y)/1000)))
      .slice(0,maxTargets);
    beeTargets.forEach((e,i)=>{
      battle.shots.push({x:t.x,y:t.y-8,tx:e.x,ty:e.y,life:.22,maxLife:.22,type:"beeLightning",boltIndex:i});
      const hitDamage=(t.level>=10 && i>=3)?animals.bee.dmg*4:dmg;
      e.hp-=hitDamage;
      if(e.hp<=0)killEnemy(e);
    });
    t.cd=cardRate(t.key);
    return;
  }

  let parrotBomb=false;'''
if marker not in s:
    raise SystemExit('Bee attack insertion marker not found')
s=s.replace(marker,insert,1)

# 3) Draw a jagged lightning bolt for every Bee target.
draw_marker='''  battle.shots?.forEach(s=>{
    if(s.type==="parrotPineapple"||s.type==="pineapple"){'''
draw_new='''  battle.shots?.forEach(s=>{
    if(s.type==="beeLightning"){
      const fade=Math.max(0,Math.min(1,s.life/(s.maxLife||.22)));
      const dx=s.tx-s.x,dy=s.ty-s.y,len=Math.hypot(dx,dy)||1;
      const nx=-dy/len,ny=dx/len;
      ctx.save();ctx.globalAlpha=fade;ctx.lineCap="round";ctx.lineJoin="round";
      ctx.shadowColor="#fff36a";ctx.shadowBlur=14;
      ctx.strokeStyle="#fff36a";ctx.lineWidth=7;
      ctx.beginPath();ctx.moveTo(s.x,s.y);
      for(let i=1;i<6;i++){
        const q=i/6;
        const jitter=(i%2?1:-1)*(7+(s.boltIndex||0)*1.5);
        ctx.lineTo(s.x+dx*q+nx*jitter,s.y+dy*q+ny*jitter);
      }
      ctx.lineTo(s.tx,s.ty);ctx.stroke();
      ctx.shadowBlur=4;ctx.strokeStyle="#ffffff";ctx.lineWidth=2.5;ctx.stroke();
      ctx.restore();
    }else if(s.type==="parrotPineapple"||s.type==="pineapple"){'''
if draw_marker not in s:
    raise SystemExit('Bee lightning draw marker not found')
s=s.replace(draw_marker,draw_new,1)

p.write_text(s)
