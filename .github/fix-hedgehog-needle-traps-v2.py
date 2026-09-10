from pathlib import Path
p=Path('index.html'); s=p.read_text()
old='''  if(t.key==="hedgehog"){
    battle.needles=battle.needles||[];
    const id=(battle.nextNeedleId=(battle.nextNeedleId||0)+1);
    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.34,type:"hedgehogNeedles"});
    battle.needles.push({id,x:target.x,y:target.y});
    t.cd=cardRate(t.key);
    return;
  }'''
new='''  if(t.key==="hedgehog"){
    battle.needles=battle.needles||[];
    const id=(battle.nextNeedleId=(battle.nextNeedleId||0)+1);
    battle.shots.push({x:t.x,y:t.y-9,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:"hedgehogNeedles",needleTrapId:id});
    t.cd=cardRate(t.key);
    return;
  }'''
if old not in s: raise SystemExit('hedgehog fire block not found')
s=s.replace(old,new,1)
old2='''  battle.needles=battle.needles||[];
  battle.enemies.forEach(e=>{
    if(e.dead)return;
    e.needleHits=e.needleHits||{};
    battle.needles.forEach(n=>{
      if(e.dead||e.needleHits[n.id])return;
      if(Math.hypot(e.x-n.x,e.y-n.y)<=20){
        e.needleHits[n.id]=1;
        e.hp-=12;
        if(e.hp<=0)killEnemy(e);
      }
    });
  });
  battle.enemies.forEach(e=>moveEnemy(e,dt));battle.towers.forEach(t=>towerTick(t,dt));battle.shots.forEach(s=>s.life-=dt);
  battle.enemies=battle.enemies.filter(e=>!e.dead);battle.shots=battle.shots.filter(s=>s.life>0);'''
new2='''  battle.needles=battle.needles||[];
  battle.enemies.forEach(e=>moveEnemy(e,dt));
  battle.shots.forEach(s=>{
    if(s.type==="hedgehogNeedles" && !s.landed && s.life-dt<=0){
      s.landed=true;
      battle.needles.push({id:s.needleTrapId,x:s.tx,y:s.ty});
    }
    s.life-=dt;
  });
  battle.enemies.forEach(e=>{
    if(e.dead)return;
    e.needleHits=e.needleHits||{};
    battle.needles.forEach(n=>{
      if(e.dead||e.needleHits[n.id])return;
      if(Math.hypot(e.x-n.x,e.y-n.y)<=26){
        e.needleHits[n.id]=1;
        e.hp-=12;
        if(e.hp<=0)killEnemy(e);
      }
    });
  });
  battle.towers.forEach(t=>towerTick(t,dt));
  battle.enemies=battle.enemies.filter(e=>!e.dead);battle.shots=battle.shots.filter(s=>s.life>0);'''
if old2 not in s: raise SystemExit('hedgehog update block not found')
s=s.replace(old2,new2,1)
old3='''    if(s.type==="hedgehogNeedles"){
      const p=1-Math.max(0,s.life)/.34;
      const x=s.x+(s.tx-s.x)*p,y=s.y+(s.ty-s.y)*p;
      ctx.save();ctx.translate(x,y);ctx.strokeStyle="#f1e5cf";ctx.lineWidth=2;ctx.lineCap="round";
      for(let i=0;i<5;i++){
        const off=(i-2)*3;
        ctx.beginPath();ctx.moveTo(off,-7);ctx.lineTo(off+1,7);ctx.stroke();
      }
      ctx.restore();'''
new3='''    if(s.type==="hedgehogNeedles"){
      const lifeMax=s.maxLife||.42;
      const p=1-Math.max(0,s.life)/lifeMax;
      const x=s.x+(s.tx-s.x)*p,y=s.y+(s.ty-s.y)*p;
      const ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.strokeStyle="#f1e5cf";ctx.lineWidth=2;ctx.lineCap="round";
      for(let i=0;i<5;i++){
        const off=(i-2)*3.2;
        ctx.beginPath();ctx.moveTo(-8,off*.45);ctx.lineTo(8,off);ctx.stroke();
      }
      ctx.restore();'''
if old3 not in s: raise SystemExit('hedgehog draw block not found')
s=s.replace(old3,new3,1)
p.write_text(s)
