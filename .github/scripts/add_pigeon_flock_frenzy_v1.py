from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='PIGEON_FLOCK_FRENZY_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old='bird:{name:"Pigeon",emoji:"🕊️",rarity:"Common",cost:55,range:190,rate:1/1.30,dmg:8,color:"#7f8c99",desc:"Longer-range pigeon attacker."},'
new='bird:{name:"Pigeon",emoji:"🕊️",rarity:"Common",cost:55,range:190,rate:1/1.30,dmg:8,color:"#7f8c99",desc:"Dropping Strike attacks from above. At Level 10, every 7th attack triggers Flock Frenzy: 8 pigeons swoop across enemies in range, each dealing 60% current tower damage."},'
if old not in s: raise RuntimeError('Pigeon card anchor not found')
s=s.replace(old,new,1)
anchor='''  if(t.key==="hamster"){
    let hoard=false;'''
insert='''  // PIGEON_FLOCK_FRENZY_V1: Dropping Strike + Level 10 Flock Frenzy.
  if(t.key==="bird"){
    let frenzy=false;
    if(t.level>=10){t.pigeonAttackCount=(t.pigeonAttackCount||0)+1;frenzy=t.pigeonAttackCount%7===0;}
    if(frenzy){
      battle.shots.push({x:t.x,y:t.y-18,tx:t.x,ty:t.y-18,life:.72,maxLife:.72,type:"pigeonFlockBanner"});
      for(let i=0;i<8;i++){
        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);
        if(!pool.length)break;
        const hit=pool[i%pool.length];
        hit.hp-=dmg*.60;
        battle.shots.push({x:t.x-34+(i%4)*22,y:t.y-40-(i%2)*10,tx:hit.x,ty:hit.y,life:.40+i*.045,maxLife:.40+i*.045,type:"pigeonSwoop",special:true,pigeonIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:target.x,y:target.y-75,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:"pigeonDrop",special:false});
      battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.16,maxLife:.16,type:"animalAttackFlash",flash:"bird"});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="hamster"){
    let hoard=false;'''
if anchor not in s: raise RuntimeError('Pigeon attack insertion anchor not found')
s=s.replace(anchor,insert,1)
draw_anchor='''    }else if(s.type==="hamsterSeed"){'''
draw='''    }else if(s.type==="pigeonDrop"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.42),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*.7);ctx.fillStyle="#f4f4ee";ctx.strokeStyle="#9aa3aa";ctx.lineWidth=1.4;ctx.beginPath();ctx.ellipse(0,0,6,9,.2,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();
      if(q>.82){ctx.save();ctx.translate(s.tx,s.ty);ctx.globalAlpha=Math.max(0,1-(q-.82)/.18);ctx.fillStyle="#dfe6e9";for(let i=0;i<5;i++){const a=i*Math.PI*2/5;ctx.beginPath();ctx.ellipse(Math.cos(a)*10,Math.sin(a)*7,5,2.2,a,0,Math.PI*2);ctx.fill();}ctx.restore();}
    }else if(s.type==="pigeonSwoop"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.45),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.globalAlpha=.95;ctx.font="20px serif";ctx.textAlign="center";ctx.fillText("🕊️",0,5);ctx.strokeStyle="#e8eef2";ctx.lineWidth=2;for(let i=0;i<2;i++){ctx.beginPath();ctx.moveTo(-13-i*5,-7+i*4);ctx.lineTo(-25-i*8,-11+i*5);ctx.stroke();}ctx.restore();
    }else if(s.type==="pigeonFlockBanner"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.72);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.fillStyle="#f2f5f7";ctx.shadowColor="#fff";ctx.shadowBlur=10;ctx.font="bold 14px system-ui";ctx.textAlign="center";ctx.fillText("FLOCK FRENZY!",0,-26-q*10);ctx.restore();
    }else if(s.type==="hamsterSeed"){'''
if draw_anchor not in s: raise RuntimeError('Pigeon draw insertion anchor not found')
s=s.replace(draw_anchor,draw,1)
p.write_text(s,encoding='utf-8')
print('Applied Pigeon Dropping Strike and Flock Frenzy V1')
