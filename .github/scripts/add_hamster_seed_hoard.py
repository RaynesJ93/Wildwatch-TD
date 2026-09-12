from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='hamster:{name:"Hamster",emoji:"🐹",rarity:"Common",cost:48,range:120,rate:1/1.35,dmg:8,color:"#c99b62",desc:"Quick basic attacker."}'
new='hamster:{name:"Hamster",emoji:"🐹",rarity:"Common",cost:48,range:120,rate:1/1.35,dmg:8,color:"#c99b62",desc:"Spits spinning sunflower seeds. At Level 10, every 7th attack unleashes Hamster Hoard: 8 rapid seeds dealing 60% damage each, spread across enemies or focused on one target."}'
if old not in s: raise SystemExit('hamster card anchor not found')
s=s.replace(old,new,1)
anchor='    let stampede=false;\n    if(t.level>=10){\n      t.zebraAttackCount=(t.zebraAttackCount||0)+1;'
pos=s.find(anchor)
if pos<0: raise SystemExit('zebra attack anchor not found')
# Find start of zebra branch and insert hamster branch immediately before it.
start=s.rfind('  }else if(t.key==="zebra"){',0,pos)
if start<0: raise SystemExit('zebra branch start not found')
ham='''  }else if(t.key==="hamster"){
    let hoard=false;
    if(t.level>=10){t.hamsterAttackCount=(t.hamsterAttackCount||0)+1;hoard=t.hamsterAttackCount%7===0;}
    if(hoard){
      const live=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=a.range);
      const pool=live.length?live:[target];
      for(let i=0;i<8;i++){
        const hit=pool[i%pool.length];
        hit.hp-=dmg*.60;
        battle.shots.push({x:t.x,y:t.y-4,tx:hit.x,ty:hit.y,life:.22+i*.035,maxLife:.22+i*.035,type:"hamsterSeed",special:true,seedIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.26,maxLife:.26,type:"hamsterSeed",special:false});
      if(target.hp<=0)killEnemy(target);
    }
'''
s=s[:start]+ham+s[start+3:]
# insert renderer before zebra renderer
render='''    }else if(s.type==="hamsterSeed"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.26),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const ang=q*Math.PI*7+(s.seedIndex||0)*.4;
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      ctx.fillStyle=s.special?"#f2c94c":"#d8b33f";ctx.strokeStyle="#6f5320";ctx.lineWidth=1.2;
      ctx.beginPath();ctx.ellipse(0,0,s.special?6:5,s.special?2.8:2.3,0,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.beginPath();ctx.moveTo(-2.5,0);ctx.lineTo(2.5,0);ctx.stroke();ctx.restore();
      ctx.save();ctx.globalAlpha=.65*(1-q);ctx.fillStyle="#b88935";
      for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(x-(s.tx-s.x)*.025*(i+1),y-(s.ty-s.y)*.025*(i+1)+(i-1)*2,1.2,0,Math.PI*2);ctx.fill();}ctx.restore();
      if(q>.86){ctx.save();ctx.globalAlpha=(1-q)*7;ctx.fillStyle="#e2bd55";for(let i=0;i<4;i++){const a=i*Math.PI/2;ctx.fillRect(s.tx+Math.cos(a)*7-1,s.ty+Math.sin(a)*7-1,3,2);}ctx.restore();}
'''
rmark='    }else if(s.type==="zebraStripeKick"){'
if rmark not in s: raise SystemExit('zebra renderer anchor not found')
s=s.replace(rmark,render+rmark,1)
p.write_text(s,encoding='utf-8')
print('Added Hamster Seed Spit and Level 10 Hamster Hoard')
