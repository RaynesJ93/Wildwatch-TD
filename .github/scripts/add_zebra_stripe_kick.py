from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Update Zebra description.
old='zebra:{name:"Zebra",emoji:"🦓",rarity:"Legendary",cost:175,range:215,rate:1/1.05,dmg:58,color:"#eee",desc:"Fast long-range attacker."},'
new='zebra:{name:"Zebra",emoji:"🦓",rarity:"Legendary",cost:175,range:215,rate:1/1.05,dmg:58,color:"#eee",desc:"Fires striped shockwaves. At Level 10, every 8th attack becomes Stampede Stripes: 2x damage to the target, pierces nearby enemies for 75% damage and slows them by 25% for 2s."},'
if old not in s:
    raise SystemExit('zebra card anchor not found')
s=s.replace(old,new,1)

# Add Zebra attack behaviour before the generic projectile fallback.
anchor='''  if(t.key==="parrot" && t.level>=10){
    t.parrotPineappleCount=(t.parrotPineappleCount||0)+1;
    parrotBomb=t.parrotPineappleCount%3===0;
  }
'''
zebra='''  if(t.key==="zebra"){
    let stampede=false;
    if(t.level>=10){
      t.zebraAttackCount=(t.zebraAttackCount||0)+1;
      stampede=t.zebraAttackCount%8===0;
    }
    battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:stampede?.42:.28,maxLife:stampede?.42:.28,type:"zebraStripeKick",special:stampede});
    if(stampede){
      target.hp-=dmg*2;
      target.zebraSlowTimer=Math.max(target.zebraSlowTimer||0,2);
      const targetProg=target.seg+(1-Math.hypot(target.x-t.x,target.y-t.y)/1000);
      battle.enemies.forEach(e=>{
        if(e.dead||e===target)return;
        const prog=e.seg+(1-Math.hypot(e.x-t.x,e.y-t.y)/1000);
        if(Math.hypot(e.x-target.x,e.y-target.y)<=120 && prog<=targetProg){
          e.hp-=dmg*.75;
          e.zebraSlowTimer=Math.max(e.zebraSlowTimer||0,2);
          if(e.hp<=0)killEnemy(e);
        }
      });
    }else{
      target.hp-=dmg;
    }
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }

'''
if anchor not in s:
    raise SystemExit('towerTick generic anchor not found')
s=s.replace(anchor,zebra+anchor,1)

# Add 25% Zebra slow handling without changing the existing stronger slow effects.
old_move='''  if(e.slowTimer>0)e.slowTimer-=dt;
  if(e.hp<=0){killEnemy(e);return}
  if((e.freezeTimer||0)>0){
    e.freezeTimer=Math.max(0,e.freezeTimer-dt);
    return;
  }
  let mult=e.slowTimer>0?.55:1, dist=e.speed*mult*dt;'''
new_move='''  if(e.slowTimer>0)e.slowTimer-=dt;
  if((e.zebraSlowTimer||0)>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);
  if(e.hp<=0){killEnemy(e);return}
  if((e.freezeTimer||0)>0){
    e.freezeTimer=Math.max(0,e.freezeTimer-dt);
    return;
  }
  let mult=e.slowTimer>0?.55:(e.zebraSlowTimer||0)>0?.75:1, dist=e.speed*mult*dt;'''
if old_move not in s:
    raise SystemExit('enemy movement slow anchor not found')
s=s.replace(old_move,new_move,1)

# Draw Zebra Stripe Kick before the existing water projectile renderer.
render_anchor='''    }else if(s.type==="water"){
'''
render='''    }else if(s.type==="zebraStripeKick"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.28);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const dx=s.tx-s.x,dy=s.ty-s.y,ang=Math.atan2(dy,dx);
      const scale=s.special?1.45:1;
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      ctx.globalAlpha=.92;
      ctx.lineCap="round";
      ctx.shadowColor="rgba(255,255,255,.35)";ctx.shadowBlur=s.special?9:4;
      for(let i=-2;i<=2;i++){
        ctx.strokeStyle=i%2===0?"#f5f5f5":"#171717";
        ctx.lineWidth=(s.special?5:3.4)*scale;
        ctx.beginPath();
        ctx.moveTo(-20*scale,i*5*scale);
        ctx.quadraticCurveTo(0,-i*3*scale,20*scale,i*5*scale);
        ctx.stroke();
      }
      ctx.fillStyle="#c9b18a";
      ctx.globalAlpha=.7;
      for(let i=0;i<(s.special?5:3);i++){
        const px=-22*scale-i*7,py=((i%2)*2-1)*5;
        ctx.beginPath();ctx.arc(px,py,2.2+(s.special?1:0),0,Math.PI*2);ctx.fill();
      }
      if(s.special){
        ctx.globalAlpha=.82;
        ctx.strokeStyle="#ffffff";ctx.lineWidth=2;
        ctx.beginPath();ctx.ellipse(0,0,30,13,0,0,Math.PI*2);ctx.stroke();
      }
      ctx.restore();
'''
if render_anchor not in s:
    raise SystemExit('projectile render anchor not found')
s=s.replace(render_anchor,render+render_anchor,1)

p.write_text(s,encoding='utf-8')
print('Added Zebra Stripe Kick and Level 10 Stampede Stripes ability')
