// CORAL_COAST_VISUALS_V3 — 10-map Coral Coast reef fortress + richer in-game scenery
(()=>{
 const oldDraw=draw;
 const MAP_MAX=10;

 function coastDecor(ctx,w,h,map){
  if(map<1||map>MAP_MAX)return;
  const deep=map>=8;
  ctx.save();

  // Layered water currents.
  ctx.globalAlpha=.14;ctx.strokeStyle=deep?'#063d67':'#e8ffff';ctx.lineWidth=4;
  for(let y=45;y<h;y+=88){ctx.beginPath();for(let x=-25;x<w+45;x+=44){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+11,y-7,x+22,y);ctx.quadraticCurveTo(x+33,y+7,x+44,y)}ctx.stroke()}

  // Bubble fields.
  ctx.strokeStyle='#e9ffff';ctx.lineWidth=1.4;ctx.globalAlpha=.38;
  const bubbles=[[.10,.24,3],[.15,.27,2],[.30,.48,3],[.33,.45,2],[.52,.16,2],[.68,.31,3],[.72,.34,2],[.87,.55,3],[.83,.58,2],[.58,.79,3],[.25,.82,2],[.43,.65,2]];
  bubbles.forEach((b,i)=>{if((i+map)%3!==0){ctx.beginPath();ctx.arc(w*b[0],h*b[1],b[2],0,Math.PI*2);ctx.stroke()}});

  // Small reef shelves / sandbars.
  const islands=[[.14,.18,42],[.82,.25,35],[.18,.68,31],[.72,.78,40],[.45,.39,25]];
  islands.forEach((q,i)=>{if((i+map)%2===0||map<=3){const x=w*q[0],y=h*q[1],r=q[2];ctx.globalAlpha=.9;ctx.fillStyle='#d6ad58';ctx.beginPath();ctx.ellipse(x,y+3,r,r*.5,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#f3d98d';ctx.beginPath();ctx.ellipse(x,y-2,r*.82,r*.34,0,0,Math.PI*2);ctx.fill()}});

  // Dense but small decorations, kept away from the main road visually.
  const sets=[['🪸','🐚','🌿','🫧'],['🐚','🪸','🫧','🌿'],['🪨','🐚','🪸','🌿'],['🪸','🫧','🌿','🐚']];
  const pts=[[.06,.34],[.91,.42],[.11,.85],[.85,.68],[.48,.13],[.53,.90],[.29,.53],[.71,.52],[.19,.44],[.79,.32],[.37,.72],[.63,.26],[.13,.73],[.88,.20],[.45,.80],[.57,.43]];
  ctx.globalAlpha=.9;ctx.font='20px system-ui';pts.forEach((p,i)=>ctx.fillText(sets[(map-1)%sets.length][i%4],w*p[0],h*p[1]));

  // Small seabed details.
  ctx.font='14px system-ui';ctx.globalAlpha=.82;
  [[.22,.21,'⭐'],[.58,.17,'🐚'],[.91,.76,'⭐'],[.39,.84,'🐚'],[.11,.59,'🪨'],[.66,.67,'🪨'],[.31,.38,'🐚'],[.76,.88,'⭐'],[.18,.31,'⭐'],[.81,.61,'🐚']].forEach(p=>ctx.fillText(p[2],w*p[0],h*p[1]));

  // Each of the 10 stages gets a little identity.
  if([2,4,6,9].includes(map)){ctx.globalAlpha=.88;ctx.fillStyle='#80552f';const px=w*.76,py=h*.12;for(let i=0;i<4;i++)ctx.fillRect(px+i*13,py,9,70);ctx.fillStyle='#b47b42';ctx.fillRect(px-7,py+10,65,13);ctx.font='20px system-ui';ctx.fillText('⚓',px+17,py+55)}
  if([3,5,7,10].includes(map)){ctx.font='21px system-ui';ctx.fillText('🛟',w*.08,h*.58);ctx.fillText('⚓',w*.88,h*.84)}
  if(map===5||map===7){ctx.font='18px system-ui';ctx.fillText('🐠',w*.17,h*.48);ctx.fillText('🐠',w*.78,h*.74)}
  if(map===9){ctx.font='19px system-ui';ctx.fillText('🪵',w*.26,h*.18);ctx.fillText('🪵',w*.67,h*.82)}
  if(map===10){ctx.globalAlpha=.75;ctx.font='28px system-ui';ctx.fillText('🪨',w*.37,h*.42);ctx.fillText('🪸',w*.41,h*.45);ctx.fillText('🪨',w*.61,h*.72);ctx.fillText('🪸',w*.65,h*.74)}
  ctx.restore();
 }

 function coralFortress(ctx,w,h,map){
  if(map<1||map>MAP_MAX)return;
  // Drawn over the normal base location using only canvas/in-game primitives + emoji props.
  const x=82,y=h-92;
  ctx.save();

  // Reef island foundation.
  ctx.globalAlpha=.98;ctx.fillStyle='#b58b43';ctx.beginPath();ctx.ellipse(x,y+28,64,29,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#f0d17d';ctx.beginPath();ctx.ellipse(x,y+23,58,24,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#75e4e8';ctx.lineWidth=5;ctx.globalAlpha=.72;ctx.beginPath();ctx.ellipse(x,y+29,66,30,0,0,Math.PI*2);ctx.stroke();

  // Pale stone reef-fort shell around the existing base.
  ctx.globalAlpha=.96;ctx.fillStyle='#e9e1c9';ctx.strokeStyle='#9b8f72';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(x-35,y-39,70,57,12);ctx.fill();ctx.stroke();
  // Battlements.
  for(let bx=-34;bx<=22;bx+=19){ctx.fillStyle='#f3ead3';ctx.fillRect(x+bx,y-49,14,17);ctx.strokeRect(x+bx,y-49,14,17)}

  // Glowing blue portal entrance.
  const grad=ctx.createRadialGradient(x,y-2,2,x,y-2,23);grad.addColorStop(0,'#c8ffff');grad.addColorStop(.35,'#29d9ff');grad.addColorStop(1,'#0758c7');ctx.fillStyle=grad;ctx.beginPath();ctx.arc(x,y-5,20,Math.PI,0);ctx.lineTo(x+20,y+16);ctx.lineTo(x-20,y+16);ctx.closePath();ctx.fill();
  ctx.strokeStyle='#fff5d6';ctx.lineWidth=5;ctx.stroke();

  // Short wooden jetty from portal.
  ctx.fillStyle='#6f4729';ctx.fillRect(x-22,y+15,7,35);ctx.fillRect(x+15,y+15,7,35);
  for(let j=0;j<5;j++){ctx.fillStyle=j%2?'#9b6838':'#ad7540';ctx.fillRect(x-25,y+17+j*7,50,6)}
  ctx.strokeStyle='#e4c18b';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x-24,y+17);ctx.lineTo(x-24,y+50);ctx.moveTo(x+24,y+17);ctx.lineTo(x+24,y+50);ctx.stroke();

  // Flag mast + shell crest.
  ctx.strokeStyle='#6d4528';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x,y-48);ctx.lineTo(x,y-79);ctx.stroke();
  ctx.fillStyle='#176f9b';ctx.beginPath();ctx.moveTo(x+2,y-76);ctx.lineTo(x+34,y-69);ctx.lineTo(x+2,y-59);ctx.closePath();ctx.fill();
  ctx.font='13px system-ui';ctx.fillText('🐚',x+8,y-62);

  // Coral, seaweed, anchor, shells and starfish around the fortress.
  ctx.font='22px system-ui';ctx.fillText('🪸',x-54,y+9);ctx.fillText('🪸',x+35,y+7);ctx.font='18px system-ui';ctx.fillText('🌿',x-47,y-10);ctx.fillText('🌿',x+39,y-13);ctx.fillText('⚓',x-53,y+31);ctx.font='15px system-ui';ctx.fillText('🐚',x+39,y+34);ctx.fillText('⭐',x-35,y+43);

  // Extra bubbles around the base.
  ctx.strokeStyle='#d8ffff';ctx.globalAlpha=.72;ctx.lineWidth=1.5;[[-43,-28,3],[-37,-40,2],[42,-31,3],[36,-47,2],[51,1,2]].forEach(b=>{ctx.beginPath();ctx.arc(x+b[0],y+b[1],b[2],0,Math.PI*2);ctx.stroke()});
  ctx.restore();
 }

 draw=function(){
  oldDraw();
  if(currentSeries!==7||currentMap<1||currentMap>MAP_MAX)return;
  const c=document.getElementById('game')||document.querySelector('canvas');if(!c)return;
  const ctx=c.getContext('2d');if(!ctx)return;
  coastDecor(ctx,c.width,c.height,currentMap);
  coralFortress(ctx,c.width,c.height,currentMap);
 };
})();
