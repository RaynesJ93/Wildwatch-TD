// CORAL_COAST_VISUALS_V2 — preserve the original base, dress it as a Coral Coast fortress, and enrich scenery
(()=>{
 const oldDraw=draw;
 function coastDecor(ctx,w,h,map){
  const deep=map>=8;
  ctx.save();

  // Layered currents and tiny bubbles make the water feel alive without hiding gameplay.
  ctx.globalAlpha=.14;ctx.strokeStyle=deep?'#063d67':'#e8ffff';ctx.lineWidth=4;
  for(let y=48;y<h;y+=92){ctx.beginPath();for(let x=-25;x<w+45;x+=44){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+11,y-7,x+22,y);ctx.quadraticCurveTo(x+33,y+7,x+44,y)}ctx.stroke()}
  ctx.globalAlpha=.28;ctx.fillStyle='#e9ffff';
  [[.29,.30,3],[.33,.32,2],[.67,.18,2],[.73,.61,3],[.26,.77,2],[.89,.34,2],[.57,.83,3],[.43,.52,2]].forEach(b=>{ctx.beginPath();ctx.arc(w*b[0],h*b[1],b[2],0,Math.PI*2);ctx.strokeStyle='#e9ffff';ctx.lineWidth=1.5;ctx.stroke()});

  // Small sandbars / reef shelves.
  const islands=[[.14,.18,42],[.82,.25,35],[.18,.68,31],[.72,.78,40],[.45,.39,25]];
  islands.forEach((q,i)=>{if((i+map)%2===0||map<4){const x=w*q[0],y=h*q[1],r=q[2];ctx.globalAlpha=.9;ctx.fillStyle='#d6ad58';ctx.beginPath();ctx.ellipse(x,y+3,r,r*.5,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#f3d98d';ctx.beginPath();ctx.ellipse(x,y-2,r*.82,r*.34,0,0,Math.PI*2);ctx.fill()}});

  // Coral Coast decoration clusters. Keep them small so towers/enemies remain readable.
  ctx.globalAlpha=.92;ctx.font='21px system-ui';
  const sets=[['🪸','🐚','🌿','🫧'],['🐚','🪸','🫧','🌿'],['🪨','🐚','🪸','🌿'],['🪸','🫧','🌿','🐚']];
  const pts=[[.07,.35],[.90,.43],[.12,.86],[.84,.68],[.48,.14],[.52,.90],[.30,.53],[.70,.52],[.20,.44],[.78,.32],[.38,.72],[.62,.26]];
  pts.forEach((p,i)=>ctx.fillText(sets[map%sets.length][i%4],w*p[0],h*p[1]));

  // Starfish, shells and pebble details.
  ctx.font='15px system-ui';ctx.globalAlpha=.78;
  [[.22,.21,'⭐'],[.58,.17,'🐚'],[.91,.76,'⭐'],[.39,.84,'🐚'],[.11,.59,'🪨'],[.66,.67,'🪨'],[.31,.38,'🐚'],[.76,.88,'⭐']].forEach(p=>ctx.fillText(p[2],w*p[0],h*p[1]));

  // Occasional coastal props give individual stages some identity.
  if([2,4,6,9].includes(map)){ctx.globalAlpha=.88;ctx.fillStyle='#80552f';const px=w*.76,py=h*.12;for(let i=0;i<4;i++)ctx.fillRect(px+i*13,py,9,70);ctx.fillStyle='#b47b42';ctx.fillRect(px-7,py+10,65,13);ctx.font='20px system-ui';ctx.fillText('⚓',px+17,py+55)}
  if([3,5,7,10].includes(map)){ctx.font='22px system-ui';ctx.fillText('🛟',w*.08,h*.58);ctx.fillText('⚓',w*.88,h*.84)}
  if(deep){ctx.globalAlpha=.7;ctx.font='27px system-ui';ctx.fillText('🪨',w*.38,h*.42);ctx.fillText('🪸',w*.42,h*.45);ctx.fillText('🪨',w*.60,h*.72);ctx.fillText('🪸',w*.64,h*.74)}
  ctx.restore();
 }

 function coralDressBase(ctx,w,h){
  // IMPORTANT: the normal game base has already been drawn by oldDraw().
  // This only adds Coral Coast trim around/on top of it; it does not replace or cover it.
  const x=82,y=h-92;
  ctx.save();

  // Sandy reef apron behind the visible lower edge of the original base.
  ctx.globalAlpha=.72;ctx.fillStyle='#e7c66f';ctx.beginPath();ctx.ellipse(x,y+38,60,14,0,0,Math.PI*2);ctx.fill();

  // Coral reef clusters framing the original base.
  ctx.globalAlpha=.96;ctx.font='23px system-ui';ctx.fillText('🪸',x-56,y+22);ctx.fillText('🪸',x+35,y+25);ctx.font='17px system-ui';ctx.fillText('🐚',x-43,y+38);ctx.fillText('⭐',x+43,y+38);

  // Two turquoise coastal posts either side, leaving the old base centre fully visible.
  ctx.fillStyle='#176f7d';ctx.strokeStyle='#8be7e8';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(x-55,y-25,12,45,5);ctx.fill();ctx.stroke();
  ctx.beginPath();ctx.roundRect(x+43,y-25,12,45,5);ctx.fill();ctx.stroke();
  ctx.fillStyle='#f3d66f';ctx.beginPath();ctx.arc(x-49,y-28,5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(x+49,y-28,5,0,Math.PI*2);ctx.fill();

  // Small wave crest / shell badge above the old base, rather than a replacement building.
  ctx.globalAlpha=.95;ctx.fillStyle='#0f8797';ctx.beginPath();ctx.arc(x,y-38,13,Math.PI,0);ctx.lineTo(x+13,y-34);ctx.lineTo(x-13,y-34);ctx.closePath();ctx.fill();
  ctx.font='14px system-ui';ctx.fillText('🐚',x-8,y-36);

  // Bubbles rising around the base.
  ctx.strokeStyle='#c8fbff';ctx.globalAlpha=.6;ctx.lineWidth=1.5;
  [[-34,-35,3],[-27,-48,2],[35,-40,3],[30,-54,2]].forEach(b=>{ctx.beginPath();ctx.arc(x+b[0],y+b[1],b[2],0,Math.PI*2);ctx.stroke()});
  ctx.restore();
 }

 draw=function(){
  oldDraw();
  if(currentSeries!==7)return;
  const c=document.getElementById('game')||document.querySelector('canvas');if(!c)return;
  const ctx=c.getContext('2d');if(!ctx)return;
  coastDecor(ctx,c.width,c.height,currentMap);
  coralDressBase(ctx,c.width,c.height);
 };
})();
