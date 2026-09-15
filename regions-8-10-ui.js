// REGIONS_8_10_UI_V1
(()=>{
 const names={8:'Lost Jungle',9:'Enchanted Wilds',10:'Sky Highlands'};
 const icons={8:'🌿',9:'🍄',10:'🌩️'};
 // Region 8 becomes available after Coral Coast 7-10 Normal is cleared.
 if(save.normalCompleted?.['7-10']&&!(save.region8Unlocked>0))save.region8Unlocked=1;
 if(save.normalCompleted?.['8-10']&&!(save.region9Unlocked>0))save.region9Unlocked=1;
 if(save.normalCompleted?.['9-10']&&!(save.region10Unlocked>0))save.region10Unlocked=1;
 persist();
 sanctuaryUnlocked=function(series){if(series===7)return save.coralCoastUnlocked||0;if(series>=8&&series<=10)return save['region'+series+'Unlocked']||0;return seriesUnlockedCount(series)};
 renderMapSanctuary=function(){
  const wrap=document.getElementById('mapSanctuary');if(!wrap)return;
  if(!SANCTUARY_META[mapMenuSeries]||!sanctuaryUnlocked(mapMenuSeries))mapMenuSeries=1;
  const meta=SANCTUARY_META[mapMenuSeries],unlocked=Math.max(mapMenuSeries===1?1:0,sanctuaryUnlocked(mapMenuSeries));
  const tabs=document.getElementById('regionTabs');
  tabs.innerHTML=Array.from({length:10},(_,i)=>i+1).map(series=>{const m=SANCTUARY_META[series],locked=series>1&&sanctuaryUnlocked(series)<1;return `<button class="region-tab ${series===mapMenuSeries?'active':''} ${locked?'locked':''}" data-region="${series}" ${locked?'disabled':''}>REGION ${series}<b>${locked?'🔒 LOCKED':m.icon+' '+m.name.toUpperCase()}</b></button>`}).join('');
  tabs.querySelectorAll('.region-tab:not(.locked)').forEach(btn=>btn.onclick=()=>{mapMenuSeries=+btn.dataset.region;renderMapSanctuary()});
  const hero=document.getElementById('regionHero');hero.className=`region-hero ${meta.className}`;
  document.getElementById('sanctuaryRegionName').textContent=meta.name;document.getElementById('sanctuaryRegionDesc').textContent=meta.desc;document.getElementById('sanctuaryRegionNumber').textContent=`REGION ${mapMenuSeries}`;document.getElementById('sanctuaryStageTitle').textContent=meta.name.toUpperCase();
  const normalBtn=document.getElementById('sanctuaryNormal'),hardBtn=document.getElementById('sanctuaryHard');normalBtn.classList.toggle('active',mapMenuDifficulty==='normal');hardBtn.classList.toggle('active',mapMenuDifficulty==='hard');normalBtn.onclick=()=>{mapMenuDifficulty='normal';renderMapSanctuary()};hardBtn.onclick=()=>{mapMenuDifficulty='hard';renderMapSanctuary()};
  document.getElementById('sanctuaryModeHint').textContent=mapMenuDifficulty==='hard'?'Hard stages require that same stage to be cleared on Normal first.':'Complete each Normal stage to unlock the next stage and its Hard mode.';
  const grid=document.getElementById('sanctuaryStageGrid');grid.innerHTML=meta.stages.map((name,i)=>{const n=i+1,key=`${mapMenuSeries}-${n}`,locked=n>unlocked,normalDone=!!save.normalCompleted?.[key],hardDone=!!save.hardCompleted?.[key],modeLocked=mapMenuDifficulty==='hard'&&!normalDone,inaccessible=locked||modeLocked,cleared=mapMenuDifficulty==='hard'?hardDone:normalDone,stars=hardDone?3:normalDone?2:0,starText=[0,1,2].map(x=>x<stars?'★':'☆').join('<br>'),status=locked?'Locked':modeLocked?'Clear Normal first':cleared?'Cleared • 15/15 waves':'Unlocked • 15 waves';return `<button class="stage-card ${cleared?'cleared':''} ${inaccessible?'locked':''}" data-stage="${n}" ${inaccessible?'disabled':''}><div class="stage-thumb ${meta.className}">${sanctuaryStageIcon(mapMenuSeries,n)}</div><div class="stage-copy"><div class="stage-num">${mapMenuSeries}-${n}</div><div class="stage-name">${name}</div><div class="stage-status">${status}</div></div><div>${inaccessible?'<div class="stage-lock">🔒</div>':`<div class="stage-stars">${starText}</div>`}</div></button>`}).join('');
  grid.querySelectorAll('.stage-card:not(.locked)').forEach(btn=>btn.onclick=()=>startSanctuaryStage(+btn.dataset.stage));
 };
 nextMap.onclick=()=>{if(currentMap<10){if(currentMap<currentSeriesUnlocked()){clearBattleState();applyMap(currentSeries,currentMap+1);resetBattle();draw()}return}if(currentSeries<10&&seriesUnlockedCount(currentSeries+1)>0){clearBattleState();applyMap(currentSeries+1,1);resetBattle();draw()}};
 // Re-render immediately so newly available region tabs appear without a reload.
 if(document.getElementById('mapSanctuary'))renderMapSanctuary();
})();
