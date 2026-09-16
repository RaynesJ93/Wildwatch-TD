// HOME_MOBILE_FIT_V4 — compact Home + safe global map-base removal.
(()=>{
 const css=`
@media (max-width:600px){
  body.home-fit{overflow:hidden}
  body.home-fit #app{height:100dvh;min-height:100dvh;padding:calc(env(safe-area-inset-top) + 2px) 10px calc(67px + env(safe-area-inset-bottom));overflow:hidden}
  body.home-fit .topbar{height:82px;padding:2px 2px 4px;align-items:center}
  body.home-fit .topbar .brand img{height:68px!important;width:min(285px,58vw)!important}
  body.home-fit .topbar .stats{gap:4px;max-width:39vw}
  body.home-fit .topbar .pill{padding:5px 8px;font-size:12px}
  body.home-fit #homeScreen{height:calc(100dvh - 151px - env(safe-area-inset-top) - env(safe-area-inset-bottom));display:flex!important;flex-direction:column;overflow:hidden}
  body.home-fit #homeScreen>.hero{padding:10px 14px!important;border-radius:18px;flex:0 0 auto}
  body.home-fit #homeScreen>.hero h1{font-size:clamp(20px,5.2vw,27px)!important;line-height:1!important;margin:0 0 4px!important}
  body.home-fit #homeScreen>.hero p{font-size:clamp(12px,3.25vw,16px);line-height:1.25}
  body.home-fit #homeScreen>.hero>div[style*="height:14px"]{height:5px!important}
  body.home-fit #chooseSaveBtn img{max-height:82px!important;width:94%!important;margin:auto}
  body.home-fit #continueBtn{height:67px!important;min-height:67px!important;margin-top:2px!important;padding:10px 54px!important;font-size:15px!important}
  body.home-fit #homeScreen>.section-title{font-size:17px;margin:7px 3px 3px}
  body.home-fit #homeDeck{margin:1px 0 3px;gap:6px;min-height:75px}
  body.home-fit #homeDeck>.deckslot{min-height:73px!important;height:73px!important;padding:3px!important;font-size:10px!important}
  body.home-fit #homeDeck .mini-portrait{width:36px!important;height:36px!important;margin-bottom:1px!important}
  body.home-fit #homeDeck .animal{font-size:31px!important;margin:1px 0!important}
  body.home-fit #homeScreen>.info-grid{gap:5px;min-height:78px}
  body.home-fit #homeScreen>.info-grid>.info-box{min-height:78px!important;height:78px!important;padding:8px 11px!important;background-size:200% 100%!important}
  body.home-fit #homeScreen>.info-grid>.info-box:first-child{background-position:left center!important}
  body.home-fit #homeScreen>.info-grid>.info-box:last-child{background-position:right center!important}
  body.home-fit #homeScreen>.info-grid>.info-box b{font-size:14px!important;line-height:1.05!important}
  body.home-fit #bestWave,body.home-fit #ownedCount{font-size:24px!important;line-height:1!important;margin-top:3px}
  body.home-fit .nav{padding-top:4px;padding-bottom:calc(4px + env(safe-area-inset-bottom))}
  body.home-fit .nav button{padding:3px 2px;font-size:10px}
  body.home-fit .nav .ico{font-size:20px}
}
@media (max-width:600px) and (max-height:760px){
  body.home-fit .topbar{height:70px}
  body.home-fit .topbar .brand img{height:57px!important}
  body.home-fit #homeScreen{height:calc(100dvh - 139px - env(safe-area-inset-top) - env(safe-area-inset-bottom))}
  body.home-fit #homeScreen>.hero{padding:7px 12px!important}
  body.home-fit #homeScreen>.hero p{font-size:11px;line-height:1.15}
  body.home-fit #chooseSaveBtn img{max-height:68px!important}
  body.home-fit #continueBtn{height:56px!important;min-height:56px!important}
  body.home-fit #homeScreen>.section-title{margin:4px 3px 2px;font-size:15px}
  body.home-fit #homeDeck>.deckslot{height:62px!important;min-height:62px!important}
  body.home-fit #homeDeck .mini-portrait{width:30px!important;height:30px!important}
  body.home-fit #homeScreen>.info-grid>.info-box{height:68px!important;min-height:68px!important}
}
`;
 const style=document.createElement('style');style.id='home-mobile-fit-style';style.textContent=css;document.head.appendChild(style);
 function sync(){document.body.classList.toggle('home-fit',document.getElementById('homeScreen')?.classList.contains('active'));}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',sync);else sync();
 const screens=[...document.querySelectorAll('.screen')];
 const observer=new MutationObserver(sync);screens.forEach(el=>observer.observe(el,{attributes:true,attributeFilter:['class']}));

 // REMOVE_ALL_MAP_BASES_V1
 // Install the canvas hooks once. During normal drawing they are transparent pass-throughs.
 // Only while draw() is running do they suppress the legacy THEMATIC_MAP_BASES block and
 // its artificial route extension. Enemy paths, spawning, towers and gameplay are untouched.
 const c=document.getElementById('game'),g=c?.getContext('2d');
 if(g&&typeof draw==='function'&&!window.__critterNoMapBases){
   window.__critterNoMapBases=true;
   const oldDraw=draw;
   const o={
     save:g.save.bind(g),restore:g.restore.bind(g),translate:g.translate.bind(g),beginPath:g.beginPath.bind(g),moveTo:g.moveTo.bind(g),lineTo:g.lineTo.bind(g),stroke:g.stroke.bind(g),fill:g.fill.bind(g),fillRect:g.fillRect.bind(g),strokeRect:g.strokeRect.bind(g),fillText:g.fillText.bind(g),strokeText:g.strokeText.bind(g)
   };
   const st={on:false,bx:0,by:0,px:0,py:0,armed:false,depth:0,baseDepth:-1,lastMove:null,lastLine:null};
   g.save=function(){if(st.on)st.depth++;return o.save();};
   g.translate=function(x,y){if(st.on&&!st.armed&&Math.abs(x-st.bx)<.02&&Math.abs(y-st.by)<.02){st.armed=true;st.baseDepth=st.depth;return o.translate(100000,100000);}return o.translate(x,y);};
   g.restore=function(){const base=st.on&&st.armed&&st.depth===st.baseDepth,r=o.restore();if(st.on){if(base){st.armed=false;st.baseDepth=-1;}st.depth=Math.max(0,st.depth-1);}return r;};
   g.beginPath=function(){if(st.on){st.lastMove=null;st.lastLine=null;}return o.beginPath();};
   g.moveTo=function(x,y){if(st.on)st.lastMove=[x,y];return o.moveTo(x,y);};
   g.lineTo=function(x,y){if(st.on)st.lastLine=[x,y];return o.lineTo(x,y);};
   g.stroke=function(){if(st.on){const route=!!(st.lastMove&&st.lastLine&&Math.hypot(st.lastMove[0]-st.px,st.lastMove[1]-st.py)<.02&&Math.hypot(st.lastLine[0]-st.bx,st.lastLine[1]-st.by)<.02&&g.lineWidth===72);if(st.armed||route)return;}return o.stroke();};
   g.fill=function(){if(st.on&&st.armed)return;return o.fill();};
   g.fillRect=function(...a){if(st.on&&st.armed)return;return o.fillRect(...a);};
   g.strokeRect=function(...a){if(st.on&&st.armed)return;return o.strokeRect(...a);};
   g.fillText=function(...a){if(st.on&&st.armed)return;return o.fillText(...a);};
   g.strokeText=function(...a){if(st.on&&st.armed)return;return o.strokeText(...a);};
   draw=function(){
     if(!Array.isArray(path)||path.length<2)return oldDraw();
     const end=path[path.length-1],prev=path[path.length-2],dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1,ux=dx/len,uy=dy/len,margin=82;
     st.bx=Math.max(margin,Math.min(c.width-margin,end[0]-ux*78));st.by=Math.max(margin,Math.min(c.height-margin,end[1]-uy*78));st.px=prev[0];st.py=prev[1];st.armed=false;st.depth=0;st.baseDepth=-1;st.lastMove=null;st.lastLine=null;st.on=true;
     try{return oldDraw();}finally{st.on=false;st.armed=false;st.depth=0;st.baseDepth=-1;}
   };
 }
})();
