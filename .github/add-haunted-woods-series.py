from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1,required=True):
    global s
    if old not in s:
        if required: raise SystemExit('marker not found: '+old[:120])
        return
    s=s.replace(old,new,count)

# Save data for third series.
if 'hauntedWoodsUnlocked' not in s:
    rep('  desertDunesUnlocked:0,\n  selectedSeries:1,','  desertDunesUnlocked:0,\n  hauntedWoodsUnlocked:0,\n  hauntedWoodsSelected:1,\n  selectedSeries:1,')

# Add 10 Haunted Woods maps before current map state.
if 'const hauntedWoodsMaps=' not in s:
    marker='let currentSeries=Math.max(1,Math.min(2,save.selectedSeries||1));'
    maps=r'''// Haunted Woods series: 10 spooky woodland maps. All maps use the standard 15-wave battle length.
const hauntedWoodsMaps=[
 {path:[[-45,125],[155,125],[155,305],[410,305],[410,160],[690,160],[690,420],[290,420],[290,650],[610,650],[610,875],[860,875]],pads:[[75,235],[260,210],[520,250],[760,285],[105,455],[430,530],[720,560],[150,730],[430,770],[730,760],[250,930],[540,950]]},
 {path:[[-45,210],[230,210],[230,95],[520,95],[520,330],[745,330],[745,565],[415,565],[415,790],[125,790],[125,1025]],pads:[[105,105],[350,190],[635,205],[120,360],[350,430],[630,455],[780,690],[555,700],[280,680],[250,900],[520,910],[750,920]]},
 {path:[[90,-40],[90,185],[345,185],[345,405],[690,405],[690,610],[475,610],[475,825],[205,825],[205,1060]],pads:[[210,80],[480,100],[700,150],[165,315],[500,300],[775,320],[245,535],[565,720],[760,735],[85,700],[335,930],[650,930]]},
 {path:[[-45,105],[330,105],[330,285],[130,285],[130,500],[560,500],[560,295],[790,295],[790,720],[375,720],[375,935],[860,935]],pads:[[145,195],[470,190],[665,120],[35,390],[280,410],[680,410],[455,600],[720,600],[120,650],[225,835],[520,840],[700,980]]},
 {path:[[185,-45],[185,175],[620,175],[620,380],[310,380],[310,580],[720,580],[720,800],[465,800],[465,1060]],pads:[[70,120],[350,85],[740,100],[80,305],[460,285],[755,330],[160,480],[500,490],[820,685],[580,690],[260,720],[300,930],[650,930]]},
 {path:[[-45,300],[175,300],[175,120],[455,120],[455,330],[730,330],[730,550],[495,550],[495,760],[190,760],[190,940],[860,940]],pads:[[70,185],[315,225],[590,215],[95,430],[330,450],[610,445],[800,430],[365,650],[650,680],[80,850],[330,870],[605,860]]},
 {path:[[810,-45],[810,150],[555,150],[555,350],[255,350],[255,555],[610,555],[610,760],[335,760],[335,1025]],pads:[[680,80],[390,105],[120,180],[715,285],[400,260],[100,455],[420,455],[760,470],[160,650],[475,665],[740,875],[180,880],[520,920]]},
 {path:[[-45,145],[260,145],[260,345],[670,345],[670,125],[815,125],[815,560],[525,560],[525,805],[105,805],[105,1025]],pads:[[95,250],[405,245],[560,160],[740,250],[115,460],[345,470],[700,680],[350,675],[180,900],[480,920],[750,920],[40,650]]},
 {path:[[60,-45],[60,250],[315,250],[315,100],[590,100],[590,420],[775,420],[775,665],[430,665],[430,480],[160,480],[160,865],[650,865],[650,1040]],pads:[[175,120],[430,185],[720,180],[120,365],[455,350],[650,540],[270,600],[590,750],[780,790],[300,950],[520,970],[90,720]]},
 {path:[[-45,110],[220,110],[220,300],[500,300],[500,120],[760,120],[760,470],[360,470],[360,690],[690,690],[690,900],[410,900],[410,1045]],pads:[[95,215],[350,205],[620,215],[95,400],[470,390],[790,300],[190,585],[540,585],[800,610],[235,810],[540,800],[780,840],[250,970]]}
];
function seriesMaps(series){return series===1?forestPinesMaps:series===2?desertDunesMaps:hauntedWoodsMaps}
function seriesUnlockedCount(series){return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):(save.hauntedWoodsUnlocked||0)}
function seriesDisplayName(series){return series===1?'Forest Pines':series===2?'Desert Dunes':'Haunted Woods'}
function seriesDisplayIcon(series){return series===1?'🌲':series===2?'🏜️':'👻'}

'''
    rep(marker,maps+marker)

