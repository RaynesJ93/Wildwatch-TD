from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''  save.bestWave=Math.max(save.bestWave,clearedWave);\n  save.xp+=Math.round((12+clearedWave*3)*(hardMode?1.5:1));\n  save.metaCoins+=hardMode?30:20;\n  if(clearedWave%3===0)save.metaCoins+=hardMode?75:50;'''
new='''  save.bestWave=Math.max(save.bestWave,clearedWave);\n  save.xp+=Math.round((12+clearedWave*3)*(hardMode?1.5:1));\n  // Permanent coin economy: exactly 7 Coins for every cleared wave.\n  save.metaCoins+=7;'''
if old not in s:
    raise SystemExit('wave reward block not found')
s=s.replace(old,new,1)
old2='''    save.metaCoins+=hardMode?175:100;\n'''
if old2 not in s:
    raise SystemExit('map completion coin reward not found')
s=s.replace(old2,'',1)
p.write_text(s)
