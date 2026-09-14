// CORAL_COAST_PLAYABLE_V2
// Region 7 gameplay integration. Loaded after index.html's main game script.
const coralCoastPlayableMaps=[
 {path:[[-45,160],[210,160],[210,355],[610,355],[610,155],[790,155],[790,585],[430,585],[430,835],[120,835],[-45,965]],pads:[[95,270],[340,255],[510,245],[705,275],[115,480],[335,475],[705,470],[570,710],[260,710],[250,930],[555,930],[760,860]]},
 {path:[[885,170],[650,170],[650,390],[260,390],[260,180],[85,180],[85,620],[500,620],[500,840],[790,840],[885,980]],pads:[[760,290],[520,285],[380,275],[155,300],[110,505],[360,510],[690,520],[350,735],[640,735],[170,820],[420,950],[720,960]]},
 {path:[[90,-45],[90,250],[390,250],[390,110],[720,110],[720,470],[520,470],[520,700],[180,700],[180,930],[720,930],[885,930]],pads:[[220,120],[510,205],[805,245],[260,370],[600,350],[815,590],[380,575],[80,820],[330,820],[610,805],[350,990],[760,770]]},
 {path:[[-45,300],[190,300],[190,105],[520,105],[520,310],[760,310],[760,570],[390,570],[390,780],[690,780],[690,1025]],pads:[[75,180],[340,205],[655,195],[90,430],[300,430],[640,430],[815,450],[250,675],[525,675],[805,690],[500,900],[200,900]]},
 {path:[[885,115],[560,115],[560,300],[160,300],[160,540],[670,540],[670,745],[360,745],[360,1025]],pads:[[720,225],[420,210],[270,175],[70,420],[300,420],[520,425],[790,630],[510,650],[210,650],[190,870],[560,885],[800,880]]},
 {path:[[210,-45],[210,175],[700,175],[700,420],[340,420],[340,620],[760,620],[760,860],[470,860],[470,1045]],pads:[[85,110],[390,85],[580,290],[805,300],[500,310],[190,530],[525,525],[815,740],[610,750],[300,750],[260,950],[650,965]]},
 {path:[[-45,125],[300,125],[300,340],[690,340],[690,120],[825,120],[825,560],[520,560],[520,805],[150,805],[150,1025]],pads:[[110,235],[445,230],[580,145],[760,245],[105,455],[365,460],[710,690],[355,680],[260,920],[560,925],[780,900],[65,670]]},
 {path:[[60,-45],[60,240],[300,240],[300,95],[590,95],[590,385],[790,385],[790,640],[445,640],[445,470],[160,470],[160,860],[650,860],[650,1045]],pads:[[175,115],[420,180],[720,175],[120,355],[450,330],[670,510],[275,590],[600,750],[790,785],[300,955],[520,975],[85,720]]},
 {path:[[885,215],[625,215],[625,85],[335,85],[335,330],[105,330],[105,605],[560,605],[560,790],[260,790],[260,1025]],pads:[[760,100],[500,190],[205,190],[80,470],[250,465],[445,470],[710,500],[700,705],[420,700],[130,900],[430,910],[760,900]]},
 {path:[[-45,120],[250,120],[250,300],[600,300],[600,115],[800,115],[800,470],[420,470],[420,665],[720,665],[720,875],[390,875],[390,1045]],pads:[[100,215],[390,205],[700,225],[115,405],[500,395],[820,300],[245,565],[565,565],[820,585],[265,780],[550,780],[790,820],[220,965]]}
];

save.coralCoastUnlocked=Math.max(0,Number(save.coralCoastUnlocked||0));
SANCTUARY_META[7]={name:'Coral Coast',icon:'🌊',desc:'Tropical islands, sandy shores, turquoise channels, reefs and wooden piers. New coastal enemies are introduced as you progress.',className:'coral',stages:['Sandy Shores','Turtle Bay','Seagull Point','Reef Run','Stingray Sands','Shark Waters','Octopus Cove','Barracuda Bay','Deepwater Crossing',"Kraken's Reach"]};

