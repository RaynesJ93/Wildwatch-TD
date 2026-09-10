from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":(t.key==="parrot"&&t.level>=10)?"pineapple":"beam"'''
new='''type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":t.key==="parrot"?"pineapple":"beam"'''
if old not in s:
    raise SystemExit('Parrot projectile marker not found')
s=s.replace(old,new,1)
# Give Parrot pineapple travel timing at every level; level-10 bomb logic remains unchanged.
s=s.replace('(t.key==="parrot"&&t.level>=10)?.30:.12','t.key==="parrot"?.30:.12',1)
p.write_text(s)
