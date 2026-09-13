from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='CRYSTAL_CAVERNS_REGION_V2'
if MARK in s:
    print('Already applied')
    raise SystemExit(0)

def rep(old,new,count=1,label='anchor'):
    global s
    if old not in s:
        raise RuntimeError(f'{label} not found')
    s=s.replace(old,new,count)

# Sanctuary UI
rep('.region-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;', '.region-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;', label='region tabs css')
rep('.region-hero.tundra{background:radial-gradient(circle at 80% 12%,#ffffffaa,transparent 18%),radial-gradient(circle at 72% 20%,#a9e8ff88,transparent 34%),linear-gradient(145deg,#2b6f8d,#102f46 72%)}', '.region-hero.tundra{background:radial-gradient(circle at 80% 12%,#ffffffaa,transparent 18%),radial-gradient(circle at 72% 20%,#a9e8ff88,transparent 34%),linear-gradient(145deg,#2b6f8d,#102f46 72%)}\n.region-hero.crystal{background:radial-gradient(circle at 80% 14%,#e5c8ffcc,transparent 19%),radial-gradient(circle at 68% 26%,#69f1ff88,transparent 35%),linear-gradient(145deg,#33205f,#102d46 72%)}\n.region-hero.crystal h1{color:#dffcff;text-shadow:0 0 16px #6fefff99}\n.stage-thumb.crystal{background:radial-gradient(circle at 52% 18%,#e9d4ffcc,transparent 24%),linear-gradient(#34698b,#221640)}', label='crystal css')
rep('🗺️ 30 Stages','🗺️ 60 Stages',label='stage count')

# Save state
rep('  volcanicWastelandUnlocked:0,\n  volcanicWastelandSelected:1,','  volcanicWastelandUnlocked:0,\n  volcanicWastelandSelected:1,\n  crystalCavernsUnlocked:0,\n  crystalCavernsSelected:1,',label='defaults')
mig='if(save.normalCompleted["4-10"]||save.hardCompleted["4-10"])save.volcanicWastelandUnlocked=Math.max(save.volcanicWastelandUnlocked||0,1);'
rep(mig,mig+'\n// '+MARK+': preserve progression for players who already cleared Volcanic 5-10.\nif(save.normalCompleted["5-10"]||save.hardCompleted["5-10"])save.crystalCavernsUnlocked=Math.max(save.crystalCavernsUnlocked||0,1);',label='migration')

# Sanctuary metadata
old_meta='''  5:{name:'Volcanic Wasteland',icon:'🌋',desc:'A scorched wasteland of molten rivers, black basalt, burning vents and erupting volcanoes. The toughest region yet.',className:'volcanic',stages:['Ashen Pass','Lava Crossing','Ember Ridge','The Crater','Magma Bridges','Obsidian Run','Firestorm Basin','The Forge','Inferno Trail',"Volcano's Edge"]}\n};'''
new_meta='''  5:{name:'Volcanic Wasteland',icon:'🌋',desc:'A scorched wasteland of molten rivers, black basalt, burning vents and erupting volcanoes.',className:'volcanic',stages:['Ashen Pass','Lava Crossing','Ember Ridge','The Crater','Magma Bridges','Obsidian Run','Firestorm Basin','The Forge','Inferno Trail',"Volcano's Edge"]},\n  6:{name:'Crystal Caverns',icon:'💎',desc:'A deep subterranean crystal biome of glowing geodes, prism-lit caves, underground lakes and dangerous crystalline creatures. Harder than Volcanic Wasteland.',className:'crystal',stages:['Cavern Entrance','Shimmering Chasm','Glowshroom Grotto','Prismatic Passage','Underground Lake','Geode Gallery','Echoing Depths','Crystal Forest','The Shattered Core','Heart of the Caverns']}\n};'''
rep(old_meta,new_meta,label='sanctuary meta')
rep('return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):series===3?(save.hauntedWoodsUnlocked||0):series===4?(save.tundraFallsUnlocked||0):(save.volcanicWastelandUnlocked||0);','return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):series===3?(save.hauntedWoodsUnlocked||0):series===4?(save.tundraFallsUnlocked||0):series===5?(save.volcanicWastelandUnlocked||0):(save.crystalCavernsUnlocked||0);',label='sanctuary unlock')
rep("5:['🌋','🔥','🪨','🕳️','🌉','💎','🌪️','⚒️','🔥','🌋']};","5:['🌋','🔥','🪨','🕳️','🌉','💎','🌪️','⚒️','🔥','🌋'],6:['💎','🔷','🍄','🔮','💧','🪨','🔊','✨','💥','💠']};",label='stage icons')
rep('tabs.innerHTML=[1,2,3,4,5].map(series=>','tabs.innerHTML=[1,2,3,4,5,6].map(series=>',label='region tabs')

