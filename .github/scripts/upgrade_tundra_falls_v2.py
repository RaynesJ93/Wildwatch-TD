from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'TUNDRA_FALLS_V2' in s:
    print('Tundra Falls V2 already installed')
    raise SystemExit(0)

# 1) Replace the mirrored Haunted Woods-derived layouts with 10 genuinely different icy routes.
new_maps=r'''// TUNDRA_FALLS_V2: ten unique icy routes, each with its own bends and placement pads.
const tundraFallsMaps=[
  {path:[[-45,120],[180,120],[180,300],[520,300],[520,150],[760,150],[760,500],[340,500],[340,760],[650,760],[650,1045]],pads:[[80,220],[335,205],[635,235],[95,420],[505,405],[805,335],[175,625],[505,650],[785,645],[210,855],[510,900]]},
  {path:[[905,130],[700,130],[700,330],[430,330],[430,170],[150,170],[150,520],[610,520],[610,760],[280,760],[280,1045]],pads:[[795,245],[555,215],[275,285],[80,335],[285,455],[770,455],[455,635],[770,650],[135,680],[455,875],[120,930]]},
  {path:[[-45,160],[250,160],[250,410],[640,410],[640,210],[790,210],[790,620],[430,620],[430,860],[700,860],[700,1045]],pads:[[85,275],[395,270],[565,160],[720,365],[110,480],[330,520],[600,555],[250,710],[610,735],[810,790],[520,970]]},
  {path:[[905,110],[620,110],[620,280],[260,280],[260,500],[700,500],[700,710],[170,710],[170,900],[500,900],[500,1045]],pads:[[760,215],[470,195],[115,205],[410,395],[810,410],[510,600],[95,600],[360,810],[690,820],[290,975]]},
  {path:[[-45,120],[150,120],[150,250],[720,250],[720,430],[310,430],[310,620],[610,620],[610,820],[220,820],[220,1045]],pads:[[75,330],[285,170],[485,170],[815,330],[500,350],[120,515],[455,535],[765,555],[455,725],[90,760],[405,930],[720,930]]},
  {path:[[905,150],[730,150],[730,360],[480,360],[480,160],[180,160],[180,560],[560,560],[560,740],[790,740],[790,920],[470,920],[470,1045]],pads:[[810,270],[600,245],[330,275],[80,335],[330,475],[700,485],[410,655],[680,650],[165,700],[390,825],[655,835],[285,965]]},
  {path:[[-45,130],[300,130],[300,300],[700,300],[700,520],[420,520],[420,700],[150,700],[150,880],[620,880],[620,1045]],pads:[[115,250],[475,205],[805,205],[555,410],[155,430],[285,585],[590,625],[790,650],[300,800],[790,815],[430,970]]},
  {path:[[905,130],[650,130],[650,260],[220,260],[220,440],[520,440],[520,610],[760,610],[760,800],[360,800],[360,1045]],pads:[[780,235],[480,185],[80,180],[365,350],[690,375],[120,560],[370,560],[640,705],[820,700],[180,710],[555,910]]},
  {path:[[-45,140],[200,140],[200,360],[500,360],[500,180],[780,180],[780,560],[300,560],[300,760],[680,760],[680,940],[460,940],[460,1045]],pads:[[80,260],[350,230],[630,310],[820,350],[95,455],[420,470],[650,650],[145,670],[480,845],[810,850],[290,975]]},
  {path:[[905,100],[720,100],[720,260],[380,260],[380,430],[150,430],[150,650],[580,650],[580,830],[790,830],[790,980],[560,980],[560,1045]],pads:[[805,200],[555,175],[220,185],[520,350],[80,330],[270,545],[720,535],[410,745],[690,725],[230,830],[425,925]]}
];
'''
pat=r'// TUNDRA_FALLS_V1:.*?const tundraFallsMaps=.*?\n\}\));\n'
ns,n=re.subn(pat,new_maps,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('Could not replace Tundra Falls map definition')

# 2) Add high-detail frozen scenery. Everything is deterministic per map and kept off the enemy road.
helper=r'''
// TUNDRA_FALLS_V2 scenery: ice fishing holes, frozen props, snowbanks and crystals instead of trees.
function drawTundraScenery(){
  if(currentSeries!==4)return;
  const cfg=[
    {holes:[[92,355],[600,410],[170,690],[520,910]],igloo:[780,690],sled:[115,900],snowman:[740,580]},
    {holes:[[805,270],[335,430],[755,650],[130,845]],igloo:[95,650],sled:[540,900],snowman:[300,585]},
    {holes:[[105,520],[455,260],[660,700],[190,895]],igloo:[760,790],sled:[105,770],snowman:[590,525]},
    {holes:[[735,375],[110,350],[520,610],[760,875]],igloo:[95,805],sled:[400,830],snowman:[710,580]},
    {holes:[[95,390],[450,350],[785,560],[410,890]],igloo:[760,720],sled:[90,770],snowman:[520,535]},
    {holes:[[790,290],[95,430],[690,525],[275,810]],igloo:[115,690],sled:[630,870],snowman:[370,650]},
    {holes:[[110,380],[545,410],[765,650],[310,930]],igloo:[775,780],sled:[95,790],snowman:[500,610]},
    {holes:[[790,330],[110,540],[620,720],[185,900]],igloo:[795,900],sled:[370,365],snowman:[470,540]},
    {holes:[[90,430],[610,310],[165,670],[520,860]],igloo:[790,710],sled:[315,470],snowman:[690,640]},
    {holes:[[790,340],[95,550],[665,565],[275,915]],igloo:[110,810],sled:[465,770],snowman:[690,700]}
  ][currentMap-1];
  const segDist=(px,py,a,b)=>{const vx=b[0]-a[0],vy=b[1]-a[1],wx=px-a[0],wy=py-a[1],c1=vx*wx+vy*wy,c2=vx*vx+vy*vy,t=c2?Math.max(0,Math.min(1,c1/c2)):0;return Math.hypot(px-(a[0]+vx*t),py-(a[1]+vy*t));};
  const clear=(x,y,r=72)=>{for(let i=1;i<path.length;i++)if(segDist(x,y,path[i-1],path[i])<r)return false;return true;};
  ctx.save();
  // Fine frozen-lake cracks and wind streaks over the snow field.
  ctx.globalAlpha=.18;ctx.strokeStyle='#5ab4dc';ctx.lineWidth=2;
  for(let i=0;i<20;i++){const x=35+((i*137+currentMap*71)%780),y=70+((i*193+currentMap*43)%900);if(!clear(x,y,60))continue;ctx.beginPath();ctx.moveTo(x-18,y);ctx.lineTo(x,y-8);ctx.lineTo(x+13,y+3);ctx.lineTo(x+27,y-5);ctx.stroke();}
  ctx.globalAlpha=1;
  // Ice fishing holes with dark water, frosted rims, rods and occasional fish/crates.
  cfg.holes.forEach((h,idx)=>{const [x,y]=h;if(!clear(x,y,78))return;
    ctx.fillStyle='#dff8ff';ctx.strokeStyle='#85cbe8';ctx.lineWidth=4;ctx.beginPath();ctx.ellipse(x,y,31,20,0,0,Math.PI*2);ctx.fill();ctx.stroke();
    ctx.fillStyle='#0c5b83';ctx.strokeStyle='#073d5c';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(x,y+1,21,13,0,0,Math.PI*2);ctx.fill();ctx.stroke();
    ctx.strokeStyle='#8a5b2d';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x+22,y-29);ctx.lineTo(x+7,y-4);ctx.stroke();ctx.strokeStyle='#d8f6ff';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(x+7,y-4);ctx.lineTo(x+3,y+8);ctx.stroke();
    if(idx%2===0){ctx.fillStyle='#a77036';ctx.strokeStyle='#60401f';ctx.lineWidth=2;ctx.fillRect(x-43,y+13,18,15);ctx.strokeRect(x-43,y+13,18,15);}
    if(idx===cfg.holes.length-1){ctx.font='17px serif';ctx.textAlign='center';ctx.fillText('🐟',x-4,y+6);}
  });
  // Igloo.
  if(clear(cfg.igloo[0],cfg.igloo[1],86)){const [x,y]=cfg.igloo;ctx.fillStyle='#eafaff';ctx.strokeStyle='#91cfe5';ctx.lineWidth=3;ctx.beginPath();ctx.arc(x,y,38,Math.PI,0);ctx.lineTo(x+38,y+20);ctx.lineTo(x-38,y+20);ctx.closePath();ctx.fill();ctx.stroke();ctx.strokeStyle='#b5deed';ctx.lineWidth=2;for(let yy=y-25;yy<=y+10;yy+=12){ctx.beginPath();ctx.moveTo(x-32,yy);ctx.lineTo(x+32,yy);ctx.stroke();}ctx.fillStyle='#2d6d8a';ctx.beginPath();ctx.roundRect(x-12,y-4,24,25,10);ctx.fill();}
  // Sled.
  if(clear(cfg.sled[0],cfg.sled[1],72)){const [x,y]=cfg.sled;ctx.strokeStyle='#6b4728';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x-24,y);ctx.lineTo(x+20,y);ctx.moveTo(x-17,y-11);ctx.lineTo(x+15,y-11);ctx.stroke();ctx.strokeStyle='#b7dfea';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x-28,y+8);ctx.quadraticCurveTo(x,y+17,x+30,y+5);ctx.stroke();}
  // Snowman.
  if(clear(cfg.snowman[0],cfg.snowman[1],70)){const [x,y]=cfg.snowman;ctx.fillStyle='#fff';ctx.strokeStyle='#c8e7f1';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y+12,20,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.beginPath();ctx.arc(x,y-13,14,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle='#1e3440';ctx.beginPath();ctx.arc(x-5,y-16,2,0,Math.PI*2);ctx.arc(x+5,y-16,2,0,Math.PI*2);ctx.fill();ctx.fillStyle='#ef8d2c';ctx.beginPath();ctx.moveTo(x+2,y-10);ctx.lineTo(x+17,y-7);ctx.lineTo(x+2,y-5);ctx.closePath();ctx.fill();ctx.fillStyle='#28333a';ctx.fillRect(x-14,y-32,28,7);ctx.fillRect(x-9,y-45,18,15);}
  // Blue ice crystal clusters in safe open snow.
  for(let i=0;i<13;i++){const x=55+((i*149+currentMap*67)%750),y=85+((i*211+currentMap*89)%875);if(!clear(x,y,68))continue;ctx.fillStyle=i%2?'#62c8ed':'#8ce1f7';ctx.strokeStyle='#d4f8ff';ctx.lineWidth=1.5;for(let j=0;j<3;j++){const ox=(j-1)*10,h=18+j*8;ctx.beginPath();ctx.moveTo(x+ox,y-h);ctx.lineTo(x+ox+7,y);ctx.lineTo(x+ox-7,y);ctx.closePath();ctx.fill();ctx.stroke();}}
  // Footprints crossing some clear snow pockets.
  ctx.fillStyle='rgba(76,143,172,.28)';for(let i=0;i<16;i++){const x=40+((i*53+currentMap*37)%760),y=120+((i*71+currentMap*41)%780);if(!clear(x,y,55))continue;ctx.beginPath();ctx.ellipse(x,y,4,7,(i%2?-.25:.25),0,Math.PI*2);ctx.fill();}
  ctx.restore();
}
'''
if 'function draw(){' not in s:
    raise SystemExit('draw() anchor missing')
s=s.replace('function draw(){',helper+'\nfunction draw(){',1)

# Call the richer tundra scenery immediately before the road is painted, so towers/enemies remain on top.
road_anchor='  // Road outline and road surface use the exact enemy path.'
if road_anchor not in s:
    raise SystemExit('road anchor missing')
s=s.replace(road_anchor,"  if(currentSeries===4)drawTundraScenery();\n\n"+road_anchor,1)

# 3) Make the enemy road itself frozen instead of inheriting the Haunted Woods purple road.
repls={
'ctx.strokeStyle=currentSeries===1?"#8b612d":currentSeries===2?"#9b6b38":"#160d20";ctx.lineWidth=92;ctx.stroke();':'ctx.strokeStyle=currentSeries===1?"#8b612d":currentSeries===2?"#9b6b38":currentSeries===3?"#160d20":"#4b9fc6";ctx.lineWidth=92;ctx.stroke();',
'ctx.strokeStyle=currentSeries===1?"#a7834f":currentSeries===2?"#f0d18a":"#57405f";ctx.lineWidth=72;ctx.stroke();':'ctx.strokeStyle=currentSeries===1?"#a7834f":currentSeries===2?"#f0d18a":currentSeries===3?"#57405f":"#bdefff";ctx.lineWidth=72;ctx.stroke();',
'ctx.strokeStyle=currentSeries===1?"#d8b35b":currentSeries===2?"#f0d18a":"#57405f";':'ctx.strokeStyle=currentSeries===1?"#d8b35b":currentSeries===2?"#f0d18a":currentSeries===3?"#57405f":"#bdefff";'
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit('road/base route style anchor missing: '+old[:65])
    s=s.replace(old,new,1)

old_haunted_road='''  }else if(currentSeries===3){
    ctx.globalAlpha=.35;ctx.strokeStyle="#2a1b31";ctx.lineWidth=46;ctx.stroke();
    ctx.globalAlpha=.18;ctx.strokeStyle="#a68caf";ctx.lineWidth=3;ctx.setLineDash([10,24]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }
'''
new_haunted_road='''  }else if(currentSeries===3){
    ctx.globalAlpha=.35;ctx.strokeStyle="#2a1b31";ctx.lineWidth=46;ctx.stroke();
    ctx.globalAlpha=.18;ctx.strokeStyle="#a68caf";ctx.lineWidth=3;ctx.setLineDash([10,24]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }else if(currentSeries===4){
    // Glassy packed-ice centre, bright frost edge and irregular frozen cracks.
    ctx.globalAlpha=.34;ctx.strokeStyle="#75c9e8";ctx.lineWidth=50;ctx.stroke();
    ctx.globalAlpha=.55;ctx.strokeStyle="#effcff";ctx.lineWidth=4;ctx.setLineDash([22,15]);ctx.stroke();ctx.setLineDash([]);
    ctx.globalAlpha=.34;ctx.strokeStyle="#4ea8cf";ctx.lineWidth=2;ctx.setLineDash([5,18,2,26]);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;
  }
'''
if old_haunted_road not in s:
    raise SystemExit('Haunted road detail block missing')
s=s.replace(old_haunted_road,new_haunted_road,1)

# 4) Stop Tundra Falls inheriting the Haunted Woods crypt and give it a unique ice fortress base.
old_else='''    }else{
      // Haunted Woods: ruined gothic crypt with cracked stone, iron gate and ghostly light.'''
new_else='''    }else if(currentSeries===3){
      // Haunted Woods: ruined gothic crypt with cracked stone, iron gate and ghostly light.'''
if old_else not in s:
    raise SystemExit('Haunted base else anchor missing')
s=s.replace(old_else,new_else,1)

old_tail='''      ctx.fillStyle="#4a4350";for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(-36+i*18,35+(i%2)*3,13,6,0,0,Math.PI*2);ctx.fill();}
      ctx.font="17px serif";ctx.textAlign="center";ctx.fillText("💀",0,8);
    }

    // Shared sign plate, kept compact so the structure remains the focus.'''
new_tail='''      ctx.fillStyle="#4a4350";for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(-36+i*18,35+(i%2)*3,13,6,0,0,Math.PI*2);ctx.fill();}
      ctx.font="17px serif";ctx.textAlign="center";ctx.fillText("💀",0,8);
    }else{
      // Tundra Falls: frozen citadel grown from ice, snow and glowing blue crystals.
      ctx.fillStyle="#9bdcf2";ctx.strokeStyle="#286c91";ctx.lineWidth=5;
      ctx.beginPath();ctx.roundRect(-49,-29,98,63,8);ctx.fill();ctx.stroke();
      ctx.shadowColor="transparent";
      // Ice side towers with sharp frozen caps.
      ctx.fillStyle="#77c7e8";ctx.strokeStyle="#245b78";ctx.lineWidth=4;
      ctx.fillRect(-57,-44,21,75);ctx.strokeRect(-57,-44,21,75);ctx.fillRect(36,-44,21,75);ctx.strokeRect(36,-44,21,75);
      ctx.beginPath();ctx.moveTo(-61,-44);ctx.lineTo(-47,-70);ctx.lineTo(-32,-44);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.beginPath();ctx.moveTo(32,-44);ctx.lineTo(47,-70);ctx.lineTo(61,-44);ctx.closePath();ctx.fill();ctx.stroke();
      // Layered snow roof.
      ctx.fillStyle="#eafaff";ctx.strokeStyle="#70b8d6";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-45,-28);ctx.lineTo(0,-62);ctx.lineTo(45,-28);ctx.lineTo(29,-22);ctx.lineTo(0,-46);ctx.lineTo(-30,-22);ctx.closePath();ctx.fill();ctx.stroke();
      // Dark frozen gateway with cyan glow.
      ctx.fillStyle="#143a53";ctx.beginPath();ctx.moveTo(-16,34);ctx.lineTo(-16,7);ctx.arc(0,7,16,Math.PI,0);ctx.lineTo(16,34);ctx.closePath();ctx.fill();
      ctx.fillStyle="#76e7ff";ctx.shadowColor="#55dcff";ctx.shadowBlur=15;ctx.beginPath();ctx.arc(-28,-8,6,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(28,-8,6,0,Math.PI*2);ctx.fill();
      // Central magic ice crystal.
      ctx.beginPath();ctx.moveTo(0,-31);ctx.lineTo(9,-10);ctx.lineTo(0,2);ctx.lineTo(-9,-10);ctx.closePath();ctx.fill();ctx.shadowColor="transparent";
      // Icicles and snow drift at the foot of the base.
      ctx.fillStyle="#dff8ff";for(let i=0;i<7;i++){const x=-42+i*14,h=8+(i%3)*5;ctx.beginPath();ctx.moveTo(x,-27);ctx.lineTo(x+6,-27);ctx.lineTo(x+3,-27+h);ctx.closePath();ctx.fill();}
      ctx.beginPath();ctx.ellipse(0,36,57,10,0,0,Math.PI*2);ctx.fill();
      ctx.font="17px serif";ctx.textAlign="center";ctx.fillText("❄️",0,13);
    }

    // Shared sign plate, kept compact so the structure remains the focus.'''
if old_tail not in s:
    raise SystemExit('Haunted base tail anchor missing')
s=s.replace(old_tail,new_tail,1)

p.write_text(s,encoding='utf-8')
print('Installed Tundra Falls V2: 10 unique roads, icy road art, fishing-hole scenery, and frozen citadel base')
