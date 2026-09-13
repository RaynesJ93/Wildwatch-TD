from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='DUCK_DIVE_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old='duck:{name:"Duck",emoji:"🦆",rarity:"Common",cost:58,range:160,rate:1/1.10,dmg:11,color:"#6b8e45",desc:"Balanced basic attacker."},'
new='duck:{name:"Duck",emoji:"🦆",rarity:"Common",cost:58,range:160,rate:1/1.10,dmg:11,color:"#6b8e45",desc:"Fires Water Peck splashes. At Level 10, every 6th attack becomes Duck Dive: a piercing wave hits up to 5 enemies, dealing 1.5x damage to the first and 75% damage to enemies behind, slowing all hit enemies by 20% for 2s."},'
if old not in s: raise RuntimeError('Duck card anchor not found')
s=s.replace(old,new,1)
anchor='''  // PIGEON_FLOCK_FRENZY_V1: Dropping Strike + Level 10 Flock Frenzy.
  if(t.key==="bird"){'''
if anchor not in s: raise RuntimeError('Pigeon block anchor not found')
insert='''  // DUCK_DIVE_V1: Water Peck + Level 10 Duck Dive.
  if(t.key==="duck"){
    let duckDive=false;
    if(t.level>=10){t.duckAttackCount=(t.duckAttackCount||0)+1;duckDive=t.duckAttackCount%6===0;}
    if(duckDive){
      const candidates=battle.enemies
        .filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range)
        .sort((a,b)=>(b.seg+(1-Math.hypot(b.x-t.x,b.y-t.y)/1000))-(a.seg+(1-Math.hypot(a.x-t.x,a.y-t.y)/1000)))
        .slice(0,5);
      candidates.forEach((e,i)=>{
        e.hp-=i===0?dmg*1.5:dmg*.75;
        e.chickenSlowTimer=Math.max(e.chickenSlowTimer||0,2);
        battle.shots.push({x:t.x,y:t.y-4,tx:e.x,ty:e.y,life:.34+i*.045,maxLife:.34+i*.045,type:"duckDiveWave",special:true,waveIndex:i});
        if(e.hp<=0)killEnemy(e);
      });
      battle.shots.push({x:t.x,y:t.y-8,tx:t.x,ty:t.y-8,life:.52,maxLife:.52,type:"duckDiveBanner"});
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.34,maxLife:.34,type:"duckWaterPeck",special:false});
      battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.16,maxLife:.16,type:"animalAttackFlash",flash:"duck"});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

'''
s=s.replace(anchor,insert+anchor,1)
draw_anchor='''    }else if(s.type==="pigeonDrop"){'''
if draw_anchor not in s: raise RuntimeError('Projectile draw anchor not found')
draw='''    }else if(s.type==="duckWaterPeck"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.34),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.translate(x,y);ctx.rotate(Math.atan2(s.ty-s.y,s.tx-s.x));ctx.fillStyle="#7fdcff";ctx.shadowColor="#65cfff";ctx.shadowBlur=8;ctx.beginPath();ctx.moveTo(10,0);ctx.quadraticCurveTo(-2,-7,-9,0);ctx.quadraticCurveTo(-2,7,10,0);ctx.fill();ctx.restore();
      if(q>.82){ctx.save();ctx.translate(s.tx,s.ty);ctx.globalAlpha=Math.max(0,1-(q-.82)/.18);ctx.strokeStyle="#b9efff";ctx.lineWidth=2;for(let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.moveTo(Math.cos(a)*4,Math.sin(a)*4);ctx.lineTo(Math.cos(a)*14,Math.sin(a)*14);ctx.stroke();}ctx.restore();}
    }else if(s.type==="duckDiveWave"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.34),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.globalAlpha=.88;ctx.strokeStyle="#8de3ff";ctx.shadowColor="#4bc7ff";ctx.shadowBlur=12;ctx.lineWidth=7;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-22,0);ctx.quadraticCurveTo(-4,-10,18,0);ctx.stroke();ctx.strokeStyle="#d7f7ff";ctx.lineWidth=2.5;ctx.beginPath();ctx.moveTo(-20,-3);ctx.quadraticCurveTo(-2,-10,17,-2);ctx.stroke();ctx.restore();
    }else if(s.type==="duckDiveBanner"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.52);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#bfefff";ctx.shadowColor="#5dd8ff";ctx.shadowBlur=12;ctx.font="bold 14px system-ui";ctx.textAlign="center";ctx.fillText("DUCK DIVE!",0,-25-q*9);ctx.restore();
    }else if(s.type==="pigeonDrop"){'''
s=s.replace(draw_anchor,draw,1)
p.write_text(s,encoding='utf-8')
print('Applied Duck Water Peck and Duck Dive V1')
# trigger: 2026-09-13