const _seriesMapsBase=seriesMaps;
seriesMaps=function(series){return series===7?coralCoastPlayableMaps:_seriesMapsBase(series)};
const _seriesUnlockedBase=seriesUnlockedCount;
seriesUnlockedCount=function(series){return series===7?(save.coralCoastUnlocked||0):_seriesUnlockedBase(series)};
const _seriesNameBase=seriesDisplayName;
seriesDisplayName=function(series){return series===7?'Coral Coast':_seriesNameBase(series)};
const _seriesIconBase=seriesDisplayIcon;
seriesDisplayIcon=function(series){return series===7?'🌊':_seriesIconBase(series)};
sanctuaryUnlocked=function(series){return series===7?(save.coralCoastUnlocked||0):seriesUnlockedCount(series)};

sanctuaryStageIcon=function(series,n){
  if(series===7)return ['🏖️','🐢','🐦','🪸','🌊','🦈','🐙','🐟','🦞','🦑'][n-1]||'🌊';
  const sets={1:['🌿','🌲','🌉','🏡','💧','🗼','🌳','🌸','🪵','🏰'],2:['☀️','🏜️','🌴','🦂','🪨','🌫️','🐪','🏛️','🦅','👑'],3:['🌙','🕯️','🪦','🕳️','🌫️','⛪','🌉','🔮','💀','🏰'],4:['❄️','🌨️','🧊','🏔️','🌬️','🐺','💎','☃️','🌊','👑'],5:['🌋','🔥','🪨','🕳️','🌉','💎','🌪️','⚒️','🔥','🌋'],6:['💎','🔷','🍄','🔮','💧','🪨','🔊','✨','💥','💠']};
  return sets[series]?.[n-1]||'🗺️';
};

renderMapSanctuary=function(){
  const wrap=document.getElementById('mapSanctuary');if(!wrap)return;
  if(!sanctuaryUnlocked(mapMenuSeries))mapMenuSeries=1;
  const meta=SANCTUARY_META[mapMenuSeries],unlocked=Math.max(mapMenuSeries===1?1:0,sanctuaryUnlocked(mapMenuSeries));
  const tabs=document.getElementById('regionTabs');
  tabs.innerHTML=[1,2,3,4,5,6,7].map(series=>{const m=SANCTUARY_META[series],locked=series>1&&sanctuaryUnlocked(series)<1;return `<button class="region-tab ${series===mapMenuSeries?'active':''} ${locked?'locked':''}" data-region="${series}" ${locked?'disabled':''}>REGION ${series}<b>${locked?'🔒 LOCKED':m.icon+' '+m.name.toUpperCase()}</b></button>`}).join('');
  tabs.querySelectorAll('.region-tab:not(.locked)').forEach(btn=>btn.onclick=()=>{mapMenuSeries=+btn.dataset.region;renderMapSanctuary()});
  const hero=document.getElementById('regionHero');hero.className=`region-hero ${meta.className}`;
  document.getElementById('sanctuaryRegionName').textContent=meta.name;
  document.getElementById('sanctuaryRegionDesc').textContent=meta.desc;
  document.getElementById('sanctuaryRegionNumber').textContent=`REGION ${mapMenuSeries}`;
  document.getElementById('sanctuaryStageTitle').textContent=meta.name.toUpperCase();
  const normalBtn=document.getElementById('sanctuaryNormal'),hardBtn=document.getElementById('sanctuaryHard');
  normalBtn.classList.toggle('active',mapMenuDifficulty==='normal');hardBtn.classList.toggle('active',mapMenuDifficulty==='hard');
  normalBtn.onclick=()=>{mapMenuDifficulty='normal';renderMapSanctuary()};hardBtn.onclick=()=>{mapMenuDifficulty='hard';renderMapSanctuary()};
  document.getElementById('sanctuaryModeHint').textContent=mapMenuDifficulty==='hard'?'Hard stages require that same stage to be cleared on Normal first.':'Complete each Normal stage to unlock the next stage and its Hard mode.';
  const grid=document.getElementById('sanctuaryStageGrid');
  grid.innerHTML=meta.stages.map((name,i)=>{const n=i+1,key=`${mapMenuSeries}-${n}`,locked=n>unlocked,normalDone=!!save.normalCompleted?.[key],hardDone=!!save.hardCompleted?.[key],modeLocked=mapMenuDifficulty==='hard'&&!normalDone,inaccessible=locked||modeLocked,cleared=mapMenuDifficulty==='hard'?hardDone:normalDone,stars=hardDone?3:normalDone?2:0,starText=[0,1,2].map(x=>x<stars?'★':'☆').join('<br>'),status=locked?'Locked':modeLocked?'Clear Normal first':cleared?'Cleared • 15/15 waves':'Unlocked • 15 waves';return `<button class="stage-card ${cleared?'cleared':''} ${inaccessible?'locked':''}" data-stage="${n}" ${inaccessible?'disabled':''}><div class="stage-thumb ${meta.className}">${sanctuaryStageIcon(mapMenuSeries,n)}</div><div class="stage-copy"><div class="stage-num">${mapMenuSeries}-${n}</div><div class="stage-name">${name}</div><div class="stage-status">${status}</div></div><div>${inaccessible?'<div class="stage-lock">🔒</div>':`<div class="stage-stars">${starText}</div>`}</div></button>`}).join('');
  grid.querySelectorAll('.stage-card:not(.locked)').forEach(btn=>btn.onclick=()=>startSanctuaryStage(+btn.dataset.stage));
};

