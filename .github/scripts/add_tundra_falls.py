from pathlib import Path
p=Path('index.html')
s=p.read_text()

def rep(old,new,label):
    global s
    if old not in s: raise SystemExit(f'{label} anchor not found')
    s=s.replace(old,new,1)

# Save fields
rep('''  hauntedWoodsUnlocked:0,\n  hauntedWoodsSelected:1,\n  selectedSeries:1,''','''  hauntedWoodsUnlocked:0,\n  hauntedWoodsSelected:1,\n  tundraFallsUnlocked:0,\n  tundraFallsSelected:1,\n  selectedSeries:1,''','save defaults')

# Sanctuary metadata + fourth tab styling
rep("""  3:{name:'Haunted Woods',icon:'👻',desc:'A dark and mysterious woodland filled with twisted trees, forgotten graves, drifting fog and restless spirits.',className:'haunted',stages:['Shadow Path','Cursed Glade','Gravestone Grove','The Hollow','Whispering Brook','Ruined Chapel','Spectral Crossing',\"Witch's Circle\",'Fallen Giant','The Final Stand']}\n};""","""  3:{name:'Haunted Woods',icon:'👻',desc:'A dark and mysterious woodland filled with twisted trees, forgotten graves, drifting fog and restless spirits.',className:'haunted',stages:['Shadow Path','Cursed Glade','Gravestone Grove','The Hollow','Whispering Brook','Ruined Chapel','Spectral Crossing',\"Witch's Circle\",'Fallen Giant','The Final Stand']},\n  4:{name:'Tundra Falls',icon:'❄️',desc:'A frozen wilderness of snowdrifts, ice caverns, frozen rivers and towering glacial falls. Enemies here have 1.60x HP.',className:'tundra',stages:['Frostbite Trail','Snowdrift Pass','Frozen River','Icefang Ridge','Glacier Hollow','Whiteout Crossing','Crystal Cavern','Avalanche Run','Frozen Falls','Heart of Winter']}\n};""",'sanctuary meta')
rep('grid-template-columns:repeat(3,1fr)','grid-template-columns:repeat(4,1fr)','region tabs css')
rep('.region-hero.haunted{background:radial-gradient(circle at 79% 16%,#9c84ff55,transparent 26%),radial-gradient(circle at 75% 14%,#d8d0ff40 0 8%,transparent 9%),linear-gradient(145deg,#251d39,#0d1715 70%)}','.region-hero.haunted{background:radial-gradient(circle at 79% 16%,#9c84ff55,transparent 26%),radial-gradient(circle at 75% 14%,#d8d0ff40 0 8%,transparent 9%),linear-gradient(145deg,#251d39,#0d1715 70%)}\n.region-hero.tundra{background:radial-gradient(circle at 80% 12%,#ffffffaa,transparent 18%),radial-gradient(circle at 72% 20%,#a9e8ff88,transparent 34%),linear-gradient(145deg,#2b6f8d,#102f46 72%)}','tundra hero css')
rep('.stage-thumb.haunted{background:radial-gradient(circle at 58% 22%,#a78cff66,transparent 30%),linear-gradient(#241d3b,#0a1512)}','.stage-thumb.haunted{background:radial-gradient(circle at 58% 22%,#a78cff66,transparent 30%),linear-gradient(#241d3b,#0a1512)}.stage-thumb.tundra{background:radial-gradient(circle at 50% 20%,#ffffffaa,transparent 28%),linear-gradient(#75cbe8,#173d56)}','tundra thumb css')
rep('tabs.innerHTML=[1,2,3].map','tabs.innerHTML=[1,2,3,4].map','region tab list')
rep("const sets={1:['🌿','🌲','🌉','🏡','💧','🗼','🌳','🌸','🪵','🏰'],2:['☀️','🏜️','🌴','🦂','🪨','🌫️','🐪','🏛️','🦅','👑'],3:['🌙','🕯️','🪦','🕳️','🌫️','⛪','🌉','🔮','💀','🏰']};","const sets={1:['🌿','🌲','🌉','🏡','💧','🗼','🌳','🌸','🪵','🏰'],2:['☀️','🏜️','🌴','🦂','🪨','🌫️','🐪','🏛️','🦅','👑'],3:['🌙','🕯️','🪦','🕳️','🌫️','⛪','🌉','🔮','💀','🏰'],4:['❄️','🌨️','🧊','🏔️','🌬️','🐺','💎','☃️','🌊','👑']};",'stage icons')
rep("return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):(save.hauntedWoodsUnlocked||0);","return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):series===3?(save.hauntedWoodsUnlocked||0):(save.tundraFallsUnlocked||0);",'sanctuary unlock')

