from pathlib import Path

p=Path('index.html')
s=p.read_text()

# Add Elephant card to the animal roster.
if 'elephant:{name:"Elephant"' not in s:
    start=s.index('const animals = {')
    end=s.index('\n};', start)
    block=s[start:end].rstrip()
    elephant='  elephant:{name:"Elephant", emoji:"🐘", rarity:"Epic", cost:120, range:140, rate:.70, dmg:25, color:"#708da3", desc:"Epic water attacker that sprays a continuous stream from its trunk."}'
    insertion=('\n'+elephant) if block.endswith(',') else (',\n'+elephant)
    s=s[:end]+insertion+s[end:]

# Elephant is exclusive to the purple/internal epic chest, including exclusion from Legendary.
anchor='  const allowedPool=Object.keys(animals).filter(k=>{\n'
if 'if(k==="elephant") return btn.dataset.chest==="epic";' not in s:
    if anchor not in s: raise SystemExit('Chest pool anchor not found')
    s=s.replace(anchor,anchor+'    if(k==="elephant") return btn.dataset.chest==="epic";\n',1)

# Make the Elephant attack a long-lived water stream so successive attacks visually overlap.
if 't.key==="elephant"?.78:' not in s:
    old='life:t.key==="owl"?'
    if old not in s: raise SystemExit('Shot life anchor not found')
    s=s.replace(old,'life:t.key==="elephant"?.78:t.key==="owl"?',1)
if 't.key==="elephant"?"water":' not in s:
    old='type:t.key==="owl"?'
    if old not in s: raise SystemExit('Shot type anchor not found')
    s=s.replace(old,'type:t.key==="elephant"?"water":t.key==="owl"?',1)

# Draw a bright continuous water spray from the tower/trunk toward the target.
water_marker='  battle.shots?.forEach(s=>{\n    if(s.type==="soundwave"){'
if 'if(s.type==="water"){' not in s:
    if water_marker not in s: raise SystemExit('Shot renderer anchor not found')
    water='''  battle.shots?.forEach(s=>{\n    if(s.type==="water"){\n      const fade=Math.min(1,Math.max(0,s.life/.16));\n      const baseDx=s.tx-s.x,baseDy=s.ty-(s.y-4),len=Math.hypot(baseDx,baseDy)||1;\n      const ux=baseDx/len,uy=baseDy/len,nx=-uy,ny=ux;\n      const sx=s.x+ux*17,sy=(s.y-4)+uy*17;\n      const dx=s.tx-sx,dy=s.ty-sy;\n      const wob=Math.sin((performance.now()/1000)*20+s.x*.01)*5;\n      ctx.save();ctx.lineCap="round";ctx.lineJoin="round";\n      ctx.globalAlpha=.78*fade;ctx.strokeStyle="#4bc9ff";ctx.lineWidth=11;ctx.shadowColor="#29bfff";ctx.shadowBlur=13;\n      ctx.beginPath();ctx.moveTo(sx,sy);ctx.bezierCurveTo(sx+dx*.30+nx*wob,sy+dy*.30+ny*wob,sx+dx*.68-nx*wob*.7,sy+dy*.68-ny*wob*.7,s.tx,s.ty);ctx.stroke();\n      ctx.globalAlpha=.95*fade;ctx.strokeStyle="#d8f8ff";ctx.lineWidth=3;ctx.shadowBlur=4;\n      ctx.beginPath();ctx.moveTo(sx,sy);ctx.bezierCurveTo(sx+dx*.30+nx*wob,sy+dy*.30+ny*wob,sx+dx*.68-nx*wob*.7,sy+dy*.68-ny*wob*.7,s.tx,s.ty);ctx.stroke();\n      ctx.fillStyle="#8de7ff";ctx.shadowBlur=5;\n      for(let i=0;i<4;i++){const q=(i+1)/5,drift=Math.sin((performance.now()/1000)*15+i*1.7)*5;const px=sx+dx*q+nx*drift,py=sy+dy*q+ny*drift;ctx.beginPath();ctx.arc(px,py,2.4+(i%2),0,Math.PI*2);ctx.fill();}\n      ctx.restore();\n    }else if(s.type==="soundwave"){'''
    s=s.replace(water_marker,water,1)

# Show Epic rarity consistently in the collection badge.
old='a.rarity==="Legendary"?"🌟 LEGENDARY":a.rarity==="Rare"?"💎 RARE"'
if old in s and 'a.rarity==="Epic"?"🟣 EPIC"' not in s:
    s=s.replace(old,'a.rarity==="Legendary"?"🌟 LEGENDARY":a.rarity==="Epic"?"🟣 EPIC":a.rarity==="Rare"?"💎 RARE"',1)

p.write_text(s)
