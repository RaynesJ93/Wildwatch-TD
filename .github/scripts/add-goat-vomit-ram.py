from pathlib import Path

p=Path('index.html')
s=p.read_text()

old='goat:{name:"Goat",emoji:"🐐",rarity:"Uncommon",cost:88,range:160,rate:1/.90,dmg:25,color:"#ddd",desc:"Strong attacker."},'
new='goat:{name:"Goat",emoji:"🐐",rarity:"Uncommon",cost:88,range:160,rate:1/.90,dmg:25,color:"#ddd",desc:"Vomit Spray attacks enemies. Every 5th attack poisons. At Level 10, every 5th attack becomes Ram Rage: 3x damage and confuses the target."},'
if old not in s: raise SystemExit('goat card definition not found')
s=s.replace(old,new,1)

anchor='  if(t.key==="mouse"){\n'
if anchor not in s: raise SystemExit('mouse branch anchor not found')
branch='''  if(t.key==="goat"){
    t.goatAttackCount=(t.goatAttackCount||0)+1;
    const fifth=t.goatAttackCount%5===0;
    const ram=t.level>=10&&fifth;
    if(ram){
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.52,maxLife:.52,type:"goatRam"});
      target.hp-=dmg*3;
      target.goatConfuseTimer=Math.max(target.goatConfuseTimer||0,2.5);
      if(target.hp<=0)killEnemy(target);
    }else{
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:"goatVomit",special:fifth});
      target.hp-=dmg;
      if(fifth){
        target.poison=Math.max(target.poison||0,6);
        target.poisonTick=Math.min(target.poisonTick||2,2);
        target.poisonDmg=Math.max(target.poisonDmg||0,dmg*.25);
      }
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

'''
s=s.replace(anchor,branch+anchor,1)

oldmove='''  if(e.slowTimer>0)e.slowTimer-=dt;
  if((e.zebraSlowTimer||0)>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);
  if(e.hp<=0){killEnemy(e);return}
'''
newmove='''  if(e.slowTimer>0)e.slowTimer-=dt;
  if((e.zebraSlowTimer||0)>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);
  if((e.goatConfuseTimer||0)>0)e.goatConfuseTimer=Math.max(0,e.goatConfuseTimer-dt);
  if(e.hp<=0){killEnemy(e);return}
'''
if oldmove not in s: raise SystemExit('enemy status anchor not found')
s=s.replace(oldmove,newmove,1)
oldmult='let mult=e.slowTimer>0?.55:(e.zebraSlowTimer||0)>0?.75:1, dist=e.speed*mult*dt;'
newmult='let mult=e.slowTimer>0?.55:(e.zebraSlowTimer||0)>0?.75:(e.goatConfuseTimer||0)>0?.50:1, dist=e.speed*mult*dt;'
if oldmult not in s: raise SystemExit('enemy speed multiplier anchor not found')
s=s.replace(oldmult,newmult,1)

render_anchor='''    }else if(s.type==="mouseCheeseWedge"||s.type==="mouseCheeseWheel"||s.type==="mouseCheeseBounce"){
'''
if render_anchor not in s: raise SystemExit('shot renderer anchor not found')
render='''    }else if(s.type==="goatVomit"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.42),x=s.x+(s.tx-s.x)*q,y=(s.y-7)+(s.ty-(s.y-7))*q;
      const ang=Math.atan2(s.ty-(s.y-7),s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.globalAlpha=.92;
      ctx.strokeStyle=s.special?"#9df34d":"#78c83e";ctx.lineWidth=s.special?9:7;ctx.lineCap="round";ctx.shadowColor="#8eff43";ctx.shadowBlur=8;
      ctx.beginPath();ctx.moveTo(-18,0);ctx.quadraticCurveTo(-6,-5,8,1);ctx.lineTo(18,0);ctx.stroke();ctx.restore();
      ctx.save();ctx.fillStyle=s.special?"#b7ff62":"#87d94c";ctx.globalAlpha=.8;
      for(let i=0;i<5;i++){const tq=Math.max(0,q-i*.04),dx=s.x+(s.tx-s.x)*tq,dy=(s.y-7)+(s.ty-(s.y-7))*tq;ctx.beginPath();ctx.arc(dx,dy+(i%2?4:-3),2.5+(i%2),0,Math.PI*2);ctx.fill();}ctx.restore();
      if(q>.78){const a=Math.max(0,1-(q-.78)/.22);ctx.save();ctx.translate(s.tx,s.ty);ctx.globalAlpha=a;ctx.fillStyle=s.special?"#a8f14e":"#73bd3b";for(let i=0;i<7;i++){const an=i*.9;ctx.beginPath();ctx.ellipse(Math.cos(an)*12,Math.sin(an)*8,5,2.5,an,0,Math.PI*2);ctx.fill();}ctx.restore();}
    }else if(s.type==="goatRam"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.52),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      ctx.save();ctx.translate(x,y);ctx.globalAlpha=.98;ctx.font="28px 'Apple Color Emoji','Segoe UI Emoji'";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🐐",0,0);ctx.restore();
      if(q>.72){const a=Math.max(0,1-(q-.72)/.28);ctx.save();ctx.translate(s.tx,s.ty);ctx.globalAlpha=a;ctx.strokeStyle="#f5e7c4";ctx.lineWidth=4;ctx.beginPath();ctx.arc(0,0,12+(q-.72)*45,0,Math.PI*2);ctx.stroke();ctx.font="18px system-ui";ctx.fillText("❓",-13,-18);ctx.fillText("❓",12,-22);ctx.restore();}
'''
s=s.replace(render_anchor,render+render_anchor,1)

health_anchor='''    const bw=44,bh=7;
'''
confuse='''    if((e.goatConfuseTimer||0)>0){
      ctx.save();ctx.globalAlpha=.95;ctx.font="16px system-ui";ctx.textAlign="center";ctx.fillText("❓",e.x-10,e.y-e.size-15);ctx.fillText("❔",e.x+10,e.y-e.size-20);ctx.restore();
    }
'''
if health_anchor not in s: raise SystemExit('enemy render anchor not found')
s=s.replace(health_anchor,confuse+health_anchor,1)

p.write_text(s)
print('Goat Vomit Spray, poison and Level 10 Ram Rage added')
