// ATTACK_BATCH_1_V1 — Parrot, Penguin, Butterfly and Ram bespoke attacks + Level 10 abilities.
(()=>{
 if(window.__attackBatch1V1||typeof towerTickCore!=='function'||typeof draw!=='function')return;
 window.__attackBatch1V1=true;
 const oldTick=towerTickCore,oldDraw=draw;
 const keys=new Set(['parrot','penguin','butterfly','ram']);
 const desc={
  parrot:'Fires a bright spinning feather. At Level 10, every 7th attack triggers Screech: all enemies in range take 125% current tower damage and are slowed by 25% for 2s.',
  penguin:'Throws a spinning snowball that bursts into ice. At Level 10, every 8th attack drops an Iceberg for 175% area damage and leaves a slowing ice patch for 4s.',
  butterfly:'Launches a glowing wing-shaped gust. At Level 10, every 6th attack creates Wing Storm for 4s, repeatedly damaging and slowing enemies inside the whirlwind.',
  ram:'Fires a curved horn shockwave. At Level 10, every 6th attack triggers Headbutt Chain: 2x damage to the first target then chains into up to 3 nearby enemies for 100% damage each.'
 };
 Object.keys(desc).forEach(k=>{if(animals[k])animals[k].desc=desc[k]});
 function targetFor(t,range){
  const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);if(!pool.length)return null;
  const mode=t.targetMode||'first';
  if(mode==='strongest')return pool.reduce((a,e)=>!a||e.hp>a.hp?e:a,null);
  if(mode==='last')return pool.reduce((a,e)=>!a||Number(e.seg||0)<Number(a.seg||0)?e:a,null);
  if(mode==='closest')return pool.reduce((a,e)=>!a||Math.hypot(e.x-t.x,e.y-t.y)<Math.hypot(a.x-t.x,a.y-t.y)?e:a,null);
  return pool.reduce((a,e)=>!a||Number(e.seg||0)>Number(a.seg||0)?e:a,null);
 }
 function hit(e,d){if(!e||e.dead)return;e.hp-=d;if(e.hp<=0)killEnemy(e)}
 function fx(o){battle.batch1Fx=battle.batch1Fx||[];battle.batch1Fx.push(o)}
 function updateZones(t,dt){
  t.batch1Zones=t.batch1Zones||[];
  for(const z of t.batch1Zones){z.life-=dt;z.tick=(z.tick||0)-dt;
   const inside=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-z.x,e.y-z.y)<=z.r);
   inside.forEach(e=>e.zebraSlowTimer=Math.max(e.zebraSlowTimer||0,.16));
   if(z.kind==='wing'&&z.tick<=0){z.tick=.5;inside.forEach(e=>hit(e,z.dmg));}
  }
  t.batch1Zones=t.batch1Zones.filter(z=>z.life>0);
 }
 towerTickCore=function(t,dt){
  if(!keys.has(t.key))return oldTick(t,dt);
  battle.lastAttackingTower=t;updateZones(t,dt);t.cd-=dt;if(t.cd>0)return;
  const range=cardBaseRange(t.key)*(1+(t.level-1)*.06),target=targetFor(t,range);if(!target)return;
  const lion=battle.towers.some(o=>o.key==='lion'&&o!==t&&Math.hypot(o.x-t.x,o.y-t.y)<145),dmg=towerDamage(t)*(lion?1.15:1);
  if(typeof addQuestProgress==='function')addQuestProgress('damage',Math.max(0,Math.round(dmg)));if(typeof addWeeklyProgress==='function')addWeeklyProgress('damage',Math.max(0,Math.round(dmg)));
  if(t.key==='parrot'){
   t.batch1Count=(t.batch1Count||0)+1;const special=t.level>=10&&t.batch1Count%7===0;
   if(special){const victims=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);victims.forEach(e=>{hit(e,dmg*1.25);e.zebraSlowTimer=Math.max(e.zebraSlowTimer||0,2)});fx({kind:'screech',x:t.x,y:t.y,life:.65,max:.65,r:range});}
   else{hit(target,dmg);fx({kind:'feather',x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.34,max:.34});}
  }else if(t.key==='penguin'){
   t.batch1Count=(t.batch1Count||0)+1;const special=t.level>=10&&t.batch1Count%8===0;
   if(special){const r=82;for(const e of battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-target.x,e.y-target.y)<=r))hit(e,dmg*1.75);t.batch1Zones.push({kind:'ice',x:target.x,y:target.y,r:82,life:4});fx({kind:'iceberg',x:target.x,y:target.y,life:.75,max:.75});}
   else{hit(target,dmg);fx({kind:'snowball',x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.36,max:.36});}
  }else if(t.key==='butterfly'){
   t.batch1Count=(t.batch1Count||0)+1;const special=t.level>=10&&t.batch1Count%6===0;
   if(special){t.batch1Zones.push({kind:'wing',x:target.x,y:target.y,r:88,life:4,tick:0,dmg:dmg*.25});fx({kind:'wingBurst',x:target.x,y:target.y,life:.7,max:.7});}
   else{hit(target,dmg);fx({kind:'wing',x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.38,max:.38});}
  }else{
   t.batch1Count=(t.batch1Count||0)+1;const special=t.level>=10&&t.batch1Count%6===0;
   if(special){hit(target,dmg*2);fx({kind:'ramChain',x:t.x,y:t.y,tx:target.x,ty:target.y,life:.32,max:.32});let prev=target;const used=new Set([target]);for(let i=0;i<3;i++){const p=battle.enemies.filter(e=>!e.dead&&e.hp>0&&!used.has(e)&&Math.hypot(e.x-prev.x,e.y-prev.y)<=135).sort((a,b)=>Math.hypot(a.x-prev.x,a.y-prev.y)-Math.hypot(b.x-prev.x,b.y-prev.y));if(!p.length)break;const e=p[0];used.add(e);hit(e,dmg);fx({kind:'ramChain',x:prev.x,y:prev.y,tx:e.x,ty:e.y,life:.28+i*.04,max:.28+i*.04});prev=e;}}
   else{hit(target,dmg);fx({kind:'hornWave',x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.32,max:.32});}
  }
  t.cd=cardRate(t.key);
 };
 function drawFx(){
  const now=performance.now()/1000;battle.batch1Fx=battle.batch1Fx||[];
  for(const s of battle.batch1Fx){const q=1-Math.max(0,s.life)/(s.max||.35),x=s.tx==null?s.x:s.x+(s.tx-s.x)*q,y=s.ty==null?s.y:s.y+(s.ty-s.y)*q;ctx.save();
   if(s.kind==='feather'){ctx.translate(x,y);ctx.rotate(Math.atan2(s.ty-s.y,s.tx-s.x)+q*4);ctx.strokeStyle='#45e2d0';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-13,0);ctx.quadraticCurveTo(0,-8,15,0);ctx.quadraticCurveTo(0,8,-13,0);ctx.stroke();}
   else if(s.kind==='screech'){ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle='#ffd85a';ctx.lineWidth=7;ctx.beginPath();ctx.arc(s.x,s.y,18+s.r*q,0,Math.PI*2);ctx.stroke();ctx.font='bold 25px sans-serif';ctx.textAlign='center';ctx.fillStyle='#fff4a8';ctx.fillText('SCREECH!',s.x,s.y-32);}
   else if(s.kind==='snowball'){ctx.translate(x,y);ctx.rotate(q*8);ctx.fillStyle='#f4fbff';ctx.strokeStyle='#7edcff';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,10,0,Math.PI*2);ctx.fill();ctx.stroke();}
   else if(s.kind==='iceberg'){ctx.globalAlpha=Math.max(.2,1-q);ctx.translate(s.x,s.y);ctx.fillStyle='#8fe8ff';ctx.strokeStyle='#e7fbff';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-30,20);ctx.lineTo(-12,-34);ctx.lineTo(2,-12);ctx.lineTo(18,-42);ctx.lineTo(34,20);ctx.closePath();ctx.fill();ctx.stroke();}
   else if(s.kind==='wing'){ctx.translate(x,y);ctx.rotate(Math.atan2(s.ty-s.y,s.tx-s.x));ctx.fillStyle='#d98cff';ctx.globalAlpha=.85;ctx.beginPath();ctx.ellipse(-7,-5,14,7,-.5,0,Math.PI*2);ctx.ellipse(7,5,14,7,-.5,0,Math.PI*2);ctx.fill();}
   else if(s.kind==='wingBurst'){ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle='#d98cff';ctx.lineWidth=6;for(let i=0;i<5;i++){ctx.beginPath();ctx.arc(0,0,18+q*65+i*4,i*.7,i*.7+4.5);ctx.stroke();}}
   else if(s.kind==='hornWave'){ctx.translate(x,y);ctx.rotate(Math.atan2(s.ty-s.y,s.tx-s.x));ctx.strokeStyle='#e7d2a6';ctx.lineWidth=6;ctx.beginPath();ctx.arc(0,0,15,-1.1,1.1);ctx.stroke();}
   else if(s.kind==='ramChain'){ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle='#f5e1ae';ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(s.tx,s.ty);ctx.stroke();ctx.font='24px sans-serif';ctx.textAlign='center';ctx.fillText('🐏',x,y);}
   ctx.restore();s.life-=1/60;
  }
  battle.batch1Fx=battle.batch1Fx.filter(s=>s.life>0);
  for(const t of battle.towers||[])for(const z of t.batch1Zones||[]){ctx.save();const a=Math.min(.55,z.life/1.2);ctx.globalAlpha=a;if(z.kind==='ice'){ctx.fillStyle='#8de8ff';ctx.strokeStyle='#e7fbff';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(z.x,z.y,z.r,z.r*.45,0,0,Math.PI*2);ctx.fill();ctx.stroke();}else{ctx.strokeStyle='#d98cff';ctx.lineWidth=5;for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(z.x,z.y,22+i*14,now*2+i,now*2+i+4.2);ctx.stroke();}}ctx.restore();}
 }
 draw=function(){oldDraw();if(battle&&battle.started&&!battle.ended)drawFx()};
})();