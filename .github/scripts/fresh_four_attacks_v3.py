from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Fresh descriptions while keeping the existing in-game balance stats/rarities.
desc_updates={
 'peacock':'Feather Shot: fires a sharp peacock feather. Level 10 Royal Fan: every 6th attack fires 7 golden feathers across enemies in range, each dealing 90% damage.',
 'turtle':'Shell Throw: hurls a spinning shell. Level 10 Shell Ricochet: every 5th attack hits the first target normally then bounces to up to 4 more enemies for 80% damage each.',
 'lizard':'Tongue Lash: snaps a long tongue at the target. Level 10 Toxic Spray: every 7th attack lashes 5 times for 50% damage each and applies a 4-second poison dealing 50% damage per second.',
 'scorpion':'Stinger Shot: fires a venomous stinger and builds poison. Level 10 Venom Burst: every 6th attack deals 2x impact damage and creates a 6-second poison cloud around the target.'
}
for key,desc in desc_updates.items():
    pat=rf'({key}:\{{name:"[^"]+",emoji:"[^"]+",rarity:"[^"]+",cost:[^,]+,range:[^,]+,rate:[^,]+,dmg:[^,]+,color:"[^"]+",desc:")[^"]*("\}})'
    s,n=re.subn(pat,lambda m:m.group(1)+desc+m.group(2),s,count=1)
    if n!=1:
        raise RuntimeError(f'description anchor missing for {key}')

# Replace the entire previous four-animal attack block with a clean V3 block.
start=s.find('  // PEACOCK_TURTLE_LIZARD_SCORPION_ATTACKS_V1')
if start<0:
    start=s.find('  if(t.key==="peacock"){')
end=s.find('  if(t.key==="parrot" && t.level>=10){',start)
if start<0 or end<0:
    raise RuntimeError('four-animal attack block anchors missing')

logic=r'''  // FRESH_FOUR_ATTACKS_V3: rebuilt from scratch; no generic beam/projectile is created for these four.
  if(t.key==="peacock"){
    t.peacockFreshCount=(t.peacockFreshCount||0)+1;
    const royal=t.level>=10 && t.peacockFreshCount%6===0;
    if(royal){
      const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);
      for(let i=0;i<7;i++){
        const hit=pool.length?pool[i%pool.length]:target;
        if(!hit||hit.dead)break;
        hit.hp-=dmg*.90;
        battle.shots.push({x:t.x,y:t.y-8,tx:hit.x,ty:hit.y,life:.34+i*.035,maxLife:.34+i*.035,type:"peacockRoyalFeatherV3",fanIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.36,maxLife:.36,type:"peacockFeatherV3"});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="turtle"){
    t.turtleFreshCount=(t.turtleFreshCount||0)+1;
    const ricochet=t.level>=10 && t.turtleFreshCount%5===0;
    target.hp-=dmg;
    battle.shots.push({x:t.x,y:t.y-3,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:ricochet?"turtleRicochetV3":"turtleShellV3",bounceIndex:0});
    if(target.hp<=0)killEnemy(target);
    if(ricochet){
      const hits=battle.enemies.filter(e=>!e.dead&&e!==target&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range).slice(0,4);
      let bx=target.x,by=target.y;
      hits.forEach((e,i)=>{
        e.hp-=dmg*.80;
        battle.shots.push({x:bx,y:by,tx:e.x,ty:e.y,life:.24+i*.045,maxLife:.24+i*.045,type:"turtleRicochetV3",bounceIndex:i+1});
        if(e.hp<=0)killEnemy(e);bx=e.x;by=e.y;
      });
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="lizard"){
    t.lizardFreshCount=(t.lizardFreshCount||0)+1;
    const toxic=t.level>=10 && t.lizardFreshCount%7===0;
    if(toxic){
      for(let i=0;i<5;i++){
        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);
        const hit=pool.length?pool[i%pool.length]:target;
        if(!hit||hit.dead)break;
        hit.hp-=dmg*.50;
        hit.poison=Math.max(hit.poison||0,4);
        hit.poisonTick=Math.min(hit.poisonTick||1,1);
        hit.poisonDmg=Math.max(hit.poisonDmg||0,dmg*.50);
        battle.shots.push({x:t.x,y:t.y-5,tx:hit.x,ty:hit.y,life:.18+i*.04,maxLife:.18+i*.04,type:"lizardToxicLashV3",lashIndex:i});
        if(hit.hp<=0)killEnemy(hit);
      }
    }else{
      target.hp-=dmg;
      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.20,maxLife:.20,type:"lizardTongueV3"});
      if(target.hp<=0)killEnemy(target);
    }
    t.cd=cardRate(t.key);return;
  }

  if(t.key==="scorpion"){
    t.scorpionFreshCount=(t.scorpionFreshCount||0)+1;
    const burst=t.level>=10 && t.scorpionFreshCount%6===0;
    target.hp-=burst?dmg*2:dmg;
    target.poison=Math.max(target.poison||0,4);
    target.poisonTick=Math.min(target.poisonTick||1,1);
    target.poisonDmg=Math.min(dmg*.60,(target.poisonDmg||0)+dmg*.15);
    battle.shots.push({x:t.x,y:t.y-6,tx:target.x,ty:target.y,life:burst?.38:.30,maxLife:burst?.38:.30,type:burst?"scorpionBurstStingerV3":"scorpionStingerV3"});
    if(burst){
      battle.scorpionClouds=battle.scorpionClouds||[];
      battle.scorpionClouds.push({x:target.x,y:target.y,life:6,maxLife:6,tick:.1,radius:74,damage:dmg*.30});
    }
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);return;
  }

'''
s=s[:start]+logic+s[end:]

