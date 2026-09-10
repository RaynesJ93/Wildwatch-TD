from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''    if(s.type==="raccoonBin"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.48);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*28;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*1.6);ctx.font="30px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🗑️",0,0);ctx.restore();
    }else if(s.type==="beeLightning"){'''
new='''    if(s.type==="raccoonBin"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.48);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*28;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*1.8);
      ctx.shadowColor="rgba(0,0,0,.45)";ctx.shadowBlur=5;
      ctx.fillStyle="#5f6973";ctx.strokeStyle="#1f252b";ctx.lineWidth=2;
      ctx.beginPath();ctx.roundRect(-11,-10,22,24,3);ctx.fill();ctx.stroke();
      ctx.fillStyle="#75818b";ctx.beginPath();ctx.roundRect(-14,-14,28,6,2);ctx.fill();ctx.stroke();
      ctx.strokeStyle="#cbd2d8";ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(-6,-7);ctx.lineTo(-6,10);ctx.moveTo(0,-7);ctx.lineTo(0,10);ctx.moveTo(6,-7);ctx.lineTo(6,10);ctx.stroke();
      ctx.fillStyle="#20262b";ctx.beginPath();ctx.arc(-7,16,3,0,Math.PI*2);ctx.arc(7,16,3,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }else if(s.type==="beeLightning"){'''
if old not in s: raise SystemExit('Raccoon projectile draw marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
