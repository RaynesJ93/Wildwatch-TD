const fs=require('fs'),vm=require('vm'),assert=require('assert');
const noop=()=>{},buttons=[];
const ctx={CHALLENGE_QUESTS:[],save:{normalCompleted:{},hardCompleted:{},epicCompleted:{},metaCoins:0},battle:{},epicMode:false,hardMode:false,animals:{a:{rarity:'Common'},b:{rarity:'Uncommon'},c:{rarity:'Legendary'}},questState:()=>({completed:false}),renderExtraQuestBoards:noop,persist:noop,renderHome:noop,renderCards:noop,addCardXp:noop,document:{querySelectorAll:s=>s==='.challengeClaimBtn'?buttons:[]}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('epic-challenges.js','utf8'),ctx);
assert.equal(ctx.CHALLENGE_QUESTS.length,20);assert.equal(new Set(ctx.CHALLENGE_QUESTS.map(q=>q.id)).size,20);
const stats=()=>ctx.save.expandedChallengeStats;
const fresh=()=>ctx.battle={wave:1,lives:15,mapStartLives:15,usedCards:['a'],totalPlaced:4,soldCount:0,upgradeCount:0};
fresh();ctx.recordExpandedChallengeKill({elite:true});ctx.recordExpandedChallengeWave(1);ctx.recordExpandedChallengeWin();assert(!stats().kills&&!stats().waves&&!stats().wins);
ctx.hardMode=true;fresh();ctx.recordExpandedChallengeWin();assert.equal(stats().hardCommonPerfect,1);assert.equal(stats().hardNoUpgrade,1);assert(!stats().wins);
fresh();ctx.battle.usedCards=['a','b'];ctx.recordExpandedChallengeWin();assert.equal(stats().hardDuo,1);
ctx.epicMode=true;fresh();ctx.recordExpandedChallengeWin();ctx.recordExpandedChallengeWin();assert.equal(stats().wins,1);for(const k of ['perfect','four','noUpgrade','budget','ultimate'])assert.equal(stats()[k],1);
fresh();ctx.battle.totalPlaced=5;ctx.battle.soldCount=1;ctx.battle.upgradeCount=1;ctx.battle.usedCards=['c'];ctx.battle.lives=1;ctx.recordExpandedChallengeWin();assert.equal(stats().oneLife,1);for(const k of ['perfect','four','noUpgrade','budget','ultimate'])assert.equal(stats()[k],1);
ctx.recordExpandedChallengeWave(3);ctx.recordExpandedChallengeWave(3);assert.equal(stats().waves,1);
ctx.recordExpandedChallengeKill({elite:true});ctx.battle.wave=10;ctx.recordExpandedChallengeKill({boss:true});assert(!stats().finalBosses);ctx.battle.wave=20;ctx.recordExpandedChallengeKill({boss:true});assert.equal(stats().kills,3);assert.equal(stats().elites,1);assert.equal(stats().finalBosses,1);
ctx.save=JSON.parse(JSON.stringify(ctx.save));assert.equal(stats().wins,2);assert.equal(ctx.battle.expansionLastWave,3);
for(let r=1;r<=10;r++){ctx.save.epicCompleted[r]=true;for(let m=1;m<=10;m++)ctx.save.hardCompleted[`${r}-${m}`]=true;}
for(const q of ctx.CHALLENGE_QUESTS){if(!['regions','hardAtlas'].includes(q.stat))stats()[q.stat]=q.goal;}
for(const q of ctx.CHALLENGE_QUESTS)assert(ctx.questState(q).completed,q.id);
// Exercise the real claim handlers, including their repeat-claim guard.
const html=fs.readFileSync('index.html','utf8');function fn(name){const start=html.indexOf('function '+name+'(');for(let end=html.indexOf('\n}',start);end>=0;end=html.indexOf('\n}',end+2)){const src=html.slice(start,end+2);try{new vm.Script(src);return src;}catch{}}throw Error(name);}
for(const n of ['ensureChallengeQuests','giveChallengeReward','bindMilestoneClaimButtons'])vm.runInContext(fn(n),ctx);
for(const q of ctx.CHALLENGE_QUESTS)buttons.push({dataset:{id:q.id}});ctx.bindMilestoneClaimButtons();
const expected=ctx.CHALLENGE_QUESTS.reduce((sum,q)=>sum+q.reward,0);for(const b of buttons){b.onclick();b.onclick();}assert.equal(ctx.save.metaCoins,expected);assert.equal(Object.keys(ctx.save.challengeQuests.claimed).length,20);
ctx.save={};assert.equal(ctx.questState(ctx.CHALLENGE_QUESTS.find(q=>q.stat==='wins')).progress,0);
console.log('PASS: 20 quests; mode isolation; win restrictions; unique regions; kill/elite/boss/wave counters; save round-trip; independent save slots; all rewards claim exactly once.');
