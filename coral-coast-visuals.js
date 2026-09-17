// CORAL_COAST_VISUALS_V23 — UI, map reward fix, and quest tracking audit
(()=>{
 const coreDraw=draw,MAP_MAX=10;
 function installTopBrandBanner(){const brand=document.querySelector('.topbar .brand');if(!brand||brand.dataset.ccBanner==='1')return;brand.dataset.ccBanner='1';brand.setAttribute('aria-label','Critter Clash Tower Defence');brand.innerHTML='';const img=document.createElement('img');img.src='assets/critter-clash-tower-defence-banner.png?v=23';img.alt='Critter Clash Tower Defence';img.style.cssText='display:block;width:min(290px,52vw);height:74px;object-fit:contain;object-position:left center;';brand.appendChild(img);}
 function installSquadHeading(){const el=[...document.querySelectorAll('h1,h2,h3')].find(e=>/build\s+your\s+animal\s+squad/i.test((e.textContent||'').trim()));if(!el||el.dataset.ccSquadHeading==='1')return;el.dataset.ccSquadHeading='1';el.style.cssText+='color:#ffd65a!important;font-family:Impact,"Arial Black",system-ui,sans-serif!important;font-size:clamp(22px,5.4vw,34px)!important;font-weight:800!important;letter-spacing:.2px!important;line-height:1.05!important;white-space:nowrap!important;margin-right:0!important;';}
 function installPlayNowArtwork(){const btn=[...document.querySelectorAll('button')].find(b=>/play\s*now/i.test((b.textContent||'').trim()));if(!btn||btn.dataset.ccPlayArtwork==='1')return;btn.dataset.ccPlayArtwork='1';btn.setAttribute('aria-label','Play Now');btn.textContent='';btn.style.cssText+='background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;overflow:visible!important;height:auto!important;min-height:0!important;';const img=document.createElement('img');img.src='assets/critter-clash-play-now-button.png?v=23';img.alt='Play Now';img.draggable=false;img.style.cssText='display:block;width:100%;height:auto;max-height:118px;object-fit:contain;pointer-events:none;';btn.appendChild(img);}
 function installContinueBattleBorder(){const btn=[...document.querySelectorAll('button')].find(b=>/continue\s*battle/i.test((b.textContent||'').trim()));if(!btn||btn.dataset.ccContinueBorder==='2')return;btn.dataset.ccContinueBorder='2';btn.style.cssText+='background-color:transparent!important;background-image:url("assets/critter-clash-continue-battle-border.png?v=23")!important;background-size:contain!important;background-position:center!important;background-repeat:no-repeat!important;border:0!important;box-shadow:none!important;height:92px!important;min-height:92px!important;padding:18px 70px!important;overflow:visible!important;display:flex!important;align-items:center!important;justify-content:center!important;';}
 function installDeckCardBorders(){const heading=[...document.querySelectorAll('h1,h2,h3,h4,.section-title')].find(e=>/current\s*deck/i.test((e.textContent||'').trim()));if(!heading)return;const area=heading.nextElementSibling;if(!area)return;[...area.children].filter(e=>e.nodeType===1).slice(0,4).forEach(card=>{if(card.dataset.ccVineBorder==='2')return;card.dataset.ccVineBorder='2';card.style.cssText+='border-color:transparent!important;border-style:solid!important;background-image:url("assets/critter-clash-card-vine-border.png?v=23")!important;background-size:100% 100%!important;background-position:center!important;background-repeat:no-repeat!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;text-align:center!important;padding:8px 5px!important;box-sizing:border-box!important;';[...card.children].forEach(child=>{child.style.marginLeft='auto';child.style.marginRight='auto';});});}
 function installUiArtwork(){installTopBrandBanner();installSquadHeading();installPlayNowArtwork();installContinueBattleBorder();installDeckCardBorders();}
 function bootUi(){installUiArtwork();setTimeout(installUiArtwork,150);setTimeout(installUiArtwork,600);}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bootUi,{once:true});else bootUi();

 // QUEST_TRACKING_AUDIT_V1 — wire every currently defined quest family to gameplay events.
 const n=v=>Math.max(0,Number(v||0));
 function saveNow(){if(typeof persist==='function')persist();}
 function weeklySet(type,value){
   if(typeof ensureWeeklyQuests!=='function')return;
   ensureWeeklyQuests();
   const q=(typeof WEEKLY_QUESTS!=='undefined'?WEEKLY_QUESTS:[]).find(x=>x.type===type);if(!q)return;
   save.weeklyQuests.progress[type]=Math.min(Number(q.goal||1),Math.max(n(save.weeklyQuests.progress[type]),n(value)));
 }
 // Mirror normal quest events into permanent milestone counters.
 if(typeof addQuestProgress==='function'){
   const oldAddQuestProgress=addQuestProgress;
   addQuestProgress=function(type,amount=1){
     const inc=n(amount);oldAddQuestProgress(type,amount);
     if(type==='kills')save.totalKills=n(save.totalKills)+inc;
     if(type==='placed')save.totalTowersPlaced=n(save.totalTowersPlaced)+inc;
     if(type==='upgrades')save.totalTowerUpgrades=n(save.totalTowerUpgrades)+inc;
     if(type==='firstKills')save.totalFirstKills=n(save.totalFirstKills)+inc;
     saveNow();
   };
 }
 // Card XP is used by both Daily Experienced and Weekly Training Week.
 if(typeof addCardXp==='function'){
   const oldAddCardXp=addCardXp;
   addCardXp=function(k,amount){const inc=n(amount);const r=oldAddCardXp(k,amount);if(inc){if(typeof addQuestProgress==='function')addQuestProgress('cardXp',inc);if(typeof addWeeklyProgress==='function')addWeeklyProgress('cardXp',inc);}return r;};
 }
 // Attribute kill-based quests to the tower that actually registered the kill.
 if(typeof killEnemy==='function'){
   const oldKillEnemy=killEnemy;
   killEnemy=function(e){
     if(!e||e.dead)return oldKillEnemy(e);
     const killer=battle?.lastAttackingTower||null,key=killer?.key,mode=killer?.targetMode||'first',level=n(killer?.level);
     const r=oldKillEnemy(e);
     if(mode==='last'&&typeof addQuestProgress==='function')addQuestProgress('lastKills',1);
     if(key==='silverback'&&typeof addChallengeProgress==='function')addChallengeProgress('challengeSilverbackKills',1);
     if(key==='skunk'&&typeof addChallengeProgress==='function')addChallengeProgress('challengeSkunkKills',1);
     if(key==='eagle'&&level>=10&&typeof addChallengeProgress==='function')addChallengeProgress('challengeGoldenEagleKills',1);
     if(key){
       if(typeof ensureWeeklyQuests==='function'){
         ensureWeeklyQuests();save.weeklyQuests.singleCardKillCounts=save.weeklyQuests.singleCardKillCounts||{};
         save.weeklyQuests.singleCardKillCounts[key]=n(save.weeklyQuests.singleCardKillCounts[key])+1;
         weeklySet('singleCardKills',Math.max(0,...Object.values(save.weeklyQuests.singleCardKillCounts).map(n)));
       }
     }
     saveNow();return r;
   };
 }
 // Exact Elephant damage tracking for the Water Cannon challenge.
 if(typeof towerTickCore==='function'){
   const oldTowerTickCore= towerTickCore;
   towerTickCore=function(t,dt){
     if(t?.key!=='elephant')return oldTowerTickCore(t,dt);
     const before=(battle.enemies||[]).reduce((s,e)=>s+(!e.dead?n(e.hp):0),0),r=oldTowerTickCore(t,dt),after=(battle.enemies||[]).reduce((s,e)=>s+(!e.dead?n(e.hp):0),0);
     const dealt=Math.max(0,Math.round(before-after));if(dealt&&typeof addChallengeProgress==='function')addChallengeProgress('challengeElephantDamage',dealt);return r;
   };
 }
 // Wave-level challenge tracking, including Hands Off streaks.
 if(typeof finishWave==='function'){
   const oldFinishWave=finishWave;
   finishWave=function(){
     const perfect=battle.lives===(battle.waveStartLives??battle.lives),placed=n(battle.totalPlaced),upgraded=n(battle.upgradeCount);
     const quiet=placed===n(battle._questPrevPlaced)&&upgraded===n(battle._questPrevUpgrades);
     battle._questHandsOffStreak=quiet?n(battle._questHandsOffStreak)+1:0;
     battle._questPrevPlaced=placed;battle._questPrevUpgrades=upgraded;
     const r=oldFinishWave();
     if(perfect&&typeof addChallengeProgress==='function')addChallengeProgress('challengeNoLossWaves',1);
     if(battle._questHandsOffStreak>=3&&!battle._questHandsOffAwarded&&typeof addChallengeProgress==='function'){battle._questHandsOffAwarded=true;addChallengeProgress('challengeHandsOff',1);}
     return r;
   };
 }
 function installQuestControlHooks(){
   if(typeof upgradeTower!=='undefined'&&upgradeTower?.onclick&&!upgradeTower.dataset.questAudit){
     upgradeTower.dataset.questAudit='1';const old=upgradeTower.onclick;upgradeTower.onclick=function(ev){const beforeCoins=n(battle?.coins),beforeLevel=n(selectedTower?.level),tower=selectedTower;const r=old.call(this,ev);const spent=Math.max(0,beforeCoins-n(battle?.coins));if(spent){save.totalUpgradeSpend=n(save.totalUpgradeSpend)+spent;if(tower&&beforeLevel<10&&n(tower.level)>=10&&!tower._questLevel10Counted){tower._questLevel10Counted=true;if(typeof addWeeklyProgress==='function')addWeeklyProgress('level10Towers',1);if(typeof addChallengeProgress==='function')addChallengeProgress('challengeMaxPower',1);}}saveNow();return r;};
   }
   if(typeof towerTargetMode!=='undefined'&&towerTargetMode?.onchange&&!towerTargetMode.dataset.questAudit){
     towerTargetMode.dataset.questAudit='1';const old=towerTargetMode.onchange;towerTargetMode.onchange=function(ev){const r=old.call(this,ev);battle.questTargetModes=Array.isArray(battle.questTargetModes)?battle.questTargetModes:['first'];const mode=this.value||'first';if(!battle.questTargetModes.includes(mode)){battle.questTargetModes.push(mode);if(typeof addQuestProgress==='function')addQuestProgress('targetModes',1);}return r;};
   }
   document.querySelectorAll('.chestBtn').forEach(btn=>{if(btn.dataset.questAudit||!btn.onclick)return;btn.dataset.questAudit='1';const old=btn.onclick;btn.onclick=function(ev){const beforeCoins=n(save.metaCoins),beforeShards=Object.values(save.shards||{}).reduce((s,v)=>s+n(v),0),r=old.call(this,ev),spent=Math.max(0,beforeCoins-n(save.metaCoins)),afterShards=Object.values(save.shards||{}).reduce((s,v)=>s+n(v),0);if(spent)save.totalMetaCoinsSpent=n(save.totalMetaCoinsSpent)+spent;if(afterShards>beforeShards)save.totalShardsCollected=n(save.totalShardsCollected)+(afterShards-beforeShards);saveNow();return r;};});
 }
 setTimeout(installQuestControlHooks,0);setTimeout(installQuestControlHooks,500);

 let completionRewardArmed=false;
 function processMapCompletion(){
   if(typeof battle==='undefined'||!battle)return;
   const complete=!!(battle.ended&&battle.mapComplete);if(!complete){completionRewardArmed=false;return;}if(completionRewardArmed)return;completionRewardArmed=true;
   if(!battle._mapCompletion200Awarded){battle._mapCompletion200Awarded=true;save.metaCoins=n(save.metaCoins)+200;battle.mapCoinsEarned=n(battle.mapCoinsEarned)+200;}
   if(!battle._questMapCompletionTracked){
     battle._questMapCompletionTracked=true;
     const used=[...new Set(battle.usedCards||[])],perfect=battle.lives===(battle.mapStartLives??battle.lives);
     if(typeof addWeeklyProgress==='function'){addWeeklyProgress('maps',1);if(perfect)addWeeklyProgress('flawlessMaps',1);if(hardMode&&!epicMode)addWeeklyProgress('hardMaps',1);}
     if(hardMode&&!epicMode)save.totalHardMaps=n(save.totalHardMaps)+1;if(perfect)save.totalFlawlessMaps=n(save.totalFlawlessMaps)+1;
     if(typeof ensureWeeklyQuests==='function'){
       ensureWeeklyQuests();save.weeklyQuests.winningCardsSeen=Array.isArray(save.weeklyQuests.winningCardsSeen)?save.weeklyQuests.winningCardsSeen:[];used.forEach(k=>{if(!save.weeklyQuests.winningCardsSeen.includes(k))save.weeklyQuests.winningCardsSeen.push(k)});weeklySet('winningCards',save.weeklyQuests.winningCardsSeen.length);
       save.weeklyQuests.regionsSeen=Array.isArray(save.weeklyQuests.regionsSeen)?save.weeklyQuests.regionsSeen:[];if(!save.weeklyQuests.regionsSeen.includes(currentSeries))save.weeklyQuests.regionsSeen.push(currentSeries);weeklySet('regions',save.weeklyQuests.regionsSeen.length);
     }
     if(used.length&&used.every(k=>['Common','Uncommon'].includes(animals[k]?.rarity)))addWeeklyProgress('commonUncommonWins',1);
     if(used.length&&used.every(k=>['Rare','Epic','Legendary'].includes(animals[k]?.rarity)))addWeeklyProgress('rarePlusWins',1);
     if(n(battle.totalPlaced)>=8&&n(battle._questEightPlacedWave)<=4&&typeof addChallengeProgress==='function')addChallengeProgress('challengeRapidExpansion',1);
   }
   saveNow();if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards();
 }
 // Record the wave at which the eighth tower was first present.
 function auditLiveBattle(){if(typeof battle==='undefined'||!battle)return;if(n(battle.totalPlaced)>=8&&battle._questEightPlacedWave==null)battle._questEightPlacedWave=n(battle.wave);}

 draw=function(){coreDraw();auditLiveBattle();processMapCompletion();};
 const s=document.createElement('script');s.src='regions-8-10.js?v=24';s.onload=()=>{const u=document.createElement('script');u.src='regions-8-10-ui.js?v=25';document.body.appendChild(u)};document.body.appendChild(s);
 const homeFit=document.createElement('script');homeFit.src='home-mobile-fit.js?v=3';document.body.appendChild(homeFit);
})();