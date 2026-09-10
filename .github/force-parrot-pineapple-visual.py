from pathlib import Path
p=Path('index.html'); s=p.read_text()
# Make Parrot projectile unmistakably a pineapple at every level.
old='''battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:t.key==="parrot"?.42:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":t.key==="parrot"?"pineapple":"beam"});'''
new='''if(t.key==="parrot"){
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.70,maxLife:.70,type:"parrotPineapple"});
  }else{
    battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:t.key==="elephant"?.78:t.key==="owl"?.34:t.key==="snake"?.28:t.key==="monkey"?.32:t.key==="frog"?.20:t.key==="silverback"?.42:t.key==="penguin"?.24:(t.key==="rhino"||t.key==="whiteRhino")?.28:(t.key==="jaguar"||t.key==="lion")?.22:t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:.12,type:t.key==="elephant"?"water":t.key==="owl"?"soundwave":t.key==="snake"?"poisonblob":t.key==="monkey"?"banana":t.key==="frog"?"tongue":t.key==="silverback"?"quake":t.key==="penguin"?"ice":(t.key==="rhino"||t.key==="whiteRhino")?"horn":(t.key==="jaguar"||t.key==="lion")?"claw":t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":"beam"});
  }'''
if old not in s: raise SystemExit('Current generic projectile block not found')
s=s.replace(old,new,1)
old_draw='''    if(s.type==="pineapple"){
      const lifeMax=.42,pct=1-Math.max(0,s.life)/lifeMax;
      const x=s.x+(s.tx-s.x)*pct;
      const baseY=s.y+(s.ty-s.y)*pct;
      const y=baseY-Math.sin(pct*Math.PI)*26;
      ctx.save();ctx.translate(x,y);ctx.rotate(pct*9);
      ctx.font="34px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";
      ctx.shadowColor="#ffe36e";ctx.shadowBlur=12;
      ctx.fillText("🍍",0,0);ctx.restore();
    }else if(s.type==="pineappleExplosion"){'''
new_draw='''    if(s.type==="parrotPineapple"||s.type==="pineapple"){
      const lifeMax=s.maxLife||.70,pct=1-Math.max(0,s.life)/lifeMax;
      const x=s.x+(s.tx-s.x)*pct;
      const baseY=s.y+(s.ty-s.y)*pct;
      const y=baseY-Math.sin(pct*Math.PI)*34;
      ctx.save();ctx.translate(x,y);ctx.rotate(pct*7);
      ctx.shadowColor="#ffd54a";ctx.shadowBlur=12;
      ctx.fillStyle="#f4c542";ctx.strokeStyle="#7a5a00";ctx.lineWidth=2;
      ctx.beginPath();ctx.ellipse(0,3,11,15,0,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.strokeStyle="#b07b00";ctx.lineWidth=1.3;
      for(let yy=-6;yy<=10;yy+=6){ctx.beginPath();ctx.moveTo(-8,yy);ctx.lineTo(8,yy+6);ctx.stroke();ctx.beginPath();ctx.moveTo(8,yy);ctx.lineTo(-8,yy+6);ctx.stroke();}
      ctx.fillStyle="#3d9b42";ctx.strokeStyle="#185b24";ctx.lineWidth=1.5;
      for(let i=-2;i<=2;i++){ctx.beginPath();ctx.moveTo(0,-10);ctx.lineTo(i*5,-25+Math.abs(i)*3);ctx.lineTo(i*2,-9);ctx.closePath();ctx.fill();ctx.stroke();}
      ctx.restore();
    }else if(s.type==="pineappleExplosion"){'''
if old_draw not in s: raise SystemExit('Current pineapple draw block not found')
s=s.replace(old_draw,new_draw,1)
p.write_text(s)
