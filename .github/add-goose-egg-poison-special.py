from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''  if(t.key==="raccoon"){
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
  }

  let parrotBomb=false;'''
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
  }

  if(t.key==="goose"){
    let gooseSpecial=false;
    if(t.level>=10){
      t.gooseAttackCount=(t.gooseAttackCount||0)+1;
      gooseSpecial=t.gooseAttackCount%4===0;
    }
    battle.shots.push({x:t.x,y:t.y-9,tx:target.x,ty:target.y,life:.42,maxLife:.42,type:"gooseEgg",special:gooseSpecial});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }

  let parrotBomb=false;'''
if old not in s: raise SystemExit('goose attack insertion marker not found')
s=s.replace(old,new,1)

old='''  battle.trashZones=battle.trashZones.filter(z=>z.life>0);
  battle.needles=battle.needles||[];
  battle.enemies.forEach(e=>moveEnemy(e,dt));
  battle.shots.forEach(s=>{
    if(s.type==="raccoonBin" && s.special && !s.spilled && s.life-dt<=0){'''
new='''  battle.trashZones=battle.trashZones.filter(z=>z.life>0);
  battle.eggSplashes=battle.eggSplashes||[];
  battle.eggSplashes.forEach(z=>{
    z.life-=dt;
    if(z.life>0){
      battle.enemies.forEach(e=>{
        if(!e.dead && Math.hypot(e.x-z.x,e.y-z.y)<=z.radius){
          e.poison=Math.max(e.poison||0,3);
          e.poisonTick=Math.min(e.poisonTick||.6,.6);
          e.poisonDmg=Math.max(e.poisonDmg||0,5);
        }
      });
    }
  });
  battle.eggSplashes=battle.eggSplashes.filter(z=>z.life>0);
  battle.needles=battle.needles||[];
  battle.enemies.forEach(e=>moveEnemy(e,dt));
  battle.shots.forEach(s=>{
    if(s.type==="gooseEgg" && s.special && !s.splashed && s.life-dt<=0){
      s.splashed=true;
      battle.eggSplashes=battle.eggSplashes||[];
      battle.eggSplashes.push({x:s.tx,y:s.ty,life:3,maxLife:3,radius:82});
    }
    if(s.type==="raccoonBin" && s.special && !s.spilled && s.life-dt<=0){'''
if old not in s: raise SystemExit('goose poison update marker not found')
s=s.replace(old,new,1)

old='''  (battle.trashZones||[]).forEach(z=>{
    const a=Math.max(.3,Math.min(1,z.life/z.maxLife));'''
new='''  (battle.eggSplashes||[]).forEach(z=>{
    const a=Math.max(.28,Math.min(1,z.life/z.maxLife));
    ctx.save();ctx.globalAlpha=a;
    ctx.fillStyle="rgba(255,255,235,.82)";ctx.strokeStyle="rgba(245,210,55,.95)";ctx.lineWidth=3;
    ctx.beginPath();ctx.ellipse(z.x,z.y+4,52,27,-.12,0,Math.PI*2);ctx.fill();ctx.stroke();
    ctx.fillStyle="rgba(255,208,28,.95)";
    ctx.beginPath();ctx.arc(z.x-8,z.y+2,16,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(z.x+27,z.y-5,8,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="rgba(255,255,245,.82)";
    ctx.beginPath();ctx.arc(z.x-43,z.y-5,8,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(z.x+43,z.y+12,6,0,Math.PI*2);ctx.fill();
    ctx.restore();
  });
  (battle.trashZones||[]).forEach(z=>{
    const a=Math.max(.3,Math.min(1,z.life/z.maxLife));'''
if old not in s: raise SystemExit('goose splash draw marker not found')
s=s.replace(old,new,1)

old='''  battle.shots?.forEach(s=>{
    if(s.type==="raccoonBin"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.48);'''
new='''  battle.shots?.forEach(s=>{
    if(s.type==="gooseEgg"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.42);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*24;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*3);
      ctx.fillStyle="#fffdf2";ctx.strokeStyle="#c9b98f";ctx.lineWidth=2;ctx.shadowColor="rgba(255,245,190,.8)";ctx.shadowBlur=7;
      ctx.beginPath();ctx.ellipse(0,0,9,12,0,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.restore();
    }else if(s.type==="raccoonBin"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.48);'''
if old not in s: raise SystemExit('goose egg projectile draw marker not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Goose egg projectile + every-4th level-10 poison splash added')