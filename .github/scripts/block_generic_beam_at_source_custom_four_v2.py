from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='BLOCK_GENERIC_BEAM_AT_SOURCE_CUSTOM_FOUR_V2'
if marker in s:
    print('Already applied')
    raise SystemExit(0)
old='''  if(t.key==="parrot"){
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.70,maxLife:.70,type:"parrotPineapple"});
  }else{
    battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":"beam"});
  }
'''
if old not in s:
    raise RuntimeError('generic fallback projectile block not found')
new='''  // BLOCK_GENERIC_BEAM_AT_SOURCE_CUSTOM_FOUR_V2: custom-animation towers must never create the legacy fallback beam.
  if(t.key==="parrot"){
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.70,maxLife:.70,type:"parrotPineapple"});
  }else if(!["peacock","turtle","lizard","scorpion"].includes(t.key)){
    battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":"beam"});
  }
'''
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Blocked generic beam creation at source for Peacock Turtle Lizard Scorpion')