# Current map boot state.
rep('let currentSeries=Math.max(1,Math.min(2,save.selectedSeries||1));','let currentSeries=Math.max(1,Math.min(3,save.selectedSeries||1));')
rep('let currentMap=Math.max(1,Math.min(10,currentSeries===1?(save.forestPinesSelected||1):(save.selectedSeriesMap||1)));','let currentMap=Math.max(1,Math.min(10,currentSeries===1?(save.forestPinesSelected||1):currentSeries===2?(save.selectedSeriesMap||1):(save.hauntedWoodsSelected||1)));')
rep('let path=(currentSeries===1?forestPinesMaps:desertDunesMaps)[currentMap-1].path;\nlet pads=(currentSeries===1?forestPinesMaps:desertDunesMaps)[currentMap-1].pads;','let path=seriesMaps(currentSeries)[currentMap-1].path;\nlet pads=seriesMaps(currentSeries)[currentMap-1].pads;')

# Three-series map helper + applyMap internals.
rep('function currentSeriesUnlocked(){\n  return currentSeries===1?(save.forestPinesUnlocked||1):(save.desertDunesUnlocked||0);\n}','function currentSeriesUnlocked(){return seriesUnlockedCount(currentSeries)}')
rep('const targetSeries=Math.max(1,Math.min(2,series));','const targetSeries=Math.max(1,Math.min(3,series));')
rep('const unlocked=targetSeries===1?(save.forestPinesUnlocked||1):(save.desertDunesUnlocked||0);','const unlocked=seriesUnlockedCount(targetSeries);')
rep('if(targetSeries===2 && unlocked<1)return false;','if(targetSeries>1 && unlocked<1)return false;')
rep('const maps=currentSeries===1?forestPinesMaps:desertDunesMaps;','const maps=seriesMaps(currentSeries);')
rep('save.selectedSeriesMap=currentMap;\n  if(currentSeries===1)save.forestPinesSelected=currentMap;','save.selectedSeriesMap=currentMap;\n  if(currentSeries===1)save.forestPinesSelected=currentMap;\n  if(currentSeries===3)save.hauntedWoodsSelected=currentMap;')
rep('seriesTitle.textContent=currentSeries===1?"🌲 Forest Pines":"🏜️ Desert Dunes";','seriesTitle.textContent=`${seriesDisplayIcon(currentSeries)} ${seriesDisplayName(currentSeries)}`;')
rep('prevMap.disabled=currentSeries===1&&currentMap===1;','prevMap.disabled=currentSeries===1&&currentMap===1;')
rep('nextMap.disabled=(currentSeries===1&&currentMap===10&&!(save.desertDunesUnlocked||0)) || (currentMap>=seriesUnlocked && !(currentSeries===1&&currentMap===10&&(save.desertDunesUnlocked||0)>0));','nextMap.disabled=(currentMap>=seriesUnlocked && !(currentMap===10&&currentSeries<3&&seriesUnlockedCount(currentSeries+1)>0));')

# Navigation across 1 -> 2 -> 3 and back.
nav_start=s.find('prevMap.onclick=()=>{')
nav_end=s.find('startWave.onclick=()=>{',nav_start)
if nav_start<0 or nav_end<0: raise SystemExit('navigation markers missing')
nav=r'''prevMap.onclick=()=>{
  if(currentMap>1){clearBattleState();applyMap(currentSeries,currentMap-1);resetBattle();return;}
  if(currentSeries>1){clearBattleState();applyMap(currentSeries-1,10);resetBattle();}
};
nextMap.onclick=()=>{
  if(currentMap<10){
    if(currentMap<currentSeriesUnlocked()){clearBattleState();applyMap(currentSeries,currentMap+1);resetBattle();}
    return;
  }
  if(currentSeries<3&&seriesUnlockedCount(currentSeries+1)>0){clearBattleState();applyMap(currentSeries+1,1);resetBattle();}
};
'''
s=s[:nav_start]+nav+s[nav_end:]

