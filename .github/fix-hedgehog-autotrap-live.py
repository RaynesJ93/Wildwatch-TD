from pathlib import Path
p=Path('index.html'); s=p.read_text()
# Slow Hedgehog attack: about one stack every 3 seconds.
s=s.replace('hedgehog:{name:"Hedgehog",emoji:"🦔",rarity:"Common",cost:60,range:135,rate:1,dmg:12,color:"#76543b"','hedgehog:{name:"Hedgehog",emoji:"🦔",rarity:"Common",cost:60,range:135,rate:3,dmg:12,color:"#76543b"',1)
old='''  let target=null,best=-1;
  battle.enemies.forEach(e=>{if(e.dead)return;const d=Math.hypot(e.x-t.x,e.y-t.y);if(d<=range){const prog=e.seg+(1-d/1000);if(prog>best){best=prog;target=e}}});
  if(!target)return;
  if(t.key==="hedgehog"){
    battle.needles=battle.needles||[];
    const id=(battle.nextNeedleId=(battle.nextNeedleId||0)+1);
    battle.shots.push({x:t.x,y:t.y-9,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:"hedgehogNeedles",needleTrapId:id});
    t.cd=cardRate(t.key);
    return;
  }'''
new='''  let target=null,best=-1;
  battle.enemies.forEach(e=>{if(e.dead)return;const d=Math.hypot(e.x-t.x,e.y-t.y);if(d<=range){const prog=e.seg+(1-d/1000);if(prog>best){best=prog;target=e}}});
  if(t.key==="hedgehog"){
    // Always place a trap during an active wave, even when no enemy is nearby.
    if(!battle.waveActive){t.cd=.25;return;}
    let tx,ty;
    if(target){tx=target.x;ty=target.y;}
    else{
      const candidates=[];
      for(let i=0;i<path.length-1;i++){
        const [ax,ay]=path[i],[bx,by]=path[i+1];
        for(let j=0;j<=16;j++){
          const q=j/16,x=ax+(bx-ax)*q,y=ay+(by-ay)*q;
          if(Math.hypot(x-t.x,y-t.y)<=range)candidates.push([x,y]);
        }
      }
      if(!candidates.length){t.cd=.5;return;}
      const pick=candidates[Math.floor(Math.random()*candidates.length)];
      tx=pick[0];ty=pick[1];
    }
    battle.needles=battle.needles||[];
    const id=(battle.nextNeedleId=(battle.nextNeedleId||0)+1);
    battle.shots.push({x:t.x,y:t.y-9,tx,ty,life:.42,maxLife:.42,type:"hedgehogNeedles",needleTrapId:id});
    t.cd=cardRate(t.key);
    return;
  }
  if(!target)return;'''
if old not in s: raise SystemExit('CURRENT hedgehog block not found')
s=s.replace(old,new,1)
p.write_text(s)
