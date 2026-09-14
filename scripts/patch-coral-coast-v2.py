from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'coral-coast.js' in s:
    raise SystemExit('already patched')
# Load Region 7 gameplay after the main game script.
s=s.replace('</body>','<script src="coral-coast.js"></script>\n</body>',1)
# Add Coral Coast map selector styling.
style='''<style id="coral-coast-v2-style">\n.region-hero.coral{background:linear-gradient(135deg,#073d5b,#0d91a8 55%,#ddb967);border-color:#58dbe4}\n.stage-thumb.coral{background:linear-gradient(145deg,#1aaec4,#50d8dc 52%,#edcd7a);color:#fff;text-shadow:0 2px 5px #06475d}\n</style>\n'''
s=s.replace('</head>',style+'</head>',1)
# Give Region 7 a true water palette instead of falling through to Crystal Caverns.
s=s.replace('  const crystalStone=["#172238","#192740","#20234b","#152d45","#251d50","#18354a","#212b55","#172c42","#2a2058","#193149"];','  const crystalStone=["#172238","#192740","#20234b","#152d45","#251d50","#18354a","#212b55","#172c42","#2a2058","#193149"];\n  const coralWater=["#36bfd0","#2eb6ca","#43c7d4","#27afc4","#3ac1cf","#2ab4c7","#45c9d3","#25aec1","#36bdcd","#22a8bd"];',1)
s=s.replace('currentSeries===5?volcanicRock[currentMap-1]:crystalStone[currentMap-1]','currentSeries===5?volcanicRock[currentMap-1]:currentSeries===6?crystalStone[currentMap-1]:coralWater[currentMap-1]',1)
s=s.replace('currentSeries===5?"#120e0d":"#101a35"','currentSeries===5?"#120e0d":currentSeries===6?"#101a35":"#087f97"',1)
s=s.replace('currentSeries===5?"#4a2118":"#3b3670"','currentSeries===5?"#4a2118":currentSeries===6?"#3b3670":"#d2ab62"',1)
s=s.replace('currentSeries===5?"#3b2521":"#5969a8"','currentSeries===5?"#3b2521":currentSeries===6?"#5969a8":"#f1d38e"',1)
p.write_text(s)
