from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='VOLCANIC_WASTELAND_VISUALS_V2'
if marker in s:
    print('already installed')
    raise SystemExit(0)
old='''  if(currentSeries===5){
    ctx.save();
    // Glowing lava rivers, basalt boulders, vents, embers and obsidian shards.
    for(let i=0;i<24;i++){const x=35+decorRand(1800+i*4)*760,y=55+decorRand(1801+i*4)*900;if(!decorSafe(x,y))continue;const kind=i%4;
      if(kind===0){ctx.fillStyle="#171313";ctx.strokeStyle="#5a3024";ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(x,y,16,10,.2,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.strokeStyle="#ff5a1f";ctx.beginPath();ctx.moveTo(x-8,y);ctx.lineTo(x,y-3);ctx.lineTo(x+7,y+2);ctx.stroke();}
      else if(kind===1){ctx.fillStyle="#121010";ctx.strokeStyle="#ff6a22";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,y-22);ctx.lineTo(x+11,y+8);ctx.lineTo(x-10,y+8);ctx.closePath();ctx.fill();ctx.stroke();}
      else if(kind===2){ctx.fillStyle="#ff5a18";ctx.shadowColor="#ff3b00";ctx.shadowBlur=12;ctx.beginPath();ctx.ellipse(x,y,19,7,0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#ffd34d";ctx.beginPath();ctx.ellipse(x,y,10,3,0,0,Math.PI*2);ctx.fill();ctx.shadowColor="transparent";}
      else{ctx.strokeStyle="#ff7b31";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,y+8);ctx.quadraticCurveTo(x-7,y-4,x,y-14);ctx.quadraticCurveTo(x+7,y-4,x,y+8);ctx.stroke();}
    }
    ctx.fillStyle="#ff8a35";ctx.globalAlpha=.65;for(let i=0;i<30;i++){const x=(i*97+currentMap*53)%W,y=(i*149+currentMap*37)%H;if(!decorSafe(x,y))continue;ctx.beginPath();ctx.arc(x,y,1.5+(i%2),0,Math.PI*2);ctx.fill();}
    ctx.restore();
  }'''
new='''  if(currentSeries===5){
    // VOLCANIC_WASTELAND_VISUALS_V2: richer animated volcanic terrain using only in-game canvas assets.
    ctx.save();
    const vt=performance.now()/1000;

    // Deep heat glow under the scorched floor so the map feels hot rather than flat brown.
    ctx.globalAlpha=.16;
    for(let i=0;i<14;i++){
      const x=40+decorRand(1700+i*5)*750,y=55+decorRand(1701+i*5)*890;
      if(!decorSafe(x,y))continue;
      const pulse=.72+.28*Math.sin(vt*1.5+i);
      ctx.fillStyle=i%2?"#8b1f0f":"#ff4a12";
      ctx.beginPath();ctx.ellipse(x,y,(34+decorRand(1702+i)*44)*pulse,8+decorRand(1703+i)*16,.25,0,Math.PI*2);ctx.fill();
    }
    ctx.globalAlpha=1;

    // Distant volcano silhouettes around the rim of the battlefield.
    ctx.fillStyle="#120d0d";ctx.strokeStyle="#3e1812";ctx.lineWidth=3;
    for(let i=0;i<7;i++){
      const x=55+i*122+(currentMap%2)*18,y=i%2?70:H-42,h=36+(i%3)*13,w=38+(i%2)*12;
      ctx.beginPath();ctx.moveTo(x-w,y);ctx.lineTo(x,y-h);ctx.lineTo(x+w,y);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.strokeStyle="#ff5a1f";ctx.globalAlpha=.55;ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(x-7,y-h+8);ctx.lineTo(x,y-h+15);ctx.lineTo(x+9,y-h+9);ctx.stroke();
      ctx.globalAlpha=1;ctx.strokeStyle="#3e1812";ctx.lineWidth=3;
    }

    // Basalt boulders, obsidian shards, lava pools, fire vents, skulls and cooled magma plates.
    for(let i=0;i<42;i++){
      const x=30+decorRand(1800+i*5)*770,y=50+decorRand(1801+i*5)*900;
      if(!decorSafe(x,y))continue;
      const kind=i%6;
      if(kind===0){
        ctx.fillStyle="#171313";ctx.strokeStyle="#603125";ctx.lineWidth=2;
        ctx.beginPath();ctx.ellipse(x,y,13+decorRand(1802+i)*9,8+decorRand(1803+i)*6,.2,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.strokeStyle="#ff5a1f";ctx.lineWidth=2.4;ctx.beginPath();ctx.moveTo(x-10,y+1);ctx.lineTo(x-3,y-4);ctx.lineTo(x+3,y+1);ctx.lineTo(x+10,y-3);ctx.stroke();
      }else if(kind===1){
        ctx.fillStyle="#0c0a0b";ctx.strokeStyle="#8f3520";ctx.lineWidth=2;
        ctx.beginPath();ctx.moveTo(x,y-25);ctx.lineTo(x+12,y+9);ctx.lineTo(x-11,y+9);ctx.closePath();ctx.fill();ctx.stroke();
        ctx.strokeStyle="#ff7131";ctx.beginPath();ctx.moveTo(x,y-20);ctx.lineTo(x+2,y+4);ctx.stroke();
      }else if(kind===2){
        const pulse=1+Math.sin(vt*2.2+i)*.08;
        ctx.save();ctx.translate(x,y);ctx.scale(pulse,pulse);ctx.shadowColor="#ff3b00";ctx.shadowBlur=18;
        ctx.fillStyle="#5e180e";ctx.beginPath();ctx.ellipse(0,0,25,10,.1,0,Math.PI*2);ctx.fill();
        ctx.fillStyle="#f04412";ctx.beginPath();ctx.ellipse(0,0,20,7,.1,0,Math.PI*2);ctx.fill();
        ctx.fillStyle="#ffbd3d";ctx.beginPath();ctx.ellipse(-2,-1,10,3,.1,0,Math.PI*2);ctx.fill();
        ctx.restore();
      }else if(kind===3){
        const flame=5+Math.sin(vt*5+i)*3;
        ctx.strokeStyle="#ff6b24";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,y+9);ctx.quadraticCurveTo(x-8,y-flame,x,y-18-flame);ctx.quadraticCurveTo(x+8,y-flame,x,y+9);ctx.stroke();
        ctx.fillStyle="#ffc14a";ctx.beginPath();ctx.arc(x,y+5,3,0,Math.PI*2);ctx.fill();
      }else if(kind===4){
        ctx.fillStyle="#2b1b18";ctx.strokeStyle="#4c2a23";ctx.lineWidth=2;
        ctx.beginPath();ctx.roundRect(x-15,y-8,30,16,4);ctx.fill();ctx.stroke();
        ctx.strokeStyle="#ff4d18";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x-12,y+2);ctx.lineTo(x-5,y-4);ctx.lineTo(x,y+2);ctx.lineTo(x+7,y-5);ctx.lineTo(x+13,y+1);ctx.stroke();
      }else{
        ctx.font="15px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=.65;ctx.fillText(i%12===5?"💀":"🪨",x,y);ctx.globalAlpha=1;
      }
    }

    // Animated ash/smoke plumes.
    for(let i=0;i<8;i++){
      const x=60+decorRand(2100+i)*720,y=110+decorRand(2120+i)*760;if(!decorSafe(x,y))continue;
      for(let j=0;j<3;j++){
        const rise=((vt*18+i*23+j*17)%42),r=7+j*4;
        ctx.globalAlpha=.14*(1-j*.2);ctx.fillStyle="#b7a6a0";ctx.beginPath();ctx.arc(x+(j-1)*5,y-rise,r,0,Math.PI*2);ctx.fill();
      }
    }

    // Floating embers bring the whole map to life without external images.
    ctx.globalAlpha=.8;
    for(let i=0;i<44;i++){
      const x=(i*97+currentMap*53)%W,y=(i*149+currentMap*37-(vt*13*(1+i%3)))%H;
      const yy=y<0?y+H:y;if(!decorSafe(x,yy))continue;
      ctx.fillStyle=i%3?"#ff7a2c":"#ffd25a";ctx.beginPath();ctx.arc(x,yy,1.2+(i%3)*.65,0,Math.PI*2);ctx.fill();
    }
    ctx.globalAlpha=1;ctx.restore();
  }'''
