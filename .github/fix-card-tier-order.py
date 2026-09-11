from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='const rarityOrder={Common:1,Rare:2,Epic:3,Legendary:4};'
new='const rarityOrder={Common:1,Uncommon:2,Rare:3,Epic:4,Legendary:5};'
if old not in s:
    raise SystemExit('rarityOrder marker not found')
s=s.replace(old,new,1)
if 'Uncommon:2' not in s:
    raise SystemExit('Uncommon tier order not applied')
p.write_text(s,encoding='utf-8')
print('Cards now sort Common, Uncommon, Rare, Epic, Legendary')
