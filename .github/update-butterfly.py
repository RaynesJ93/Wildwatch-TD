from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Butterfly base damage -> 12
s2, n = re.subn(r'(butterfly:\{name:"Butterfly",emoji:"🦋",rarity:"Common",cost:48,range:180,rate:1/1\.40,dmg:)\d+(,)', r'\g<1>12\2', s, count=1)
if n:
    s=s2
else:
    if 'butterfly:{name:"Butterfly"' not in s:
        raise SystemExit('Butterfly card definition not found')

# 2) Give butterfly its own projectile type and slightly longer visible life
old_life='t.key==="fox"?.30:t.key==="eagle"?.28:.12'
new_life='t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="butterfly"?.34:.12'
if old_life in s:
    s=s.replace(old_life,new_life,1)

old_type='t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":"beam"'
new_type='t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="butterfly"?"seedpod":"beam"'
if old_type in s:
    s=s.replace(old_type,new_type,1)

# 3) Draw a travelling seed pod projectile
marker='    }else if(s.type==="horn"){'
seed_branch='''    }else if(s.type==="seedpod"){
      const p=1-Math.max(0,s.life)/.34;
      const x=s.x+(s.tx-s.x)*p,y=(s.y-6)+(s.ty-(s.y-6))*p;
      const ang=Math.atan2(s.ty-(s.y-6),s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      ctx.shadowColor="#90c957";ctx.shadowBlur=7;
      ctx.fillStyle="#7a4f24";ctx.beginPath();ctx.ellipse(0,0,8,4.5,0,0,Math.PI*2);ctx.fill();
      ctx.fillStyle="#c59b55";ctx.beginPath();ctx.ellipse(-2,-1,4.5,2.1,0,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle="#557b2f";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-7,0);ctx.lineTo(-12,-4);ctx.stroke();
      ctx.restore();
'''
if 's.type==="seedpod"' not in s:
    if marker not in s:
        raise SystemExit('Projectile renderer marker not found')
    s=s.replace(marker,seed_branch+marker,1)

p.write_text(s,encoding='utf-8')
print('Butterfly updated: 12 damage + seed pod projectile')
