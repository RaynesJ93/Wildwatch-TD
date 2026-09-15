// CORAL_COAST_VISUALS_V11 — Coral Coast visuals only; all base-specific overlays removed
(()=>{
 const oldDraw=draw,MAP_MAX=10;
 function coastDecor(ctx,w,h,map){ctx.save();ctx.globalAlpha=.14;ctx.strokeStyle=map>=8?'#063d67':'#e8ffff';ctx.lineWidth=4;for(let y=45;y<h;y+=88){ctx.beginPath();for(let x=-25;x<w+45;x+=44){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+11,y-7,x+22,y);ctx.quadraticCurveTo(x+33,y+7,x+44,y)}ctx.stroke()}ctx.globalAlpha=.42;ctx.font='15px system-ui';const a=['🪸','🐚','🌿','🫧'],pts=[[.06,.34],[.91,.42],[.11,.85],[.85,.68],[.48,.13],[.53,.90],[.29,.53],[.71,.52],[.19,.44],[.79,.32],[.37,.72],[.63,.26]];pts.forEach((p,i)=>ctx.fillText(a[(i+map)%4],w*p[0],h*p[1]));ctx.restore();}
 draw=function(){oldDraw();if(currentSeries!==7||currentMap<1||currentMap>MAP_MAX)return;const c=document.getElementById('game')||document.querySelector('canvas'),ctx=c?.getContext('2d');if(!ctx)return;coastDecor(ctx,c.width,c.height,currentMap);};
 const s=document.createElement('script');s.src='regions-8-10.js?v=3';s.onload=()=>{const u=document.createElement('script');u.src='regions-8-10-ui.js?v=3';document.body.appendChild(u)};document.body.appendChild(s);
})();
