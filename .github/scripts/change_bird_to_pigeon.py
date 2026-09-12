from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='bird:{name:"Bird",emoji:"🐦",rarity:"Common",cost:55,range:190,rate:1/1.30,dmg:8,color:"#58a",desc:"Longer-range basic attacker."},'
new='bird:{name:"Pigeon",emoji:"🕊️",rarity:"Common",cost:55,range:190,rate:1/1.30,dmg:8,color:"#7f8c99",desc:"Longer-range pigeon attacker."},'
if old not in s:
    raise SystemExit('Bird card anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Changed Bird card to Pigeon while keeping the internal bird key for save compatibility')
