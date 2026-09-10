from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('Math.floor((cardLevel(k)-1)/5)*.025','Math.floor(cardLevel(k)/5)*.025',1)
s=s.replace('Math.pow(.98,Math.floor((cardLevel(k)-1)/5))','Math.pow(.98,Math.floor(cardLevel(k)/5))',1)
p.write_text(s)