# Create ten tundra layouts by mirroring Haunted Woods maps, keeping gameplay geometry valid.
anchor=']\nfunction seriesMaps(series){'
pos=s.find(anchor, s.find('const hauntedWoodsMaps=['))
if pos<0: raise SystemExit('haunted maps end not found')
insert='''\n\n// TUNDRA_FALLS_V1: 10 icy maps derived as mirrored layouts for a distinct fourth region.\nconst tundraFallsMaps=hauntedWoodsMaps.map((m,i)=>({\n  path:m.path.map(([x,y])=>i%2?[860-x,y]:[x,y]),\n  pads:m.pads.map(([x,y])=>i%2?[860-x,y]:[x,y])\n}));\n'''
s=s[:pos+2]+insert+s[pos+2:]

rep("function seriesMaps(series){return series===1?forestPinesMaps:series===2?desertDunesMaps:hauntedWoodsMaps}","function seriesMaps(series){return series===1?forestPinesMaps:series===2?desertDunesMaps:series===3?hauntedWoodsMaps:tundraFallsMaps}",'series maps')
rep("function seriesUnlockedCount(series){return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):(save.hauntedWoodsUnlocked||0)}","function seriesUnlockedCount(series){return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):series===3?(save.hauntedWoodsUnlocked||0):(save.tundraFallsUnlocked||0)}",'series unlock count')
rep("function seriesDisplayName(series){return series===1?'Forest Pines':series===2?'Desert Dunes':'Haunted Woods'}","function seriesDisplayName(series){return series===1?'Forest Pines':series===2?'Desert Dunes':series===3?'Haunted Woods':'Tundra Falls'}",'series name')
rep("function seriesDisplayIcon(series){return series===1?'🌲':series===2?'🏜️':'👻'}","function seriesDisplayIcon(series){return series===1?'🌲':series===2?'🏜️':series===3?'👻':'❄️'}",'series icon')
rep('Math.min(3,save.selectedSeries||1)','Math.min(4,save.selectedSeries||1)','current series max')
rep("currentSeries===1?(save.forestPinesSelected||1):currentSeries===2?(save.selectedSeriesMap||1):(save.hauntedWoodsSelected||1)","currentSeries===1?(save.forestPinesSelected||1):currentSeries===2?(save.selectedSeriesMap||1):currentSeries===3?(save.hauntedWoodsSelected||1):(save.tundraFallsSelected||1)",'selected map')
rep('Math.min(3,series)','Math.min(4,series)','apply map max')
rep('if(currentSeries===3)save.hauntedWoodsSelected=currentMap;','if(currentSeries===3)save.hauntedWoodsSelected=currentMap;\n  if(currentSeries===4)save.tundraFallsSelected=currentMap;','tundra selected save')
rep('currentSeries<3&&seriesUnlockedCount(currentSeries+1)>0','currentSeries<4&&seriesUnlockedCount(currentSeries+1)>0','next series nav')

# Tundra enemy roster
rep('''  // HAUNTED_ENEMIES_V1: Haunted Woods uses its own spooky enemy roster.\n  if(currentSeries===3){''','''  // TUNDRA_ENEMIES_V1: frozen wildlife and ice spirits.\n  if(currentSeries===4){\n    if(w>=7 && r<.12)return {type:"frostMammoth",emoji:"🦣",hp:(205+w*22)*.8,speed:38,reward:20,size:30,boss:true};\n    if(w>=6 && r<.26)return {type:"polarBear",emoji:"🐻‍❄️",hp:(125+w*15)*.8,speed:52,reward:12,size:22};\n    if(w>=4 && r<.42)return {type:"arcticWolf",emoji:"🐺",hp:(92+w*12)*.8,speed:70,reward:10,size:20};\n    if(r<.38)return {type:"snowyOwl",emoji:"🦉",hp:(44+w*8)*.8,speed:86,reward:7,size:16};\n    return {type:"iceSeal",emoji:"🦭",hp:(66+w*10)*.8,speed:60,reward:9,size:18};\n  }\n  // HAUNTED_ENEMIES_V1: Haunted Woods uses its own spooky enemy roster.\n  if(currentSeries===3){''','tundra enemies')

# 1.60x HP
rep('''  // Forest Pines = 1.00x, Desert Dunes = 1.20x, Haunted Woods = 1.45x.\n  const seriesDifficulty=currentSeries===1?1:currentSeries===2?1.20:1.45;''','''  // Forest Pines = 1.00x, Desert Dunes = 1.20x, Haunted Woods = 1.45x, Tundra Falls = 1.60x.\n  const seriesDifficulty=currentSeries===1?1:currentSeries===2?1.20:currentSeries===3?1.45:1.60;''','difficulty multiplier')

