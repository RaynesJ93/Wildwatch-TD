// Expanded Milestone + Challenge quests V1
(()=>{
 const addMilestones=[
  {id:'animalKeeper10',icon:'🐾',name:'Animal Keeper',text:'Unlock 10 animal cards',reward:500,type:'allOwned',goal:10},
  {id:'masterCollector25',icon:'🃏',name:'Master Collector',text:'Unlock 25 animal cards',reward:750,type:'allOwned',goal:25},
  {id:'zooKeeper75',icon:'🦁',name:'Zoo Keeper',text:'Collect 75 cards from packs',reward:1500,type:'cardsCollected',goal:75},
  {id:'fullSanctuary',icon:'🏆',name:'Full Sanctuary',text:'Unlock every animal card',reward:2500,type:'allOwned',goal:'allCards'},
  {id:'veteranDefenderKills',icon:'⚔️',name:'Veteran Defender',text:'Defeat 1,000 enemies',reward:500,type:'totalKills',goal:1000},
  {id:'exterminator',icon:'💥',name:'Exterminator',text:'Defeat 10,000 enemies',reward:2000,type:'totalKills',goal:10000},
  {id:'towerArchitect',icon:'🏗️',name:'Tower Architect',text:'Place 500 towers',reward:750,type:'totalPlaced',goal:500},
  {id:'upgradeAddict',icon:'⬆️',name:'Upgrade Addict',text:'Upgrade towers 500 times',reward:1000,type:'totalUpgrades',goal:500},
  {id:'risingStars',icon:'⭐',name:'Rising Stars',text:'Get 5 cards to Card Level 5',reward:500,type:'cardsLevel5',goal:5},
  {id:'animalMasters',icon:'🔟',name:'Animal Masters',text:'Get 5 cards to Card Level 10',reward:1500,type:'cardsLevel10',goal:5},
  {id:'hardcoreDefender25',icon:'🔥',name:'Hardcore Defender',text:'Complete 25 Hard Mode maps',reward:1500,type:'hardMapsTotal',goal:25},
  {id:'untouchable25',icon:'❤️',name:'Untouchable',text:'Complete 25 maps without losing a life',reward:1500,type:'flawlessMapsTotal',goal:25},
  {id:'bigSpenderMeat',icon:'🥩',name:'Big Spender — Upgrades',text:'Spend 25,000 meat on tower upgrades',reward:1000,type:'upgradeSpend',goal:25000},
  {id:'bigSpenderCoins',icon:'🪙',name:'Big Spender',text:'Spend 50,000 coins',reward:2000,type:'metaCoinsSpent',goal:50000},
  {id:'shardHoarder',icon:'💠',name:'Shard Hoarder',text:'Collect 500 shards',reward:1500,type:'totalShards',goal:500},
  {id:'firstThingsFirst',icon:'🎯',name:'First Things First',text:'Get 2,500 kills using First targeting',reward:750,type:'firstKillsTotal',goal:2500}
 ];
 addMilestones.forEach(q=>{if(!MILESTONE_QUESTS.some(x=>x.id===q.id))MILESTONE_QUESTS.push(q)});
 const addChallenges=[
  {id:'threeCompany',icon:'3️⃣',name:"Three’s Company",text:'Complete a map using only 3 animal types',reward:400,rewardKind:'coins',type:'challengeThreeTypes',goal:1,tier:1},
  {id:'maxPower',icon:'🔟',name:'Max Power',text:'Get a tower to Level 10',reward:500,rewardKind:'coins',type:'challengeMaxPower',goal:1,tier:1},
  {id:'rapidExpansion',icon:'🏗️',name:'Rapid Expansion',text:'Place 8 towers before Wave 5',reward:350,rewardKind:'coins',type:'challengeRapidExpansion',goal:1,tier:1},
  {id:'firstContact',icon:'🎯',name:'First Contact',text:'Get 150 kills using First targeting',reward:400,rewardKind:'coins',type:'challengeFirstKills',goal:150,tier:1},
  {id:'strongestSurvives',icon:'💪',name:'Strongest Survives',text:'Get 100 kills using Strongest targeting',reward:400,rewardKind:'coins',type:'challengeStrongestKills',goal:100,tier:1},
  {id:'lastChance',icon:'⏮️',name:'Last Chance',text:'Get 75 kills using Last targeting',reward:400,rewardKind:'coins',type:'challengeLastKills',goal:75,tier:1},
  {id:'silverbackSmash',icon:'🦍',name:'Silverback Smash',text:'Get 100 kills with Silverback Gorilla',reward:600,rewardKind:'coins',type:'challengeSilverbackKills',goal:100,tier:1},
  {id:'toxicWarfare',icon:'🦨',name:'Toxic Warfare',text:'Get 100 kills with Skunk',reward:600,rewardKind:'coins',type:'challengeSkunkKills',goal:100,tier:1},
  {id:'goldenFeathers',icon:'🦅',name:'Golden Feathers',text:'Get 50 kills with a Level 10 Eagle',reward:900,rewardKind:'coins',type:'challengeGoldenEagleKills',goal:50,tier:1},
  {id:'waterCannon',icon:'🐘',name:'Water Cannon',text:'Deal 10,000 damage with Elephant',reward:600,rewardKind:'coins',type:'challengeElephantDamage',goal:10000,tier:1},
  {id:'waveWarrior',icon:'🌊',name:'Wave Warrior',text:'Clear 15 waves without losing a life',reward:500,rewardKind:'coins',type:'challengeNoLossWaves',goal:15,tier:1},
  {id:'hardModeHero',icon:'🔥',name:'Hard Mode Hero',text:'Complete a Hard Mode map',reward:600,rewardKind:'coins',type:'challengeHardWin',goal:1,tier:1},
  {id:'rareSquad',icon:'💎',name:'Rare Squad',text:'Win using only Rare-or-better cards',reward:900,rewardKind:'coins',type:'challengeRarePlus',goal:1,tier:1},
  {id:'closeCall',icon:'❤️',name:'Close Call',text:'Win a map with 5 or fewer lives remaining',reward:500,rewardKind:'coins',type:'challengeCloseCall',goal:1,tier:1},
  {id:'handsOff',icon:'🙌',name:'Hands Off',text:'Clear 3 consecutive waves without placing or upgrading',reward:600,rewardKind:'coins',type:'challengeHandsOff',goal:1,tier:1}
 ];
 addChallenges.forEach(q=>{if(!CHALLENGE_QUESTS.some(x=>x.id===q.id))CHALLENGE_QUESTS.push(q)});
 const oldState=questState;
 questState=function(q){
  let st=oldState(q);
  const n=v=>Math.max(0,Number(v||0));
  if(q.goal==='allCards'&&q.type==='allOwned'){const g=Object.keys(animals).length,p=(save.unlocked||[]).length;return {goal:g,progress:p,completed:p>=g,ratio:g?Math.min(1,p/g):0}}
  const counters={totalKills:'totalKills',totalPlaced:'totalTowersPlaced',totalUpgrades:'totalTowerUpgrades',hardMapsTotal:'totalHardMaps',flawlessMapsTotal:'totalFlawlessMaps',upgradeSpend:'totalUpgradeSpend',metaCoinsSpent:'totalMetaCoinsSpent',totalShards:'totalShardsCollected',firstKillsTotal:'totalFirstKills'};
  if(counters[q.type]){const g=Number(q.goal||1),p=n(save[counters[q.type]]);return {goal:g,progress:p,completed:p>=g,ratio:Math.min(1,p/g)}}
  if(q.type==='cardsLevel5'||q.type==='cardsLevel10'){const lvl=q.type==='cardsLevel5'?5:10,g=Number(q.goal||1),p=Object.keys(animals).filter(k=>typeof cardLevel==='function'&&cardLevel(k)>=lvl).length;return {goal:g,progress:p,completed:p>=g,ratio:Math.min(1,p/g)}}
  return st;
 };
 const oldEval=evaluateMapChallenges;
 evaluateMapChallenges=function(){oldEval();const used=[...new Set(battle.usedCards||[])];if(used.length===3)addChallengeProgress('challengeThreeTypes',1);if(hardMode)addChallengeProgress('challengeHardWin',1);if(used.length&&used.every(k=>['Rare','Epic','Legendary'].includes(animals[k]?.rarity)))addChallengeProgress('challengeRarePlus',1);if(Number(battle.lives||0)<=5)addChallengeProgress('challengeCloseCall',1)};
 const oldAdd=addQuestProgress;
 addQuestProgress=function(type,n=1){oldAdd(type,n);if(type==='firstKills')addChallengeProgress('challengeFirstKills',n);if(type==='strongestKills')addChallengeProgress('challengeStrongestKills',n);if(type==='lastKills')addChallengeProgress('challengeLastKills',n);};
 setTimeout(()=>{if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards()},0);

 // HOME_YELLOW_TEXT_PROGRESS_FIT_V2
 const homeStyle=document.createElement('style');
 homeStyle.id='home-yellow-text-progress-fit-v2';
 homeStyle.textContent=`
   #homeScreen, #homeScreen .section-title, #homeScreen .hero h1, #homeScreen .hero p,
   #homeScreen .deckslot, #homeScreen .info-box, #homeScreen .info-box b,
   #homeScreen #bestWave, #homeScreen #ownedCount { color:#ffd65a !important; }
   #homeScreen .info-grid { grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important; gap:8px !important; }
   #homeScreen .info-grid .info-box { min-width:0 !important; overflow:hidden !important; padding:7px 5px !important; text-align:center !important; }
   #homeScreen .info-grid .info-box b { display:block !important; width:100% !important; font-size:11px !important; line-height:1 !important; white-space:nowrap !important; overflow:hidden !important; text-overflow:clip !important; letter-spacing:-0.2px !important; }
   #homeScreen #bestWave, #homeScreen #ownedCount { font-size:22px !important; line-height:.95 !important; margin-top:3px !important; white-space:nowrap !important; }
   @media(max-width:390px){ #homeScreen .info-grid .info-box b{font-size:10px !important;} #homeScreen #bestWave,#homeScreen #ownedCount{font-size:20px !important;} }
 `;
 document.head.appendChild(homeStyle);
})();
