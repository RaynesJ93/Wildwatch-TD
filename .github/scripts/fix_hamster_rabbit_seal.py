from pathlib import Path
import re
p=Path('index.html'); s=p.read_text(encoding='utf-8')

# Update descriptions
s=s.replace('hamster:{name:"Hamster",emoji:"🐹",rarity:"Common",cost:48,range:120,rate:1/1.35,dmg:8,color:"#c99b62",desc:"Quick basic attacker."}',
'''hamster:{name:"Hamster",emoji:"🐹",rarity:"Common",cost:48,range:120,rate:1/1.35,dmg:8,color:"#c99b62",desc:"Spits spinning sunflower seeds. At Level 10, every 7th attack becomes Hamster Hoard: 8 rapid seeds at 60% damage each, spread across enemies or focused on one target."}''')
s=s.replace('rabbit:{name:"Rabbit",emoji:"🐰",rarity:"Common",cost:52,range:145,rate:1/1.30,dmg:9,color:"#ddd",desc:"Fast basic attacker."}',
'''rabbit:{name:"Rabbit",emoji:"🐰",rarity:"Common",cost:52,range:145,rate:1/1.30,dmg:9,color:"#ddd",desc:"Fires spinning carrots. At Level 10, every 6th attack becomes Bunny Barrage: 4 rapid kicks dealing 1.5x damage each, spread across enemies or focused on one target."}''')

# Insert hamster and rabbit branches before mouse if not already present
if 'type:"hamsterSeed"' not in s or 'type:"rabbitCarrot"' not in s:
    m=re.search(r'(\s*)if\(t\.key==="mouse"\)\{', s)
    if not m: raise SystemExit('mouse attack branch not found')
    indent=m.group(1)
    branches='''\n  if(t.key==="hamster"){
    let hoard=false;
    if(t.level>=10){t.hamsterAttackCount=(t.hamsterAttackCount||0)+1;hoard=t.hamsterAttackCount%7===0;}
    if(hoard){
      for(let i=0;i<8;i++){
        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=cardRange(t.key));
        const hit=pool.length?pool[i%pool.length]:target;
        if(!hit||hit.dead) break;
        hit.hp-=dmg*.60;
        battle.shots.push({x:t.x,y:t.y-4,tx:hit.x,ty:hit.y,life:.24+i*.045,maxLife:.24+i*.045,type:"hamsterSeed",special:true,seedIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.28,maxLife:.28,type:"hamsterSeed",special:false});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }
  if(t.key==="rabbit"){
    let barrage=false;
    if(t.level>=10){t.rabbitAttackCount=(t.rabbitAttackCount||0)+1;barrage=t.rabbitAttackCount%6===0;}
    if(barrage){
      for(let i=0;i<4;i++){
        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=cardRange(t.key));
        const hit=pool.length?pool[i%pool.length]:target;
        if(!hit||hit.dead) break;
        hit.hp-=dmg*1.5;
        battle.shots.push({x:t.x,y:t.y-3,tx:hit.x,ty:hit.y,life:.20+i*.075,maxLife:.20+i*.075,type:"rabbitBarrage",hop:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.27,maxLife:.27,type:"rabbitCarrot"});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }
'''
    s=s[:m.start()]+branches+s[m.start():]

