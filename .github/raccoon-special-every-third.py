from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''  if(t.key==="raccoon"){
    const raccoonSpecial=t.level>=10;
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.48,maxLife:.48,type:"raccoonBin",special:raccoonSpecial});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }'''
new='''  if(t.key==="raccoon"){
    let raccoonSpecial=false;
    if(t.level>=10){
      t.raccoonAttackCount=(t.raccoonAttackCount||0)+1;
      raccoonSpecial=t.raccoonAttackCount%3===0;
    }
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.48,maxLife:.48,type:"raccoonBin",special:raccoonSpecial});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }'''
if old not in s: raise SystemExit('Raccoon attack block not found')
s=s.replace(old,new,1)
old_indicator='''    ctx.fillStyle="#fff3b0";ctx.font="bold 13px sans-serif";ctx.textAlign="center";ctx.fillText("SLOW",z.x,z.y-30);
'''
if old_indicator not in s: raise SystemExit('SLOW indicator marker not found')
s=s.replace(old_indicator,'',1)
p.write_text(s,encoding='utf-8')
