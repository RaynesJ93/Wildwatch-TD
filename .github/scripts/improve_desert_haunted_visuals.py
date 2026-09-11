from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='DESERT_HAUNTED_VISUALS_V2'
if marker in s:
    print('Desert/Haunted visual assets already installed')
    raise SystemExit(0)
needle='''  // Road outline and road surface use the exact enemy path.
  ctx.save();'''
insert='''  // DESERT_HAUNTED_VISUALS_V2: richer procedural assets for Desert Dunes and Haunted Woods.
  if(currentSeries===2){
    ctx.save();
    // Uneven sand tones, wind streaks and shallow dune shadows.
    ctx.globalAlpha=.16;
    for(let i=0;i<28;i++){
      const x=25+decorRand(900+i*4)*775,y=45+decorRand(901+i*4)*900;
      if(!decorSafe(x,y))continue;
      const rx=24+decorRand(902+i*4)*42,ry=7+decorRand(903+i*4)*15;
      ctx.fillStyle=i%2?"#f2cf80":"#9f7437";
      ctx.beginPath();ctx.ellipse(x,y,rx,ry,(decorRand(904+i)-.5)*.5,0,Math.PI*2);ctx.fill();
    }
    ctx.globalAlpha=1;
    // Desert props: sandstone rocks, cactus clumps, dry grass, bones, pottery and ruined pillars.
    for(let i=0;i<34;i++){
      const x=35+decorRand(1000+i*3)*750,y=55+decorRand(1001+i*3)*890;
      if(!decorSafe(x,y))continue;
      const kind=i%6;
      if(kind===0){
        ctx.fillStyle="#9f7642";ctx.strokeStyle="#694a2b";ctx.lineWidth=2;
        ctx.beginPath();ctx.ellipse(x,y,13,8,-.25,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.fillStyle="#c0965c";ctx.beginPath();ctx.ellipse(x-3,y-4,7,2,-.2,0,Math.PI*2);ctx.fill();
      }else if(kind===1){
        ctx.strokeStyle="#3e743f";ctx.lineWidth=5;ctx.lineCap="round";
        ctx.beginPath();ctx.moveTo(x,y+9);ctx.lineTo(x,y-12);ctx.moveTo(x,y-3);ctx.lineTo(x-8,y-8);ctx.moveTo(x,y-7);ctx.lineTo(x+8,y-14);ctx.stroke();
        ctx.lineCap="butt";
      }else if(kind===2){
        ctx.strokeStyle="#a98a4e";ctx.lineWidth=2;
        for(let j=-2;j<=2;j++){ctx.beginPath();ctx.moveTo(x+j*2,y+6);ctx.lineTo(x+j*4,y-7-(j%2)*3);ctx.stroke();}
      }else if(kind===3){
        ctx.strokeStyle="#e6d7aa";ctx.lineWidth=3;ctx.lineCap="round";
        ctx.beginPath();ctx.moveTo(x-8,y);ctx.lineTo(x+8,y);ctx.moveTo(x-10,y-3);ctx.lineTo(x-6,y+3);ctx.moveTo(x+10,y-3);ctx.lineTo(x+6,y+3);ctx.stroke();ctx.lineCap="butt";
      }else if(kind===4){
        ctx.fillStyle="#9b5f33";ctx.strokeStyle="#5c351e";ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(x,y,6,8,0,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle="#d29a62";ctx.fillRect(x-4,y-6,8,2);
      }else{
        ctx.fillStyle="#b88b4e";ctx.strokeStyle="#6e4d2b";ctx.lineWidth=2;ctx.fillRect(x-5,y-16,10,23);ctx.strokeRect(x-5,y-16,10,23);ctx.fillStyle="#d0a66d";ctx.fillRect(x-8,y-18,16,4);
      }
    }
    // Faint wind-carved lines near the map edges.
    ctx.globalAlpha=.22;ctx.strokeStyle="#fff0bd";ctx.lineWidth=2;
    for(let i=0;i<10;i++){
      const y=70+i*92+(currentMap%3)*7;ctx.beginPath();ctx.moveTo(18,y);ctx.quadraticCurveTo(42,y-6,68,y);ctx.stroke();
      ctx.beginPath();ctx.moveTo(W-68,y+25);ctx.quadraticCurveTo(W-42,y+19,W-18,y+25);ctx.stroke();
    }
    ctx.restore();
  }else if(currentSeries===3){
    ctx.save();
    // Purple-black ground stains and moonlit patches add depth to the haunted floor.
    ctx.globalAlpha=.18;
    for(let i=0;i<26;i++){
      const x=30+decorRand(1200+i*4)*760,y=45+decorRand(1201+i*4)*900;
      if(!decorSafe(x,y))continue;
      const rx=20+decorRand(1202+i*4)*38,ry=8+decorRand(1203+i*4)*18;
      ctx.fillStyle=i%2?"#6d4b7c":"#0d0814";
      ctx.beginPath();ctx.ellipse(x,y,rx,ry,(decorRand(1204+i)-.5)*.8,0,Math.PI*2);ctx.fill();
    }
    ctx.globalAlpha=1;
    // Haunted props: broken fencing, bones, dead roots, candles, mushrooms, stones and thorn bushes.
    for(let i=0;i<34;i++){
      const x=35+decorRand(1300+i*3)*750,y=55+decorRand(1301+i*3)*890;
      if(!decorSafe(x,y))continue;
      const kind=i%6;
      if(kind===0){
        ctx.strokeStyle="#5a514f";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x-12,y+7);ctx.lineTo(x-10,y-10);ctx.moveTo(x+9,y+7);ctx.lineTo(x+11,y-12);ctx.moveTo(x-14,y-1);ctx.lineTo(x+14,y-5);ctx.stroke();
      }else if(kind===1){
        ctx.strokeStyle="#d2c9ba";ctx.lineWidth=3;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(x-8,y);ctx.lineTo(x+8,y);ctx.moveTo(x-10,y-3);ctx.lineTo(x-6,y+3);ctx.moveTo(x+10,y-3);ctx.lineTo(x+6,y+3);ctx.stroke();ctx.lineCap="butt";
      }else if(kind===2){
        ctx.strokeStyle="#3b2a3f";ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x,y+8);ctx.quadraticCurveTo(x-5,y-2,x-14,y-10);ctx.moveTo(x,y+5);ctx.quadraticCurveTo(x+4,y-4,x+13,y-13);ctx.moveTo(x-2,y+3);ctx.lineTo(x-17,y+1);ctx.stroke();
      }else if(kind===3){
        ctx.fillStyle="#d9d2b7";ctx.fillRect(x-2,y-6,4,10);ctx.fillStyle="#ffd36a";ctx.shadowColor="#ffb347";ctx.shadowBlur=8;ctx.beginPath();ctx.ellipse(x,y-8,3,5,0,0,Math.PI*2);ctx.fill();ctx.shadowColor="transparent";
      }else if(kind===4){
        ctx.fillStyle="#d8d1c8";ctx.fillRect(x-1,y-4,2,6);ctx.fillStyle=i%2?"#8d57a8":"#c6b2dc";ctx.beginPath();ctx.arc(x,y-5,4,Math.PI,0);ctx.fill();
      }else{
        ctx.strokeStyle="#2b1730";ctx.lineWidth=3;for(let a=-1;a<=1;a+=.5){ctx.beginPath();ctx.moveTo(x,y+7);ctx.lineTo(x+Math.sin(a)*13,y-11);ctx.stroke();}
        ctx.fillStyle="#80569a";ctx.beginPath();ctx.arc(x-6,y-3,2,0,Math.PI*2);ctx.arc(x+5,y-7,2,0,Math.PI*2);ctx.fill();
      }
    }
    // Low wisps of fog close to the ground.
    ctx.globalAlpha=.12;ctx.fillStyle="#d8d4e3";
    for(let i=0;i<12;i++){const x=20+decorRand(1500+i)*780,y=100+decorRand(1520+i)*820;if(!decorSafe(x,y))continue;ctx.beginPath();ctx.ellipse(x,y,58,12,.05,0,Math.PI*2);ctx.fill();}
    ctx.restore();
  }

  // Road outline and road surface use the exact enemy path.
  ctx.save();'''
