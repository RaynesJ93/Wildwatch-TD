from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Insert Tiger custom attack before Pig block.
anchor='''  if(t.key==="pig"){'''
if anchor not in s:
    raise SystemExit('Pig attack anchor not found')
if 't.tigerAttackCount' not in s:
    block='''  if(t.key==="tiger"){
    let tigerRoar=false;
    if(t.level>=10){
      t.tigerAttackCount=(t.tigerAttackCount||0)+1;
      tigerRoar=t.tigerAttackCount%9===0;
    }
    battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.28,maxLife:.28,type:"tigerSwipe"});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    if(tigerRoar){
      battle.roars=battle.roars||[];
      battle.roars.push({x:t.x,y:t.y,life:.65,maxLife:.65,radius:range});
      battle.enemies.forEach(e=>{
        if(e.dead)return;
        if(Math.hypot(e.x-t.x,e.y-t.y)<=range)e.tigerRoar=Math.max(e.tigerRoar||0,2);
      });
    }
    t.cd=cardRate(t.key);
    return;
  }\n\n'''
    s=s.replace(anchor,block+anchor,1)

# Make enemies retreat toward the start while Tiger roar is active.
move_anchor='''function moveEnemy(e,dt){\n'''
if move_anchor not in s:
    raise SystemExit('moveEnemy anchor not found')
if 'e.tigerRoar' not in s[s.find('function moveEnemy'):s.find('function killEnemy')]:
    retreat='''  if((e.tigerRoar||0)>0){
    e.tigerRoar=Math.max(0,e.tigerRoar-dt);
    let dist=e.speed*dt;
    while(dist>0){
      const seg=Math.max(0,e.seg||0);
      const [tx,ty]=path[seg],dx=tx-e.x,dy=ty-e.y,len=Math.hypot(dx,dy);
      if(len>.001){
        e.dirX=dx/len;e.dirY=dy/len;e.walkPhase=(e.walkPhase||0)+dt*e.speed*.16;
        if(dist>=len){e.x=tx;e.y=ty;dist-=len;if(e.seg>0)e.seg--;else dist=0;}
        else{e.x+=dx/len*dist;e.y+=dy/len*dist;dist=0;}
      }else if(e.seg>0)e.seg--;else break;
    }
    return;
  }\n'''
    s=s.replace(move_anchor,move_anchor+retreat,1)

# Draw swipe projectile as three claw arcs travelling to the target.
shots_anchor='''  battle.shots?.forEach(s=>{'''
if shots_anchor not in s:
    raise SystemExit('battle shots draw anchor not found')
if 's.type==="tigerSwipe"' not in s:
    draw='''  battle.shots?.forEach(s=>{
    if(s.type==="tigerSwipe"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.28);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.strokeStyle="#ffd36a";ctx.lineWidth=5;ctx.lineCap="round";
      [-10,0,10].forEach(off=>{ctx.beginPath();ctx.arc(0,off,18,-.85,.85);ctx.stroke()});
      ctx.restore();
      return;
    }'''
    s=s.replace(shots_anchor,draw,1)

# Draw expanding roar ring.
render_anchor='''  (battle.eggSplashes||[]).forEach(z=>{'''
if render_anchor not in s:
    raise SystemExit('effect render anchor not found')
if '(battle.roars||[]).forEach' not in s:
    roar_draw='''  (battle.roars||[]).forEach(r=>{
    const q=1-Math.max(0,r.life)/(r.maxLife||.65);
    ctx.save();ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle="#ffb84d";ctx.lineWidth=6;
    ctx.beginPath();ctx.arc(r.x,r.y,20+(r.radius||180)*q,0,Math.PI*2);ctx.stroke();
    ctx.font="30px sans-serif";ctx.textAlign="center";ctx.fillText("ROAR!",r.x,r.y-34);ctx.restore();
  });
'''
    s=s.replace(render_anchor,roar_draw+render_anchor,1)

# Tick roar visual lifetime near other battle effects.
tick_anchor='''  battle.trashZones=battle.trashZones.filter(z=>z.life>0);'''
if tick_anchor not in s:
    raise SystemExit('effect tick anchor not found')
if 'battle.roars=battle.roars||[];' not in s[s.find('function updateBattle'):s.find('function draw') if 'function draw' in s else len(s)]:
    tick='''  battle.roars=battle.roars||[];
  battle.roars.forEach(r=>r.life-=dt);
  battle.roars=battle.roars.filter(r=>r.life>0);
'''
    s=s.replace(tick_anchor,tick_anchor+'\n'+tick,1)

# Update Tiger description to surface its Level 10 special.
old='tiger:{name:"Tiger",emoji:"🐯",rarity:"Legendary",cost:175,range:185,rate:1/1.10,dmg:70,color:"#e83",desc:"Elite fast attacker."}'
new='tiger:{name:"Tiger",emoji:"🐯",rarity:"Legendary",cost:175,range:185,rate:1/1.10,dmg:70,color:"#e83",desc:"Swipes enemies. At tower level 10 every 9th attack roars, forcing nearby enemies back toward the start for 2 seconds."}'
if old in s:
    s=s.replace(old,new,1)

for marker in ['t.tigerAttackCount','type:"tigerSwipe"','e.tigerRoar','(battle.roars||[]).forEach']:
    if marker not in s:
        raise SystemExit(f'missing final marker: {marker}')

p.write_text(s,encoding='utf-8')
print('Added Tiger swipe attack and Level 10 roar retreat ability')
