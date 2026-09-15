// CORAL_COAST_VISUALS_V4 — 10-map Coral Coast, route-connected fortress, no purple base artefact
(()=>{
 const oldDraw=draw;
 const MAP_MAX=10;
 function basePos(w,h){
  if(typeof path==='undefined'||!path||path.length<2)return {x:82,y:h-92,prev:null};
  const end=path[path.length-1],prev=path[path.length-2],dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1,ux=dx/len,uy=dy/len,margin=82;
  let x=end[0]-ux*78,y=end[1]-uy*78;x=Math.max(margin,Math.min(w-margin,x));y=Math.max(margin,Math.min(h-margin,y));return{x,y,prev};
 }
 function coastDecor(ctx,w,h,map){
  if(map<1||map>MAP_MAX)return;ctx.save();const deep=map>=8;
  ctx.globalAlpha=.14;ctx.strokeStyle=deep?'#063d67':'#e8ffff';ctx.lineWidth=4;for(let y=45;y<h;y+=88){ctx.beginPath();for(let x=-25;x<w+45;x+=44){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+11,y-7,x+22,y);ctx.quadraticCurveTo(x+33,y+7,x+44,y)}ctx.stroke()}
  ctx.strokeStyle='#e9ffff';ctx.lineWidth=1.4;ctx.globalAlpha=.38;[[.10,.24,3],[.15,.27,2],[.30,.48,3],[.33,.45,2],[.52,.16,2],[.68,.31,3],[.72,.34,2],[.87,.55,3],[.83,.58,2],[.58,.79,3],[.25,.82,2],[.43,.65,2]].forEach((b,i)=>{if((i+map)%3!==0){ctx.beginPath();ctx.arc(w*b[0],h*b[1],b[2],0,Math.PI*2);ctx.stroke()}});
  const islands=[[.14,.18,42],[.82,.25,35],[.18,.68,31],[.72,.78,40],[.45,.39,25]];islands.forEach((q,i)=>{if((i+map)%2===0||map<=3){const x=w*q[0],y=h*q[1],r=q[2];ctx.globalAlpha=.9;ctx.fillStyle='#d6ad58';ctx.beginPath();ctx.ellipse(x,y+3,r,r*.5,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#f3d98d';ctx.beginPath();ctx.ellipse(x,y-2,r*.82,r*.34,0,0,Math.PI*2);ctx.fill()}});
  const sets=[['🪸','🐚','🌿','🫧'],['🐚','🪸','🫧','🌿'],['🪨','🐚','🪸','🌿'],['🪸','🫧','🌿','🐚']],pts=[[.06,.34],[.91,.42],[.11,.85],[.85,.68],[.48,.13],[.53,.90],[.29,.53],[.71,.52],[.19,.44],[.79,.32],[.37,.72],[.63,.26],[.13,.73],[.88,.20],[.45,.80],[.57,.43]];ctx.globalAlpha=.9;ctx.font='20px system-ui';pts.forEach((p,i)=>ctx.fillText(sets[(map-1)%sets.length][i%4],w*p[0],h*p[1]));
  ctx.font='14px system-ui';ctx.globalAlpha=.82;[[.22,.21,'⭐'],[.58,.17,'🐚'],[.91,.76,'⭐'],[.39,.84,'🐚'],[.11,.59,'🪨'],[.66,.67,'🪨'],[.31,.38,'🐚'],[.76,.88,'⭐']].forEach(p=>ctx.fillText(p[2],w*p[0],h*p[1]));ctx.restore();
 }
 function fixCoralRoute(ctx,w,h){
  const b=basePos(w,h);if(!b.prev)return;
  // Cover the old Crystal-purple fallback extension, then redraw the Coral Coast sand road right into the base entrance.
  ctx.save();ctx.lineCap='round';ctx.lineJoin='round';ctx.beginPath();ctx.moveTo(b.prev[0],b.prev[1]);ctx.lineTo(b.x,b.y);ctx.strokeStyle='#d2ab62';ctx.lineWidth=92;ctx.stroke();ctx.beginPath();ctx.moveTo(b.prev[0],b.prev[1]);ctx.lineTo(b.x,b.y);ctx.strokeStyle='#f1d38e';ctx.lineWidth=72;ctx.stroke();ctx.restore();
 }
 function coralFortress(ctx,w,h,map){
  if(map<1||map>MAP_MAX)return;const b=basePos(w,h),x=b.x,y=b.y;ctx.save();
  ctx.globalAlpha=.98;ctx.fillStyle='#b58b43';ctx.beginPath();ctx.ellipse(x,y+28,64,29,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#f0d17d';ctx.beginPath();ctx.ellipse(x,y+23,58,24,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#75e4e8';ctx.lineWidth=5;ctx.globalAlpha=.72;ctx.beginPath();ctx.ellipse(x,y+29,66,30,0,0,Math.PI*2);ctx.stroke();
  ctx.globalAlpha=.96;ctx.fillStyle='#e9e1c9';ctx.strokeStyle='#9b8f72';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(x-35,y-39,70,57,12);ctx.fill();ctx.stroke();for(let q=-34;q<=22;q+=19){ctx.fillStyle='#f3ead3';ctx.fillRect(x+q,y-49,14,17);ctx.strokeRect(x+q,y-49,14,17)}
  const g=ctx.createRadialGradient(x,y-2,2,x,y-2,23);g.addColorStop(0,'#c8ffff');g.addColorStop(.35,'#29d9ff');g.addColorStop(1,'#0758c7');ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y-5,20,Math.PI,0);ctx.lineTo(x+20,y+16);ctx.lineTo(x-20,y+16);ctx.closePath();ctx.fill();ctx.strokeStyle='#fff5d6';ctx.lineWidth=5;ctx.stroke();
  ctx.fillStyle='#6f4729';ctx.fillRect(x-22,y+15,7,35);ctx.fillRect(x+15,y+15,7,35);for(let j=0;j<5;j++){ctx.fillStyle=j%2?'#9b6838':'#ad7540';ctx.fillRect(x-25,y+17+j*7,50,6)}
  ctx.strokeStyle='#6d4528';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x,y-48);ctx.lineTo(x,y-79);ctx.stroke();ctx.fillStyle='#176f9b';ctx.beginPath();ctx.moveTo(x+2,y-76);ctx.lineTo(x+34,y-69);ctx.lineTo(x+2,y-59);ctx.closePath();ctx.fill();ctx.font='13px system-ui';ctx.fillText('🐚',x+8,y-62);
  ctx.font='22px system-ui';ctx.fillText('🪸',x-54,y+9);ctx.fillText('🪸',x+35,y+7);ctx.font='18px system-ui';ctx.fillText('🌿',x-47,y-10);ctx.fillText('🌿',x+39,y-13);ctx.fillText('⚓',x-53,y+31);ctx.font='15px system-ui';ctx.fillText('🐚',x+39,y+34);ctx.fillText('⭐',x-35,y+43);ctx.restore();
 }
 draw=function(){oldDraw();if(currentSeries!==7||currentMap<1||currentMap>MAP_MAX)return;const c=document.getElementById('game')||document.querySelector('canvas');if(!c)return;const ctx=c.getContext('2d');if(!ctx)return;coastDecor(ctx,c.width,c.height,currentMap);fixCoralRoute(ctx,c.width,c.height);coralFortress(ctx,c.width,c.height,currentMap)};
})();