applyMap=function(series,n){
  const targetSeries=Math.max(1,Math.min(7,Number(series)||1)),unlocked=seriesUnlockedCount(targetSeries);if(targetSeries>1&&unlocked<1)return false;
  currentSeries=targetSeries;currentMap=Math.max(1,Math.min(10,Number(n)||1));
  if(hardMode&&!save.normalCompleted?.[`${currentSeries}-${currentMap}`]){hardMode=false;save.battleDifficulty='normal';}
  const maps=seriesMaps(currentSeries);path=maps[currentMap-1].path;pads=maps[currentMap-1].pads;
  save.selectedSeries=currentSeries;save.selectedSeriesMap=currentMap;if(currentSeries===1)save.forestPinesSelected=currentMap;if(currentSeries===3)save.hauntedWoodsSelected=currentMap;if(currentSeries===4)save.tundraFallsSelected=currentMap;if(currentSeries===5)save.volcanicWastelandSelected=currentMap;if(currentSeries===6)save.crystalCavernsSelected=currentMap;if(currentSeries===7)save.coralCoastSelected=currentMap;
  seriesTitle.textContent=`${seriesDisplayIcon(currentSeries)} ${seriesDisplayName(currentSeries)}`;mapLabel.textContent=`${currentSeries}-${currentMap}${hardMode?' • 🔥 HARD':''}`;prevMap.disabled=currentSeries===1&&currentMap===1;
  const unlockedHere=currentSeriesUnlocked();nextMap.disabled=(currentMap>=unlockedHere&&!(currentMap===10&&currentSeries<7&&seriesUnlockedCount(currentSeries+1)>0));return true;
};
nextMap.onclick=()=>{if(currentMap<10){if(currentMap<currentSeriesUnlocked()){clearBattleState();applyMap(currentSeries,currentMap+1);resetBattle();draw();}return;}if(currentSeries<7&&seriesUnlockedCount(currentSeries+1)>0){clearBattleState();applyMap(currentSeries+1,1);resetBattle();draw();}};

