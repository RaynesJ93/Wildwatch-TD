const fs=require('fs'),vm=require('vm'),assert=require('assert');const html=fs.readFileSync('index.html','utf8');
function fn(name){const start=html.indexOf('function '+name+'(');for(let end=html.indexOf('\n}',start);end>=0;end=html.indexOf('\n}',end+2)){const src=html.slice(start,end+2);try{new vm.Script(src);return src;}catch{}}throw Error(name);}
const events=[];const noop=()=>{};const storage=new Map();const ctx={save:{normalCompleted:{},hardCompleted:{},bestWave:0,xp:0,metaCoins:0},epicMode:false,hardMode:false,battle:{},currentSeries:1,currentMap:10,speed:1,autoWave:false,autoWaveTimer:0,raf:0,saveSlotSwitching:false,speedBtn:{},continueBtn:{style:{}},localStorage:{setItem:(k,v)=>storage.set(k,v),getItem:k=>storage.get(k),removeItem:k=>storage.delete(k)},battleSaveKey:()=> 'battle',ACTIVE_SLOT_KEY:'slot',BATTLE_SAVE_PREFIX:'legacy',cancelAnimationFrame:noop,requestAnimationFrame:()=>1,performance:{now:()=>0},loop:noop,applyMap:()=>true,renderDecks:noop,updateDifficultyUI:noop,draw:noop,selectedCard:null,selectedTower:null,startWave:{},message:{},levelCheck:noop,persist:noop,updateHud:noop,setTimeout:noop,clearTimeout:noop,addQuestProgress:(t)=>events.push(t),addWeeklyProgress:noop,addChallengeProgress:noop,awardWaveUsedKillXp:()=>({usedCount:0}),awardMapDeckXp:()=>300,showMapSummary:noop,seriesDisplayName:()=> 'Region',battleCoinReward:()=>20,evaluateMapChallenges:noop,bossForSeriesMap:()=>({boss:true})};vm.createContext(ctx);
for(const n of ['epicProgress','battleWaveLimit','finalMapBossForWave','finishWave','saveBattleState','clearBattleState','loadBattleState'])vm.runInContext(fn(n),ctx);
for(let r=1;r<=10;r++){
 ctx.currentSeries=r;assert(!ctx.epicProgress(r).unlocked);
 for(let n=1;n<=10;n++){ctx.save.normalCompleted[`${r}-${n}`]=true;ctx.save.hardCompleted[`${r}-${n}`]=true;}
 delete ctx.save.hardCompleted[`${r}-1`];assert(!ctx.epicProgress(r).unlocked);ctx.save.hardCompleted[`${r}-1`]=true;
 delete ctx.save.normalCompleted[`${r}-2`];assert(!ctx.epicProgress(r).unlocked);ctx.save.normalCompleted[`${r}-2`]=true;assert(ctx.epicProgress(r).unlocked);
 ctx.epicMode=ctx.hardMode=true;ctx.battle={started:true,epicMode:true,hardMode:true,wave:1,lives:15,waveStartLives:15,shots:[],coins:110};
 for(let w=1;w<=20;w++){
  assert.equal(ctx.battle.wave,w);assert.equal(ctx.battleWaveLimit(),20);assert.equal(!!ctx.finalMapBossForWave(),w===10||w===20);
  ctx.finishWave();assert.equal(!!ctx.battle.ended,w===20);
  if(w===15){ctx.epicMode=false;assert(ctx.loadBattleState());assert(ctx.epicMode);assert.equal(ctx.battle.wave,16);}
 }
 assert(ctx.save.epicCompleted[r]);
}
assert(!events.includes('hardMaps'));assert(!events.includes('normalMaps'));
ctx.epicMode=ctx.hardMode=false;ctx.currentSeries=1;ctx.currentMap=1;ctx.battle={wave:15,shots:[],lives:20};ctx.finishWave();assert(ctx.battle.ended);assert(events.includes('normalMaps'));assert.equal(ctx.battleWaveLimit(),15);
console.log('PASS: all 10 regions, missing Normal/Hard gate, all 20 waves, bosses 10/20, resume at wave 16, separate Epic completion, Normal still ends at 15.');
// Epic boosts only spendable battle cash; replayed kill callbacks cannot pay twice.
for(const n of ['resetBattle','killEnemy'])vm.runInContext(fn(n),ctx);
for(const [epic,hard,start] of [[false,false,130],[false,true,110],[true,true,300]]){
 ctx.epicMode=epic;ctx.hardMode=hard;ctx.resetBattle();assert.equal(ctx.battle.coins,start);
 const permanent=ctx.save.metaCoins;
 for(const kind of ['normal','elite','boss']){
  ctx.battleCoinReward=k=>({normal:0,elite:36,boss:99})[k]||0;
  const enemy={reward:17,coinRewardKind:kind};const before=ctx.battle.coins;
  ctx.killEnemy(enemy);assert.equal(ctx.battle.coins-before,(17+ctx.battleCoinReward(kind))*(epic?2:1));
  const paid=ctx.battle.coins;ctx.killEnemy(enemy);assert.equal(ctx.battle.coins,paid);
 }
 assert.equal(ctx.save.metaCoins,permanent);
}
console.log('PASS: Normal 130 / Hard 110 / Epic 300 start, Epic-only double kill cash, no duplicate payouts or permanent coin changes.');
// Verify the actual spawned enemy counts and final boss HP, not just the schedule.
for(const n of ['waveEliteCount','spawnEnemy'])vm.runInContext(fn(n),ctx);
ctx.path=[[0,0],[100,0]];ctx.enemyForWave=()=>({hp:100,speed:10,size:20,reward:10});
ctx.bossForSeriesMap=()=>({hp:1000,speed:10,size:40,reward:100,boss:true});
for(const epic of [false,true]){
 ctx.epicMode=epic;ctx.hardMode=true;
 for(let w=1;w<=20;w++){
  ctx.battle={wave:w,enemies:[]};let expected=epic?({3:3,7:6,15:10}[w]||0):({5:2,10:6}[w]||0);
  assert.equal(ctx.waveEliteCount(),expected);
  for(let n=0;n<80;n++)ctx.spawnEnemy();
  assert.equal(ctx.battle.enemies.filter(e=>e.elite).length,expected);
  const boss=ctx.battle.enemies.find(e=>e.boss);
  if(boss){const baseline=epic?Math.round(1750*(1.25+(w-1)*.025)):1750;assert.equal(boss.hp,baseline*(epic&&w===20?2:1));assert.equal(boss.maxHp,boss.hp);}
 }
}
console.log('PASS: Epic elites 3/6/10 on waves 3/7/15 only; wave 20 boss doubles HP; wave 10 boss and other modes unchanged.');
