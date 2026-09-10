from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Update Raccoon description.
old='raccoon:{name:"Raccoon",emoji:"🦝",rarity:"Uncommon",cost:82,range:180,rate:1/1.15,dmg:20,color:"#888",desc:"Balanced ranged attacker."}'
new='raccoon:{name:"Raccoon",emoji:"🦝",rarity:"Uncommon",cost:82,range:180,rate:1/1.15,dmg:20,color:"#888",desc:"Throws dustbins. At Level 10+, trash spills onto the track for 4s and slows enemies."}'
if old not in s: raise SystemExit('Raccoon data marker not found')
s=s.replace(old,new,1)

# Give Raccoon a dustbin projectile and Level 10 trash slow zone.
marker='''  if(t.key==="bee"){
    const maxTargets=t.level>=10?5:3;'''
idx=s.find(marker)
if idx<0: raise SystemExit('Bee attack marker not found')
end=s.find('''  let parrotBomb=false;''',idx)
if end<0: raise SystemExit('Post-Bee marker not found')
raccoon='''  if(t.key==="raccoon"){
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.48,maxLife:.48,type:"raccoonBin"});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    if(t.level>=10){
      battle.trashZones=battle.trashZones||[];
      battle.trashZones.push({x:target.x,y:target.y,life:4,maxLife:4,radius:78});
    }
    t.cd=cardRate(t.key);
    return;
  }

'''
s=s[:end]+raccoon+s[end:]

# Update trash zones before enemies move so the existing slowTimer movement modifier applies.
update_marker='''  battle.pineapples=battle.pineapples.filter(p=>!p.exploded);
  battle.needles=battle.needles||[];
  battle.enemies.forEach(e=>moveEnemy(e,dt));'''
update_new='''  battle.pineapples=battle.pineapples.filter(p=>!p.exploded);
  battle.trashZones=battle.trashZones||[];
  battle.trashZones.forEach(z=>{
    z.life-=dt;
    if(z.life>0){
      battle.enemies.forEach(e=>{
        if(!e.dead && Math.hypot(e.x-z.x,e.y-z.y)<=z.radius){
          e.slowTimer=Math.max(e.slowTimer||0,.12);
        }
      });
    }
  });
  battle.trashZones=battle.trashZones.filter(z=>z.life>0);
  battle.needles=battle.needles||[];
  battle.enemies.forEach(e=>moveEnemy(e,dt));'''
if update_marker not in s: raise SystemExit('Battle update marker not found')
s=s.replace(update_marker,update_new,1)

# Draw persistent trash piles on the track.
draw_anchor='''  battle.shots?.forEach(s=>{
    if(s.type==="beeLightning"){'''
trash_draw='''  (battle.trashZones||[]).forEach(z=>{
    const a=Math.max(.25,Math.min(1,z.life/z.maxLife));
    ctx.save();ctx.globalAlpha=a;
    ctx.fillStyle="rgba(90,70,45,.55)";
    ctx.beginPath();ctx.ellipse(z.x,z.y+4,44,22,0,0,Math.PI*2);ctx.fill();
    ctx.font="24px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("🗑️",z.x-18,z.y);
    ctx.fillText("🧻",z.x+10,z.y+4);
    ctx.fillText("🥫",z.x+25,z.y-4);
    ctx.restore();
  });
  battle.shots?.forEach(s=>{
    if(s.type==="raccoonBin"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.48);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*28;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*1.6);ctx.font="30px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🗑️",0,0);ctx.restore();
    }else if(s.type==="beeLightning"){'''
if draw_anchor not in s: raise SystemExit('Shot draw marker not found')
s=s.replace(draw_anchor,trash_draw,1)

p.write_text(s,encoding='utf-8')
