from pathlib import Path

p = Path('index.html')
s = p.read_text()

old = 'life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":"beam"'
new = 'life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":"beam"'
if old not in s:
    raise SystemExit('Rhino shot selector insertion point not found')
s = s.replace(old, new, 1)

marker = '    }else if(s.type==="soundwave"){' 
horn = '''    }else if(s.type==="horn"){
      const p=1-Math.max(0,s.life)/.28;
      const x=s.x+(s.tx-s.x)*p,y=(s.y-8)+(s.ty-(s.y-8))*p;
      const ang=Math.atan2(s.ty-(s.y-8),s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      ctx.shadowColor="#fff1b8";ctx.shadowBlur=9;
      ctx.fillStyle="#f1e1b8";ctx.strokeStyle="#6c593e";ctx.lineWidth=2;
      ctx.beginPath();
      ctx.moveTo(18,0);
      ctx.quadraticCurveTo(5,-8,-13,-5.5);
      ctx.quadraticCurveTo(-8,0,-13,5.5);
      ctx.quadraticCurveTo(5,8,18,0);
      ctx.closePath();ctx.fill();ctx.stroke();
      ctx.strokeStyle="#fff9de";ctx.lineWidth=1.4;
      ctx.beginPath();ctx.moveTo(-9,-2.8);ctx.quadraticCurveTo(4,-2,15,0);ctx.stroke();
      ctx.restore();
'''
if marker not in s:
    raise SystemExit('Projectile renderer insertion point not found')
s = s.replace(marker, horn + marker, 1)

p.write_text(s)
