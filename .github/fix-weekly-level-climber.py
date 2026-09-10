from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''function levelCheck(){
  let need=100+save.level*35;
  while(save.xp>=need){save.xp-=need;save.level++;save.metaCoins+=150;need=100+save.level*35;}
}'''
new='''function levelCheck(){
  let need=100+save.level*35;
  let gainedLevels=0;
  while(save.xp>=need){save.xp-=need;save.level++;save.metaCoins+=150;gainedLevels++;need=100+save.level*35;}
  if(gainedLevels>0)addWeeklyProgress("weeklyLevels",gainedLevels);
}'''
if old not in s: raise SystemExit('levelCheck marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
