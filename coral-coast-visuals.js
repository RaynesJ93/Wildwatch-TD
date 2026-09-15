// CORAL_COAST_VISUALS_V5 — 10-map Coral Coast, road-mounted reef base, no foreground sand spots
(()=>{
 const oldDraw=draw;
 const MAP_MAX=10;
 function basePos(w,h){
  if(typeof path==='undefined'||!path||path.length<2)return {x:82,y:h-82,prev:null,end:null};
  const end=path[path.length-1],prev=path[path.length-2];
  // The base belongs ON the final road node. Only clamp enough to keep the artwork visible.
  const margin=58;
  return {x:Math.max(margin,Math.min(w-margin,end[0])),y:Math.max(margin,Math.min(h-margin,end[1])),prev,end};
 }
 function coastDecor(ctx,w,h,map){
  if(map<1||map>MAP_MAX)return;ctx.save();const deep=map>=8;
  // Water-only decoration. Sand circles/islets were deliberately removed because this overlay
  // is drawn after the battle renderer and could cover enemies/towers.
  ctx.globalAlpha=.14;ctx.strokeStyle=deep?'#063d67':'#e8ffff';ctx.lineWidth=4;
  for(let y=45;y<h;y+=88){ctx.beginPath();for(let x=-25;x<w+45;x+=44){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+11,y-7,x+22,y);ctx.quadraticCurveTo(x+33,y+7,x+44,y)}ctx.stroke()}
  ctx.strokeStyle='#e9ffff';ctx.lineWidth=1.4;ctx.globalAlpha=.30;
  [[.10,.24,3],[.15,.27,2],[.30,.48,3],[.33,.45,2],[.52,.16,2],[.68,.31,3],[.72,.34,2],[.87,.55,3],[.83,.58,2],[.58,.79,3],[.25,.82,2],[.43,.65,2]].forEach((b,i)=>{if((i+map)%3!==0){ctx.beginPath();ctx.arc(w*b[0],h*b[1],b[2],0,Math.PI*2);ctx.stroke()}});
  // Keep small sea-life details away from the road/tower layer by making them subtle.
  const sets=[['🪸','🐚','🌿','🫧'],['🐚','🪸','🫧','🌿'],['🪨','🐚','🪸','🌿'],['🪸','🫧','🌿','🐚']],pts=[[.06,.34],[.91,.42],[.11,.85],[.85,.68],[.48,.13],[.53,.90],[.29,.53],[.71,.52],[.19,.44],[.79,.32],[.37,.72],[.63,.26],[.13,.73],[.88,.20],[.45,.80],[.57,.43]];
  ctx.globalAlpha=.42;ctx.font='15px system-ui';pts.forEach((p,i)=>ctx.fillText(sets[(map-1)%sets.length][i%4],w*p[0],h*p[1]));ctx.restore();
 }
 function fixCoralRoute(ctx,w,h){
  const b=basePos(w,h);if(!b.prev)return;
  // Repaint the final Coral Coast road segment directly underneath the new base.
  ctx.save();ctx.lineCap='round';ctx.lineJoin='round';
  ctx.beginPath();ctx.moveTo(b.prev[0],b.prev[1]);ctx.lineTo(b.x,b.y);ctx.strokeStyle='#d2ab62';ctx.lineWidth=92;ctx.stroke();
  ctx.beginPath();ctx.moveTo(b.prev[0],b.prev[1]);ctx.lineTo(b.x,b.y);ctx.strokeStyle='#f1d38e';ctx.lineWidth=72;ctx.stroke();ctx.restore();
 }
 function coralFortress(ctx,w,h,map){
  if(map<1||map>MAP_MAX)return;const b=basePos(w,h),x=b.x,y=b.y;ctx.save();
  // NEW CORAL COAST BASE: compact reef keep mounted centrally on the road endpoint.
  ctx.globalAlpha=.98;
  ctx.fillStyle='#c99c4d';ctx.beginPath();ctx.ellipse(x,y+18,53,25,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#f4d98e';ctx.beginPath();ctx.ellipse(x,y+13,48,20,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#68e5ea';ctx.lineWidth=4;ctx.globalAlpha=.78;ctx.beginPath();ctx.ellipse(x,y+17,55,27,0,0,Math.PI*2);ctx.stroke();
  // Main shell/stone keep.
  ctx.globalAlpha=1;ctx.fillStyle='#f2ead8';ctx.strokeStyle='#8e8169';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(x-30,y-34,60,47,10);ctx.fill();ctx.stroke();
  // Battlements.
  for(let q=-29;q<=19;q+=16){ctx.fillStyle='#fff4dc';ctx.fillRect(x+q,y-43,11,13);ctx.strokeRect(x+q,y-43,11,13)}
  // Bright aqua portal facing the track.
  const g=ctx.createRadialGradient(x,y-1,2,x,y-1,20);g.addColorStop(0,'#eaffff');g.addColorStop(.38,'#33e4ff');g.addColorStop(1,'#0864c7');ctx.fillStyle=g;
  ctx.beginPath();ctx.arc(x,y-2,17,Math.PI,0);ctx.lineTo(x+17,y+13);ctx.lineTo(x-17,y+13);ctx.closePath();ctx.fill();ctx.strokeStyle='#fff8dd';ctx.lineWidth=4;ctx.stroke();
  // Timber jetty/doorstep sits on the road, not beside it.
  ctx.fillStyle='#7a4d2d';ctx.fillRect(x-19,y+13,5,28);ctx.fillRect(x+14,y+13,5,28);
  for(let j=0;j<4;j++){ctx.fillStyle=j%2?'#9d693b':'#b77b43';ctx.fillRect(x-22,y+15+j*7,44,6)}
  // Coral crest and flag make this base unique to Coral Coast.
  ctx.strokeStyle='#70452a';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x,y-42);ctx.lineTo(x,y-67);ctx.stroke();
  ctx.fillStyle='#16a8c5';ctx.beginPath();ctx.moveTo(x+2,y-65);ctx.lineTo(x+27,y-59);ctx.lineTo(x+2,y-49);ctx.closePath();ctx.fill();
  ctx.font='16px system-ui';ctx.fillText('🪸',x-43,y+7);ctx.fillText('🐚',x+29,y+9);ctx.font='13px system-ui';ctx.fillText('⭐',x-31,y+29);ctx.fillText('🌿',x+27,y+29);ctx.restore();
 }
 draw=function(){
  oldDraw();
  if(currentSeries!==7||currentMap<1||currentMap>MAP_MAX)return;
  const c=document.getElementById('game')||document.querySelector('canvas');if(!c)return;const ctx=c.getContext('2d');if(!ctx)return;
  coastDecor(ctx,c.width,c.height,currentMap);
  fixCoralRoute(ctx,c.width,c.height);
  coralFortress(ctx,c.width,c.height,currentMap);
 };
})();
