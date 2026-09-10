from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''  for(let i=0;i<42;i++){
    const x=35+decorRand(i*3)*770,y=45+decorRand(i*3+1)*925;
    if(!decorSafe(x,y))continue;
    const tree=decorRand(i*3+2)>.38;'''
new='''  const decorCount=currentSeries===1?78:42;
  for(let i=0;i<decorCount;i++){
    const x=35+decorRand(i*3)*770,y=45+decorRand(i*3+1)*925;
    if(!decorSafe(x,y))continue;
    const tree=decorRand(i*3+2)>(currentSeries===1?.30:.38);'''
if old not in s: raise SystemExit('forest decor loop marker not found')
s=s.replace(old,new,1)
p.write_text(s)
