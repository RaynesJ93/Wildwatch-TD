// HOME_MOBILE_FIT_V2 — compact Home + lower-cost mobile battle rendering.
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
 // Observe only screen class changes, not every descendant mutation.
 const screens=[...document.querySelectorAll('.screen')];
 const observer=new MutationObserver(sync);screens.forEach(el=>observer.observe(el,{attributes:true,attributeFilter:['class']}));

 // MOBILE_BATTLE_RENDER_THROTTLE_V1
 // Keep simulation/update running at requestAnimationFrame speed, but cap expensive
 // full-canvas painting to ~30 FPS on phone-sized screens. This does NOT alter
 // enemy speed, tower cooldowns, damage, wave timing or the 1x/2x/3x speed setting.
 if(window.matchMedia('(max-width:600px)').matches && typeof draw==='function'){
   const fullDraw=draw;
   let lastPaint=0;
   draw=function(){
     const active=(typeof battle!=='undefined'&&battle&&battle.started&&document.getElementById('battleScreen')?.classList.contains('active'));
     if(active){
       const now=performance.now();
       if(now-lastPaint<32)return;
       lastPaint=now;
     }
     return fullDraw();
   };
 }
})();
