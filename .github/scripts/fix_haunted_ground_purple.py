from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='HAUNTED_PURPLE_GROUND_V1'
if marker in s:
    print('Haunted purple ground already installed')
    raise SystemExit(0)
old='''  const desertSands=["#d6b25d","#cfa957","#dbb968","#c9a252","#dfbd6b","#d2aa58","#d9b563","#cba657","#dfba64","#d1ad5c"];
  ctx.fillStyle=currentSeries===1?forestGreens[currentMap-1]:desertSands[currentMap-1];ctx.fillRect(0,0,W,H);'''
new='''  const desertSands=["#d6b25d","#cfa957","#dbb968","#c9a252","#dfbd6b","#d2aa58","#d9b563","#cba657","#dfba64","#d1ad5c"];
  // HAUNTED_PURPLE_GROUND_V1: Haunted Woods has its own dark purple ground instead of inheriting Desert sand.
  const hauntedPurples=["#24152f","#291735","#21132c","#30183b","#261431","#2d1738","#22142e","#321a3d","#281533","#25122f"];
  ctx.fillStyle=currentSeries===1?forestGreens[currentMap-1]:currentSeries===2?desertSands[currentMap-1]:hauntedPurples[currentMap-1];ctx.fillRect(0,0,W,H);'''
if old not in s:
    raise SystemExit('battlefield ground block not found')
s=s.replace(old,new,1)
# Give Haunted Woods a purple-black edge rather than the old green-black edge.
s=s.replace('ctx.fillStyle=currentSeries===1?"#24552b":currentSeries===2?"#a77c36":"#16241d";','ctx.fillStyle=currentSeries===1?"#24552b":currentSeries===2?"#a77c36":"#140b1d";',1)
# Haunted road should also stop using the Desert sand road palette.
s=s.replace('ctx.strokeStyle=currentSeries===1?"#8b612d":"#9b6b38";ctx.lineWidth=92;ctx.stroke();','ctx.strokeStyle=currentSeries===1?"#8b612d":currentSeries===2?"#9b6b38":"#160d20";ctx.lineWidth=92;ctx.stroke();',1)
s=s.replace('ctx.strokeStyle=currentSeries===1?"#d8b35b":"#f0d18a";ctx.lineWidth=72;ctx.stroke();','ctx.strokeStyle=currentSeries===1?"#d8b35b":currentSeries===2?"#f0d18a":"#57405f";ctx.lineWidth=72;ctx.stroke();',1)
s=s.replace('ctx.strokeStyle=currentSeries===1?"#d8b35b":"#f0d18a";\n    ctx.lineWidth=72;ctx.lineCap="round";','ctx.strokeStyle=currentSeries===1?"#d8b35b":currentSeries===2?"#f0d18a":"#57405f";\n    ctx.lineWidth=72;ctx.lineCap="round";',1)
# Haunted base gets a dark haunted palette too, rather than Desert browns.
s=s.replace('ctx.fillStyle=currentSeries===1?"#654321":"#8a6338";ctx.strokeStyle=currentSeries===1?"#2d2116":"#4f3820";ctx.lineWidth=5;','ctx.fillStyle=currentSeries===1?"#654321":currentSeries===2?"#8a6338":"#28172f";ctx.strokeStyle=currentSeries===1?"#2d2116":currentSeries===2?"#4f3820":"#0d0712";ctx.lineWidth=5;',1)
s=s.replace('ctx.fillStyle=currentSeries===1?"#355d2c":"#b78a4d";','ctx.fillStyle=currentSeries===1?"#355d2c":currentSeries===2?"#b78a4d":"#4b3157";',1)
p.write_text(s)
print('Haunted Woods ground changed to dark purple with haunted road/base palette')
