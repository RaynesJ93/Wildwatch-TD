from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Insert Seal attack logic immediately before the Tiger attack block.
anchor='''  if(t.key==="tiger"){'''
if anchor not in s:
    raise SystemExit('Tiger attack anchor not found')
if 'if(t.key==="seal")' not in s:
    block='''  if(t.key==="seal"){
    const boltCount=t.level>=10?3:1;
    for(let i=0;i<boltCount;i++){
      battle.shots.push({
        x:t.x,y:t.y-7,tx:target.x,ty:target.y,
        life:.34+i*.08,maxLife:.34+i*.08,
        type:"sealWaterBolt",boltIndex:i
      });
    }
    const totalDamage=t.level>=10?dmg+(dmg*.5)+(dmg*.5):dmg;
    target.hp-=totalDamage;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }

'''
    s=s.replace(anchor,block+anchor,1)

# Add drawing before the Tiger swipe renderer, which is definitely present now.
draw_anchor='''    if(s.type==="tigerSwipe"){'''
if draw_anchor not in s:
    raise SystemExit('Tiger swipe draw anchor not found')
if 's.type==="sealWaterBolt"' not in s:
    draw='''    if(s.type==="sealWaterBolt"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.34);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const dx=s.tx-s.x,dy=s.ty-s.y,ang=Math.atan2(dy,dx);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      ctx.globalAlpha=.95;
      ctx.fillStyle="#55cfff";ctx.strokeStyle="#d9f8ff";ctx.lineWidth=2;
      ctx.beginPath();ctx.ellipse(0,0,15,7,0,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle="#aeeeff";
      ctx.beginPath();ctx.moveTo(-10,-5);ctx.lineTo(-22,0);ctx.lineTo(-10,5);ctx.closePath();ctx.fill();
      ctx.restore();
    }else if(s.type==="tigerSwipe"){'''
    s=s.replace(draw_anchor,draw,1)

if 'if(t.key==="seal")' not in s or 's.type==="sealWaterBolt"' not in s:
    raise SystemExit('Seal attack or renderer missing after patch')

p.write_text(s,encoding='utf-8')
print('Seal water bolt attack and level 10 triple-bolt special applied')
