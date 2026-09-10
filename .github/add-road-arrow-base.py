from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''  ctx.beginPath();ctx.moveTo(path[0][0],path[0][1]);for(let i=1;i<path.length;i++)ctx.lineTo(path[i][0],path[i][1]);
  ctx.strokeStyle=currentSeries===1?"#d8b35b":"#f0d18a";ctx.lineWidth=72;ctx.stroke();
  ctx.restore();'''
new='''  ctx.beginPath();ctx.moveTo(path[0][0],path[0][1]);for(let i=1;i<path.length;i++)ctx.lineTo(path[i][0],path[i][1]);
  ctx.strokeStyle=currentSeries===1?"#d8b35b":"#f0d18a";ctx.lineWidth=72;ctx.stroke();
  ctx.restore();

  // Green direction arrow near the enemy entrance, pointing down the road.
  if(path.length>1){
    const a=path[0],b=path[1],dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy)||1;
    const ux=dx/len,uy=dy/len,px=-uy,py=ux;
    const ax=a[0]+ux*58,ay=a[1]+uy*58;
    ctx.save();
    ctx.fillStyle="#39e75f";ctx.strokeStyle="#0d6b25";ctx.lineWidth=5;ctx.lineJoin="round";
    ctx.beginPath();
    ctx.moveTo(ax+ux*30,ay+uy*30);
    ctx.lineTo(ax-ux*5+px*22,ay-uy*5+py*22);
    ctx.lineTo(ax-ux*5+px*9,ay-uy*5+py*9);
    ctx.lineTo(ax-ux*34+px*9,ay-uy*34+py*9);
    ctx.lineTo(ax-ux*34-px*9,ay-uy*34-py*9);
    ctx.lineTo(ax-ux*5-px*9,ay-uy*5-py*9);
    ctx.lineTo(ax-ux*5-px*22,ay-uy*5-py*22);
    ctx.closePath();ctx.fill();ctx.stroke();ctx.restore();
  }

  // Base building at the end of every map so the road finishes at a clear objective.
  if(path.length>1){
    const end=path[path.length-1],prev=path[path.length-2],dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1;
    const bx=end[0]-dx/len*18,by=end[1]-dy/len*18;
    ctx.save();
    ctx.translate(bx,by);
    ctx.shadowColor="#0008";ctx.shadowBlur=12;ctx.shadowOffsetY=6;
    ctx.fillStyle=currentSeries===1?"#654321":"#8a6338";ctx.strokeStyle=currentSeries===1?"#2d2116":"#4f3820";ctx.lineWidth=5;
    ctx.fillRect(-34,-28,68,56);ctx.strokeRect(-34,-28,68,56);
    ctx.shadowColor="transparent";
    ctx.fillStyle=currentSeries===1?"#355d2c":"#b78a4d";
    ctx.beginPath();ctx.moveTo(-43,-28);ctx.lineTo(0,-58);ctx.lineTo(43,-28);ctx.closePath();ctx.fill();ctx.stroke();
    ctx.fillStyle="#20170f";ctx.fillRect(-10,2,20,26);
    ctx.fillStyle="#f7d35c";ctx.fillRect(-25,-12,12,12);ctx.fillRect(13,-12,12,12);
    ctx.font="bold 16px Trebuchet MS";ctx.textAlign="center";ctx.fillStyle="#fff";ctx.strokeStyle="#000";ctx.lineWidth=4;ctx.strokeText("BASE",0,48);ctx.fillText("BASE",0,48);
    ctx.restore();
  }'''
if old not in s: raise SystemExit('road draw marker not found')
s=s.replace(old,new,1)
p.write_text(s)
