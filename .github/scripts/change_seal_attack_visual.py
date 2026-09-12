from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''    if(s.type==="sealWaterBolt"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.34);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const dx=s.tx-s.x,dy=s.ty-s.y,ang=Math.atan2(dy,dx);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      ctx.globalAlpha=.95;
      ctx.fillStyle="#55cfff";ctx.strokeStyle="#d9f8ff";ctx.lineWidth=2;
      ctx.beginPath();ctx.ellipse(0,0,15,7,0,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle="#aeeeff";
      ctx.beginPath();ctx.moveTo(-10,-5);ctx.lineTo(-22,0);ctx.lineTo(-10,5);ctx.closePath();ctx.fill();
      ctx.restore();'''
new='''    if(s.type==="sealWaterBolt"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.34);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const dx=s.tx-s.x,dy=s.ty-s.y,ang=Math.atan2(dy,dx);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      // Seal attack: water splash projectile only — no white beam/line.
      ctx.globalAlpha=.95;
      ctx.shadowColor="#28bfff";ctx.shadowBlur=10;
      ctx.fillStyle="#45c8ff";
      ctx.beginPath();ctx.ellipse(0,0,13,6,0,0,Math.PI*2);ctx.fill();
      ctx.fillStyle="#8ee8ff";
      ctx.beginPath();ctx.ellipse(6,-2,5,2.8,0,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=5;
      for(let i=0;i<4;i++){
        const back=12+i*7;
        const drift=Math.sin((performance.now()/1000)*16+i*1.8)*3;
        ctx.beginPath();ctx.arc(-back,drift,2.2+(i%2)*.8,0,Math.PI*2);ctx.fill();
      }
      if(q>.72){
        const impact=(q-.72)/.28;
        ctx.globalAlpha=Math.max(0,.9-impact*.55);
        ctx.fillStyle="#61d7ff";
        for(let i=0;i<6;i++){
          const a=(Math.PI*2*i/6)+(s.boltIndex||0)*.35;
          const r=7+impact*14;
          ctx.beginPath();ctx.arc(Math.cos(a)*r,Math.sin(a)*r,2.1,0,Math.PI*2);ctx.fill();
        }
      }
      ctx.restore();'''

count=s.count(old)
if count<1:
    raise SystemExit('sealWaterBolt render block not found')
s=s.replace(old,new)

# Also remove the pale centre-line from the curved water effect if it is used by a seal-related animation.
old2='''      ctx.globalAlpha=.95*fade;ctx.strokeStyle="#d8f8ff";ctx.lineWidth=3;ctx.shadowBlur=4;
      ctx.beginPath();ctx.moveTo(sx,sy);ctx.bezierCurveTo(sx+dx*.30+nx*wob,sy+dy*.30+ny*wob,sx+dx*.68-nx*wob*.7,sy+dy*.68-ny*wob*.7,s.tx,s.ty);ctx.stroke();
      ctx.fillStyle="#8de7ff";ctx.shadowBlur=5;'''
new2='''      ctx.fillStyle="#8de7ff";ctx.shadowBlur=5;'''
if old2 in s:
    s=s.replace(old2,new2)

p.write_text(s,encoding='utf-8')
print(f'Updated {count} seal water-bolt render block(s); removed white attack line')
