from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='RECENT_ATTACK_VISIBILITY_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)

helper=r'''
// RECENT_ATTACK_VISIBILITY_V1: stronger halos/trails so newer attacks stay readable on iPhone-sized battlefields.
function drawRecentAttackVisibility(s){
  const types=new Set(["hedgehogQuill","hedgehogStormBurst","gooseHonk","gooseRageBurst","crowFeather","crowBlackoutBurst","snailAcid","snailToxicBurst","dungBall","dungAvalancheBanner","chirpWave","deafeningChirp","wormMud","wormStampede","wormStampedeBanner","dogBark","dogBone","fetchBanner","badgerClaw","badgerMaul","savageMaulBanner","otterPebble","riverRush","slothStick","treeTopple","koalaBranch","koalaFuryBanner","woolBall","woolTrapBanner"]);
  if(!types.has(s.type))return;
  const q=1-Math.max(0,s.life)/(s.maxLife||.4),x=(s.tx==null?s.x:s.x+(s.tx-s.x)*Math.min(1,q)),y=(s.ty==null?s.y:s.y+(s.ty-s.y)*Math.min(1,q));
  ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=.72;
  let col="#fff7a8",r=13;
  if(["crowFeather","crowBlackoutBurst"].includes(s.type)){col="#c69cff";r=18;}
  else if(["snailAcid","snailToxicBurst"].includes(s.type)){col="#b8ff4d";r=18;}
  else if(["riverRush","otterPebble"].includes(s.type)){col="#70d9ff";r=18;}
  else if(["chirpWave","deafeningChirp"].includes(s.type)){col="#9dff76";r=19;}
  else if(["treeTopple","slothStick","koalaBranch","koalaFuryBanner"].includes(s.type)){col="#c9ff7b";r=17;}
  else if(["woolBall","woolTrapBanner"].includes(s.type)){col="#ffffff";r=18;}
  else if(["dogBark","dogBone","fetchBanner"].includes(s.type)){col="#ffe58d";r=16;}
  else if(["badgerClaw","badgerMaul","savageMaulBanner"].includes(s.type)){col="#ff8f72";r=17;}
  else if(["dungBall","dungAvalancheBanner","wormMud","wormStampede","wormStampedeBanner"].includes(s.type)){col="#d7a56a";r=17;}
  else if(["gooseHonk","gooseRageBurst"].includes(s.type)){col="#fff39a";r=19;}
  else if(["hedgehogQuill","hedgehogStormBurst"].includes(s.type)){col="#ffd89a";r=16;}
  ctx.shadowColor=col;ctx.shadowBlur=18;ctx.strokeStyle=col;ctx.lineWidth=5;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.stroke();
  if(s.tx!=null&&s.ty!=null&&Math.hypot(s.tx-s.x,s.ty-s.y)>8){ctx.globalAlpha=.38;ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(x,y);ctx.stroke();}
  ctx.restore();
}
'''
anchor='function draw(){'
if anchor not in s: raise RuntimeError('draw() anchor not found')
s=s.replace(anchor,helper+'\n'+anchor,1)

loop='battle.shots?.forEach(s=>{'
if loop not in s: raise RuntimeError('shot draw loop anchor not found')
s=s.replace(loop,loop+'\n    drawRecentAttackVisibility(s);',1)

# Make persistent zones more obvious too.
s=s.replace('ctx.globalAlpha=Math.min(.58,c.life*.3);ctx.fillStyle="#130f19";ctx.shadowColor="#4e326a";ctx.shadowBlur=18;', 'ctx.globalAlpha=Math.min(.78,c.life*.38);ctx.fillStyle="#130f19";ctx.shadowColor="#8a55c7";ctx.shadowBlur=30;',1)
s=s.replace('ctx.globalAlpha=Math.min(.62,c.life*.25);ctx.fillStyle="#6fbd24";ctx.shadowColor="#8dff35";ctx.shadowBlur=14;', 'ctx.globalAlpha=Math.min(.80,c.life*.34);ctx.fillStyle="#6fbd24";ctx.shadowColor="#b4ff4d";ctx.shadowBlur=28;',1)
# Wool trap zone if present.
s=s.replace('ctx.globalAlpha=Math.min(.75,z.life);ctx.fillStyle="#f5f5f2";ctx.strokeStyle="#d5dde0";ctx.lineWidth=3;', 'ctx.globalAlpha=Math.min(.88,z.life);ctx.fillStyle="#f5f5f2";ctx.strokeStyle="#ffffff";ctx.shadowColor="#ffffff";ctx.shadowBlur=20;ctx.lineWidth=5;',1)

p.write_text(s,encoding='utf-8')
print('Boosted visibility for recent attacks')
