from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='speedBtn.onclick=()=>{speed=speed===1?2:1;speedBtn.textContent=`⏩ Speed: ${speed}×`};'
new='speedBtn.onclick=()=>{speed=speed===1?2:speed===2?3:1;speedBtn.textContent=`⏩ Speed: ${speed}×`};'
if old not in s:
    raise SystemExit('speed handler not found')
s=s.replace(old,new,1)
p.write_text(s)
