from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

new_boss_code=r'''function bossForSeriesMap(){
  const rosters={
    1:[
      {type:"boarBoss",emoji:"🐗",name:"Ancient Boar",hp:2200,speed:36,reward:85,size:34,boss:true,bossAbility:"charge"},
      {type:"stagBoss",emoji:"🦌",name:"Great Stag",hp:2400,speed:38,reward:90,size:35,boss:true,bossAbility:"rush"},
      {type:"wolfBoss",emoji:"🐺",name:"Alpha Wolf",hp:2650,speed:43,reward:95,size:34,boss:true,bossAbility:"howl"},
      {type:"badgerBoss",emoji:"🦡",name:"Iron Badger",hp:2850,speed:34,reward:100,size:35,boss:true,bossAbility:"burrow"},
      {type:"mooseBoss",emoji:"🫎",name:"Mighty Moose",hp:3100,speed:32,reward:110,size:38,boss:true,bossAbility:"stampede"},
      {type:"owlBoss",emoji:"🦉",name:"Elder Owl",hp:3300,speed:46,reward:115,size:34,boss:true,bossAbility:"gust"},
      {type:"lynxBoss",emoji:"🐈",name:"Shadow Lynx",hp:3500,speed:48,reward:120,size:34,boss:true,bossAbility:"pounce"},
      {type:"bisonBoss",emoji:"🦬",name:"Forest Bison",hp:3750,speed:31,reward:130,size:40,boss:true,bossAbility:"stampede"},
      {type:"grizzlyBoss",emoji:"🐻",name:"Grizzly Guardian",hp:4000,speed:32,reward:140,size:41,boss:true,bossAbility:"swipe"},
      {type:"alphaBearBoss",emoji:"🐻",name:"Alpha Bear",hp:4200,speed:31,reward:150,size:42,boss:true,bossAbility:"roar"}
    ],
    2:[
      {type:"cobraBoss",emoji:"🐍",name:"Desert Cobra",hp:2450,speed:44,reward:95,size:34,boss:true,bossAbility:"venom"},
      {type:"jackalBoss",emoji:"🐕",name:"Dune Jackal",hp:2700,speed:48,reward:100,size:34,boss:true,bossAbility:"dash"},
      {type:"vultureBoss",emoji:"🦅",name:"Giant Vulture",hp:2950,speed:46,reward:110,size:36,boss:true,bossAbility:"dive"},
      {type:"camelBoss",emoji:"🐪",name:"War Camel",hp:3200,speed:36,reward:115,size:39,boss:true,bossAbility:"charge"},
      {type:"hyenaBoss",emoji:"🐕",name:"Dune Hyena",hp:3450,speed:46,reward:125,size:35,boss:true,bossAbility:"packHowl"},
      {type:"hornedViperBoss",emoji:"🐍",name:"Horned Viper",hp:3650,speed:43,reward:130,size:35,boss:true,bossAbility:"venom"},
      {type:"ostrichBoss",emoji:"🐦",name:"Giant Ostrich",hp:3900,speed:51,reward:140,size:38,boss:true,bossAbility:"sprint"},
      {type:"scarabBoss",emoji:"🪲",name:"Titan Scarab",hp:4150,speed:33,reward:150,size:39,boss:true,bossAbility:"shell"},
      {type:"crocodileBoss",emoji:"🐊",name:"Oasis Crocodile",hp:4450,speed:32,reward:160,size:42,boss:true,bossAbility:"deathRoll"},
      {type:"giantScorpionBoss",emoji:"🦂",name:"Giant Scorpion",hp:4700,speed:29,reward:175,size:43,boss:true,bossAbility:"venom"}
    ],
    3:[
      {type:"giantBatBoss",emoji:"🦇",name:"Giant Bat",hp:2700,speed:49,reward:110,size:35,boss:true,bossAbility:"screech"},
      {type:"direCrowBoss",emoji:"🐦‍⬛",name:"Dire Crow",hp:2950,speed:47,reward:120,size:35,boss:true,bossAbility:"shadowDive"},
      {type:"widowBoss",emoji:"🕷️",name:"Grave Widow",hp:3200,speed:40,reward:130,size:37,boss:true,bossAbility:"web"},
      {type:"spectralWolfBoss",emoji:"🐺",name:"Spectral Wolf",hp:3500,speed:45,reward:140,size:37,boss:true,bossAbility:"howl"},
      {type:"ghostBoss",emoji:"👻",name:"Ancient Ghost",hp:3750,speed:40,reward:150,size:39,boss:true,bossAbility:"phase"},
      {type:"witchRavenBoss",emoji:"🐦‍⬛",name:"Witch Raven",hp:4000,speed:46,reward:160,size:38,boss:true,bossAbility:"curse"},
      {type:"graveHoundBoss",emoji:"🐕",name:"Grave Hound",hp:4250,speed:43,reward:170,size:39,boss:true,bossAbility:"terror"},
      {type:"nightmareBoss",emoji:"🐎",name:"Nightmare Steed",hp:4550,speed:42,reward:180,size:41,boss:true,bossAbility:"nightmare"},
      {type:"boneGolemBoss",emoji:"☠️",name:"Bone Golem",hp:4850,speed:28,reward:190,size:44,boss:true,bossAbility:"slam"},
      {type:"hauntedReaperBoss",emoji:"💀",name:"Haunted Reaper",hp:5200,speed:27,reward:200,size:45,boss:true,bossAbility:"terror"}
    ],
    4:[
      {type:"snowyOwlBoss",emoji:"🦉",name:"Frostwing Owl",hp:2950,speed:47,reward:120,size:35,boss:true,bossAbility:"iceGust"},
      {type:"arcticFoxBoss",emoji:"🦊",name:"Arctic Fox",hp:3200,speed:50,reward:130,size:35,boss:true,bossAbility:"snowDash"},
      {type:"sealBoss",emoji:"🦭",name:"Icefang Seal",hp:3500,speed:39,reward:140,size:38,boss:true,bossAbility:"iceSlide"},
      {type:"arcticWolfBoss",emoji:"🐺",name:"Tundra Wolf",hp:3800,speed:45,reward:150,size:38,boss:true,bossAbility:"frostHowl"},
      {type:"polarBearBoss",emoji:"🐻‍❄️",name:"Polar Bear",hp:4150,speed:34,reward:165,size:42,boss:true,bossAbility:"iceSwipe"},
      {type:"muskOxBoss",emoji:"🐂",name:"Musk Ox",hp:4450,speed:31,reward:175,size:42,boss:true,bossAbility:"charge"},
      {type:"walrusBoss",emoji:"🦭",name:"Ancient Walrus",hp:4750,speed:29,reward:185,size:43,boss:true,bossAbility:"tuskRush"},
      {type:"snowLeopardBoss",emoji:"🐆",name:"Snow Leopard",hp:5050,speed:46,reward:195,size:39,boss:true,bossAbility:"pounce"},
      {type:"iceBearBoss",emoji:"🐻‍❄️",name:"Glacier Bear",hp:5400,speed:31,reward:210,size:44,boss:true,bossAbility:"blizzard"},
      {type:"frostMammothBoss",emoji:"🦣",name:"Frost Mammoth",hp:5800,speed:25,reward:225,size:47,boss:true,bossAbility:"blizzard"}
    ]
  };
  const roster=rosters[currentSeries]||rosters[1];
  return {...roster[Math.max(0,Math.min(9,currentMap-1))]};
}

function finalMapBossForWave(){
  if(battle.wave!==15 || battle.finalBossSpawned)return null;
  return bossForSeriesMap();
}'''

pat=r'function finalMapBossForWave\(\)\{.*?\n\}'
s2,n=re.subn(pat,new_boss_code,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'boss function replacement count {n}')
s=s2

old='''  const isFinalBossWave=currentMap===10&&battle.wave===15;\n  if(isFinalBossWave){\n    const bossNames={1:"ALPHA BEAR",2:"GIANT SCORPION",3:"HAUNTED REAPER",4:"FROST MAMMOTH"};\n    message.textContent=`⚠️ BOSS WAVE — ${bossNames[currentSeries]}!`;\n  }\n  battle.spawnLeft=isFinalBossWave?1:Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));'''
new='''  const isBossWave=battle.wave===15;\n  if(isBossWave){\n    const boss=bossForSeriesMap();\n    message.textContent=`⚠️ BOSS WAVE — ${boss.name.toUpperCase()}!`;\n  }\n  battle.spawnLeft=isBossWave?1:Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));'''
if old not in s:
    raise SystemExit('wave 15 setup anchor not found')
s=s.replace(old,new,1)

p.write_text(s)
print('Added map-specific Wave 15 bosses for all 40 maps')
