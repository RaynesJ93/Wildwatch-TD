from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Upgrade card descriptions.
repls={
'peacock:{name:"Peacock",emoji:"🦚",rarity:"Uncommon",cost:86,range:210,rate:1,dmg:20,color:"#38a",desc:"Long-range attacker."}':'peacock:{name:"Peacock",emoji:"🦚",rarity:"Uncommon",cost:86,range:210,rate:1,dmg:20,color:"#38a",desc:"Fires shimmering Peacock Feathers. At Level 10, every 6th attack triggers Royal Fan: 7 jeweled feathers fan across enemies in range, each dealing 90% current tower damage."}',
'turtle:{name:"Turtle",emoji:"🐢",rarity:"Uncommon",cost:92,range:130,rate:1/.65,dmg:32,color:"#587",desc:"Slow heavy attacker."}':'turtle:{name:"Turtle",emoji:"🐢",rarity:"Uncommon",cost:92,range:130,rate:1/.65,dmg:32,color:"#587",desc:"Launches a spinning shell. At Level 10, every 5th attack becomes Shell Ricochet: the shell deals 2x damage to the first target then bounces to up to 4 more enemies for 80% damage each."}',
'lizard:{name:"Lizard",emoji:"🦎",rarity:"Uncommon",cost:80,range:175,rate:1/1.35,dmg:18,color:"#5a6",desc:"Fast attacker."}':'lizard:{name:"Lizard",emoji:"🦎",rarity:"Uncommon",cost:80,range:175,rate:1/1.35,dmg:18,color:"#5a6",desc:"Snaps enemies with a lightning-fast tongue. At Level 10, every 7th attack triggers Tongue Frenzy: 5 rapid lashes deal 75% current tower damage each, retargeting enemies in range."}',
'scorpion:{name:"Scorpion",emoji:"🦂",rarity:"Uncommon",cost:90,range:160,rate:1/1.10,dmg:25,color:"#a65",desc:"Strong quick attacker."}':'scorpion:{name:"Scorpion",emoji:"🦂",rarity:"Uncommon",cost:90,range:160,rate:1/1.10,dmg:25,color:"#a65",desc:"Fires venomous stinger shots. At Level 10, every 6th attack triggers Venom Burst: 2x impact damage and a potent 6-second poison that deals 35% current tower damage per tick."}'
}
for old,new in repls.items():
    if old not in s: raise RuntimeError('description anchor missing: '+old[:30])
    s=s.replace(old,new,1)

anchor='''  if(t.key==="parrot" && t.level>=10){\n'''
if anchor not in s: raise RuntimeError('tower attack insertion anchor missing')
logic=r'''  // PEACOCK_TURTLE_LIZARD_SCORPION_ATTACKS_V1
  if(t.key==="peacock"){
    let royal=false;
    if(t.level>=10){t.peacockAttackCount=(t.peacockAttackCount||0)+1;royal=t.peacockAttackCount%6===0;}
    if(royal){
      const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);
      for(let i=0;i<7;i++){
        const hit=pool.length?pool[i%pool.length]:target;
        if(!hit||hit.dead)break;
        hit.hp-=dmg*.90;
        battle.shots.push({x:t.x,y:t.y-8,tx:hit.x,ty:hit.y,life:.40+i*.045,maxLife:.40+i*.045,type:"peacockRoyalFeather",special:true,fanIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
      battle.shots.push({x:t.x,y:t.y-8,tx:t.x,ty:t.y-8,life:.55,maxLife:.55,type:"peacockRoyalFanBanner"});
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.38,maxLife:.38,type:"peacockFeather"});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="turtle"){
    let ricochet=false;
    if(t.level>=10){t.turtleAttackCount=(t.turtleAttackCount||0)+1;ricochet=t.turtleAttackCount%5===0;}
    if(ricochet){
      target.hp-=dmg*2;
      battle.shots.push({x:t.x,y:t.y-3,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:"turtleShell",special:true,bounceIndex:0});
      if(target.hp<=0)killEnemy(target);
      const hits=battle.enemies.filter(e=>!e.dead&&e!==target&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range).slice(0,4);
      let bx=target.x,by=target.y;
      hits.forEach((e,i)=>{
        e.hp-=dmg*.80;
        battle.shots.push({x:bx,y:by,tx:e.x,ty:e.y,life:.28+i*.05,maxLife:.28+i*.05,type:"turtleShell",special:true,bounceIndex:i+1});
        if(e.hp<=0)killEnemy(e);bx=e.x;by=e.y;
      });
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-3,tx:target.x,ty:target.y,life:.44,maxLife:.44,type:"turtleShell",special:false});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="lizard"){
    let frenzy=false;
    if(t.level>=10){t.lizardAttackCount=(t.lizardAttackCount||0)+1;frenzy=t.lizardAttackCount%7===0;}
    if(frenzy){
      for(let i=0;i<5;i++){
        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);
        const hit=pool.length?pool[i%pool.length]:target;
        if(!hit||hit.dead)break;
        hit.hp-=dmg*.75;
        battle.shots.push({x:t.x,y:t.y-5,tx:hit.x,ty:hit.y,life:.22+i*.055,maxLife:.22+i*.055,type:"lizardTongue",special:true,lashIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
      battle.shots.push({x:t.x,y:t.y-6,tx:t.x,ty:t.y-6,life:.48,maxLife:.48,type:"lizardFrenzyBanner"});
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.20,maxLife:.20,type:"lizardTongue",special:false});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="scorpion"){
    let burst=false;
    if(t.level>=10){t.scorpionAttackCount=(t.scorpionAttackCount||0)+1;burst=t.scorpionAttackCount%6===0;}
    target.hp-=burst?dmg*2:dmg;
    battle.shots.push({x:t.x,y:t.y-6,tx:target.x,ty:target.y,life:burst?.46:.32,maxLife:burst?.46:.32,type:"scorpionStinger",special:burst});
    if(burst){
      target.poison=Math.max(target.poison||0,6);
      target.poisonTick=Math.min(target.poisonTick||1,1);
      target.poisonDmg=Math.max(target.poisonDmg||0,dmg*.35);
      battle.shots.push({x:target.x,y:target.y,tx:target.x,ty:target.y,life:.55,maxLife:.55,type:"scorpionVenomBurst"});
    }
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);return;
  }

'''
s=s.replace(anchor,logic+anchor,1)

