// Expanded Milestone + Challenge quests V1
(()=>{
 const addMilestones=[
  {id:'animalKeeper10',icon:'🐾',name:'Animal Keeper',text:'Unlock 10 animal cards',reward:500,type:'allOwned',goal:10},
  {id:'masterCollector25',icon:'🃏',name:'Master Collector',text:'Unlock 25 animal cards',reward:750,type:'allOwned',goal:25},
  {id:'zooKeeper75',icon:'🃏',name:'Zoo Keeper',text:'Collect 75 cards from packs',reward:1500,type:'cardsCollected',goal:75},
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
 questState=function(q){let st=oldState(q);const n=v=>Math.max(0,Number(v||0));if(q.goal==='allCards'&&q.type==='allOwned'){const g=Object.keys(animals).length,p=(save.unlocked||[]).length;return {goal:g,progress:p,completed:p>=g,ratio:g?Math.min(1,p/g):0}}const counters={totalKills:'totalKills',totalPlaced:'totalTowersPlaced',totalUpgrades:'totalTowerUpgrades',hardMapsTotal:'totalHardMaps',flawlessMapsTotal:'totalFlawlessMaps',upgradeSpend:'totalUpgradeSpend',metaCoinsSpent:'totalMetaCoinsSpent',totalShards:'totalShardsCollected',firstKillsTotal:'totalFirstKills'};if(counters[q.type]){const g=Number(q.goal||1),p=n(save[counters[q.type]]);return {goal:g,progress:p,completed:p>=g,ratio:Math.min(1,p/g)}}if(q.type==='cardsLevel5'||q.type==='cardsLevel10'){const lvl=q.type==='cardsLevel5'?5:10,g=Number(q.goal||1),p=Object.keys(animals).filter(k=>typeof cardLevel==='function'&&cardLevel(k)>=lvl).length;return {goal:g,progress:p,completed:p>=g,ratio:Math.min(1,p/g)}}return st;};
 const oldEval=evaluateMapChallenges;evaluateMapChallenges=function(){oldEval();const used=[...new Set(battle.usedCards||[])];if(used.length===3)addChallengeProgress('challengeThreeTypes',1);if(hardMode)addChallengeProgress('challengeHardWin',1);if(used.length&&used.every(k=>['Rare','Epic','Legendary'].includes(animals[k]?.rarity)))addChallengeProgress('challengeRarePlus',1);if(Number(battle.lives||0)<=5)addChallengeProgress('challengeCloseCall',1)};
 const oldAdd=addQuestProgress;addQuestProgress=function(type,n=1){oldAdd(type,n);if(type==='firstKills')addChallengeProgress('challengeFirstKills',n);if(type==='strongestKills')addChallengeProgress('challengeStrongestKills',n);if(type==='lastKills')addChallengeProgress('challengeLastKills',n);};
 setTimeout(()=>{if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards()},0);
 const homeStyle=document.createElement('style');homeStyle.id='home-yellow-text-progress-fit-v2';homeStyle.textContent=`#homeScreen,#homeScreen .section-title,#homeScreen .hero h1,#homeScreen .hero p,#homeScreen .deckslot,#homeScreen .info-box,#homeScreen .info-box b,#homeScreen #bestWave,#homeScreen #ownedCount{color:#ffd65a!important}#homeScreen .info-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:8px!important}#homeScreen .info-grid .info-box{min-width:0!important;overflow:hidden!important;padding:7px 5px!important;text-align:center!important}#homeScreen .info-grid .info-box b{display:block!important;width:100%!important;font-size:11px!important;line-height:1!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:clip!important;letter-spacing:-.2px!important}#homeScreen #bestWave,#homeScreen #ownedCount{font-size:22px!important;line-height:.95!important;margin-top:3px!important;white-space:nowrap!important}@media(max-width:390px){#homeScreen .info-grid .info-box b{font-size:10px!important}#homeScreen #bestWave,#homeScreen #ownedCount{font-size:20px!important}}`;document.head.appendChild(homeStyle);

 // FIVE_UNCOMMON_ATTACKS_V3 — bespoke attacks, visible Flamingo, adaptive late-wave renderer.
 Object.assign(animals.ram,{desc:'Horn Charge attacks head-first. At Level 10, every 6th attack becomes Battering Ram: charges through up to 5 enemies, dealing 2x damage to the first and 75% to the rest with knockback.'});
 Object.assign(animals.turkey,{desc:'Fires spinning tail feathers. At Level 10, every 7th attack triggers Turkey Tantrum: 8 rapid feathers, each dealing 65% damage.'});
 Object.assign(animals.flamingo,{desc:'Long-range Beak Strike. At Level 10, every 6th attack triggers Flamingo Flock: 5 swooping flamingos deal 90% damage each and slow enemies by 20% for 2 seconds.'});
 Object.assign(animals.swan,{desc:'Fires a white Wing Gust. At Level 10, every 7th attack triggers Swan Storm: a powerful gust deals 1.75x damage to enemies in range and pushes them backwards.'});
 Object.assign(animals.spider,{desc:'Shoots sticky Web Shots. At Level 10, every 6th attack creates a Giant Web for 4 seconds, slowing enemies by 50% and dealing 35% tower damage per second.'});
 const fiveKeys=new Set(['ram','turkey','flamingo','swan','spider']);
 const _fiveOldTick=towerTickCore;
 towerTickCore=function(t,dt){
   if(!fiveKeys.has(t.key))return _fiveOldTick(t,dt);
   battle.lastAttackingTower=t;t.cd-=dt;if(t.cd>0)return;
   const range=cardBaseRange(t.key)*(1+(t.level-1)*.06),r2=range*range,pool=[];
   for(const e of battle.enemies){if(!e.dead&&e.hp>0){const dx=e.x-t.x,dy=e.y-t.y;if(dx*dx+dy*dy<=r2)pool.push(e)}}if(!pool.length)return;
   let target=pool[0];for(let i=1;i<pool.length;i++)if((pool[i].seg||0)>(target.seg||0))target=pool[i];
   const dmg=towerDamage(t);t.fiveCount=(t.fiveCount||0)+1;
   const shot=(kind,e=target,life=.38,extra={})=>{battle.shots.push({x:t.x,y:t.y-7,tx:e.x,ty:e.y,life,maxLife:life,type:'fiveCustomAttack',customAttack:kind,...extra});if(battle.shots.length>140)battle.shots.splice(0,battle.shots.length-140)};
   if(t.key==='ram'){const special=t.level>=10&&t.fiveCount%6===0,hits=special?pool.slice(0,5):[target];hits.forEach((e,i)=>{e.hp-=dmg*(i===0?(special?2:1):.75);if(special)e.tigerRoar=Math.max(e.tigerRoar||0,.28);shot('ram',e,.40,{special,index:i});if(e.hp<=0)killEnemy(e)});
   }else if(t.key==='turkey'){const special=t.level>=10&&t.fiveCount%7===0,count=special?8:1;for(let i=0;i<count;i++){let e=null;for(let j=0;j<pool.length;j++){const p=pool[(i+j)%pool.length];if(!p.dead&&p.hp>0){e=p;break}}if(!e)break;e.hp-=dmg*(special?.65:1);shot('turkey',e,.32+i*.035,{special,index:i});if(e.hp<=0)killEnemy(e)}}
   else if(t.key==='flamingo'){const special=t.level>=10&&t.fiveCount%6===0,count=special?5:1;for(let i=0;i<count;i++){let e=null;for(let j=0;j<pool.length;j++){const p=pool[(i+j)%pool.length];if(!p.dead&&p.hp>0){e=p;break}}if(!e)break;e.hp-=dmg*(special?.9:1);if(special)e.chickenSlowTimer=Math.max(e.chickenSlowTimer||0,2);shot('flamingo',e,.52+i*.045,{special,index:i});if(e.hp<=0)killEnemy(e)}}
   else if(t.key==='swan'){const special=t.level>=10&&t.fiveCount%7===0,hits=special?pool:[target];hits.forEach(e=>{e.hp-=dmg*(special?1.75:1);if(special)e.tigerRoar=Math.max(e.tigerRoar||0,.38);shot('swan',e,.42,{special});if(e.hp<=0)killEnemy(e)});}
   else{const special=t.level>=10&&t.fiveCount%6===0;target.hp-=dmg;shot('spider',target,.34,{special});if(special){battle.spiderWebs=battle.spiderWebs||[];battle.spiderWebs.push({x:target.x,y:target.y,r:72,life:4,tick:0,slowTick:0,dmg:dmg*.35});if(battle.spiderWebs.length>5)battle.spiderWebs.splice(0,battle.spiderWebs.length-5)}if(target.hp<=0)killEnemy(target)}
   t.cd=cardRate(t.key);
 };
 // PERFORMANCE_V3: no full enemy HP scans for damage-summary bookkeeping in the hot tower loop.
 // The battle mechanics stay at full update speed; only visual rendering is adaptively capped below.
 towerTick=function(t,dt){towerTickCore(t,dt)};
 const _fiveOldUpdate=update;update=function(dt){
   _fiveOldUpdate(dt);battle.spiderWebs=battle.spiderWebs||[];
   for(const z of battle.spiderWebs){z.life-=dt;z.slowTick-=dt;z.tick-=dt;const r2=z.r*z.r;
     if(z.slowTick<=0){z.slowTick=.20;for(const e of battle.enemies){if(!e.dead){const dx=e.x-z.x,dy=e.y-z.y;if(dx*dx+dy*dy<=r2)e.slowTimer=Math.max(e.slowTimer||0,.30)}}}
     if(z.tick<=0){z.tick+=1;for(const e of battle.enemies){if(!e.dead){const dx=e.x-z.x,dy=e.y-z.y;if(dx*dx+dy*dy<=r2){e.hp-=z.dmg;if(e.hp<=0)killEnemy(e)}}}}
   }
   battle.spiderWebs=battle.spiderWebs.filter(z=>z.life>0);
   if((battle.shots||[]).length>140)battle.shots.splice(0,battle.shots.length-140);
 };
 const _fiveOldDraw=draw;let _fiveLastPaint=0;
 draw=function(){
   // On busy late waves render at ~30fps. Updates/damage still run normally, cutting canvas work roughly in half.
   const now=performance.now(),busy=((battle.enemies||[]).length>35||(battle.shots||[]).length>75);if(busy&&now-_fiveLastPaint<32)return;_fiveLastPaint=now;
   const allShots=battle.shots||[],custom=[],normal=[];for(const s of allShots)(s.customAttack?custom:normal).push(s);battle.shots=normal;_fiveOldDraw();battle.shots=allShots;
   for(const z of (battle.spiderWebs||[])){ctx.save();ctx.globalAlpha=Math.min(.65,z.life/4);ctx.strokeStyle='#e7eef2';ctx.lineWidth=2;for(let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.moveTo(z.x,z.y);ctx.lineTo(z.x+Math.cos(a)*z.r,z.y+Math.sin(a)*z.r);ctx.stroke();}for(let r=24;r<=z.r;r+=24){ctx.beginPath();ctx.arc(z.x,z.y,r,0,Math.PI*2);ctx.stroke();}ctx.restore();}
   for(const s of custom){const q=1-Math.max(0,s.life)/(s.maxLife||.4),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.textAlign='center';ctx.textBaseline='middle';
     if(s.customAttack==='ram'){ctx.font=s.special?'38px serif':'30px serif';ctx.fillText('🐏',0,0);if(s.special){ctx.strokeStyle='#f5df9a';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-30,-12);ctx.lineTo(-48,-12);ctx.moveTo(-30,12);ctx.lineTo(-48,12);ctx.stroke();}}
     if(s.customAttack==='turkey'){ctx.rotate(q*8);ctx.strokeStyle=s.special?'#ffd45b':'#8d5a35';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-14,0);ctx.quadraticCurveTo(0,-8,15,0);ctx.quadraticCurveTo(0,8,-14,0);ctx.stroke();}
     if(s.customAttack==='flamingo'){ctx.rotate(-ang);ctx.shadowColor='#ff2f92';ctx.shadowBlur=s.special?24:18;ctx.fillStyle='rgba(255,70,155,.30)';ctx.beginPath();ctx.arc(0,0,s.special?28:23,0,Math.PI*2);ctx.fill();ctx.font=s.special?'46px serif':'38px serif';ctx.fillText('🦩',0,0);ctx.strokeStyle='#fff0fa';ctx.lineWidth=2.5;ctx.beginPath();ctx.moveTo(-24,18);ctx.lineTo(24,18);ctx.stroke();}
     if(s.customAttack==='swan'){ctx.strokeStyle=s.special?'#dff8ff':'#ffffff';ctx.shadowColor='#bcecff';ctx.shadowBlur=10;ctx.lineWidth=s.special?8:5;for(let i=-1;i<=1;i++){ctx.beginPath();ctx.arc(0,i*7,15+q*18,-.7,.7);ctx.stroke();}}
     if(s.customAttack==='spider'){ctx.strokeStyle='#e8eef2';ctx.lineWidth=s.special?4:2.5;ctx.beginPath();ctx.moveTo(-20,0);ctx.lineTo(20,0);ctx.stroke();for(let i=-12;i<=12;i+=8){ctx.beginPath();ctx.moveTo(i,-5);ctx.lineTo(i+5,5);ctx.stroke();}}
     ctx.restore();
   }
 };
 if(typeof renderCollection==='function')renderCollection();
})();