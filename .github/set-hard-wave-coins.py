from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''  // Permanent coin economy: exactly 7 Coins for every cleared wave.\n  save.metaCoins+=7;'''
new='''  // Permanent coin economy: 7 Coins per Normal wave, 12 Coins per Hard wave.\n  save.metaCoins+=hardMode?12:7;'''
if old not in s:
    raise SystemExit('current 7-coin wave reward block not found')
s=s.replace(old,new,1)
p.write_text(s)
