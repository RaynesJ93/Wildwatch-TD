from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='parrot:{name:"Parrot",emoji:"🦜",rarity:"Common",cost:64,range:205,rate:1/1.20,dmg:11,color:"#e44"'
new='parrot:{name:"Parrot",emoji:"🦜",rarity:"Common",cost:64,range:205,rate:1/1.20,dmg:19,color:"#e44"'
if old not in s: raise SystemExit('Parrot base damage marker not found')
s=s.replace(old,new,1)
p.write_text(s)