# Maps and series helpers
series_line='function seriesMaps(series){return series===1?forestPinesMaps:series===2?desertDunesMaps:series===3?hauntedWoodsMaps:series===4?tundraFallsMaps:volcanicWastelandMaps}'
crystal_maps='''// CRYSTAL_CAVERNS_MAPS_V1: ten late-game cave routes, alternating orientation for visual variety.\nconst crystalCavernsMaps=volcanicWastelandMaps.map((m,i)=>({\n  path:m.path.map(([x,y])=>[i%2?860-x:x,y]),\n  pads:m.pads.map(([x,y])=>[i%2?860-x:x,y])\n}));\nfunction seriesMaps(series){return series===1?forestPinesMaps:series===2?desertDunesMaps:series===3?hauntedWoodsMaps:series===4?tundraFallsMaps:series===5?volcanicWastelandMaps:crystalCavernsMaps}'''
rep(series_line,crystal_maps,label='series maps')
rep('function seriesUnlockedCount(series){return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):series===3?(save.hauntedWoodsUnlocked||0):series===4?(save.tundraFallsUnlocked||0):(save.volcanicWastelandUnlocked||0)}','function seriesUnlockedCount(series){return series===1?(save.forestPinesUnlocked||1):series===2?(save.desertDunesUnlocked||0):series===3?(save.hauntedWoodsUnlocked||0):series===4?(save.tundraFallsUnlocked||0):series===5?(save.volcanicWastelandUnlocked||0):(save.crystalCavernsUnlocked||0)}',label='series unlock helper')
rep("function seriesDisplayName(series){return series===1?'Forest Pines':series===2?'Desert Dunes':series===3?'Haunted Woods':series===4?'Tundra Falls':'Volcanic Wasteland'}","function seriesDisplayName(series){return series===1?'Forest Pines':series===2?'Desert Dunes':series===3?'Haunted Woods':series===4?'Tundra Falls':series===5?'Volcanic Wasteland':'Crystal Caverns'}",label='series name')
rep("function seriesDisplayIcon(series){return series===1?'🌲':series===2?'🏜️':series===3?'👻':series===4?'❄️':'🌋'}","function seriesDisplayIcon(series){return series===1?'🌲':series===2?'🏜️':series===3?'👻':series===4?'❄️':series===5?'🌋':'💎'}",label='series icon')
rep('Math.min(5,save.selectedSeries||1)','Math.min(6,save.selectedSeries||1)',label='selected series max')
rep('currentSeries===4?(save.tundraFallsSelected||1):(save.volcanicWastelandSelected||1)','currentSeries===4?(save.tundraFallsSelected||1):currentSeries===5?(save.volcanicWastelandSelected||1):(save.crystalCavernsSelected||1)',label='selected map')
rep('Math.min(5,series)','Math.min(6,series)',label='apply max')
rep('  if(currentSeries===5)save.volcanicWastelandSelected=currentMap;','  if(currentSeries===5)save.volcanicWastelandSelected=currentMap;\n  if(currentSeries===6)save.crystalCavernsSelected=currentMap;',label='save selected crystal')
rep('currentSeries<5&&seriesUnlockedCount(currentSeries+1)>0','currentSeries<6&&seriesUnlockedCount(currentSeries+1)>0',label='next region button')

# Map-complete continue logic
rep('    else if(currentSeries===1 && (save.desertDunesUnlocked||0)>=1){applyMap(2,1);resetBattle();}\n    else{message.textContent="🏆 All available levels complete!";startWave.textContent="Completed";}','    else if(currentSeries<6 && seriesUnlockedCount(currentSeries+1)>0){applyMap(currentSeries+1,1);resetBattle();draw();}\n    else{message.textContent="🏆 All available levels complete!";startWave.textContent="Completed";}',label='next level continue')

