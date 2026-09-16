// REGIONS_8_10_V1 — 30 new maps, progressive enemies, unique bases
(()=>{
const defs={
8:{name:'Lost Jungle',icon:'🌿',className:'jungle',desc:'Dense rainforest, ancient ruins, waterfalls and overgrown temples.',stages:['Vine Trail','Caiman Creek','Parrot Pass','Temple Steps','Cobra Crossing','Jaguar Run','Gorilla Grove','Ruined Causeway','Emerald Temple','Silverback Throne'],enemies:[['cobra','🐍',145,68,13,20],['iguana','🦎',185,58,15,22],['macaw','🦜',120,105,12,19],['caiman','🐊',280,48,20,27],['baboon','🐒',240,78,19,25],['jaguar','🐆',260,110,22,25],['gorilla','🦍',430,42,29,32],['anaconda','🐍',510,38,32,34],['tapir','🐗',600,35,35,35]],boss:['silverbackKing','🦍','Silverback King',12800,25,390,62]},
9:{name:'Enchanted Wilds',icon:'🍄',className:'enchanted',desc:'Giant mushrooms, glowing plants, magical ponds and strange enchanted wildlife.',stages:['Spore Meadow','Snail Hollow','Mooncap Marsh','Spider Glade','Mothlight Path','Poison Garden','Beetle Grove','Owlwood','Spirit Crossing','Antler Sanctum'],enemies:[['giantSnail','🐌',210,34,17,23],['poisonFrog','🐸',170,72,16,21],['mysticMoth','🦋',145,108,15,20],['giantSpider','🕷️',285,76,22,25],['caterpillar','🐛',330,48,23,27],['stagBeetle','🪲',440,45,29,31],['enchantedOwl','🦉',310,100,25,26],['spiritFox','🦊',390,92,29,28],['moonBear','🐻',690,34,39,37]],boss:['spiritStag','🦌','Spirit Stag',15400,30,440,65]},
10:{name:'Sky Highlands',icon:'🌩️',className:'sky',desc:'Floating mountain islands, cloud bridges, waterfalls and violent high-altitude storms.',stages:['Cloud Gate','Goat Ridge','Ram Run','Condor Crossing','Yak Heights','Leopard Peak','Thunder Bridge','Storm Islands','Roc Ascent','Citadel Above'],enemies:[['mountainGoat','🐐',260,65,20,23],['ram','🐏',340,62,23,26],['condor','🦅',230,112,20,23],['llama','🦙',380,70,26,28],['yak','🐂',600,40,35,34],['snowLeopard','🐆',430,108,31,28],['goldenEagle','🦅',390,120,30,27],['stormRam','🐏',700,58,39,36],['thunderYak','🐂',900,38,46,40]],boss:['thunderRoc','🦅','Thunder Roc',18500,34,520,70]}
};
const templates=[
[[-45,145],[205,145],[205,350],[650,350],[650,150],[885,150]],
[[885,160],[620,160],[620,390],[235,390],[235,650],[720,650],[720,1045]],
[[100,-45],[100,245],[410,245],[410,115],[740,115],[740,500],[470,500],[470,790],[170,790],[170,1045]],
[[-45,290],[210,290],[210,100],[540,100],[540,330],[790,330],[790,590],[390,590],[390,820],[690,820],[690,1045]],
[[885,115],[570,115],[570,300],[155,300],[155,545],[675,545],[675,760],[355,760],[355,1045]],
[[215,-45],[215,180],[705,180],[705,425],[335,425],[335,625],[770,625],[770,865],[470,865],[470,1045]],
[[-45,125],[305,125],[305,345],[700,345],[700,125],[825,125],[825,570],[515,570],[515,815],[145,815],[145,1045]],
[[60,-45],[60,245],[305,245],[305,95],[595,95],[595,390],[795,390],[795,645],[445,645],[445,475],[155,475],[155,865],[650,865],[650,1045]],
[[885,215],[625,215],[625,85],[335,85],[335,330],[105,330],[105,605],[560,605],[560,790],[260,790],[260,1045]],
[[-45,120],[250,120],[250,300],[600,300],[600,115],[800,115],[800,470],[420,470],[420,665],[720,665],[720,875],[390,875],[390,1045]]];
function padsFor(path){const out=[];for(let i=1;i<path.length-1&&out.length<12;i++){const a=path[i],b=path[i+1],mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;out.push([Math.max(65,Math.min(820,mx+95)),Math.max(70,Math.min(980,my+85))]);}while(out.length<12)out.push([80+(out.length%4)*220,210+Math.floor(out.length/4)*300]);return out;}
const maps={};[8,9,10].forEach(r=>maps[r]=templates.map((p,i)=>({path:p.map(([x,y])=>[x+(r-8)*((i%2)?8:-8),y]),pads:padsFor(p)})));
Object.entries(defs).forEach(([r,d])=>{r=+r;SANCTUARY_META[r]={name:d.name,icon:d.icon,desc:d.desc,className:d.className,stages:d.stages};save['region'+r+'Unlocked']=Math.max(0,Number(save['region'+r+'Unlocked']||0));});
const sm=seriesMaps;seriesMaps=s=>maps[s]||sm(s);const su=seriesUnlockedCount;seriesUnlockedCount=s=>s>=8&&s<=10?(save['region'+s+'Unlocked']||0):su(s);const sn=seriesDisplayName;seriesDisplayName=s=>defs[s]?.name||sn(s);const si=seriesDisplayIcon;seriesDisplayIcon=s=>defs[s]?.icon||si(s);
const oldIcon=sanctuaryStageIcon;sanctuaryStageIcon=(s,n)=>s>=8&&s<=10?defs[s].icon:oldIcon(s,n);
const oldEnemy=enemyForWave;enemyForWave=function(){if(!defs[currentSeries])return oldEnemy();const d=defs[currentSeries],w=battle.wave,available=Math.max(1,Math.min(9,currentMap)),e=d.enemies[Math.floor(Math.random()*available)];return {type:e[0],emoji:e[1],hp:e[2]+w*(16+(currentSeries-8)*4),speed:e[3],reward:e[4],size:e[5]};};
const oldBoss=bossForSeriesMap;bossForSeriesMap=function(){if(!defs[currentSeries])return oldBoss();const d=defs[currentSeries],b=d.boss,scale=1+(currentMap-1)*.075;return {type:b[0],emoji:b[1],name:currentMap===10?b[2]:d.stages[currentMap-1]+' Guardian',hp:Math.round(b[3]*scale),speed:b[4],reward:Math.round(b[5]*scale),size:b[6],boss:true};};
const oldMult=regionCoinMultiplier;regionCoinMultiplier=()=>defs[currentSeries]?(currentSeries===8?2.05:currentSeries===9?2.25:2.5):oldMult();
const oldFinish=finishWave;finishWave=function(){const s=currentSeries,m=currentMap,w=battle.wave,h=hardMode;oldFinish();if(w>=15&&!h&&s>=7&&s<10&&m===10){save['region'+(s+1)+'Unlocked']=Math.max(save['region'+(s+1)+'Unlocked']||0,1);persist();}};
// Extend navigation and sanctuary UI without replacing core progression.
const oldApply=applyMap;applyMap=function(series,n){if(series<=7)return oldApply(series,n);const s=Math.max(8,Math.min(10,+series||8));if(seriesUnlockedCount(s)<1)return false;currentSeries=s;currentMap=Math.max(1,Math.min(10,+n||1));const mm=seriesMaps(s);path=mm[currentMap-1].path;pads=mm[currentMap-1].pads;save.selectedSeries=s;save.selectedSeriesMap=currentMap;seriesTitle.textContent=`${seriesDisplayIcon(s)} ${seriesDisplayName(s)}`;mapLabel.textContent=`${s}-${currentMap}${hardMode?' • 🔥 HARD':''}`;prevMap.disabled=false;nextMap.disabled=currentMap>=seriesUnlockedCount(s)&&!(currentMap===10&&s<10&&seriesUnlockedCount(s+1)>0);return true;};
// All region scenery and endpoint bases are rendered beneath combat by CritterAtlas.
})();