old='''"woolBall","woolTrapBanner"]);'''
new='''"woolBall","woolTrapBanner","peacockFeather","peacockRoyalFeather","peacockRoyalFanBanner","turtleShell","lizardTongue","lizardFrenzyBanner","scorpionStinger","scorpionVenomBurst"]);'''
if old not in s: raise RuntimeError('visibility set anchor missing')
s=s.replace(old,new,1)

draw_anchor='''    }else if(s.type==="sealWaterBolt"){\n'''
if draw_anchor not in s: raise RuntimeError('shot renderer anchor missing')
draw=r'''    }else if(s.type==="peacockFeather"||s.type==="peacockRoyalFeather"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.38),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang+q*4);ctx.shadowColor=s.special?"#ffe46b":"#46e0ff";ctx.shadowBlur=s.special?20:12;
      ctx.strokeStyle=s.special?"#ffe46b":"#36b9e8";ctx.lineWidth=s.special?6:4;ctx.beginPath();ctx.moveTo(-15,0);ctx.quadraticCurveTo(0,-10,18,0);ctx.quadraticCurveTo(0,10,-15,0);ctx.stroke();
      ctx.fillStyle=s.special?"#8d5cff":"#37d9c8";ctx.beginPath();ctx.arc(4,0,s.special?5:3.5,0,Math.PI*2);ctx.fill();ctx.restore();
    }else if(s.type==="peacockRoyalFanBanner"){
      const a=Math.max(0,s.life/(s.maxLife||.55));ctx.save();ctx.globalAlpha=a;ctx.translate(s.x,s.y);ctx.strokeStyle="#ffe46b";ctx.lineWidth=5;ctx.shadowColor="#8b61ff";ctx.shadowBlur=20;for(let i=-3;i<=3;i++){ctx.save();ctx.rotate(i*.22);ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,-42);ctx.stroke();ctx.restore();}ctx.restore();
    }else if(s.type==="turtleShell"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.44),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*8);ctx.shadowColor=s.special?"#baff6b":"#7fd37a";ctx.shadowBlur=s.special?20:10;ctx.fillStyle="#527d4d";ctx.strokeStyle="#d8e69b";ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,s.special?15:11,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.strokeStyle="#98b96f";ctx.beginPath();ctx.moveTo(-8,-8);ctx.lineTo(8,8);ctx.moveTo(8,-8);ctx.lineTo(-8,8);ctx.stroke();ctx.restore();
    }else if(s.type==="lizardTongue"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.20);ctx.save();ctx.globalAlpha=Math.sin(Math.PI*Math.min(1,q));ctx.strokeStyle=s.special?"#ff5577":"#ff7890";ctx.lineWidth=s.special?7:5;ctx.lineCap="round";ctx.shadowColor="#ff5d80";ctx.shadowBlur=12;ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.quadraticCurveTo((s.x+s.tx)/2,(s.y+s.ty)/2-10,s.tx,s.ty);ctx.stroke();ctx.fillStyle="#ff9aad";ctx.beginPath();ctx.arc(s.tx,s.ty,5,0,Math.PI*2);ctx.fill();ctx.restore();
    }else if(s.type==="lizardFrenzyBanner"){
      const a=Math.max(0,s.life/(s.maxLife||.48));ctx.save();ctx.globalAlpha=a;ctx.strokeStyle="#a9ff65";ctx.lineWidth=5;ctx.shadowColor="#7cff43";ctx.shadowBlur=20;for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(s.x,s.y,16+i*10+(1-a)*12,0,Math.PI*2);ctx.stroke();}ctx.restore();
    }else if(s.type==="scorpionStinger"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.32),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.shadowColor=s.special?"#c65cff":"#8cff60";ctx.shadowBlur=s.special?22:12;ctx.fillStyle=s.special?"#8d39d6":"#77bf46";ctx.beginPath();ctx.moveTo(18,0);ctx.lineTo(-10,-7);ctx.lineTo(-4,0);ctx.lineTo(-10,7);ctx.closePath();ctx.fill();ctx.restore();
    }else if(s.type==="scorpionVenomBurst"){
      const a=Math.max(0,s.life/(s.maxLife||.55)),r=18+(1-a)*42;ctx.save();ctx.globalAlpha=a;ctx.fillStyle="#8136c7";ctx.strokeStyle="#b9ff55";ctx.lineWidth=4;ctx.shadowColor="#a74cff";ctx.shadowBlur=22;ctx.beginPath();ctx.arc(s.x,s.y,r,0,Math.PI*2);ctx.fill();ctx.stroke();for(let i=0;i<7;i++){const an=i*Math.PI*2/7;ctx.fillStyle="#c8ff72";ctx.beginPath();ctx.arc(s.x+Math.cos(an)*r*.65,s.y+Math.sin(an)*r*.65,4,0,Math.PI*2);ctx.fill();}ctx.restore();
'''
s=s.replace(draw_anchor,draw+draw_anchor,1)

p.write_text(s,encoding='utf-8')
print('Added attacks + level 10 abilities for Peacock, Turtle, Lizard and Scorpion')