# The generic fallback must still exclude these four at source.
old='''  }else{\n    battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:'''
if old in s:
    s=s.replace(old,'''  }else if(!["peacock","turtle","lizard","scorpion"].includes(t.key)){\n    battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:''',1)

# Remove these animals from the old visibility helper so no laser/glow overlay is added.
for token in ['"peacockFeather",','"peacockRoyalFeather",','"peacockRoyalFanBanner",','"turtleShell",','"lizardTongue",','"lizardFrenzyBanner",','"scorpionStinger",','"scorpionVenomBurst",']:
    s=s.replace(token,'')

# Replace the old dedicated renderers with clean, readable V3 effects using only canvas/in-game rendering.
rstart=s.find('    }else if(s.type==="peacockFeather"||s.type==="peacockRoyalFeather"){')
rend=s.find('    }else if(s.type==="sealWaterBolt"){',rstart)
if rstart<0 or rend<0:
    raise RuntimeError('old custom renderer block anchors missing')
render=r'''    }else if(s.type==="peacockFeatherV3"||s.type==="peacockRoyalFeatherV3"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.36),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.strokeStyle=s.type==="peacockRoyalFeatherV3"?"#f4cf4b":"#32c9b8";ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-15,0);ctx.quadraticCurveTo(0,-8,16,0);ctx.quadraticCurveTo(0,8,-15,0);ctx.stroke();ctx.fillStyle=s.type==="peacockRoyalFeatherV3"?"#f7df78":"#3b8ec9";ctx.beginPath();ctx.arc(5,0,4,0,Math.PI*2);ctx.fill();ctx.restore();
    }else if(s.type==="turtleShellV3"||s.type==="turtleRicochetV3"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.42),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*7);ctx.fillStyle="#536f42";ctx.strokeStyle=s.type==="turtleRicochetV3"?"#d6c76c":"#9fbd76";ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,s.type==="turtleRicochetV3"?13:11,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.strokeStyle="#80965f";ctx.beginPath();ctx.moveTo(-7,-7);ctx.lineTo(7,7);ctx.moveTo(7,-7);ctx.lineTo(-7,7);ctx.stroke();ctx.restore();
    }else if(s.type==="lizardTongueV3"||s.type==="lizardToxicLashV3"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.20);ctx.save();ctx.globalAlpha=Math.sin(Math.PI*Math.min(1,q));ctx.strokeStyle=s.type==="lizardToxicLashV3"?"#8bd34a":"#e97483";ctx.lineWidth=s.type==="lizardToxicLashV3"?6:5;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.quadraticCurveTo((s.x+s.tx)/2,(s.y+s.ty)/2-8,s.tx,s.ty);ctx.stroke();ctx.restore();
    }else if(s.type==="scorpionStingerV3"||s.type==="scorpionBurstStingerV3"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.30),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.fillStyle=s.type==="scorpionBurstStingerV3"?"#8d4bb7":"#7f9b43";ctx.beginPath();ctx.moveTo(16,0);ctx.lineTo(-9,-6);ctx.lineTo(-3,0);ctx.lineTo(-9,6);ctx.closePath();ctx.fill();ctx.restore();
'''
s=s[:rstart]+render+s[rend:]

# Add poison-cloud gameplay and drawing once, immediately after enemies move.
cloud_marker='SCORPION_VENOM_CLOUDS_V3'
if cloud_marker not in s:
    anchor='  battle.enemies.forEach(e=>moveEnemy(e,dt));\n'
    if anchor not in s: raise RuntimeError('enemy movement anchor missing')
    cloud=r'''  // SCORPION_VENOM_CLOUDS_V3
  battle.scorpionClouds=battle.scorpionClouds||[];
  for(const c of battle.scorpionClouds){
    c.life-=dt;c.tick-=dt;
    if(c.tick<=0){c.tick+=1;for(const e of battle.enemies){if(!e.dead&&e.hp>0&&Math.hypot(e.x-c.x,e.y-c.y)<=c.radius){e.hp-=c.damage;if(e.hp<=0)killEnemy(e);}}}
    ctx.save();ctx.globalAlpha=Math.max(0,.20*(c.life/c.maxLife));ctx.fillStyle="#6f3b7f";ctx.beginPath();ctx.arc(c.x,c.y,c.radius,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.45;ctx.strokeStyle="#9860a8";ctx.lineWidth=3;ctx.stroke();ctx.restore();
  }
  battle.scorpionClouds=battle.scorpionClouds.filter(c=>c.life>0);
'''
    s=s.replace(anchor,anchor+cloud,1)

p.write_text(s,encoding='utf-8')
print('Fresh V3 attacks installed for Peacock Turtle Lizard Scorpion')
