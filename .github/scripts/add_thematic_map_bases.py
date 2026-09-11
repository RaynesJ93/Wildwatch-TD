from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='THEMATIC_MAP_BASES_V1'
if marker in s:
    print('Thematic map bases already installed')
    raise SystemExit(0)
start=s.index('  // Base building at the end of every map so the road finishes at a clear objective.')
end=s.index('  // Frog acid puddles.', start)
new=r'''  // THEMATIC_MAP_BASES_V1: region-specific in-game base assets drawn directly on the canvas.
  // These are vector/canvas assets, not external images, so they stay sharp on iPhone.
  if(path.length>1){
    const end=path[path.length-1],prev=path[path.length-2],dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1;
    const ux=dx/len,uy=dy/len;
    const margin=82;
    let bx=end[0]-ux*78,by=end[1]-uy*78;
    bx=Math.max(margin,Math.min(W-margin,bx));
    by=Math.max(margin,Math.min(H-margin,by));

    // Finish the route beneath the themed entrance.
    ctx.save();
    ctx.strokeStyle=currentSeries===1?"#d8b35b":currentSeries===2?"#f0d18a":"#57405f";
    ctx.lineWidth=72;ctx.lineCap="round";
    ctx.beginPath();ctx.moveTo(prev[0],prev[1]);ctx.lineTo(bx,by);ctx.stroke();
    ctx.restore();

    ctx.save();ctx.translate(bx,by);
    ctx.shadowColor="rgba(0,0,0,.62)";ctx.shadowBlur=18;ctx.shadowOffsetY=9;

    if(currentSeries===1){
      // Forest Pines: fortified ranger lodge built from timber and mossy stone.
      ctx.fillStyle="#3a2a1d";ctx.strokeStyle="#17120d";ctx.lineWidth=5;
      ctx.beginPath();ctx.roundRect(-48,-34,96,66,8);ctx.fill();ctx.stroke();
      ctx.shadowColor="transparent";
      // Timber beams.
      ctx.fillStyle="#6b4a2a";
      ctx.fillRect(-42,-28,10,55);ctx.fillRect(32,-28,10,55);ctx.fillRect(-7,-31,14,61);
      ctx.fillRect(-44,-6,88,8);
      // Roof with layered shingles.
      ctx.fillStyle="#263c25";ctx.strokeStyle="#142016";ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(-58,-31);ctx.lineTo(0,-69);ctx.lineTo(58,-31);ctx.lineTo(43,-22);ctx.lineTo(0,-51);ctx.lineTo(-43,-22);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.strokeStyle="#4f6842";ctx.lineWidth=3;
      for(let y=-44;y>=-58;y-=7){ctx.beginPath();ctx.moveTo(-34+(y+58)*1.5,y);ctx.lineTo(34-(y+58)*1.5,y);ctx.stroke();}
      // Stone footings and moss.
      ctx.fillStyle="#626456";ctx.strokeStyle="#2e332b";ctx.lineWidth=3;
      for(let i=0;i<6;i++){const x=-45+i*18;ctx.beginPath();ctx.roundRect(x,22,17,15,3);ctx.fill();ctx.stroke();}
      ctx.fillStyle="#4d7b3a";ctx.beginPath();ctx.ellipse(-27,-31,18,6,-.2,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(25,-29,15,5,.15,0,Math.PI*2);ctx.fill();
      // Door and warm windows.
      ctx.fillStyle="#1a120d";ctx.strokeStyle="#8c6335";ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(-12,2,24,31,5);ctx.fill();ctx.stroke();
      ctx.fillStyle="#f2c45d";ctx.shadowColor="#ffc84c";ctx.shadowBlur=9;
      ctx.fillRect(-31,-15,13,13);ctx.fillRect(18,-15,13,13);
      ctx.shadowColor="transparent";
      ctx.font="16px serif";ctx.textAlign="center";ctx.fillText("🌲",0,-8);
    }else if(currentSeries===2){
      // Desert Dunes: sandstone outpost / desert fortress.
      ctx.fillStyle="#a7773d";ctx.strokeStyle="#55391f";ctx.lineWidth=5;
      ctx.beginPath();ctx.roundRect(-49,-31,98,65,5);ctx.fill();ctx.stroke();
      ctx.shadowColor="transparent";
      // Corner towers.
      ctx.fillStyle="#bd8b4a";
      ctx.fillRect(-56,-39,22,70);ctx.fillRect(34,-39,22,70);
      ctx.strokeRect(-56,-39,22,70);ctx.strokeRect(34,-39,22,70);
      // Battlements.
      ctx.fillStyle="#c99a58";
      [-54,-37,-10,8,35,52].forEach(x=>ctx.fillRect(x,-48,12,13));
      // Brick texture.
      ctx.strokeStyle="rgba(90,55,25,.45)";ctx.lineWidth=2;
      for(let y=-23;y<26;y+=14){ctx.beginPath();ctx.moveTo(-46,y);ctx.lineTo(46,y);ctx.stroke();}
      for(let y=-23;y<26;y+=28){for(let x=-30;x<=30;x+=30){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+14);ctx.stroke();}}
      for(let y=-9;y<26;y+=28){for(let x=-45;x<=45;x+=30){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+14);ctx.stroke();}}
      // Arched gateway.
      ctx.fillStyle="#2b1b12";ctx.beginPath();ctx.moveTo(-14,34);ctx.lineTo(-14,8);ctx.arc(0,8,14,Math.PI,0);ctx.lineTo(14,34);ctx.closePath();ctx.fill();
      ctx.fillStyle="#f5d77c";ctx.shadowColor="#ffd96a";ctx.shadowBlur=9;ctx.fillRect(-31,-12,10,12);ctx.fillRect(21,-12,10,12);ctx.shadowColor="transparent";
      ctx.fillStyle="#795428";ctx.beginPath();ctx.ellipse(0,37,58,9,0,0,Math.PI*2);ctx.fill();
      ctx.font="17px serif";ctx.textAlign="center";ctx.fillText("☀️",0,-12);
    }else{
      // Haunted Woods: ruined gothic crypt with cracked stone, iron gate and ghostly light.
      ctx.fillStyle="#29232f";ctx.strokeStyle="#0c0910";ctx.lineWidth=5;
      ctx.beginPath();ctx.roundRect(-50,-27,100,61,5);ctx.fill();ctx.stroke();
      ctx.shadowColor="transparent";
      // Tall gothic side pillars.
      ctx.fillStyle="#393143";ctx.strokeStyle="#17121d";ctx.lineWidth=4;
      ctx.fillRect(-57,-42,20,72);ctx.strokeRect(-57,-42,20,72);
      ctx.fillRect(37,-42,20,72);ctx.strokeRect(37,-42,20,72);
      ctx.beginPath();ctx.moveTo(-60,-42);ctx.lineTo(-47,-63);ctx.lineTo(-34,-42);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.beginPath();ctx.moveTo(34,-42);ctx.lineTo(47,-63);ctx.lineTo(60,-42);ctx.closePath();ctx.fill();ctx.stroke();
      // Broken slate roof.
      ctx.fillStyle="#1b1522";ctx.beginPath();ctx.moveTo(-43,-27);ctx.lineTo(0,-65);ctx.lineTo(45,-27);ctx.lineTo(25,-31);ctx.lineTo(10,-45);ctx.lineTo(-2,-38);ctx.lineTo(-18,-49);ctx.closePath();ctx.fill();ctx.stroke();
      // Cracks in the masonry.
      ctx.strokeStyle="#55485f";ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(-26,-16);ctx.lineTo(-17,-5);ctx.lineTo(-23,5);ctx.lineTo(-14,13);ctx.stroke();
      ctx.beginPath();ctx.moveTo(25,-18);ctx.lineTo(17,-7);ctx.lineTo(23,1);ctx.lineTo(13,10);ctx.stroke();
      // Gothic arched doorway and iron bars.
      ctx.fillStyle="#08060b";ctx.beginPath();ctx.moveTo(-17,33);ctx.lineTo(-17,5);ctx.arc(0,5,17,Math.PI,0);ctx.lineTo(17,33);ctx.closePath();ctx.fill();
      ctx.strokeStyle="#5f536b";ctx.lineWidth=3;[-10,-3,4,11].forEach(x=>{ctx.beginPath();ctx.moveTo(x,8);ctx.lineTo(x,32);ctx.stroke();});
      ctx.beginPath();ctx.moveTo(-15,20);ctx.lineTo(15,20);ctx.stroke();
      // Sickly green/purple supernatural window glow.
      ctx.fillStyle="#baff87";ctx.shadowColor="#91ff65";ctx.shadowBlur=13;ctx.beginPath();ctx.arc(-29,-9,6,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(29,-9,6,0,Math.PI*2);ctx.fill();
      ctx.fillStyle="#b980ff";ctx.shadowColor="#b980ff";ctx.shadowBlur=15;ctx.beginPath();ctx.ellipse(0,-22,8,13,0,0,Math.PI*2);ctx.fill();ctx.shadowColor="transparent";
      // Ground stones and skull detail.
      ctx.fillStyle="#4a4350";for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(-36+i*18,35+(i%2)*3,13,6,0,0,Math.PI*2);ctx.fill();}
      ctx.font="17px serif";ctx.textAlign="center";ctx.fillText("💀",0,8);
    }

    // Shared sign plate, kept compact so the structure remains the focus.
    ctx.shadowColor="transparent";ctx.fillStyle="rgba(8,8,10,.78)";ctx.strokeStyle="rgba(255,255,255,.22)";ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(-27,42,54,21,6);ctx.fill();ctx.stroke();
    ctx.font="bold 12px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillStyle="#fff";ctx.fillText("BASE",0,53);
    ctx.restore();
  }

'''
s=s[:start]+new+s[end:]
p.write_text(s)
print('Installed realistic region-specific Forest, Desert and Haunted base assets')
