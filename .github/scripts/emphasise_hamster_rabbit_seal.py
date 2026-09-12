from pathlib import Path

p=Path('index.html')
s=p.read_text()

repls={
'life:.28,maxLife:.28,type:"hamsterSeed",special:false':'life:.52,maxLife:.52,type:"hamsterSeed",special:false',
'life:.24+i*.045,maxLife:.24+i*.045,type:"hamsterSeed"':'life:.42+i*.06,maxLife:.42+i*.06,type:"hamsterSeed"',
'life:.27,maxLife:.27,type:"rabbitCarrot"':'life:.54,maxLife:.54,type:"rabbitCarrot"',
'life:.20+i*.075,maxLife:.20+i*.075,type:"rabbitBarrage"':'life:.34+i*.09,maxLife:.34+i*.09,type:"rabbitBarrage"',
'life:.34+i*.08,maxLife:.34+i*.08,\n        type:"sealWaterBolt"':'life:.55+i*.08,maxLife:.55+i*.08,\n        type:"sealWaterBolt"',
'const q=1-Math.max(0,s.life)/(s.maxLife||.34),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;':'const q=1-Math.max(0,s.life)/(s.maxLife||.55),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;',
'ctx.beginPath();ctx.ellipse(0,0,16,8,0,0,Math.PI*2);ctx.fill();':'ctx.beginPath();ctx.ellipse(0,0,22,11,0,0,Math.PI*2);ctx.fill();',
'ctx.beginPath();ctx.ellipse(5,-2,6,2.5,0,0,Math.PI*2);ctx.fill();':'ctx.beginPath();ctx.ellipse(7,-3,8,3.5,0,0,Math.PI*2);ctx.fill();',
'ctx.beginPath();ctx.ellipse(0,0,7,3.5,0,0,Math.PI*2);ctx.fill();ctx.stroke();':'ctx.beginPath();ctx.ellipse(0,0,11,5.5,0,0,Math.PI*2);ctx.fill();ctx.stroke();',
'ctx.beginPath();ctx.moveTo(-7,-5);ctx.lineTo(10,0);ctx.lineTo(-7,5);ctx.closePath();ctx.fill();':'ctx.beginPath();ctx.moveTo(-12,-8);ctx.lineTo(16,0);ctx.lineTo(-12,8);ctx.closePath();ctx.fill();'
}

for old,new in repls.items():
    if old not in s:
        print('warning missing:', old[:80])
    s=s.replace(old,new)

# Add unmistakable launch flashes for the three cards by injecting extra short-lived pulse shots.
s=s.replace('battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.52,maxLife:.52,type:"hamsterSeed",special:false});',
'''battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.52,maxLife:.52,type:"hamsterSeed",special:false});\n      battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.16,maxLife:.16,type:"animalAttackFlash",flash:"hamster"});''')
s=s.replace('battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.54,maxLife:.54,type:"rabbitCarrot"});',
'''battle.shots.push({x:t.x,y:t.y-4,tx:target.x,ty:target.y,life:.54,maxLife:.54,type:"rabbitCarrot"});\n      battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.16,maxLife:.16,type:"animalAttackFlash",flash:"rabbit"});''')
s=s.replace('type:"sealWaterBolt",boltIndex:i', 'type:"sealWaterBolt",boltIndex:i')

anchor='''    if(s.type==="sealWaterBolt"){'''
if 's.type==="animalAttackFlash"' not in s and anchor in s:
    s=s.replace(anchor,'''    if(s.type==="animalAttackFlash"){\n      const a=Math.max(0,s.life/(s.maxLife||.16));\n      ctx.save();ctx.globalAlpha=a;ctx.strokeStyle=s.flash==="rabbit"?"#ff8a1f":"#ffd95a";ctx.lineWidth=4;ctx.beginPath();ctx.arc(s.x,s.y,8+(1-a)*18,0,Math.PI*2);ctx.stroke();ctx.restore();\n    }else if(s.type==="sealWaterBolt"){''',1)

p.write_text(s)
print('emphasised Hamster Rabbit Seal attack visuals')