if needle not in s:
    raise SystemExit('road insertion point not found')
s=s.replace(needle,insert,1)
# Give Desert and Haunted roads extra texture after the main surface stroke.
needle2='''  if(currentSeries===1){
    // Irregular darker centre and wheel-worn highlights make the forest track feel less flat.
    ctx.globalAlpha=.28;ctx.strokeStyle="#6d5233";ctx.lineWidth=48;ctx.stroke();
    ctx.globalAlpha=.22;ctx.strokeStyle="#d2b277";ctx.lineWidth=5;ctx.setLineDash([16,24]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }
  ctx.restore();'''
replace2='''  if(currentSeries===1){
    // Irregular darker centre and wheel-worn highlights make the forest track feel less flat.
    ctx.globalAlpha=.28;ctx.strokeStyle="#6d5233";ctx.lineWidth=48;ctx.stroke();
    ctx.globalAlpha=.22;ctx.strokeStyle="#d2b277";ctx.lineWidth=5;ctx.setLineDash([16,24]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }else if(currentSeries===2){
    ctx.globalAlpha=.22;ctx.strokeStyle="#b48749";ctx.lineWidth=46;ctx.stroke();
    ctx.globalAlpha=.24;ctx.strokeStyle="#ffe2a0";ctx.lineWidth=4;ctx.setLineDash([13,28]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }else if(currentSeries===3){
    ctx.globalAlpha=.35;ctx.strokeStyle="#2a1b31";ctx.lineWidth=46;ctx.stroke();
    ctx.globalAlpha=.18;ctx.strokeStyle="#a68caf";ctx.lineWidth=3;ctx.setLineDash([10,24]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }
  ctx.restore();'''
if needle2 not in s:
    raise SystemExit('road texture block not found')
s=s.replace(needle2,replace2,1)
p.write_text(s)
print('Improved Desert Dunes and Haunted Woods with richer in-game procedural assets and road textures')