if old not in s:
    raise SystemExit('volcanic scenery anchor missing')
s=s.replace(old,new,1)
oldroad='''  }else if(currentSeries===5){
    ctx.globalAlpha=.72;ctx.strokeStyle="#d93a12";ctx.lineWidth=50;ctx.stroke();
    ctx.globalAlpha=.95;ctx.strokeStyle="#ff9a2f";ctx.lineWidth=24;ctx.stroke();
    ctx.globalAlpha=.8;ctx.strokeStyle="#ffd35a";ctx.lineWidth=7;ctx.setLineDash([18,12]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }'''
newroad='''  }else if(currentSeries===5){
    // Cooled basalt path with glowing magma fissures instead of a bright orange neon road.
    ctx.globalAlpha=.96;ctx.strokeStyle="#30201d";ctx.lineWidth=58;ctx.stroke();
    ctx.globalAlpha=.9;ctx.strokeStyle="#1b1514";ctx.lineWidth=42;ctx.stroke();
    ctx.globalAlpha=.82;ctx.strokeStyle="#ff4b18";ctx.lineWidth=7;ctx.setLineDash([7,24,3,31]);ctx.stroke();ctx.setLineDash([]);
    ctx.globalAlpha=.55;ctx.strokeStyle="#ffb13b";ctx.lineWidth=3;ctx.setLineDash([4,29,2,19]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }'''
if oldroad not in s:
    raise SystemExit('volcanic road detail anchor missing')
s=s.replace(oldroad,newroad,1)
s=s.replace('currentSeries===4?"#bdefff":"#ff6a1f";ctx.lineWidth=72;ctx.stroke();','currentSeries===4?"#bdefff":"#3b2521";ctx.lineWidth=72;ctx.stroke();',1)
# Make the route segment under the base match the cooled basalt road too.
s=s.replace('currentSeries===4?"#bdefff":"#ff6a1f";\n    ctx.lineWidth=72;ctx.lineCap="round";','currentSeries===4?"#bdefff":"#3b2521";\n    ctx.lineWidth=72;ctx.lineCap="round";',1)
p.write_text(s,encoding='utf-8')
print('Volcanic Wasteland visuals V2 installed')
