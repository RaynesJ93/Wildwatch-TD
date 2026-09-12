from pathlib import Path

p=Path('index.html')
s=p.read_text()
old='''  if(t.key==="seal"){
    const boltCount=t.level>=10?3:1;
    for(let i=0;i<boltCount;i++){
      battle.shots.push({
        x:t.x,y:t.y-7,tx:target.x,ty:target.y,
        life:.55+i*.08,maxLife:.55+i*.08,
        type:"sealWaterBolt",boltIndex:i
      });
    }
    const totalDamage=t.level>=10?dmg+(dmg*.5)+(dmg*.5):dmg;
    target.hp-=totalDamage;
    if(target.hp<=0)killEnemy(target);
  }
'''
new='''  if(t.key==="seal"){
    const boltCount=t.level>=10?3:1;
    for(let i=0;i<boltCount;i++){
      battle.shots.push({
        x:t.x,y:t.y-7,tx:target.x,ty:target.y,
        life:.55+i*.08,maxLife:.55+i*.08,
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
if old not in s:
    raise SystemExit('seal attack block not found')
if s.count(old)!=1:
    raise SystemExit(f'expected 1 seal block, found {s.count(old)}')
p.write_text(s.replace(old,new,1))
print('Removed generic follow-on attack from Seal by returning after custom water attack.')
