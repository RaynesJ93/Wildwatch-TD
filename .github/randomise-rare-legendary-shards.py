from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('''    }else if(chestType==="epic"){
      shardAmount=Math.random()<.80 ? 2+Math.floor(Math.random()*3) : 1;
    }else if(chestType==="legendary"){
      shardAmount=Math.random()<.70 ? 2+Math.floor(Math.random()*3) : 1;''','''    }else if(chestType==="epic"){
      // Rare Chest: always award a random 1-4 shards.
      shardAmount=1+Math.floor(Math.random()*4);
    }else if(chestType==="legendary"){
      // Legendary Chest: always award a random 1-3 shards.
      shardAmount=1+Math.floor(Math.random()*3);''')
p.write_text(s)
