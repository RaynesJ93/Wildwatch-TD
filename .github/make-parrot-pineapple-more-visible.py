from pathlib import Path
p=Path('index.html'); s=p.read_text()
# Keep Parrot pineapple projectile at all levels, but make it slower and much more visible.
old_time='t.key==="parrot"?.30:.12'
new_time='t.key==="parrot"?.42:.12'
if old_time not in s: raise SystemExit('Parrot travel timing marker not found')
s=s.replace(old_time,new_time,1)
old_draw='''    if(s.type==="pineapple"){
      const lifeMax=.30,pct=1-Math.max(0,s.life)/lifeMax;
      const x=s.x+(s.tx-s.x)*pct,y=s.y+(s.ty-s.y)*pct;
      ctx.save();ctx.translate(x,y);ctx.rotate(pct*8);ctx.font="24px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("🍍",0,0);ctx.restore();
    }else if(s.type==="pineappleExplosion"){'''
new_draw='''    if(s.type==="pineapple"){
      const lifeMax=.42,pct=1-Math.max(0,s.life)/lifeMax;
      const x=s.x+(s.tx-s.x)*pct;
      const baseY=s.y+(s.ty-s.y)*pct;
      const y=baseY-Math.sin(pct*Math.PI)*26;
      ctx.save();ctx.translate(x,y);ctx.rotate(pct*9);
      ctx.font="34px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";
      ctx.shadowColor="#ffe36e";ctx.shadowBlur=12;
      ctx.fillText("🍍",0,0);ctx.restore();
    }else if(s.type==="pineappleExplosion"){'''
if old_draw not in s: raise SystemExit('Pineapple draw block not found')
s=s.replace(old_draw,new_draw,1)
p.write_text(s)
