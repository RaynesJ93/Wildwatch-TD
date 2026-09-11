from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Caterpillar base damage -> 12 and description update.
pat=r'caterpillar:\{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1\.20,dmg:\d+,color:"#7c5",desc:"[^"]*"\}'
rep='caterpillar:{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1.20,dmg:12,color:"#7c5",desc:"Fires leaves; at tower level 10 every 4th attack launches a giant leaf for 5x base damage."}'
s2,n=re.subn(pat,rep,s,count=1)
if n!=1: raise SystemExit(f'caterpillar data marker not found or duplicated: {n}')
s=s2

# 2) Add Caterpillar attack logic before the Parrot block.
anchor='''  let parrotBomb=false;\n'''
if anchor not in s: raise SystemExit('parrot attack anchor not found')
block='''  if(t.key==="caterpillar"){
    let bigLeaf=false;
    if(t.level>=10){
      t.caterpillarAttackCount=(t.caterpillarAttackCount||0)+1;
      bigLeaf=t.caterpillarAttackCount%4===0;
    }
    battle.shots.push({x:t.x,y:t.y-6,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:bigLeaf?"caterpillarBigLeaf":"caterpillarLeaf"});
    const leafDamage=bigLeaf?animals.caterpillar.dmg*5:dmg;
    target.hp-=leafDamage;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }

'''
s=s.replace(anchor,block+anchor,1)

# 3) Add leaf projectile rendering before Raccoon projectile rendering.
draw_anchor='''    if(s.type==="raccoonBin"){'''
if draw_anchor not in s: raise SystemExit('projectile draw anchor not found')
draw='''    if(s.type==="caterpillarLeaf"||s.type==="caterpillarBigLeaf"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.42);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*18;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*2.5);
      ctx.font=(s.type==="caterpillarBigLeaf"?"58px":"26px")+" sans-serif";
      ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🍃",0,0);ctx.restore();
    }else if(s.type==="raccoonBin"){'''
s=s.replace(draw_anchor,draw,1)

p.write_text(s,encoding='utf-8')
print('Updated Caterpillar: 12 base damage, leaf projectile, level-10 every-4th giant leaf for 5x base damage')
