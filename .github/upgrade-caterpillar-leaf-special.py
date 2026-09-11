from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Caterpillar data: force base damage to 12 and update description.
pat=r'caterpillar:\{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1\.20,dmg:\d+,color:"#7c5",desc:"[^"]*"\}'
rep='caterpillar:{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1.20,dmg:12,color:"#7c5",desc:"Fires leaves; at tower level 10 every 4th attack launches a giant leaf for 5x base damage."}'
s,n=re.subn(pat,rep,s,count=1)
if n!=1: raise SystemExit(f'Caterpillar data marker problem: {n}')

# Caterpillar attack logic. Add only if it is not already present.
if 't.caterpillarAttackCount' not in s:
    anchor='  let parrotBomb=false;\n'
    if anchor not in s: raise SystemExit('Parrot attack anchor not found')
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

# Caterpillar projectile rendering. Insert at the top of the shot draw callback
# so it doesn't depend on which projectile branch currently comes first.
if 's.type==="caterpillarLeaf"||s.type==="caterpillarBigLeaf"' not in s:
    anchor='  battle.shots?.forEach(s=>{\n'
    if anchor not in s: raise SystemExit('Shot draw callback anchor not found')
    draw='''    if(s.type==="caterpillarLeaf"||s.type==="caterpillarBigLeaf"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.42);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*18;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*2.5);
      ctx.font=(s.type==="caterpillarBigLeaf"?"58px":"26px")+" sans-serif";
      ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🍃",0,0);ctx.restore();
      return;
    }
'''
    s=s.replace(anchor,anchor+draw,1)

# Fail loudly if the expected final state is not present.
checks=[
    'caterpillar:{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1.20,dmg:12',
    't.caterpillarAttackCount',
    'caterpillarBigLeaf',
    'animals.caterpillar.dmg*5',
]
for c in checks:
    if c not in s: raise SystemExit(f'Missing Caterpillar final marker: {c}')

p.write_text(s,encoding='utf-8')
print('Caterpillar fixed: base damage 12, leaf projectile, level-10 every-4th giant leaf for 5x base damage')
