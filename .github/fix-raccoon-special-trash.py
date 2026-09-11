from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''  if(t.key==="raccoon"){
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.48,maxLife:.48,type:"raccoonBin"});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    if(cardLevel(t.key)>=10){
      battle.trashZones=battle.trashZones||[];
      battle.trashZones.push({x:target.x,y:target.y,life:4,maxLife:4,radius:78});
    }
    t.cd=cardRate(t.key);
    return;
  }'''
new='''  if(t.key==="raccoon"){
    const raccoonSpecial=cardLevel(t.key)>=10;
    battle.shots.push({x:t.x,y:t.y-8,tx:target.x,ty:target.y,life:.48,maxLife:.48,type:"raccoonBin",special:raccoonSpecial});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }'''
if old not in s: raise SystemExit('raccoon attack marker not found')
s=s.replace(old,new,1)
old2='''  battle.shots.forEach(s=>{
    if(s.type==="hedgehogNeedles" && !s.landed && s.life-dt<=0){'''
new2='''  battle.shots.forEach(s=>{
    if(s.type==="raccoonBin" && s.special && !s.spilled && s.life-dt<=0){
      s.spilled=true;
      battle.trashZones=battle.trashZones||[];
      battle.trashZones.push({x:s.tx,y:s.ty,life:4,maxLife:4,radius:90});
    }
    if(s.type==="hedgehogNeedles" && !s.landed && s.life-dt<=0){'''
if old2 not in s: raise SystemExit('shot landing marker not found')
s=s.replace(old2,new2,1)
old3='''  (battle.trashZones||[]).forEach(z=>{
    const a=Math.max(.25,Math.min(1,z.life/z.maxLife));
    ctx.save();ctx.globalAlpha=a;
    ctx.fillStyle="rgba(90,70,45,.55)";
    ctx.beginPath();ctx.ellipse(z.x,z.y+4,44,22,0,0,Math.PI*2);ctx.fill();
    ctx.font="24px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("🗑️",z.x-18,z.y);
    ctx.fillText("🧻",z.x+10,z.y+4);
    ctx.fillText("🥫",z.x+25,z.y-4);
    ctx.restore();
  });'''
new3='''  (battle.trashZones||[]).forEach(z=>{
    const a=Math.max(.3,Math.min(1,z.life/z.maxLife));
    ctx.save();ctx.globalAlpha=a;
    ctx.fillStyle="rgba(82,63,38,.72)";
    ctx.strokeStyle="rgba(255,210,80,.9)";ctx.lineWidth=3;
    ctx.beginPath();ctx.ellipse(z.x,z.y+5,56,28,0,0,Math.PI*2);ctx.fill();ctx.stroke();
    ctx.fillStyle="#59636a";ctx.fillRect(z.x-34,z.y-13,20,22);
    ctx.fillStyle="#31383d";ctx.fillRect(z.x-37,z.y-17,26,6);
    ctx.fillStyle="#d7c7a2";ctx.beginPath();ctx.arc(z.x+2,z.y+3,9,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="#b84c3e";ctx.fillRect(z.x+17,z.y-7,16,12);
    ctx.fillStyle="#8cc56b";ctx.beginPath();ctx.arc(z.x+28,z.y+10,7,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="#fff3b0";ctx.font="bold 13px sans-serif";ctx.textAlign="center";ctx.fillText("SLOW",z.x,z.y-30);
    ctx.restore();
  });'''
if old3 not in s: raise SystemExit('trash draw marker not found')
s=s.replace(old3,new3,1)
p.write_text(s,encoding='utf-8')
