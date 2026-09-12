from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Update Mouse card description.
old_desc='mouse:{name:"Mouse",emoji:"🐭",rarity:"Common",cost:45,range:125,rate:1/1.45,dmg:7,color:"#aaa",desc:"Quick basic attacker."}'
new_desc='mouse:{name:"Mouse",emoji:"🐭",rarity:"Common",cost:45,range:125,rate:1/1.45,dmg:7,color:"#aaa",desc:"Throws spinning cheese wedges. At tower level 10, every 6th attack becomes Cheese Frenzy: a giant cheese wheel deals 2.5x damage and bounces to up to 3 nearby enemies for 75% damage."}'
if old_desc not in s:
    raise SystemExit('mouse description anchor not found')
s=s.replace(old_desc,new_desc,1)

# Add Mouse-specific attack logic before Zebra handling.
anchor='''  if(t.key==="zebra"){
'''
mouse_logic='''  if(t.key==="mouse"){
    let cheeseFrenzy=false;
    if(t.level>=10){
      t.mouseAttackCount=(t.mouseAttackCount||0)+1;
      cheeseFrenzy=t.mouseAttackCount%6===0;
    }
    battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:cheeseFrenzy?.42:.30,maxLife:cheeseFrenzy?.42:.30,type:cheeseFrenzy?"mouseCheeseWheel":"mouseCheeseWedge",special:cheeseFrenzy});
    if(cheeseFrenzy){
      target.hp-=dmg*2.5;
      if(target.hp<=0)killEnemy(target);
      const bounceTargets=battle.enemies
        .filter(e=>!e.dead&&e!==target&&Math.hypot(e.x-target.x,e.y-target.y)<=150)
        .sort((a,b)=>Math.hypot(a.x-target.x,a.y-target.y)-Math.hypot(b.x-target.x,b.y-target.y))
        .slice(0,3);
      let bx=target.x,by=target.y;
      bounceTargets.forEach((e,i)=>{
        battle.shots.push({x:bx,y:by,tx:e.x,ty:e.y,life:.24+i*.05,maxLife:.24+i*.05,type:"mouseCheeseBounce",bounceIndex:i});
        e.hp-=dmg*.75;
        if(e.hp<=0)killEnemy(e);
        bx=e.x;by=e.y;
      });
    }else{
      target.hp-=dmg;
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);
    return;
  }

'''
if anchor not in s:
    raise SystemExit('zebra attack anchor not found')
s=s.replace(anchor,mouse_logic+anchor,1)

# Add Mouse projectile rendering immediately before Zebra's renderer.
render_anchor='''    }else if(s.type==="zebraStripeKick"){
'''
mouse_render='''    }else if(s.type==="mouseCheeseWedge"||s.type==="mouseCheeseWheel"||s.type==="mouseCheeseBounce"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.30);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const dx=s.tx-s.x,dy=s.ty-s.y,ang=Math.atan2(dy,dx);
      const wheel=s.type!=="mouseCheeseWedge";
      const spin=q*Math.PI*(wheel?7:5);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang+spin);
      ctx.shadowColor="#f0c63a";ctx.shadowBlur=wheel?10:5;
      ctx.fillStyle=wheel?"#f3c83f":"#ffd85a";
      ctx.strokeStyle="#a87616";ctx.lineWidth=1.5;
      if(wheel){
        ctx.beginPath();ctx.arc(0,0,s.special?9:6,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.fillStyle="#9e7418";
        [[-3,-2],[3,2],[1,-4]].forEach(([hx,hy])=>{ctx.beginPath();ctx.arc(hx,hy,1.3,0,Math.PI*2);ctx.fill();});
      }else{
        ctx.beginPath();ctx.moveTo(8,0);ctx.lineTo(-7,-6);ctx.lineTo(-7,6);ctx.closePath();ctx.fill();ctx.stroke();
        ctx.fillStyle="#9e7418";ctx.beginPath();ctx.arc(-2,0,1.2,0,Math.PI*2);ctx.fill();
      }
      ctx.restore();
      ctx.save();ctx.globalAlpha=.85;ctx.fillStyle="#ffd85a";
      for(let i=0;i<3;i++){
        const back=(i+1)*7;
        const px=x-Math.cos(ang)*back,py=y-Math.sin(ang)*back+(i-1)*2;
        ctx.beginPath();ctx.arc(px,py,1.4,0,Math.PI*2);ctx.fill();
      }
      if(q>.82){
        const impact=(q-.82)/.18;
        ctx.globalAlpha=Math.max(0,.85-impact*.6);
        for(let i=0;i<5;i++){
          const a=(Math.PI*2*i/5)+.25;
          const r=4+impact*10;
          ctx.beginPath();ctx.arc(s.tx+Math.cos(a)*r,s.ty+Math.sin(a)*r,1.5,0,Math.PI*2);ctx.fill();
        }
      }
      ctx.restore();
'''
if render_anchor not in s:
    raise SystemExit('zebra renderer anchor not found')
s=s.replace(render_anchor,mouse_render+render_anchor,1)

p.write_text(s,encoding='utf-8')
print('Added Mouse Cheese Chuck animation and Level 10 Cheese Frenzy ability')
