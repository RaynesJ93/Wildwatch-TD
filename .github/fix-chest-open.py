from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''  const fresh=!save.unlocked.includes(key);
  if(fresh){
    save.unlocked.push(key);
    save.levels[key]=save.levels[key]||1;
    save.cardXP[key]=save.cardXP[key]||0;'''
new='''  const fresh=!save.unlocked.includes(key);
  save.levels=save.levels||{};
  save.cardXP=save.cardXP||{};
  save.shards=save.shards||{};
  if(fresh){
    save.unlocked.push(key);
    save.levels[key]=save.levels[key]||1;
    save.cardXP[key]=save.cardXP[key]||0;'''
if old not in s:
    raise SystemExit('target chest code not found')
s=s.replace(old,new,1)
p.write_text(s)
