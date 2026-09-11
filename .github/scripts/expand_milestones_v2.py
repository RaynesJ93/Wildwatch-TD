from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

if 'totalPacksOpened:0,totalCardsCollected:0' not in s:
    s = s.replace(
        'metaCoins:250, level:1, xp:0, packTokens:0, bestWave:0,',
        'metaCoins:250, level:1, xp:0, packTokens:0, bestWave:0, totalPacksOpened:0,totalCardsCollected:0,totalWaves:0,',
        1,
    )

migration = "save.totalCardsCollected=Math.max(Number(save.totalCardsCollected||0),(save.unlocked||[]).length);"
if migration not in s:
    marker = 'save.cardXP=save.cardXP||{};'
    if marker not in s:
        raise SystemExit('Save migration insertion point not found')
    s = s.replace(marker, marker + '\n' + migration, 1)

counter_code = """  save.totalPacksOpened=Math.max(0,Number(save.totalPacksOpened||0))+1;
  save.totalCardsCollected=Math.max(0,Number(save.totalCardsCollected||0))+1;"""
if 'save.totalPacksOpened=Math.max(0,Number(save.totalPacksOpened||0))+1;' not in s:
    marker = '  const fresh=!save.unlocked.includes(key);'
    if marker not in s:
        raise SystemExit('Pack counter insertion point not found')
    s = s.replace(marker, marker + '\n' + counter_code, 1)