# Unlock series 3 after Desert Dunes 2-10, then advance through Haunted Woods.
rep('''    }else if(currentMap<10){
      save.desertDunesUnlocked=Math.max(save.desertDunesUnlocked||1,currentMap+1);
    }''','''    }else if(currentSeries===2){
      if(currentMap<10)save.desertDunesUnlocked=Math.max(save.desertDunesUnlocked||1,currentMap+1);
      else save.hauntedWoodsUnlocked=Math.max(save.hauntedWoodsUnlocked||0,1);
    }else if(currentSeries===3&&currentMap<10){
      save.hauntedWoodsUnlocked=Math.max(save.hauntedWoodsUnlocked||1,currentMap+1);
    }''')

rep('const seriesName=currentSeries===1?"Forest Pines":"Desert Dunes";','const seriesName=seriesDisplayName(currentSeries);',1,False)
rep('const nextText=currentMap<10?`${currentSeries}-${currentMap+1} unlocked!`:currentSeries===1?"Desert Dunes 2-1 unlocked!":"Desert Dunes series complete!";','const nextText=currentMap<10?`${currentSeries}-${currentMap+1} unlocked!`:currentSeries===1?"Desert Dunes 2-1 unlocked!":currentSeries===2?"Haunted Woods 3-1 unlocked!":"Haunted Woods series complete!";')
rep("const seriesName=currentSeries===1?'Forest Pines':'Desert Dunes';","const seriesName=seriesDisplayName(currentSeries);",1,False)

# Save-slot summary supports third series.
rep('const sv=rec.save||{};const forest=sv.forestPinesUnlocked||1;const desert=sv.desertDunesUnlocked||0;const where=desert>0?`Desert ${desert}`:`Forest ${forest}`;','const sv=rec.save||{};const forest=sv.forestPinesUnlocked||1;const desert=sv.desertDunesUnlocked||0;const haunted=sv.hauntedWoodsUnlocked||0;const where=haunted>0?`Haunted ${haunted}`:desert>0?`Desert ${desert}`:`Forest ${forest}`;',1,False)

# Give Haunted Woods its own dark palette and creepy scenery.
rep('ctx.fillStyle=currentSeries===1?"#24552b":"#a77c36";','ctx.fillStyle=currentSeries===1?"#24552b":currentSeries===2?"#a77c36":"#16241d";')
needle='for(let x=0;x<W;x+=70){ctx.beginPath();ctx.arc(x,22,48,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(x,H-12,52,0,Math.PI*2);ctx.fill();}'
if 'Moonlit haunted-wood atmosphere' not in s:
    spooky=needle+r'''
  if(currentSeries===3){
    // Moonlit haunted-wood atmosphere: twisted trunks, fog, gravestones and glowing eyes.
    ctx.save();ctx.fillStyle="#0b1512";
    for(let i=0;i<13;i++){const x=(i*73+currentMap*19)%W,y=(i%2?72:H-88);ctx.fillRect(x-7,y-45,14,65);ctx.strokeStyle="#263a30";ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(x,y-20);ctx.lineTo(x-25,y-50);ctx.moveTo(x,y-8);ctx.lineTo(x+28,y-38);ctx.stroke();}
    ctx.globalAlpha=.18;ctx.fillStyle="#c7d8d1";for(let i=0;i<7;i++){const x=(i*137+currentMap*43)%W,y=170+((i*149+currentMap*31)%(H-300));ctx.beginPath();ctx.ellipse(x,y,110,28,0,0,Math.PI*2);ctx.fill();}
    ctx.globalAlpha=.7;ctx.fillStyle="#66766e";for(let i=0;i<6;i++){const x=75+((i*151+currentMap*47)%690),y=105+((i*173+currentMap*59)%780);ctx.fillRect(x-12,y,24,28);ctx.beginPath();ctx.arc(x,y,12,Math.PI,0);ctx.fill();}
    ctx.globalAlpha=.9;ctx.fillStyle="#b7ff78";for(let i=0;i<8;i++){const x=35+((i*97+currentMap*61)%760),y=80+((i*121+currentMap*29)%850);ctx.beginPath();ctx.arc(x-4,y,2.5,0,Math.PI*2);ctx.arc(x+4,y,2.5,0,Math.PI*2);ctx.fill();}
    ctx.restore();
  }'''
    rep(needle,spooky)

# Validation.
for marker in ['const hauntedWoodsMaps=[','hauntedWoodsUnlocked','Math.min(3,save.selectedSeries','Haunted Woods 3-1 unlocked','seriesMaps(currentSeries)','currentSeries===3&&currentMap<10']:
    if marker not in s: raise SystemExit('final validation missing '+marker)

p.write_text(s,encoding='utf-8')
print('Haunted Woods series 3 added: 10 maps, standard 15 waves each')
