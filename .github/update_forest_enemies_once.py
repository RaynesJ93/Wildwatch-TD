from pathlib import Path

p=Path('index.html')
s=p.read_text()
old='''  if(w>=7 && r<.12)return {type:"boss",emoji:"👹",hp:(170+w*18)*.8,speed:42,reward:16,size:22};
  if(w>=4 && r<.28)return {type:"boar",emoji:"🐗",hp:(95+w*12)*.8,speed:52,reward:10,size:19};
  if(r<.35)return {type:"rat",emoji:"🐀",hp:(38+w*8)*.8,speed:82,reward:6,size:15};
  return {type:"raccoon",emoji:"🦝",hp:(58+w*10)*.8,speed:61,reward:8,size:17};'''
new='''  // Forest Pines enemies: Rat, Raccoon and Rabbit, with a large Boar boss.
  if(w>=7 && r<.12)return {type:"boar",emoji:"🐗",hp:(170+w*18)*.8,speed:42,reward:16,size:30,boss:true};
  if(w>=4 && r<.28)return {type:"rabbit",emoji:"🐇",hp:(95+w*12)*.8,speed:68,reward:10,size:18};
  if(r<.35)return {type:"rat",emoji:"🐀",hp:(38+w*8)*.8,speed:82,reward:6,size:15};
  return {type:"raccoon",emoji:"🦝",hp:(58+w*10)*.8,speed:61,reward:8,size:17};'''
if old not in s:
    raise SystemExit('Forest enemy block not found')
s=s.replace(old,new,1)
p.write_text(s)
