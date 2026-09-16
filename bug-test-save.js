// BUG_TEST_SAVE_V1 — dedicated Slot 4 for testing; never overwrites Slots 1–3.
(()=>{
 const SLOT='4',KEY='wildwatchSaveSlot4';
 function buildBugSave(){
   if(typeof animals==='undefined'||typeof defaults==='undefined')return null;
   const keys=Object.keys(animals),all={...defaults};
   all.metaCoins=9999999;all.level=100;all.xp=0;all.packTokens=9999;all.bestWave=15;
   all.unlocked=[...keys];all.deck=keys.slice(0,4);
   all.shards={};all.cardLevels={};all.cardXP={};all.masteryLevels={};all.masteryShards={};all.mythicAnimals={};
   keys.forEach(k=>{all.shards[k]=9999;all.cardLevels[k]=50;all.cardXP[k]=0;all.masteryLevels[k]=10;all.masteryShards[k]=9999;all.mythicAnimals[k]=true;});
   all.mythicShards=9999;all.totalCardsCollected=keys.length;all.totalPacksOpened=0;all.totalWaves=0;
   all.forestPinesUnlocked=10;all.desertDunesUnlocked=10;all.hauntedWoodsUnlocked=10;all.tundraFallsUnlocked=10;all.volcanicWastelandUnlocked=10;all.crystalCavernsUnlocked=10;
   all.coralCoastUnlocked=10;all.region7Unlocked=10;all.region8Unlocked=10;all.region9Unlocked=10;all.region10Unlocked=10;
   all.forestPinesSelected=1;all.hauntedWoodsSelected=1;all.tundraFallsSelected=1;all.volcanicWastelandSelected=1;all.crystalCavernsSelected=1;all.selectedSeries=1;all.selectedSeriesMap=1;all.battleDifficulty='normal';
   all.normalCompleted={};all.hardCompleted={};for(let r=1;r<=10;r++)for(let m=1;m<=10;m++)all.normalCompleted[`${r}-${m}`]=true;
   // Leave Hard completions and quest counters fresh so progression/quest bugs can still be tested.
   all.totalKills=0;all.totalTowersPlaced=0;all.totalTowerUpgrades=0;all.totalHardMaps=0;all.totalFlawlessMaps=0;all.totalUpgradeSpend=0;all.totalMetaCoinsSpent=0;all.totalShardsCollected=0;all.totalFirstKills=0;
   delete all.dailyQuests;delete all.weeklyQuests;delete all.weeklyProgress;delete all.challengeQuests;delete all.milestoneProgress;
   return all;
 }
 function ensureRecord(force=false){
   if(!force&&localStorage.getItem(KEY))return;
   const s=buildBugSave();if(!s)return;
   localStorage.setItem(KEY,JSON.stringify({version:2,name:'🧪 Bug Test — Everything Unlocked',savedAt:new Date().toISOString(),save:s}));
 }
 function install(){
   ensureRecord(false);
   const list=document.getElementById('saveSlotList');if(!list||document.getElementById('bugTestSlotBtn'))return;
   const b=document.createElement('button');b.className='primary';b.id='bugTestSlotBtn';b.innerHTML='<b>🧪 Bug Test — Everything Unlocked</b><span style="font-size:12px;opacity:.82">All cards Lv50/Mastery 10 • All maps unlocked • 9,999,999 Coins</span>';
   b.style.cssText='display:grid;gap:4px;text-align:left;border-color:#ffd65a;';
   b.onclick=()=>{ensureRecord(false);if(typeof loadFromSlot==='function')loadFromSlot(SLOT);};list.appendChild(b);
   const reset=document.createElement('button');reset.className='secondary';reset.id='resetBugTestSaveBtn';reset.textContent='↻ Reset Bug Test Save';reset.style.cssText='width:100%;margin-top:8px';reset.onclick=()=>{if(!confirm('Reset only the Bug Test save back to everything unlocked? Your other saves will not be changed.'))return;ensureRecord(true);if(typeof renderSaveSlots==='function')renderSaveSlots();if(typeof setSaveStatus==='function')setSaveStatus('Bug Test save reset. Saves 1–3 were not changed.');};list.after(reset);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(install,0),{once:true});else setTimeout(install,0);
})();