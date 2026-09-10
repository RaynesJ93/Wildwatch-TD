from pathlib import Path
p=Path('index.html'); s=p.read_text()
changes={
"{id:'weeklyCommon50',icon:'⚪',name:'Common Commander',text:'Place 50 Common towers',goal:50,reward:200,type:'weeklyCommonPlaced'}":"{id:'weeklyCommon50',icon:'⚪',name:'Common Commander',text:'Place 50 Common towers',goal:50,reward:200,rewardType:'tierExp',rewardTier:'Common',type:'weeklyCommonPlaced'}",
"{id:'weeklyLegendary15',icon:'🌟',name:'Legendary Force',text:'Place 15 Legendary towers',goal:15,reward:400,type:'weeklyLegendaryPlaced'}":"{id:'weeklyLegendary15',icon:'🌟',name:'Legendary Force',text:'Place 15 Legendary towers',goal:15,reward:400,rewardType:'tierExp',rewardTier:'Legendary',type:'weeklyLegendaryPlaced'}"
}
for old,new in changes.items():
    if old not in s: raise SystemExit('weekly tower quest marker not found')
    s=s.replace(old,new,1)
# Update reward label to describe tier EXP for these quests.
s=s.replace("${q.rewardType==='exp'?'⭐':'🟡'} ${q.reward}${q.rewardType==='exp'?' EXP each':''}","${q.rewardType==='exp'||q.rewardType==='tierExp'?'⭐':'🟡'} ${q.reward}${q.rewardType==='exp'?' EXP each':q.rewardType==='tierExp'?` EXP to every ${q.rewardTier} card`:''}",1)
p.write_text(s)