# Crystal enemies
enemy_anchor='  // TUNDRA_ENEMIES_V1: frozen wildlife and ice spirits.'
crystal_enemy='''  // CRYSTAL_CAVERNS_ENEMIES_V1\n  if(currentSeries===6){\n    if(w>=7 && r<.12)return {type:"crystalElemental",emoji:"💠",hp:(285+w*29)*.8,speed:34,reward:26,size:32,boss:true};\n    if(w>=6 && r<.28)return {type:"gemGolem",emoji:"🗿",hp:(178+w*20)*.8,speed:42,reward:17,size:25};\n    if(w>=4 && r<.44)return {type:"crystalSpider",emoji:"🕷️",hp:(122+w*15)*.8,speed:76,reward:13,size:20};\n    if(r<.40)return {type:"crystalBat",emoji:"🦇",hp:(62+w*10)*.8,speed:98,reward:9,size:17};\n    return {type:"crystalSlime",emoji:"🫧",hp:(88+w*13)*.8,speed:60,reward:11,size:20};\n  }\n'''
rep(enemy_anchor,crystal_enemy+enemy_anchor,label='crystal enemies')

# Crystal bosses
close5='''      {type:"volcanoTitanBoss",emoji:"🌋",name:"Volcano Titan",hp:7200,speed:24,reward:260,size:52,boss:true,bossAbility:"eruption"}\n    ]\n  };'''
roster6='''      {type:"volcanoTitanBoss",emoji:"🌋",name:"Volcano Titan",hp:7200,speed:24,reward:260,size:52,boss:true,bossAbility:"eruption"}\n    ],\n    6:[\n      {type:"crystalBatBoss",emoji:"🦇",name:"Prismwing",hp:3900,speed:54,reward:150,size:37,boss:true,bossAbility:"prismDive"},\n      {type:"crystalSpiderBoss",emoji:"🕷️",name:"Gem Widow",hp:4300,speed:45,reward:165,size:39,boss:true,bossAbility:"crystalWeb"},\n      {type:"crystalSlimeBoss",emoji:"🫧",name:"Living Geode",hp:4700,speed:37,reward:180,size:42,boss:true,bossAbility:"split"},\n      {type:"caveTrollBoss",emoji:"👹",name:"Cavern Troll",hp:5200,speed:34,reward:195,size:45,boss:true,bossAbility:"slam"},\n      {type:"gemGolemBoss",emoji:"🗿",name:"Gemstone Golem",hp:5700,speed:28,reward:210,size:47,boss:true,bossAbility:"crystalArmor"},\n      {type:"burrowWormBoss",emoji:"🪱",name:"Crystal Burrower",hp:6150,speed:40,reward:225,size:45,boss:true,bossAbility:"burrow"},\n      {type:"prismElementalBoss",emoji:"💠",name:"Prism Elemental",hp:6650,speed:36,reward:240,size:48,boss:true,bossAbility:"refraction"},\n      {type:"crystalGuardianBoss",emoji:"💎",name:"Crystal Guardian",hp:7200,speed:29,reward:255,size:50,boss:true,bossAbility:"shardStorm"},\n      {type:"shatteredCoreBoss",emoji:"💥",name:"The Shattered Core",hp:7900,speed:26,reward:275,size:53,boss:true,bossAbility:"fracture"},\n      {type:"cavernHeartBoss",emoji:"💠",name:"Heart of the Caverns",hp:8800,speed:23,reward:300,size:56,boss:true,bossAbility:"crystalEruption"}\n    ]\n  };'''
rep(close5,roster6,label='crystal bosses')

# Difficulty and rewards: Crystal sits above Volcanic.
rep('return currentSeries===1?1:currentSeries===2?1.10:currentSeries===3?1.25:currentSeries===4?1.40:1.55;','return currentSeries===1?1:currentSeries===2?1.10:currentSeries===3?1.25:currentSeries===4?1.40:currentSeries===5?1.55:1.70;',label='coin multiplier')
rep('const seriesDifficulty=currentSeries===1?1:currentSeries===2?1.20:currentSeries===3?1.45:1.60;','const seriesDifficulty=currentSeries===1?1:currentSeries===2?1.20:currentSeries===3?1.45:currentSeries===4?1.60:currentSeries===5?1.75:1.90;',label='hp scaling')

