from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_attack='''  if(t.key==="pig"){
    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.44,maxLife:.44,type:"pigHam"});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }'''
new_attack='''  if(t.key==="pig"){
    let pigSpecial=false;
    if(t.level>=10){
      t.pigAttackCount=(t.pigAttackCount||0)+1;
      pigSpecial=t.pigAttackCount%3===0;
    }
    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.44,maxLife:.44,type:"pigHam",special:pigSpecial});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }'''
if old_attack not in s: raise SystemExit('Pig attack block not found')
s=s.replace(old_attack,new_attack,1)

move_anchor='''function moveEnemy(e,dt){\n'''
if move_anchor not in s: raise SystemExit('moveEnemy anchor not found')
if 'e.pigStop' not in s:
    s=s.replace(move_anchor,move_anchor+'''  if((e.pigStop||0)>0){e.pigStop=Math.max(0,e.pigStop-dt);return;}\n''',1)

zone_anchor='''  battle.eggSplashes=battle.eggSplashes||[];'''
if zone_anchor not in s: raise SystemExit('egg splash update anchor not found')
zone_update='''  battle.pigHamZones=battle.pigHamZones||[];
  battle.pigHamZones.forEach(z=>{
    z.life-=dt;
    battle.enemies.forEach(e=>{
      if(e.dead)return;
      if(Math.hypot(e.x-z.x,e.y-z.y)<=z.radius)e.pigStop=Math.max(e.pigStop||0,3);
    });
  });
  battle.pigHamZones=battle.pigHamZones.filter(z=>z.life>0);
'''
if 'battle.pigHamZones=battle.pigHamZones||[];' not in s:
    s=s.replace(zone_anchor,zone_update+zone_anchor,1)

shot_anchor='''  battle.shots.forEach(s=>{\n    if(s.type==="gooseEgg" && s.special && !s.splashed && s.life-dt<=0){'''
if shot_anchor not in s: raise SystemExit('shot landing anchor not found')
shot_new='''  battle.shots.forEach(s=>{
    if(s.type==="pigHam" && s.special && !s.dropped && s.life-dt<=0){
      s.dropped=true;
      battle.pigHamZones=battle.pigHamZones||[];
      battle.pigHamZones.push({x:s.tx,y:s.ty,life:3,maxLife:3,radius:78});
    }
    if(s.type==="gooseEgg" && s.special && !s.splashed && s.life-dt<=0){'''
s=s.replace(shot_anchor,shot_new,1)

draw_anchor='''  (battle.eggSplashes||[]).forEach(z=>{'''
if draw_anchor not in s: raise SystemExit('zone draw anchor not found')
zone_draw='''  (battle.pigHamZones||[]).forEach(z=>{
    const a=Math.max(.25,Math.min(1,z.life/z.maxLife));
    ctx.save();ctx.globalAlpha=a;
    ctx.font="34px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("🥓",z.x-16,z.y+2);ctx.fillText("🥓",z.x+16,z.y-4);ctx.fillText("🥓",z.x,z.y+18);
    ctx.restore();
  });
'''
if '(battle.pigHamZones||[]).forEach' not in s:
    s=s.replace(draw_anchor,zone_draw+draw_anchor,1)

p.write_text(s,encoding='utf-8')
print('Pig level 10 special added: every 3rd attack leaves bacon on track and stops enemies for 3 seconds')
