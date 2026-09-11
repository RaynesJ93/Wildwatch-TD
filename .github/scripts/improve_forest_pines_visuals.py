from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='FOREST_PINES_VISUALS_V2'
if marker in s:
    print('Forest Pines visual assets already installed')
    raise SystemExit(0)
needle='''  // Road outline and road surface use the exact enemy path.
  ctx.save();'''
insert='''  // FOREST_PINES_VISUALS_V2: richer procedural forest assets, drawn in-game with canvas.
  if(currentSeries===1){
    ctx.save();
    // Soft grass variation patches break up the flat green floor.
    ctx.globalAlpha=.18;
    for(let i=0;i<28;i++){
      const x=30+decorRand(500+i*4)*760,y=45+decorRand(501+i*4)*900;
      if(!decorSafe(x,y))continue;
      const rx=18+decorRand(502+i*4)*35,ry=8+decorRand(503+i*4)*18;
      ctx.fillStyle=i%2?"#86a85c":"#244f2b";
      ctx.beginPath();ctx.ellipse(x,y,rx,ry,decorRand(504+i)*2,0,Math.PI*2);ctx.fill();
    }
    ctx.globalAlpha=1;
    // Rocks, fallen logs, stumps, ferns, mushrooms and small flowers.
    for(let i=0;i<34;i++){
      const x=35+decorRand(700+i*3)*750,y=55+decorRand(701+i*3)*890;
      if(!decorSafe(x,y))continue;
      const kind=i%6;
      if(kind===0){
        ctx.fillStyle="#6b7062";ctx.strokeStyle="#3d4439";ctx.lineWidth=2;
        ctx.beginPath();ctx.ellipse(x,y,11,7,-.25,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.fillStyle="#91a274";ctx.beginPath();ctx.ellipse(x-2,y-4,6,2,-.2,0,Math.PI*2);ctx.fill();
      }else if(kind===1){
        ctx.save();ctx.translate(x,y);ctx.rotate((decorRand(702+i)-.5)*1.4);
        ctx.fillStyle="#51361f";ctx.strokeStyle="#2b2017";ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-19,-5,38,10,5);ctx.fill();ctx.stroke();
        ctx.fillStyle="#78924e";ctx.fillRect(-10,-6,14,3);ctx.restore();
      }else if(kind===2){
        ctx.fillStyle="#67462a";ctx.fillRect(x-7,y-7,14,13);ctx.fillStyle="#927050";ctx.beginPath();ctx.ellipse(x,y-7,8,4,0,0,Math.PI*2);ctx.fill();
      }else if(kind===3){
        ctx.strokeStyle="#5c8c45";ctx.lineWidth=3;
        for(let a=-1.1;a<=1.1;a+=.55){ctx.beginPath();ctx.moveTo(x,y+7);ctx.quadraticCurveTo(x+Math.sin(a)*8,y-2,x+Math.sin(a)*15,y-12);ctx.stroke();}
      }else if(kind===4){
        ctx.fillStyle="#eee3c4";ctx.fillRect(x-1,y-4,2,6);ctx.fillStyle=i%2?"#d94a3e":"#e9c85b";ctx.beginPath();ctx.arc(x,y-5,4,Math.PI,0);ctx.fill();
      }else{
        ctx.fillStyle="#f2e5a2";for(let a=0;a<5;a++){const ang=a*Math.PI*2/5;ctx.beginPath();ctx.arc(x+Math.cos(ang)*3,y+Math.sin(ang)*3,2,0,Math.PI*2);ctx.fill();}ctx.fillStyle="#d8a832";ctx.beginPath();ctx.arc(x,y,2,0,Math.PI*2);ctx.fill();
      }
    }
    // Layered pine silhouettes around the boundary add depth without blocking tower placement.
    ctx.globalAlpha=.45;
    for(let i=0;i<18;i++){
      const x=18+i*47+(currentMap%2)*9,y=i%2?42:H-34,s=20+(i%4)*4;
      ctx.fillStyle="#153e27";ctx.fillRect(x-3,y,6,15);
      ctx.beginPath();ctx.moveTo(x,y-s);ctx.lineTo(x-s*.72,y+7);ctx.lineTo(x+s*.72,y+7);ctx.closePath();ctx.fill();
      ctx.beginPath();ctx.moveTo(x,y-s*.55);ctx.lineTo(x-s*.9,y+16);ctx.lineTo(x+s*.9,y+16);ctx.closePath();ctx.fill();
    }
    ctx.restore();
  }

  // Road outline and road surface use the exact enemy path.
  ctx.save();'''
if needle not in s:
    raise SystemExit('forest insertion point not found')
s=s.replace(needle,insert,1)
# Add a more natural dirt road treatment for Forest Pines after the main road is drawn.
needle2='''  ctx.strokeStyle=currentSeries===1?"#d8b35b":currentSeries===2?"#f0d18a":"#57405f";ctx.lineWidth=72;ctx.stroke();
  ctx.restore();'''
replace2='''  ctx.strokeStyle=currentSeries===1?"#a7834f":currentSeries===2?"#f0d18a":"#57405f";ctx.lineWidth=72;ctx.stroke();
  if(currentSeries===1){
    // Irregular darker centre and wheel-worn highlights make the forest track feel less flat.
    ctx.globalAlpha=.28;ctx.strokeStyle="#6d5233";ctx.lineWidth=48;ctx.stroke();
    ctx.globalAlpha=.22;ctx.strokeStyle="#d2b277";ctx.lineWidth=5;ctx.setLineDash([16,24]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }
  ctx.restore();'''
if needle2 not in s:
    raise SystemExit('road block not found')
s=s.replace(needle2,replace2,1)
p.write_text(s)
print('Improved Forest Pines with procedural rocks, logs, stumps, ferns, mushrooms, flowers, grass variation, boundary pines and richer dirt road')