milestone_block = """const MILESTONE_QUESTS=[
 {id:'common3',icon:'⚪',name:'Common Collector I',text:'Collect 3 Common cards',reward:25,type:'commonOwned',goal:3},
 {id:'common7',icon:'⚪',name:'Common Collector II',text:'Collect 7 Common cards',reward:50,type:'commonOwned',goal:7},
 {id:'common14',icon:'⚪',name:'Common Collector III',text:'Collect 14 Common cards',reward:100,type:'commonOwned',goal:14},
 {id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:500,rewardType:'exp',type:'commonOwned',goal:'allCommon'},
 {id:'uncommon3',icon:'🟢',name:'Uncommon Collector I',text:'Collect 3 Uncommon cards',reward:30,type:'uncommonOwned',goal:3},
 {id:'uncommon7',icon:'🟢',name:'Uncommon Collector II',text:'Collect 7 Uncommon cards',reward:60,type:'uncommonOwned',goal:7},
 {id:'uncommon14',icon:'🟢',name:'Uncommon Collector III',text:'Collect 14 Uncommon cards',reward:125,type:'uncommonOwned',goal:14},
 {id:'uncommonAll',icon:'🏆',name:'Uncommon Collector IV',text:'Collect all Uncommon cards',reward:500,rewardType:'exp',type:'uncommonOwned',goal:'allUncommon'},
 {id:'rare3',icon:'💎',name:'Rare Collector I',text:'Collect 3 Rare cards',reward:75,type:'rareOwned',goal:3},
 {id:'rare7',icon:'💎',name:'Rare Collector II',text:'Collect 7 Rare cards',reward:150,type:'rareOwned',goal:7},
 {id:'rare14',icon:'💎',name:'Rare Collector III',text:'Collect 14 Rare cards',reward:300,type:'rareOwned',goal:14},
 {id:'rareAll',icon:'🏆',name:'Rare Collector IV',text:'Collect all Rare cards',reward:750,rewardType:'exp',type:'rareOwned',goal:'allRare'},
 {id:'legendary1',icon:'🌟',name:'Legendary Collector I',text:'Collect 1 Legendary card',reward:150,type:'legendaryOwned',goal:1},
 {id:'legendary3',icon:'🌟',name:'Legendary Collector II',text:'Collect 3 Legendary cards',reward:300,type:'legendaryOwned',goal:3},
 {id:'legendary7',icon:'🌟',name:'Legendary Collector III',text:'Collect 7 Legendary cards',reward:600,type:'legendaryOwned',goal:7},
 {id:'legendaryAll',icon:'🏆',name:'Legendary Collector IV',text:'Collect all Legendary cards',reward:1000,rewardType:'exp',type:'legendaryOwned',goal:'allLegendary'},
 {id:'growingCollection',icon:'🃏',name:'Growing Collection',text:'Own 10 animal cards',reward:150,type:'allOwned',goal:10},
 {id:'cardsCollected10',icon:'🃏',name:'Card Haul I',text:'Collect 10 cards from packs',reward:100,type:'cardsCollected',goal:10},
 {id:'cardsCollected25',icon:'🃏',name:'Card Haul II',text:'Collect 25 cards from packs',reward:150,rewardType:'exp',type:'cardsCollected',goal:25},
 {id:'cardsCollected50',icon:'🃏',name:'Card Haul III',text:'Collect 50 cards from packs',reward:300,type:'cardsCollected',goal:50},
 {id:'cardsCollected100',icon:'🏆',name:'Card Haul IV',text:'Collect 100 cards from packs',reward:350,rewardType:'exp',type:'cardsCollected',goal:100},
 {id:'veteranDefender',icon:'🌊',name:'Wave Veteran I',text:'Clear 100 total waves',reward:250,type:'totalWaves',goal:100},
 {id:'waves250',icon:'🌊',name:'Wave Veteran II',text:'Clear 250 total waves',reward:300,rewardType:'exp',type:'totalWaves',goal:250},
 {id:'waves500',icon:'🌊',name:'Wave Veteran III',text:'Clear 500 total waves',reward:750,type:'totalWaves',goal:500},
 {id:'waves1000',icon:'🏆',name:'Wave Legend',text:'Clear 1,000 total waves',reward:750,rewardType:'exp',type:'totalWaves',goal:1000},
 {id:'packs5',icon:'🎁',name:'Pack Opener I',text:'Open 5 card packs',reward:75,type:'packsOpened',goal:5},
 {id:'packs15',icon:'🎁',name:'Pack Opener II',text:'Open 15 card packs',reward:125,rewardType:'exp',type:'packsOpened',goal:15},
 {id:'packs30',icon:'🎁',name:'Pack Opener III',text:'Open 30 card packs',reward:250,type:'packsOpened',goal:30},
 {id:'packs75',icon:'🏆',name:'Pack Opener IV',text:'Open 75 card packs',reward:300,rewardType:'exp',type:'packsOpened',goal:75},
 {id:'masterCollector',icon:'🏆',name:'Master Collector',text:'Own your first Legendary card',reward:300,type:'legendaryOwned',goal:1}
];"""
s, n = re.subn(r"const MILESTONE_QUESTS=\[.*?\n\];", milestone_block, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Milestone quest block not found')

if "if(q.type==='cardsCollected')" not in s:
    marker = " if(q.type==='totalWaves')progress=Math.max(0,Number(save.totalWaves||0));"
    addition = marker + "\n if(q.type==='cardsCollected')progress=Math.max(0,Number(save.totalCardsCollected||0));\n if(q.type==='packsOpened')progress=Math.max(0,Number(save.totalPacksOpened||0));"
    if marker not in s:
        raise SystemExit('Lifetime progress insertion point not found')
    s = s.replace(marker, addition, 1)

uncommon_block = """ if(q.type==='uncommonOwned'){
   const uncommonKeys=Object.keys(animals).filter(k=>animals[k].rarity==='Uncommon');
   progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Uncommon').length;
   goal=q.goal==='allUncommon'?uncommonKeys.length:Number(q.goal||uncommonKeys.length);
 }"""
rarity_extra = """
 if(q.type==='rareOwned'){
   const rareKeys=Object.keys(animals).filter(k=>animals[k].rarity==='Rare');
   progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Rare').length;
   goal=q.goal==='allRare'?rareKeys.length:Number(q.goal||rareKeys.length);
 }
 if(q.type==='legendaryOwned'){
   const legendaryKeys=Object.keys(animals).filter(k=>animals[k].rarity==='Legendary');
   progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Legendary').length;
   goal=q.goal==='allLegendary'?legendaryKeys.length:Number(q.goal||legendaryKeys.length);
 }"""
if "q.goal==='allRare'" not in s:
    if uncommon_block not in s:
        raise SystemExit('Rarity progress insertion point not found')
    s = s.replace(uncommon_block, uncommon_block + rarity_extra, 1)

old_tier = "const tier=q.type==='commonOwned'?'Common':q.type==='uncommonOwned'?'Uncommon':null;"
new_tier = "const tier=q.type==='commonOwned'?'Common':q.type==='uncommonOwned'?'Uncommon':q.type==='rareOwned'?'Rare':q.type==='legendaryOwned'?'Legendary':null;"
if old_tier in s:
    s = s.replace(old_tier, new_tier, 1)

required = ['Rare Collector IV', 'Legendary Collector IV', 'Card Haul IV', 'Wave Legend', 'Pack Opener IV', 'totalPacksOpened']
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit('Missing expected updates: ' + ', '.join(missing))

p.write_text(s)
print('Milestone expansion applied successfully.')