# Unlock progression
oldprog='''    }else if(currentSeries===4){\n      if(currentMap<10)save.tundraFallsUnlocked=Math.max(save.tundraFallsUnlocked||1,currentMap+1);\n      else save.volcanicWastelandUnlocked=Math.max(save.volcanicWastelandUnlocked||0,1);\n    }else if(currentSeries===5&&currentMap<10){\n      save.volcanicWastelandUnlocked=Math.max(save.volcanicWastelandUnlocked||1,currentMap+1);\n    }'''
newprog='''    }else if(currentSeries===4){\n      if(currentMap<10)save.tundraFallsUnlocked=Math.max(save.tundraFallsUnlocked||1,currentMap+1);\n      else save.volcanicWastelandUnlocked=Math.max(save.volcanicWastelandUnlocked||0,1);\n    }else if(currentSeries===5){\n      if(currentMap<10)save.volcanicWastelandUnlocked=Math.max(save.volcanicWastelandUnlocked||1,currentMap+1);\n      else save.crystalCavernsUnlocked=Math.max(save.crystalCavernsUnlocked||0,1);\n    }else if(currentSeries===6&&currentMap<10){\n      save.crystalCavernsUnlocked=Math.max(save.crystalCavernsUnlocked||1,currentMap+1);\n    }'''
rep(oldprog,newprog,label='completion progression')
rep('currentSeries===4?"Volcanic Wasteland 5-1 unlocked!":"Volcanic Wasteland series complete!"','currentSeries===4?"Volcanic Wasteland 5-1 unlocked!":currentSeries===5?"Crystal Caverns 6-1 unlocked!":"Crystal Caverns series complete!"',label='completion message')

# Crystal battlefield ground and decor
rep('  const volcanicRock=["#2a211f","#30231f","#251d1c","#35251f","#291e1b","#33221c","#241b1a","#38251e","#2d201c","#211817"];','  const volcanicRock=["#2a211f","#30231f","#251d1c","#35251f","#291e1b","#33221c","#241b1a","#38251e","#2d201c","#211817"];\n  const crystalStone=["#172238","#192740","#20234b","#152d45","#251d50","#18354a","#212b55","#172c42","#2a2058","#193149"];',label='crystal palette')
rep('currentSeries===4?tundraIce[currentMap-1]:volcanicRock[currentMap-1]','currentSeries===4?tundraIce[currentMap-1]:currentSeries===5?volcanicRock[currentMap-1]:crystalStone[currentMap-1]',label='ground select')
rep('currentSeries===4?"#e7fbff":"#120e0d";','currentSeries===4?"#e7fbff":currentSeries===5?"#120e0d":"#101a35";',label='edge select')
rep('const decorCount=currentSeries===5?0:(currentSeries===1?78:42);','const decorCount=currentSeries>=5?0:(currentSeries===1?78:42);',label='decor count')
road_anchor='  // Road outline and road surface use the exact enemy path.'
crystal_visual='''  if(currentSeries===6){\n    // CRYSTAL_CAVERNS_VISUALS_V1: animated in-game crystal formations and floating cave sparkles.\n    ctx.save();const ct=performance.now()/1000;\n    for(let i=0;i<22;i++){const x=35+decorRand(2200+i*4)*790,y=50+decorRand(2201+i*4)*910;if(!decorSafe(x,y))continue;const h=24+decorRand(2202+i)*42,w=8+decorRand(2203+i)*9;ctx.save();ctx.translate(x,y);ctx.fillStyle=i%3===0?"#b67cff":i%3===1?"#63e6ff":"#83ffcf";ctx.strokeStyle="#e9fbff";ctx.lineWidth=1.5;ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=12;ctx.beginPath();ctx.moveTo(0,-h);ctx.lineTo(w,-h*.35);ctx.lineTo(w*.6,h*.28);ctx.lineTo(0,h*.5);ctx.lineTo(-w*.6,h*.28);ctx.lineTo(-w,-h*.35);ctx.closePath();ctx.fill();ctx.stroke();ctx.restore();}\n    ctx.globalAlpha=.7;for(let i=0;i<38;i++){const x=(i*113+currentMap*47)%W,y=(i*157+currentMap*39-(ct*8*(1+i%2)))%H,yy=y<0?y+H:y;if(!decorSafe(x,yy))continue;ctx.fillStyle=i%2?"#d8b8ff":"#9cf7ff";ctx.beginPath();ctx.arc(x,yy,1.5+(i%3)*.5,0,Math.PI*2);ctx.fill();}\n    ctx.restore();\n  }\n\n'''
rep(road_anchor,crystal_visual+road_anchor,label='crystal visuals')

