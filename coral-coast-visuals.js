// CORAL_COAST_VISUALS_V1 — richer in-game scenery + themed coastal base
(()=>{
 const oldDraw=draw;
 function coastDecor(ctx,w,h,map){
  const deep=map>=8;
  ctx.save();
  // subtle water bands / currents
  ctx.globalAlpha=.16;ctx.strokeStyle=deep?'#063d67':'#e8ffff';ctx.lineWidth=5;
  for(let y=55;y<h;y+=105){ctx.beginPath();for(let x=-20;x<w+40;x+=45){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+12,y-8,x+24,y);ctx.quadraticCurveTo(x+36,y+8,x+48,y)}ctx.stroke()}
  // sandy islands
  const islands=[[.14,.18,46],[.82,.25,38],[.18,.68,34],[.72,.78,44]];
  islands.forEach((q,i)=>{if((i+map)%2===0||map<4){const x=w*q[0],y=h*q[1],r=q[2];ctx.globalAlpha=.92;ctx.fillStyle='#e9ca7a';ctx.beginPath();ctx.ellipse(x,y,r,r*.55,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.75;ctx.fillStyle='#f8e4a7';ctx.beginPath();ctx.ellipse(x,y-4,r*.78,r*.35,0,0,Math.PI*2);ctx.fill()}});
  // reefs / rocks / seaweed / shells / bubbles
  ctx.font='25px system-ui';ctx.globalAlpha=.9;
  const sets=[['🪸','🐚','⭐','🌿'],['🐚','🪸','🫧','🌿'],['🪨','🐚','🪸','⭐'],['🪸','🫧','🌿','🐚']];
  const pts=[[.10,.36],[.87,.43],[.15,.88],[.82,.67],[.48,.15],[.52,.88],[.31,.54],[.72,.53]];
  pts.forEach((p,i)=>{ctx.fillText(sets[map%sets.length][i%4],w*p[0],h*p[1])});
  // pier / buoy details on selected maps
  if([2,4,6,9].includes(map)){ctx.globalAlpha=.9;ctx.fillStyle='#80552f';const px=w*.76,py=h*.12;for(let i=0;i<4;i++)ctx.fillRect(px+i*13,py,9,75);ctx.fillStyle='#b47b42';ctx.fillRect(px-7,py+10,65,14);ctx.font='22px system-ui';ctx.fillText('⚓',px+17,py+58)}
  if([3,5,7,10].includes(map)){ctx.font='24px system-ui';ctx.fillText('🛟',w*.08,h*.58);ctx.fillText('⚓',w*.88,h*.84)}
  // deeper maps get darker rock/coral clusters
  if(deep){ctx.globalAlpha=.72;ctx.font='30px system-ui';ctx.fillText('🪨',w*.38,h*.42);ctx.fillText('🪸',w*.42,h*.45);ctx.fillText('🪨',w*.60,h*.72);ctx.fillText('🪸',w*.64,h*.74)}
  ctx.restore();
 }
 function themedBase(ctx,w,h){
  const x=82,y=h-92;
  ctx.save();
  // rock/sand foundation
  ctx.fillStyle='#d7b56a';ctx.beginPath();ctx.ellipse(x,y+25,58,24,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#2b7f86';ctx.beginPath();ctx.roundRect(x-43,y-25,86,55,12);ctx.fill();
  ctx.strokeStyle='#8be7e8';ctx.lineWidth=4;ctx.stroke();
  // lighthouse / reef fortress
  ctx.fillStyle='#f1eee1';ctx.fillRect(x-13,y-61,26,43);ctx.fillStyle='#e45b50';ctx.fillRect(x-13,y-48,26,10);
  ctx.fillStyle='#293d52';ctx.beginPath();ctx.moveTo(x-20,y-61);ctx.lineTo(x,y-78);ctx.lineTo(x+20,y-61);ctx.closePath();ctx.fill();
  ctx.fillStyle='#ffe67a';ctx.beginPath();ctx.arc(x,y-58,5,0,Math.PI*2);ctx.fill();
  ctx.font='22px system-ui';ctx.fillText('🪸',x-50,y+9);ctx.fillText('🐚',x+28,y+12);
  ctx.restore();
 }
 draw=function(){oldDraw();if(currentSeries!==7)return;const c=document.getElementById('game')||document.querySelector('canvas');if(!c)return;const ctx=c.getContext('2d');if(!ctx)return;coastDecor(ctx,c.width,c.height,currentMap);themedBase(ctx,c.width,c.height)};
})();
