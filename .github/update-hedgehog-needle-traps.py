from pathlib import Path
p=Path('index.html'); s=p.read_text()
# Card stat/description
s=s.replace('hedgehog:{name:"Hedgehog",emoji:"🦔",rarity:"Common",cost:60,range:135,rate:1,dmg:13,color:"#76543b"','hedgehog:{name:"Hedgehog",emoji:"🦔",rarity:"Common",cost:60,range:135,rate:1,dmg:12,color:"#76543b"',1)
# New battles keep permanent needle stacks for the whole map.
old='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],usedCards:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'
new='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],needles:[],usedCards:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'
if old not in s: raise SystemExit('battle init marker not found')
s=s.replace(old,new,1)
# Hedgehog fires five needles to the enemy's current track position. Stack lands permanently and does not deal instant damage.
marker='  if(!target)return;\n  const nearbyLion='
insert='''  if(!target)return;\n  if(t.key==="hedgehog"){
    battle.needles=battle.needles||[];
    const id=(battle.nextNeedleId=(battle.nextNeedleId||0)+1);
    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.34,type:"hedgehogNeedles"});
    battle.needles.push({id,x:target.x,y:target.y});
    t.cd=cardRate(t.key);
    return;
  }\n  const nearbyLion='''
if marker not in s: raise SystemExit('tower target marker not found')
s=s.replace(marker,insert,1)
# Trap collision: each permanent five-needle stack damages each enemy once for 12 when crossed.
marker2='  battle.puddles=battle.puddles.filter(p=>p.life>0);\n  battle.enemies.forEach(e=>moveEnemy(e,dt));'
insert2='''  battle.puddles=battle.puddles.filter(p=>p.life>0);
  battle.needles=battle.needles||[];
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
  battle.enemies.forEach(e=>moveEnemy(e,dt));'''
if marker2 not in s: raise SystemExit('battle update marker not found')
s=s.replace(marker2,insert2,1)
# Draw permanent needle stacks on the track before travelling shots.
marker3='  battle.shots?.forEach(s=>{\n    if(s.type==="water"){'
insert3='''  battle.needles?.forEach(n=>{
    ctx.save();ctx.translate(n.x,n.y);ctx.strokeStyle="#e8dcc6";ctx.lineWidth=2.2;ctx.lineCap="round";
    for(let i=0;i<5;i++){
      const a=-1.35+i*.22,ox=(i-2)*3.2;
      ctx.beginPath();ctx.moveTo(ox+Math.cos(a)*3,Math.sin(a)*3);ctx.lineTo(ox+Math.cos(a)*13,Math.sin(a)*13);ctx.stroke();
    }
    ctx.restore();
  });
  battle.shots?.forEach(s=>{
    if(s.type==="hedgehogNeedles"){
      const p=1-Math.max(0,s.life)/.34;
      const x=s.x+(s.tx-s.x)*p,y=s.y+(s.ty-s.y)*p;
      ctx.save();ctx.translate(x,y);ctx.strokeStyle="#f1e5cf";ctx.lineWidth=2;ctx.lineCap="round";
      for(let i=0;i<5;i++){
        const off=(i-2)*3;
        ctx.beginPath();ctx.moveTo(off,-7);ctx.lineTo(off+1,7);ctx.stroke();
      }
      ctx.restore();
    }else if(s.type==="water"){'''
if marker3 not in s: raise SystemExit('shot draw marker not found')
s=s.replace(marker3,insert3,1)
p.write_text(s)