const _enemyForWaveBase=enemyForWave;
enemyForWave=function(){
  if(currentSeries!==7)return _enemyForWaveBase();
  const w=battle.wave,defs=[
    {type:'crab',emoji:'🦀',hp:118+w*14,speed:60,reward:12,size:20},
    {type:'seaTurtle',emoji:'🐢',hp:215+w*22,speed:38,reward:17,size:25},
    {type:'seagull',emoji:'🐦',hp:78+w*10,speed:104,reward:10,size:18},
    {type:'pufferfish',emoji:'🐡',hp:160+w*18,speed:56,reward:15,size:22},
    {type:'stingray',emoji:'🌊',hp:180+w*19,speed:82,reward:16,size:23},
    {type:'shark',emoji:'🦈',hp:255+w*25,speed:76,reward:20,size:28},
    {type:'octopus',emoji:'🐙',hp:285+w*28,speed:52,reward:22,size:29},
    {type:'barracuda',emoji:'🐟',hp:190+w*20,speed:112,reward:18,size:23},
    {type:'giantLobster',emoji:'🦞',hp:390+w*36,speed:31,reward:27,size:33}
  ];const available=Math.max(1,Math.min(9,currentMap));return {...defs[Math.floor(Math.random()*available)]};
};

const _bossBase=bossForSeriesMap;
bossForSeriesMap=function(){
  if(currentSeries!==7)return _bossBase();
  const r=[
    {type:'kingCrabBoss',emoji:'🦀',name:'King Crab',hp:4700,speed:34,reward:170,size:40,boss:true},
    {type:'ancientTurtleBoss',emoji:'🐢',name:'Ancient Sea Turtle',hp:5200,speed:27,reward:185,size:44,boss:true},
    {type:'stormGullBoss',emoji:'🐦',name:'Storm Gull',hp:5550,speed:56,reward:195,size:39,boss:true},
    {type:'spikedPufferBoss',emoji:'🐡',name:'Spiked Puffer',hp:6100,speed:36,reward:210,size:43,boss:true},
    {type:'mantaQueenBoss',emoji:'🌊',name:'Manta Queen',hp:6650,speed:45,reward:225,size:46,boss:true},
    {type:'greatWhiteBoss',emoji:'🦈',name:'Great White',hp:7300,speed:48,reward:245,size:49,boss:true},
    {type:'abyssOctopusBoss',emoji:'🐙',name:'Abyss Octopus',hp:7900,speed:33,reward:260,size:50,boss:true},
    {type:'razorBarracudaBoss',emoji:'🐟',name:'Razor Barracuda',hp:8450,speed:61,reward:275,size:46,boss:true},
    {type:'titanLobsterBoss',emoji:'🦞',name:'Titan Lobster',hp:9300,speed:25,reward:295,size:54,boss:true},
    {type:'krakenBoss',emoji:'🦑',name:'The Kraken',hp:10500,speed:22,reward:330,size:60,boss:true}
  ];return {...r[currentMap-1]};
};

const _coinMultBase=regionCoinMultiplier;regionCoinMultiplier=function(){return currentSeries===7?1.85:_coinMultBase()};
const _finishWaveBase=finishWave;
finishWave=function(){const wasSeries=currentSeries,wasMap=currentMap,wasWave=battle.wave,wasHard=hardMode;_finishWaveBase();if(wasWave>=15&&!wasHard){if(wasSeries===6&&wasMap===10){save.coralCoastUnlocked=Math.max(save.coralCoastUnlocked||0,1);message.textContent=message.textContent.replace('Crystal Caverns series complete!','Coral Coast 7-1 unlocked!');persist();}else if(wasSeries===7){if(wasMap<10)save.coralCoastUnlocked=Math.max(save.coralCoastUnlocked||1,wasMap+1);persist();}}};

if(save.selectedSeries===7&&save.coralCoastUnlocked>0){currentSeries=7;currentMap=Math.max(1,Math.min(10,save.coralCoastSelected||1));path=coralCoastPlayableMaps[currentMap-1].path;pads=coralCoastPlayableMaps[currentMap-1].pads;}
