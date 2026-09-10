from pathlib import Path
p=Path('index.html'); s=p.read_text()
start=s.find('const WEEKLY_QUESTS=['); end=s.find('];',start)
if start<0 or end<0: raise SystemExit('weekly quest block not found')
end+=2
new="""const WEEKLY_QUESTS=[
 {id:'weeklyWaves150',icon:'🌊',name:'Wave Marathon',text:'Complete 150 waves',goal:150,reward:300,type:'weeklyWaves'},
 {id:'weeklyCoins2500',icon:'🪙',name:'Coin Collector',text:'Collect 2,500 coins',goal:2500,reward:350,type:'weeklyCoins'},
 {id:'weeklyCommon50',icon:'⚪',name:'Common Commander',text:'Place 50 Common towers',goal:50,reward:200,type:'weeklyCommonPlaced'},
 {id:'weeklyLegendary15',icon:'🌟',name:'Legendary Force',text:'Place 15 Legendary towers',goal:15,reward:400,type:'weeklyLegendaryPlaced'},
 {id:'weeklyLevels5',icon:'⬆️',name:'Level Climber',text:'Gain 5 player levels',goal:5,reward:500,type:'weeklyLevels'}
];"""
s=s[:start]+new+s[end:]
# Make weekly renderer show real progress-style cards rather than placeholder cards.
s=s.replace("if(w)w.innerHTML=questPlaceholderCards(WEEKLY_QUESTS);","if(w)w.innerHTML=questDropdownCards(WEEKLY_QUESTS,'progress');",1)
p.write_text(s)
