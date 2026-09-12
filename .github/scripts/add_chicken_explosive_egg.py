from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
old='chicken:{name:"Chicken",emoji:"🐔",rarity:"Common",cost:55,range:145,rate:1/1.25,dmg:10,color:"#fff",desc:"Reliable basic attacker."}'
new='chicken:{name:"Chicken",emoji:"🐔",rarity:"Common",cost:55,range:145,rate:1/1.25,dmg:10,color:"#fff",desc:"Launches cracking egg bombs. At Level 10, every 5th attack fires an Explosive Egg: 2x damage to the target, 100% splash damage within 75 range and a 20% slow for 2s."}'
if old not in s: raise SystemExit('chicken card anchor not found')
s=s.replace(old,new,1)
anchor='  }else if(t.key==="rabbit"):'
if anchor not in s: raise SystemExit('rabbit branch anchor not found')
branch='''  }else if(t.key==="chicken"){
    let explosive=false;
    if(t.level>=10){t.chickenAttackCount=(t.chickenAttackCount||0)+1;explosive=t.chickenAttackCount%5===0;}
    if(explosive){
      target.hp-=dmg*2;
      const splash=battle.enemies.filter(e=>e!==target&&!e.dead&&e.hp>0&&Math.hypot(e.x-target.x,e.y-target.y)<=75);
      [target,...splash].forEach(e=>{if(e!==target)e.hp-=dmg;e.chickenSlowTimer=Math.max(e.chickenSlowTimer||0,2);if(e.hp<=0)killEnemy(e);});
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.34,maxLife:.34,type:"chickenEgg",special:true});
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.30,maxLife:.30,type:"chickenEgg",special:false});
      if(target.hp<=0)killEnemy(target);
    }
'''
s=s.replace(anchor,branch+anchor,1)
# Hook chicken slow into enemy update using zebra slow patterns.
oldslow='if(e.zebraSlowTimer>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);'
if oldslow not in s: raise SystemExit('zebra slow timer anchor not found')
s=s.replace(oldslow,oldslow+'if(e.chickenSlowTimer>0)e.chickenSlowTimer=Math.max(0,e.chickenSlowTimer-dt);',1)
oldmult='*(e.zebraSlowTimer>0?.75:1)'
if oldmult not in s: raise SystemExit('zebra movement multiplier anchor not found')
s=s.replace(oldmult,oldmult+'*(e.chickenSlowTimer>0?.80:1)',1)
rmark='    }else if(s.type==="rabbitCarrot"):'
if rmark not in s: raise SystemExit('rabbit renderer anchor not found')
render='''    }else if(s.type==="chickenEgg"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.30),arc=Math.sin(q*Math.PI)*(s.special?28:20),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-arc;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*5);ctx.fillStyle=s.special?"#ffd84d":"#fff8df";ctx.strokeStyle=s.special?"#e0a800":"#cfc8b5";ctx.lineWidth=s.special?2:1.2;ctx.beginPath();ctx.ellipse(0,0,s.special?8:6,s.special?10:8,0,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();
      if(q>.82){const a=(q-.82)/.18;ctx.save();ctx.globalAlpha=Math.max(0,1-a);ctx.translate(s.tx,s.ty);ctx.fillStyle=s.special?"#ffd21f":"#ffd84d";ctx.beginPath();ctx.arc(0,0,s.special?30:13,0,Math.PI*2);ctx.fill();ctx.fillStyle="#fff7dd";for(let i=0;i<(s.special?9:5);i++){const ang=i*Math.PI*2/(s.special?9:5);ctx.save();ctx.rotate(ang);ctx.fillRect(s.special?18:8,-2,s.special?13:7,4);ctx.restore();}ctx.fillStyle="#fff";for(let i=0;i<6;i++){const ang=i*Math.PI/3+.3;ctx.fillRect(Math.cos(ang)*(s.special?24:11)-2,Math.sin(ang)*(s.special?24:11)-2,5,3);}ctx.restore();}
'''
s=s.replace(rmark,render+rmark,1)
p.write_text(s,encoding='utf-8'); print('Added Chicken Egg Bomb and Level 10 Explosive Egg')
