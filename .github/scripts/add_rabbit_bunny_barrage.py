from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='rabbit:{name:"Rabbit",emoji:"🐰",rarity:"Common",cost:52,range:145,rate:1/1.30,dmg:9,color:"#ddd",desc:"Fast basic attacker."}'
new='rabbit:{name:"Rabbit",emoji:"🐰",rarity:"Common",cost:52,range:145,rate:1/1.30,dmg:9,color:"#ddd",desc:"Fires spinning carrots. At Level 10, every 6th attack becomes Bunny Barrage: 4 rapid kicks dealing 1.5x damage each, spread across enemies or focused on one target."}'
if old not in s: raise SystemExit('rabbit card anchor not found')
s=s.replace(old,new,1)
anchor='  }else if(t.key==="hamster"){' 
if anchor not in s: raise SystemExit('hamster branch anchor not found')
rabbit='''  }else if(t.key==="rabbit"){
    let barrage=false;
    if(t.level>=10){t.rabbitAttackCount=(t.rabbitAttackCount||0)+1;barrage=t.rabbitAttackCount%6===0;}
    if(barrage){
      const live=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=a.range);
      const pool=live.length?live:[target];
      for(let i=0;i<4;i++){
        const hit=pool[i%pool.length];
        hit.hp-=dmg*1.5;
        battle.shots.push({x:t.x,y:t.y-3,tx:hit.x,ty:hit.y,life:.18+i*.07,maxLife:.18+i*.07,type:"rabbitBarrage",hop:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.25,maxLife:.25,type:"rabbitCarrot"});
      if(target.hp<=0)killEnemy(target);
    }
'''
s=s.replace(anchor,rabbit+anchor,1)
rmark='    }else if(s.type==="hamsterSeed"){' 
if rmark not in s: raise SystemExit('hamster renderer anchor not found')
render='''    }else if(s.type==="rabbitCarrot"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.25),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=q*Math.PI*8;
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.fillStyle="#f28c28";ctx.beginPath();ctx.moveTo(-7,-3);ctx.lineTo(7,0);ctx.lineTo(-7,3);ctx.closePath();ctx.fill();ctx.strokeStyle="#58a83f";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-7,0);ctx.lineTo(-12,-4);ctx.moveTo(-7,0);ctx.lineTo(-12,3);ctx.stroke();ctx.restore();
      ctx.save();ctx.globalAlpha=.55*(1-q);ctx.fillStyle="#f0a33b";for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(x-(s.tx-s.x)*.025*(i+1),y-(s.ty-s.y)*.025*(i+1)+(i-1)*2,1.3,0,Math.PI*2);ctx.fill();}ctx.restore();
      if(q>.86){ctx.save();ctx.globalAlpha=(1-q)*7;for(let i=0;i<5;i++){const a=i*Math.PI*.4;ctx.fillStyle=i%2?"#58a83f":"#f28c28";ctx.fillRect(s.tx+Math.cos(a)*9-1,s.ty+Math.sin(a)*9-1,3,2);}ctx.restore();}
    }else if(s.type==="rabbitBarrage"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.18),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.globalAlpha=.7*(1-q);ctx.fillStyle="#d9c6a3";for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(x-(s.tx-s.x)*.03*(i+1),y-(s.ty-s.y)*.03*(i+1),4-i*.6,0,Math.PI*2);ctx.fill();}ctx.restore();
      ctx.save();ctx.translate(x,y);ctx.globalAlpha=.95;ctx.font="18px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🐾",0,0);ctx.restore();
      if(q>.78){ctx.save();ctx.translate(s.tx,s.ty);ctx.globalAlpha=(1-q)*4.5;ctx.strokeStyle="#fff1c9";ctx.lineWidth=3;for(let i=0;i<3;i++){const a=-.7+i*.7;ctx.beginPath();ctx.moveTo(Math.cos(a)*5,Math.sin(a)*5);ctx.lineTo(Math.cos(a)*17,Math.sin(a)*17);ctx.stroke();}ctx.restore();}
'''
s=s.replace(rmark,render+rmark,1)
p.write_text(s,encoding='utf-8')
print('Added Rabbit Carrot Kick and Level 10 Bunny Barrage')
