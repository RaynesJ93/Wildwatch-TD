from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='HAUNTED_ENEMIES_V1'
if marker in s:
    print('Haunted enemy roster already installed')
    raise SystemExit(0)
needle='''  // Forest Pines and Haunted Woods retain the established woodland enemy set.
  if(w>=7 && r<.12)return {type:"boar",emoji:"🐗",hp:(170+w*18)*.8,speed:42,reward:16,size:30,boss:true};'''
replacement='''  // HAUNTED_ENEMIES_V1: Haunted Woods uses its own spooky enemy roster.
  if(currentSeries===3){
    // Early waves: bats and crows. Later waves introduce spiders, wolves and ghosts.
    // Wave 7+ can spawn the Haunted Reaper as the heavy enemy.
    if(w>=7 && r<.12)return {type:"hauntedReaper",emoji:"💀",hp:(185+w*20)*.8,speed:40,reward:18,size:29,boss:true};
    if(w>=6 && r<.26)return {type:"ghost",emoji:"👻",hp:(105+w*13)*.8,speed:58,reward:11,size:20};
    if(w>=4 && r<.42)return {type:"hauntedWolf",emoji:"🐺",hp:(82+w*11)*.8,speed:72,reward:9,size:20};
    if(w>=3 && r<.58)return {type:"spider",emoji:"🕷️",hp:(52+w*9)*.8,speed:76,reward:7,size:17};
    if(r<.50)return {type:"bat",emoji:"🦇",hp:(34+w*7)*.8,speed:94,reward:6,size:16};
    return {type:"crow",emoji:"🐦‍⬛",hp:(48+w*8)*.8,speed:80,reward:7,size:17};
  }
  // Forest Pines keeps the established woodland enemy set.
  if(w>=7 && r<.12)return {type:"boar",emoji:"🐗",hp:(170+w*18)*.8,speed:42,reward:16,size:30,boss:true};'''
if needle not in s:
    raise SystemExit('enemy roster insertion point not found')
s=s.replace(needle,replacement,1)
p.write_text(s)
print('Added Haunted Woods bats, crows, spiders, wolves, ghosts and Haunted Reaper')