# Road base colors and crystal fissures
rep('currentSeries===4?"#4b9fc6":"#4a2118"','currentSeries===4?"#4b9fc6":currentSeries===5?"#4a2118":"#3b3670"',label='road outline color')
rep('currentSeries===4?"#bdefff":"#3b2521"','currentSeries===4?"#bdefff":currentSeries===5?"#3b2521":"#5969a8"',label='road surface color')
volc_end='''    ctx.globalAlpha=.55;ctx.strokeStyle="#ffb13b";ctx.lineWidth=3;ctx.setLineDash([4,29,2,19]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;\n  }\n  ctx.restore();'''
crys_end='''    ctx.globalAlpha=.55;ctx.strokeStyle="#ffb13b";ctx.lineWidth=3;ctx.setLineDash([4,29,2,19]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;\n  }else if(currentSeries===6){\n    ctx.globalAlpha=.96;ctx.strokeStyle="#34436f";ctx.lineWidth=58;ctx.stroke();\n    ctx.globalAlpha=.9;ctx.strokeStyle="#202b52";ctx.lineWidth=42;ctx.stroke();\n    ctx.globalAlpha=.75;ctx.strokeStyle="#78e9ff";ctx.lineWidth=6;ctx.setLineDash([10,22,4,28]);ctx.stroke();ctx.setLineDash([]);\n    ctx.globalAlpha=.5;ctx.strokeStyle="#c18cff";ctx.lineWidth=3;ctx.setLineDash([5,25,2,20]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;\n  }\n  ctx.restore();'''
rep(volc_end,crys_end,label='crystal road')

# Finish-route color uses Crystal palette too.
rep('currentSeries===4?"#bdefff":"#3b2521";','currentSeries===4?"#bdefff":currentSeries===5?"#3b2521":"#5969a8";',label='finish route color')

# Themed exit base: make Volcanic explicit and add Crystal base.
rep('    }else{\n      // Volcanic Wasteland: obsidian fortress over a molten magma gate.','    }else if(currentSeries===5){\n      // Volcanic Wasteland: obsidian fortress over a molten magma gate.',label='volcanic base condition')
shared='''    }\n\n    // Shared sign plate, kept compact so the structure remains the focus.'''
crystal_base='''    }else{\n      // Crystal Caverns: glowing geode gate.\n      ctx.fillStyle="#1d2546";ctx.strokeStyle="#7cecff";ctx.lineWidth=5;ctx.beginPath();ctx.roundRect(-50,-30,100,64,8);ctx.fill();ctx.stroke();\n      ctx.fillStyle="#2a2358";ctx.strokeStyle="#b68cff";ctx.lineWidth=4;ctx.fillRect(-58,-42,22,72);ctx.strokeRect(-58,-42,22,72);ctx.fillRect(36,-42,22,72);ctx.strokeRect(36,-42,22,72);\n      ctx.fillStyle="#63e8ff";ctx.shadowColor="#72f2ff";ctx.shadowBlur=16;ctx.beginPath();ctx.moveTo(-49,-42);ctx.lineTo(-47,-70);ctx.lineTo(-35,-43);ctx.closePath();ctx.fill();ctx.beginPath();ctx.moveTo(35,-43);ctx.lineTo(47,-72);ctx.lineTo(50,-42);ctx.closePath();ctx.fill();\n      ctx.fillStyle="#070b1c";ctx.shadowColor="transparent";ctx.beginPath();ctx.moveTo(-17,34);ctx.lineTo(-17,7);ctx.arc(0,7,17,Math.PI,0);ctx.lineTo(17,34);ctx.closePath();ctx.fill();\n      ctx.fillStyle="#9df7ff";ctx.shadowColor="#8ff4ff";ctx.shadowBlur=18;ctx.beginPath();ctx.moveTo(0,-45);ctx.lineTo(12,-15);ctx.lineTo(0,2);ctx.lineTo(-12,-15);ctx.closePath();ctx.fill();\n      ctx.fillStyle="#c395ff";ctx.beginPath();ctx.moveTo(-29,-19);ctx.lineTo(-20,-3);ctx.lineTo(-31,10);ctx.lineTo(-38,-5);ctx.closePath();ctx.fill();ctx.beginPath();ctx.moveTo(29,-19);ctx.lineTo(38,-5);ctx.lineTo(31,10);ctx.lineTo(20,-3);ctx.closePath();ctx.fill();\n      ctx.shadowColor="transparent";ctx.font="18px serif";ctx.textAlign="center";ctx.fillText("💎",0,12);\n    }\n\n    // Shared sign plate, kept compact so the structure remains the focus.'''
rep(shared,crystal_base,label='crystal base')

p.write_text(s,encoding='utf-8')
print('Applied '+MARK)