# Insert renderers before mouse cheese renderer if absent
if 's.type==="hamsterSeed"' not in s:
    anchor='}else if(s.type==="mouseCheeseWedge"||s.type==="mouseCheeseWheel"||s.type==="mouseCheeseBounce"){' 
    if anchor not in s: raise SystemExit('mouse renderer anchor not found')
    renderer='''}else if(s.type==="hamsterSeed"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.28),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*8);ctx.fillStyle="#b78b42";ctx.strokeStyle="#f4d37c";ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(0,0,7,3.5,0,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();
      ctx.save();ctx.globalAlpha=.7;ctx.fillStyle="#d9b15d";for(let i=0;i<3;i++){const tq=Math.max(0,q-i*.08);const tx=s.x+(s.tx-s.x)*tq,ty=s.y+(s.ty-s.y)*tq;ctx.beginPath();ctx.arc(tx,ty,1.8,0,Math.PI*2);ctx.fill();}ctx.restore();
      if(q>.84){ctx.save();ctx.globalAlpha=Math.max(0,1-(q-.84)/.16);ctx.translate(s.tx,s.ty);ctx.strokeStyle="#f6d77d";ctx.lineWidth=2;for(let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.moveTo(Math.cos(a)*4,Math.sin(a)*4);ctx.lineTo(Math.cos(a)*13,Math.sin(a)*13);ctx.stroke();}ctx.restore();}
    }else if(s.type==="rabbitCarrot"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.27),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*7);ctx.fillStyle="#ff8a24";ctx.beginPath();ctx.moveTo(-8,-4);ctx.lineTo(8,0);ctx.lineTo(-8,4);ctx.closePath();ctx.fill();ctx.fillStyle="#5bbf55";ctx.fillRect(-11,-4,4,3);ctx.fillRect(-11,1,4,3);ctx.restore();
      ctx.save();ctx.globalAlpha=.6;ctx.fillStyle="#ff9b35";for(let i=0;i<3;i++){const tq=Math.max(0,q-i*.09),tx=s.x+(s.tx-s.x)*tq,ty=s.y+(s.ty-s.y)*tq;ctx.beginPath();ctx.arc(tx,ty,2,0,Math.PI*2);ctx.fill();}ctx.restore();
      if(q>.84){ctx.save();ctx.globalAlpha=Math.max(0,1-(q-.84)/.16);ctx.translate(s.tx,s.ty);ctx.fillStyle="#ff9b35";ctx.fillRect(-10,-2,6,4);ctx.fillRect(4,-7,5,4);ctx.fillStyle="#5bbf55";ctx.fillRect(-3,5,5,3);ctx.restore();}
    }else if(s.type==="rabbitBarrage"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.2),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.globalAlpha=.85;ctx.translate(x,y);ctx.font="18px 'Apple Color Emoji','Segoe UI Emoji'";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🐾",0,0);ctx.restore();
      if(q>.7){ctx.save();ctx.globalAlpha=Math.max(0,1-(q-.7)/.3);ctx.translate(s.tx,s.ty);ctx.strokeStyle="#fff4d6";ctx.lineWidth=3;for(let i=0;i<3;i++){ctx.beginPath();ctx.moveTo(-10+i*4,-8);ctx.lineTo(9+i*3,8);ctx.stroke();}ctx.fillStyle="#c9a06a";for(let i=0;i<4;i++){ctx.beginPath();ctx.arc((i-1.5)*5,10,2.5,0,Math.PI*2);ctx.fill();}ctx.restore();}
    '''
    s=s.replace(anchor,renderer+anchor,1)

# Make Seal attack unmistakably blue water with large splash; replace existing renderer block.
pattern=r'if\(s\.type==="sealWaterBolt"\)\{.*?\n\s*\}else if\('
match=re.search(pattern,s,re.S)
if not match: raise SystemExit('seal renderer block not found')
seal='''if(s.type==="sealWaterBolt"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.34),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.globalAlpha=.98;ctx.shadowColor="#00bfff";ctx.shadowBlur=14;ctx.fillStyle="#22bdf5";ctx.beginPath();ctx.ellipse(0,0,16,8,0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#a8efff";ctx.beginPath();ctx.ellipse(5,-2,6,2.5,0,0,Math.PI*2);ctx.fill();ctx.restore();
      ctx.save();ctx.globalAlpha=.65;ctx.fillStyle="#52d5ff";for(let i=1;i<=4;i++){const tq=Math.max(0,q-i*.055),tx=s.x+(s.tx-s.x)*tq,ty=s.y+(s.ty-s.y)*tq;ctx.beginPath();ctx.arc(tx,ty,4-i*.55,0,Math.PI*2);ctx.fill();}ctx.restore();
      if(q>.76){const a=Math.max(0,1-(q-.76)/.24);ctx.save();ctx.globalAlpha=a;ctx.translate(s.tx,s.ty);ctx.strokeStyle="#59dcff";ctx.fillStyle="#2ec7ff";ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,22+(q-.76)*35,0,Math.PI*2);ctx.stroke();for(let i=0;i<8;i++){const an=i*Math.PI/4;ctx.beginPath();ctx.arc(Math.cos(an)*18,Math.sin(an)*18,4,0,Math.PI*2);ctx.fill();}ctx.restore();}
    }else if('''
s=s[:match.start()]+seal+s[match.end():]

p.write_text(s,encoding='utf-8')
print('Fixed Hamster, Rabbit and Seal attacks')
