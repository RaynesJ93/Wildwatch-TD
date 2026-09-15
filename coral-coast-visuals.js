// CORAL_COAST_VISUALS_V14 — global legacy-base suppression + branded title/play button
(()=>{
 const coreDraw=draw,MAP_MAX=10;

 function installTopBrandBanner(){
  const brand=document.querySelector('.topbar .brand');
  if(!brand||brand.dataset.ccBanner==='1')return;
  brand.dataset.ccBanner='1';
  brand.setAttribute('aria-label','Critter Clash Tower Defence');
  brand.innerHTML='';
  const img=document.createElement('img');
  img.src='assets/critter-clash-tower-defence-banner.png?v=14';
  img.alt='Critter Clash Tower Defence';
  img.style.cssText='display:block;width:min(290px,52vw);height:74px;object-fit:contain;object-position:left center;';
  brand.appendChild(img);
 }

 // Replace only the visual contents of the existing Play Now button. The original
 // button element, id, click listener and navigation behaviour are left untouched.
 function installPlayNowArtwork(){
  const buttons=[...document.querySelectorAll('button')];
  const btn=buttons.find(b=>/play\s*now/i.test((b.textContent||'').trim()));
  if(!btn||btn.dataset.ccPlayArtwork==='1')return;
  btn.dataset.ccPlayArtwork='1';
  btn.setAttribute('aria-label','Play Now');
  btn.textContent='';
  btn.style.cssText+='background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;overflow:visible!important;height:auto!important;min-height:0!important;';
  const img=document.createElement('img');
  img.src='assets/critter-clash-play-now-button.png?v=14';
  img.alt='Play Now';
  img.draggable=false;
  img.style.cssText='display:block;width:100%;height:auto;max-height:118px;object-fit:contain;pointer-events:none;';
  btn.appendChild(img);
 }
 function installUiArtwork(){installTopBrandBanner();installPlayNowArtwork();}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installUiArtwork);else installUiArtwork();
 new MutationObserver(installPlayNowArtwork).observe(document.body,{childList:true,subtree:true});

 function drawWithoutLegacyBase(){
  const c=document.getElementById('game')||document.querySelector('canvas');
  const g=c?.getContext('2d');
  if(!g||!Array.isArray(path)||path.length<2){coreDraw();return;}
  const end=path[path.length-1],prev=path[path.length-2];
  const dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1,ux=dx/len,uy=dy/len,margin=82;
  let bx=end[0]-ux*78,by=end[1]-uy*78;
  bx=Math.max(margin,Math.min(c.width-margin,bx));
  by=Math.max(margin,Math.min(c.height-margin,by));
  const originalTranslate=g.translate.bind(g),originalSave=g.save.bind(g),originalRestore=g.restore.bind(g),originalStroke=g.stroke.bind(g),originalFill=g.fill.bind(g),originalFillRect=g.fillRect.bind(g),originalStrokeRect=g.strokeRect.bind(g),originalFillText=g.fillText.bind(g),originalStrokeText=g.strokeText.bind(g),originalBeginPath=g.beginPath.bind(g),originalMoveTo=g.moveTo.bind(g),originalLineTo=g.lineTo.bind(g);
  let armed=false,depth=0,baseDepth=-1,lastMove=null,lastLine=null;
  g.save=function(){depth++;return originalSave();};
  g.translate=function(x,y){if(!armed&&Math.abs(x-bx)<.01&&Math.abs(y-by)<.01){armed=true;baseDepth=depth;return originalTranslate(100000,100000);}return originalTranslate(x,y);};
  g.restore=function(){const wasBase=armed&&depth===baseDepth,r=originalRestore();if(wasBase){armed=false;baseDepth=-1;}depth=Math.max(0,depth-1);return r;};
  g.beginPath=function(){lastMove=null;lastLine=null;return originalBeginPath();};
  g.moveTo=function(x,y){lastMove=[x,y];return originalMoveTo(x,y);};
  g.lineTo=function(x,y){lastLine=[x,y];return originalLineTo(x,y);};
  g.stroke=function(){const route=!!(lastMove&&lastLine&&Math.hypot(lastMove[0]-prev[0],lastMove[1]-prev[1])<.1&&Math.hypot(lastLine[0]-bx,lastLine[1]-by)<.1&&g.lineWidth===72);if(armed||route)return;return originalStroke();};
  g.fill=function(){if(armed)return;return originalFill();};
  g.fillRect=function(...a){if(armed)return;return originalFillRect(...a);};
  g.strokeRect=function(...a){if(armed)return;return originalStrokeRect(...a);};
  g.fillText=function(...a){if(armed)return;return originalFillText(...a);};
  g.strokeText=function(...a){if(armed)return;return originalStrokeText(...a);};
  try{coreDraw();}finally{g.save=originalSave;g.restore=originalRestore;g.translate=originalTranslate;g.stroke=originalStroke;g.fill=originalFill;g.fillRect=originalFillRect;g.strokeRect=originalStrokeRect;g.fillText=originalFillText;g.strokeText=originalStrokeText;g.beginPath=originalBeginPath;g.moveTo=originalMoveTo;g.lineTo=originalLineTo;}
 }

 function coastDecor(ctx,w,h,map){ctx.save();ctx.globalAlpha=.14;ctx.strokeStyle=map>=8?'#063d67':'#e8ffff';ctx.lineWidth=4;for(let y=45;y<h;y+=88){ctx.beginPath();for(let x=-25;x<w+45;x+=44){ctx.moveTo(x,y);ctx.quadraticCurveTo(x+11,y-7,x+22,y);ctx.quadraticCurveTo(x+33,y+7,x+44,y)}ctx.stroke()}ctx.globalAlpha=.42;ctx.font='15px system-ui';const a=['🪸','🐚','🌿','🫧'],pts=[[.06,.34],[.91,.42],[.11,.85],[.85,.68],[.48,.13],[.53,.90],[.29,.53],[.71,.52],[.19,.44],[.79,.32],[.37,.72],[.63,.26]];pts.forEach((p,i)=>ctx.fillText(a[(i+map)%4],w*p[0],h*p[1]));ctx.restore();}
 draw=function(){drawWithoutLegacyBase();if(currentSeries!==7||currentMap<1||currentMap>MAP_MAX)return;const c=document.getElementById('game')||document.querySelector('canvas'),ctx=c?.getContext('2d');if(!ctx)return;coastDecor(ctx,c.width,c.height,currentMap);};
 const s=document.createElement('script');s.src='regions-8-10.js?v=14';s.onload=()=>{const u=document.createElement('script');u.src='regions-8-10-ui.js?v=14';document.body.appendChild(u)};document.body.appendChild(s);
})();
