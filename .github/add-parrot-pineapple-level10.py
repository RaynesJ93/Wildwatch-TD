from pathlib import Path
p=Path('index.html'); s=p.read_text()

# Ensure battle state has pineapple bombs.
old='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],needles:[],usedCards:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'
new='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,enemies:[],towers:[],shots:[],puddles:[],needles:[],pineapples:[],usedCards:[],spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false};'
if old not in s: raise SystemExit('battle init marker not found')
s=s.replace(old,new,1)

# Parrot level 10: all attacks become pineapples; every third becomes a delayed bomb.
old='''  const selfDamageBoost=t.key==="ant"?(1+(t.antDamageBoost||0)):1;
  const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;
  battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":"beam"});'''
new='''  const selfDamageBoost=t.key==="ant"?(1+(t.antDamageBoost||0)):1;
  const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;
  let parrotBomb=false;
  if(t.key==="parrot" && t.level>=10){
    t.parrotPineappleCount=(t.parrotPineappleCount||0)+1;
    parrotBomb=t.parrotPineappleCount%3===0;
  }
  battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:(t.key==="parrot"&&t.level>=10)?.30:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":(t.key==="parrot"&&t.level>=10)?"pineapple":"beam"});
  if(parrotBomb){
    battle.pineapples=battle.pineapples||[];
    battle.pineapples.push({x:target.x,y:target.y,life:2,maxLife:2,radius:95,damage:animals.parrot.dmg*4});
  }'''
if old not in s: raise SystemExit('shot creation marker not found')
s=s.replace(old,new,1)

# Third pineapple is delayed only; normal pineapples keep normal attack damage.
old='''  if(t.key==="eagle"){
    target.hp-=dmg;'''
new='''  if(t.key==="parrot" && t.level>=10 && parrotBomb){
    // Every third pineapple becomes a 2-second track bomb instead of dealing instant damage.
  }else if(t.key==="eagle"){
    target.hp-=dmg;'''
if old not in s: raise SystemExit('damage branch marker not found')
s=s.replace(old,new,1)

# Update delayed pineapple bombs and explode into up to three targets.
marker='''  battle.puddles=battle.puddles.filter(p=>p.life>0);
  battle.needles=battle.needles||[];'''
insert='''  battle.puddles=battle.puddles.filter(p=>p.life>0);
  battle.pineapples=battle.pineapples||[];
  battle.pineapples.forEach(p=>{
    p.life-=dt;
    if(p.life<=0 && !p.exploded){
      p.exploded=true;
      const victims=battle.enemies
        .filter(e=>!e.dead&&Math.hypot(e.x-p.x,e.y-p.y)<=p.radius)
        .sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))
        .slice(0,3);
      victims.forEach(e=>{e.hp-=p.damage;if(e.hp<=0)killEnemy(e)});
      battle.shots.push({x:p.x,y:p.y,tx:p.x,ty:p.y,life:.35,maxLife:.35,type:"pineappleExplosion"});
    }
  });
  battle.pineapples=battle.pineapples.filter(p=>!p.exploded);
  battle.needles=battle.needles||[];'''
if marker not in s: raise SystemExit('update marker not found')
s=s.replace(marker,insert,1)

# Draw lingering pineapple bombs before projectile effects.
marker='''  battle.shots?.forEach(s=>{
    if(s.type==="hedgehogNeedles"){'''
insert='''  battle.pineapples?.forEach(p=>{
    ctx.save();ctx.translate(p.x,p.y);
    const pulse=1+Math.sin((2-p.life)*10)*.08;
    ctx.scale(pulse,pulse);ctx.font="26px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("🍍",0,0);
    ctx.restore();
  });
  battle.shots?.forEach(s=>{
    if(s.type==="pineapple"){
      const lifeMax=.30,pct=1-Math.max(0,s.life)/lifeMax;
      const x=s.x+(s.tx-s.x)*pct,y=s.y+(s.ty-s.y)*pct;
      ctx.save();ctx.translate(x,y);ctx.rotate(pct*8);ctx.font="24px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🍍",0,0);ctx.restore();
    }else if(s.type==="pineappleExplosion"){
      const pct=1-Math.max(0,s.life)/(s.maxLife||.35),r=16+pct*72;
      ctx.save();ctx.globalAlpha=1-pct;ctx.fillStyle="#ffb32c88";ctx.strokeStyle="#ffe46b";ctx.lineWidth=5;ctx.beginPath();ctx.arc(s.x,s.y,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();
    }else if(s.type==="hedgehogNeedles"){'''
if marker not in s: raise SystemExit('draw shot marker not found')
s=s.replace(marker,insert,1)

p.write_text(s)