# Boss on 4-10 wave 15
rep('''    3:{type:"hauntedReaperBoss",emoji:"💀",name:"Haunted Reaper",hp:5200,speed:27,reward:200,size:45,boss:true,bossAbility:"terror"}\n  };''','''    3:{type:"hauntedReaperBoss",emoji:"💀",name:"Haunted Reaper",hp:5200,speed:27,reward:200,size:45,boss:true,bossAbility:"terror"},\n    4:{type:"frostMammothBoss",emoji:"🦣",name:"Frost Mammoth",hp:5800,speed:25,reward:225,size:47,boss:true,bossAbility:"blizzard"}\n  };''','boss data')
rep('const bossNames={1:"ALPHA BEAR",2:"GIANT SCORPION",3:"HAUNTED REAPER"};','const bossNames={1:"ALPHA BEAR",2:"GIANT SCORPION",3:"HAUNTED REAPER",4:"FROST MAMMOTH"};','boss names')

# Unlock Tundra after 3-10, advance inside region 4.
rep('''    }else if(currentSeries===3&&currentMap<10){\n      save.hauntedWoodsUnlocked=Math.max(save.hauntedWoodsUnlocked||1,currentMap+1);\n    }''','''    }else if(currentSeries===3){\n      if(currentMap<10)save.hauntedWoodsUnlocked=Math.max(save.hauntedWoodsUnlocked||1,currentMap+1);\n      else save.tundraFallsUnlocked=Math.max(save.tundraFallsUnlocked||0,1);\n    }else if(currentSeries===4&&currentMap<10){\n      save.tundraFallsUnlocked=Math.max(save.tundraFallsUnlocked||1,currentMap+1);\n    }''','unlock progression')
rep('currentSeries===2?"Haunted Woods 3-1 unlocked!":"Haunted Woods series complete!"','currentSeries===2?"Haunted Woods 3-1 unlocked!":currentSeries===3?"Tundra Falls 4-1 unlocked!":"Tundra Falls series complete!"','completion text')

# Icy battlefield visuals
rep('''  const hauntedPurples=["#24152f","#291735","#21132c","#30183b","#261431","#2d1738","#22142e","#321a3d","#281533","#25122f"];\n  ctx.fillStyle=currentSeries===1?forestGreens[currentMap-1]:currentSeries===2?desertSands[currentMap-1]:hauntedPurples[currentMap-1];ctx.fillRect(0,0,W,H);''','''  const hauntedPurples=["#24152f","#291735","#21132c","#30183b","#261431","#2d1738","#22142e","#321a3d","#281533","#25122f"];\n  const tundraIce=["#bfe8f4","#abdbe9","#cbeef6","#9fd2e5","#d6f3f8","#a7d9ea","#c5edf5","#95cde1","#d9f6fb","#b2e2ef"];\n  ctx.fillStyle=currentSeries===1?forestGreens[currentMap-1]:currentSeries===2?desertSands[currentMap-1]:currentSeries===3?hauntedPurples[currentMap-1]:tundraIce[currentMap-1];ctx.fillRect(0,0,W,H);''','ground colors')
rep('ctx.fillStyle=currentSeries===1?"#24552b":currentSeries===2?"#a77c36":"#140b1d";','ctx.fillStyle=currentSeries===1?"#24552b":currentSeries===2?"#a77c36":currentSeries===3?"#140b1d":"#e7fbff";','edge color')
# Insert snow/ice decorations before haunted-specific decoration block.
rep('''  if(currentSeries===3){\n    // Moonlit haunted-wood atmosphere''','''  if(currentSeries===4){\n    ctx.save();\n    ctx.globalAlpha=.75;ctx.fillStyle="#ffffff";\n    for(let i=0;i<46;i++){const x=(i*97+currentMap*31)%W,y=(i*149+currentMap*47)%H,r=2+(i%3);ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();}\n    ctx.globalAlpha=.45;ctx.fillStyle="#7ed6f2";\n    for(let i=0;i<8;i++){const x=(i*121+currentMap*53)%W,y=120+((i*173+currentMap*61)%(H-220));ctx.beginPath();ctx.moveTo(x,y-28);ctx.lineTo(x+22,y+24);ctx.lineTo(x-24,y+20);ctx.closePath();ctx.fill();}\n    ctx.restore();\n  }\n  if(currentSeries===3){\n    // Moonlit haunted-wood atmosphere''','tundra decorations')

# Region summary slot location
rep('''const sv=rec.save||{};const forest=sv.forestPinesUnlocked||1;const desert=sv.desertDunesUnlocked||0;const haunted=sv.hauntedWoodsUnlocked||0;const where=haunted>0?`Haunted ${haunted}`:desert>0?`Desert ${desert}`:`Forest ${forest}`;''','''const sv=rec.save||{};const forest=sv.forestPinesUnlocked||1;const desert=sv.desertDunesUnlocked||0;const haunted=sv.hauntedWoodsUnlocked||0;const tundra=sv.tundraFallsUnlocked||0;const where=tundra>0?`Tundra ${tundra}`:haunted>0?`Haunted ${haunted}`:desert>0?`Desert ${desert}`:`Forest ${forest}`;''','slot summary')

p.write_text(s)
print('Added Tundra Falls region 4 with icy theme and 1.60x enemy HP')
