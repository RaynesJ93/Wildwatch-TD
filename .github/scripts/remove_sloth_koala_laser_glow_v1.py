from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove Sloth/Koala from the generic neon visibility helper that adds a bright halo and long trail.
old_types='"otterPebble","riverRush","slothStick","treeTopple","koalaBranch","koalaFuryBanner","woolBall","woolTrapBanner"'
new_types='"otterPebble","riverRush","woolBall","woolTrapBanner"'
if old_types in s:
    s=s.replace(old_types,new_types,1)

old_colour='  else if(["treeTopple","slothStick","koalaBranch","koalaFuryBanner"].includes(s.type)){col="#c9ff7b";r=17;}\n'
s=s.replace(old_colour,'',1)

# Make Sloth's actual spinning stick larger instead of relying on glow/trails.
old_sloth='''    }else if(s.type==="slothStick"){const q=1-Math.max(0,s.life)/(s.maxLife||.38),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*12);ctx.strokeStyle="#6b3f1f";ctx.lineWidth=5;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-10,0);ctx.lineTo(10,0);ctx.stroke();ctx.strokeStyle="#a56b38";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-8,-1);ctx.lineTo(8,-1);ctx.stroke();ctx.strokeStyle="#5f8d42";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(4,0);ctx.lineTo(8,-5);ctx.stroke();ctx.restore();\n'''
new_sloth='''    }else if(s.type==="slothStick"){const q=1-Math.max(0,s.life)/(s.maxLife||.38),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;ctx.save();ctx.translate(x,y);ctx.rotate((s.spin||0)+q*12);ctx.strokeStyle="#5a351b";ctx.lineWidth=9;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-19,0);ctx.lineTo(19,0);ctx.stroke();ctx.strokeStyle="#b8793f";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-16,-2);ctx.lineTo(16,-2);ctx.stroke();ctx.fillStyle="#5f8d42";ctx.beginPath();ctx.ellipse(9,-7,8,4,-.45,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(-7,6,7,3,.45,0,Math.PI*2);ctx.fill();ctx.restore();\n'''
if old_sloth not in s:
    raise RuntimeError('Sloth stick draw block not found')
s=s.replace(old_sloth,new_sloth,1)

# Enlarge Koala branch projectile and leaves, but keep natural brown/green colours with no glow.
old_koala='''    }else if(s.type==="koalaBranch"){const q=1-Math.max(0,s.life)/(s.maxLife||.27),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,a=Math.atan2(s.ty-s.y,s.tx-s.x)+Math.sin(q*Math.PI)*.45+(s.offset||0)*.13;ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.strokeStyle=s.fury?"#8f5b2e":"#72502e";ctx.lineWidth=s.fury?6:5;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-14,0);ctx.lineTo(14,0);ctx.stroke();ctx.fillStyle=s.fury?"#74d85d":"#579b49";for(let i=-1;i<=1;i+=2){ctx.beginPath();ctx.ellipse(i*7,-5,6,3,i*.5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(i*3,5,5,3,-i*.5,0,Math.PI*2);ctx.fill();}ctx.restore();\n'''
new_koala='''    }else if(s.type==="koalaBranch"){const q=1-Math.max(0,s.life)/(s.maxLife||.27),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,a=Math.atan2(s.ty-s.y,s.tx-s.x)+Math.sin(q*Math.PI)*.45+(s.offset||0)*.13;ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.strokeStyle=s.fury?"#7a4b26":"#684521";ctx.lineWidth=s.fury?10:8;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-24,0);ctx.lineTo(24,0);ctx.stroke();ctx.fillStyle=s.fury?"#6fbf59":"#4f8d43";for(let i=-1;i<=1;i+=2){ctx.beginPath();ctx.ellipse(i*12,-8,10,5,i*.5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.ellipse(i*6,8,9,5,-i*.5,0,Math.PI*2);ctx.fill();}ctx.restore();\n'''
if old_koala not in s:
    raise RuntimeError('Koala branch draw block not found')
s=s.replace(old_koala,new_koala,1)

# Make Tree Topple itself a little larger so the Level 10 special stays obvious without a neon overlay.
s=s.replace('ctx.lineWidth=15;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-65,0);ctx.lineTo(58,0);ctx.stroke();','ctx.lineWidth=20;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-82,0);ctx.lineTo(74,0);ctx.stroke();',1)
s=s.replace('ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-58,-3);ctx.lineTo(50,-3);ctx.stroke();','ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-73,-4);ctx.lineTo(65,-4);ctx.stroke();',1)
s=s.replace('const px=-45+i*17,py=(i%2?8:-9);ctx.beginPath();ctx.arc(px,py,12,0,Math.PI*2);','const px=-58+i*20,py=(i%2?11:-12);ctx.beginPath();ctx.arc(px,py,15,0,Math.PI*2);',1)

p.write_text(s,encoding='utf-8')
print('Removed neon Sloth/Koala trail effect and enlarged their natural attack animations')
